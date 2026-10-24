#!/usr/bin/env python3
"""Bộ công cụ ước tính nhiệt độ lõi (Tc) và chỉ số căng thẳng nhiệt — CHỈ DÙNG CHO NGHIÊN CỨU.

Không phải thiết bị y tế. Mọi ngưỡng đều là tham số cấu hình, phải được hiệu chỉnh/kiểm định
trên quần thể đích (vd. VĐV Việt Nam, khí hậu nóng ẩm) trước khi dùng thực địa.

Các mô hình:
  - ectemp():     Kalman filter ước tính Tc từ chuỗi nhịp tim (Buller et al., 2013, Physiol Meas 34:781).
  - double_sensor(): phương pháp cảm biến kép / dòng nhiệt (Gunga et al., 2008, J Therm Biol): Tc = T1 + K*(T1 - T2).
  - psi():        Physiological Strain Index (Moran et al., 1998, Am J Physiol 275:R129).
  - classify():   phân tầng cảnh báo từ Tc, tốc độ tăng Tc, PSI.

CLI:
  python3 heatstrain.py demo                      # chạy ca mô phỏng
  python3 heatstrain.py run data.csv [--hr0 70 --tc0 37.0]
     data.csv cần cột: minute,hr  (tuỳ chọn: tc_measured, t_skin, t_outer)
"""
import csv
import json
import sys

# --- ECTemp (Buller 2013) — tham số công bố gốc; hiệu chỉnh lại nếu dùng quần thể khác ---
ECTEMP_PARAMS = {
    "a": 1.0,               # hệ số chuyển trạng thái (Tc_t = a*Tc_{t-1})
    "gamma": 0.022 ** 2,    # phương sai nhiễu quá trình (°C^2/phút)
    "b0": -7887.1,          # HR = b2*Tc^2 + b1*Tc + b0
    "b1": 384.4286,
    "b2": -4.5714,
    "sigma": 18.88 ** 2,    # phương sai nhiễu quan sát (bpm^2)
    "tc0": 37.1,
    "v0": 0.0,
}

# Ngưỡng cảnh báo mặc định (tham số, không phải chuẩn lâm sàng tuyệt đối)
DEFAULT_THRESHOLDS = {
    "tc_levels": [  # (ngưỡng dưới, mức, nhãn)
        # IOC 2021: chẩn đoán EHS khi Tre ≥ 40,5 °C + rối loạn TKTW; 40,0 giữ làm ngưỡng cảnh báo sớm (nhạy hơn)
        (40.0, 4, "NGUY HIỂM – nghi say nắng gắng sức (EHS): dừng ngay, đánh giá thần kinh, làm mát tích cực"),
        (39.5, 3, "CAO – dừng vận động, làm mát, theo dõi sát"),
        (39.0, 2, "CẢNH GIÁC – giảm cường độ, nghỉ trong bóng râm, uống theo cảm giác khát (KHÔNG khuyến uống thêm nếu nghi hạ natri máu: tăng cân, phù, lú lẫn)"),
        (38.5, 1, "THEO DÕI – tăng tần suất kiểm tra"),
    ],
    "rise_rate_c_per_10min": 0.5,   # tốc độ tăng Tc đáng lo ngại (nâng 1 mức)
    "psi_high": 7.0,                # PSI >= 7: căng thẳng cao (Moran 1998)
}


def ectemp(hr_series, params=None, tc0=None):
    """Ước tính Tc theo phút từ HR theo phút. Trả về list[(tc, variance)]."""
    p = dict(ECTEMP_PARAMS, **(params or {}))
    tc = p["tc0"] if tc0 is None else tc0
    v = p["v0"]
    out = []
    for hr in hr_series:
        if hr is None:  # mất tín hiệu: chỉ cập nhật thời gian
            v = p["a"] ** 2 * v + p["gamma"]
            out.append((tc, v))
            continue
        tc_hat = p["a"] * tc
        v_hat = p["a"] ** 2 * v + p["gamma"]
        c = 2 * p["b2"] * tc_hat + p["b1"]
        k = v_hat * c / (c ** 2 * v_hat + p["sigma"])
        hr_pred = p["b2"] * tc_hat ** 2 + p["b1"] * tc_hat + p["b0"]
        tc = tc_hat + k * (hr - hr_pred)
        v = (1 - k * c) * v_hat
        out.append((tc, v))
    return out


def double_sensor(t_skin, t_outer, k):
    """Tc = T1 + K*(T1 - T2); K = R_mô / R_cảm_biến, phải hiệu chỉnh theo thiết bị & vị trí."""
    return t_skin + k * (t_skin - t_outer)


def psi(tc_t, hr_t, tc_0, hr_0, tc_max=39.5, hr_max=180.0):
    """PSI 0–10 (Moran 1998). Ngoài miền tham chiếu có thể vượt 10."""
    return 5 * (tc_t - tc_0) / (tc_max - tc_0) + 5 * (hr_t - hr_0) / (hr_max - hr_0)


def classify(tc, tc_10min_ago=None, psi_val=None, th=None):
    th = th or DEFAULT_THRESHOLDS
    labels = {lv: lb for _, lv, lb in th["tc_levels"]}
    level = next((lv for lo, lv, _ in th["tc_levels"] if tc >= lo), 0)
    reasons = [f"Tc≈{tc:.2f}°C"]
    if tc_10min_ago is not None and tc - tc_10min_ago >= th["rise_rate_c_per_10min"]:
        reasons.append(f"Tc tăng {tc - tc_10min_ago:.2f}°C/10 phút")
        level = min(level + 1, 4)
    if psi_val is not None and psi_val >= th["psi_high"]:
        reasons.append(f"PSI={psi_val:.1f}")
        level = max(level, 2)
    label = labels.get(level, "BÌNH THƯỜNG")
    return {"level": level, "label": label, "reasons": reasons}


def run(rows, hr0=None, tc0=None):
    hrs = [float(r["hr"]) if r.get("hr") not in (None, "") else None for r in rows]
    est = ectemp(hrs, tc0=tc0)
    hr0 = hr0 if hr0 is not None else next(h for h in hrs if h is not None)
    tc_base = est[0][0] if tc0 is None else tc0
    results = []
    for i, (r, (tc, var)) in enumerate(zip(rows, est)):
        tc_src = tc
        if r.get("tc_measured") not in (None, ""):
            tc_src = float(r["tc_measured"])  # ưu tiên giá trị đo trực tiếp nếu có
        prev = results[i - 10]["tc_used"] if i >= 10 else None
        p = psi(tc_src, hrs[i], tc_base, hr0) if hrs[i] is not None else None
        c = classify(tc_src, prev, p)
        results.append({"minute": r.get("minute", i), "hr": hrs[i], "tc_ectemp": round(tc, 3),
                        "tc_sd": round(var ** 0.5, 3), "tc_used": round(tc_src, 3),
                        "psi": None if p is None else round(p, 2), **c})
    return results


def _demo_rows():
    # Chạy 60 phút trong nắng nóng: HR 75 -> ~185, có giai đoạn tăng mạnh cuối
    rows = []
    for m in range(61):
        hr = 75 + min(m, 20) * 4.5 + max(0, m - 20) * 0.6 + (max(0, m - 45) * 0.8)
        rows.append({"minute": m, "hr": round(hr, 1)})
    return rows


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "demo":
        res = run(_demo_rows(), hr0=75, tc0=37.0)
    elif args[0] == "run":
        with open(args[1], newline="") as f:
            rows = list(csv.DictReader(f))
        opt = dict(zip(args[2::2], args[3::2]))
        res = run(rows, hr0=float(opt["--hr0"]) if "--hr0" in opt else None,
                  tc0=float(opt["--tc0"]) if "--tc0" in opt else None)
    else:
        print(__doc__)
        sys.exit(1)
    for r in res[::5] + ([res[-1]] if len(res) % 5 != 1 else []):
        print(json.dumps(r, ensure_ascii=False))
