#!/usr/bin/env python3
"""Động cơ cảnh báo nhiều tầng cho bệnh lý do nhiệt / cấp cứu ở VĐV sức bền — PROTOTYPE NGHIÊN CỨU.

KHÔNG PHẢI THIẾT BỊ Y TẾ. Mọi ngưỡng nằm trong 02_algorithm-engineer_thresholds.json (tham số, có nguồn).
Tc ước tính (eTc) chỉ dùng để sàng lọc; chẩn đoán EHS cần Tre ≥ 40,5 °C + rối loạn TKTW do người xác nhận.

Tái sử dụng thư viện của skill core-temp-modeling (không sửa): heatstrain.ectemp(), heatstrain.psi(),
heatstrain.run() (dùng làm "baseline ECTemp-only" để so sánh).

Luồng mỗi phút cho một VĐV:
  HR thô → QC tín hiệu (miền, bước nhảy, khoá nhịp bước, chất lượng) → clip HR → ECTemp (Kalman)
  → eTc ± SD, PSI (HRmax cá nhân), aPSI (nếu có Tsk; công thức ❓), tốc độ tăng, HR kéo dài, dáng đi
  → mức thiết bị (trần 3, R3; ngoại lệ nghi ngừng tim R4) → cộng WBGT (R7)
  → mức người quan sát / đo Tre / Na⁺ (R1, R2) → mức cuối = max(...) → hướng dẫn dịch (chặn "uống nước" khi nghi EAH/TKTW)
  → kênh: app VĐV + dashboard ban y tế (sự kiện khi đổi mức).

CLI:
  python3 02_algorithm-engineer_alert_engine.py            # chạy 4 kịch bản mô phỏng + tự kiểm tra
  python3 02_algorithm-engineer_alert_engine.py --json out.json
  python3 02_algorithm-engineer_alert_engine.py csv data.csv --age 30 --hr-rest 60 --hr-max 190
       (CSV: minute,hr[,t_skin,gait,cadence,wbgt])
"""
import csv
import json
import math
import os
import random
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "core-temp-modeling", "scripts"))
import heatstrain as hs  # noqa: E402  (thư viện của skill, không sửa)

CONFIG_PATH = os.path.join(HERE, "02_algorithm-engineer_thresholds.json")


def load_config(path=CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------------------------------------------------
# Văn bản hành động (tách phần "dịch" ra riêng để có thể chặn khi nghi EAH)
# ----------------------------------------------------------------------------------------------
LEVEL_NAME = {0: "BÌNH THƯỜNG", 1: "CHÚ Ý", 2: "CẢNH BÁO", 3: "NGUY CƠ CAO", 4: "CẤP CỨU"}

ATHLETE_MSG = {
    0: "",
    1: "Giảm tốc; tạt nước mát lên đầu/cổ/thân.",
    2: "Giảm tốc rõ hoặc đi bộ; người quan sát sẽ tới hỏi thăm.",
    3: "DỪNG CHẠY, ngồi/nằm nơi râm mát, chờ đội y tế đánh giá (yêu cầu đánh giá y tế, không phải loại khỏi cuộc đua).",
    4: "Đội cấp cứu đang tới.",
}
DASH_ACTION = {
    1: ("VĐV tự xử; theo dõi nền", "—"),
    2: ("Người quan sát/TNV y tế gần nhất tiếp cận, quan sát dáng chạy, hỏi định hướng (tên, km, ngày)", "≤5 phút"),
    3: ("Đội cơ động tới: đánh giá TKTW, loại trừ ngừng tim; nếu bất thường → khu xử trí nhiệt, đo Tre", "≤3–5 phút"),
}
DX_ACTION = {
    "CARDIAC": ("NGHI NGỪNG TIM: điều đội AED gần nhất; người chứng kiến CPR ngay; loại trừ tim TRƯỚC xử trí nhiệt (R4, IOC 2021)",
                "CPR ngay; sốc điện ≤3–5 phút ❓"),
    "EHS": ("EHS: ngâm nước lạnh toàn thân (CWI 5–15 °C, khuấy) NGAY; theo dõi Tre liên tục; 4 người/bồn; làm Na⁺ + glucose khi không gián đoạn làm mát",
            "làm mát ngay; hạ nhiệt ≤30 phút từ lúc gục"),
    "EAH_SEVERE": ("EAH NẶNG (nghi/xác định): NaCl 3 % 100 mL TM bolus, nhắc lại mỗi 10 phút tối đa 3 lần; KHÔNG truyền dịch nhược trương, KHÔNG cho uống nước; chuyển viện",
                   "bolus đầu ngay khi nghi ngờ"),
    "CNS_UNEXPLAINED": ("TKTW chưa rõ nguyên nhân: chuyển khu xử trí nhiệt bằng cáng/xe lăn; đo Tre; làm Na⁺ + glucose; nếu không đo được Tre và nghi do nhiệt → làm mát ngay",
                        "≤5–10 phút ❓"),
    "HEAT_CNS_TRE_LT_EHS": ("TKTW + Tre < 40,5 °C: VẪN làm mát (khăn đá luân phiên/CWI), theo dõi Tre, làm Na⁺ + glucose (DX-T2)", "ngay"),
}
FLUID_TEXT = {
    "THIRST": "Dịch: uống theo cảm giác khát, không uống ép.",
    "THIRST_EAH_RISK": "Dịch: chỉ uống khi khát; KHÔNG uống ở mọi trạm (thuộc nhóm nguy cơ hạ natri máu).",
    "RESTRICT": "Dịch: KHÔNG uống thêm nước lọc/dịch nhược trương; báo trạm y tế làm Na⁺ (nghi nguy cơ EAH).",
    "NPO": "Dịch: KHÔNG cho uống cho tới khi có Na⁺ và loại trừ EAH (IOC 2021; WMS 2019).",
}


class AlertEngine:
    """Động cơ cho MỘT VĐV. Gọi step(minute, obs) mỗi phút."""

    def __init__(self, profile, cfg=None):
        self.cfg = cfg or load_config()
        self.p = profile
        e = self.cfg["ectemp"]
        self.tc0 = profile.get("tc0_measured") or e["tc0_assumed"]
        self.v0 = e["v0_measured"] if profile.get("tc0_measured") else e["v0_assumed"]
        self.hr_rest = profile["hr_rest"]
        self.hr_max = profile.get("hr_max") or (220 - profile["age"])
        n_rf = len(profile.get("risk_factors", []))
        self.rf_offset = min(n_rf * self.cfg["risk_factor_offset_c_each"], self.cfg["risk_factor_offset_c_max"])
        self.rf_psi_offset = min(n_rf * self.cfg["risk_factor_psi_offset_each"], self.cfg["risk_factor_psi_offset_max"])
        # trạng thái
        self.hr_series = []        # HR đã QC + clip (None = thiếu) — đưa vào hs.ectemp
        self.accepted = []         # HR thô đã chấp nhận
        self.rej_streak = 0
        self.last_rej = None
        self.missing_streak = 0
        self.etc_raw, self.etc_s = [], []
        self.dev_level = 0
        self.below = 0
        self.hr_high_streak = 0
        self.gait_streak = 0
        self.human = {}            # cờ "dính" do người nhập, chỉ xoá khi nhân viên y tế 'clear'
        self.tre_log = []
        self.cooling_start = None
        self.prev = {"level": 0, "dx": None, "tech": None, "fluid": None}
        self.events = []

    # ------------------------------------------------------------------ QC tín hiệu HR
    def _qc(self, hr, quality, cadence):
        q = self.cfg["signal_qc"]
        if hr is None:
            return None, "không có mẫu"
        if quality is not None and quality < q["min_device_quality"]:
            return None, f"chất lượng thiết bị thấp ({quality})"
        if hr < q["hr_valid_min"] or hr > q["hr_valid_max"]:
            return None, f"ngoài miền sinh lý ({hr:.0f})"
        if self.accepted:
            med = self.accepted[-1]  # so với mẫu hợp lệ gần nhất (median trễ khi HR tăng dốc lúc xuất phát)
            if (cadence is not None and abs(hr - cadence) <= q["cadence_lock_tol_bpm"]
                    and abs(hr - med) >= q["cadence_lock_min_jump_bpm"]):
                self.rej_streak += 1
                self.last_rej = hr
                return None, f"nghi khoá theo nhịp bước (HR {hr:.0f} ≈ cadence {cadence:.0f}, nhảy từ {med:.0f})"
            if abs(hr - med) > q["max_jump_bpm_per_min"]:
                confirmed = (self.last_rej is not None and self.rej_streak >= q["confirm_after"] - 1
                             and abs(hr - self.last_rej) <= q["max_jump_bpm_per_min"])
                if not confirmed:
                    self.rej_streak += 1
                    self.last_rej = hr
                    return None, f"bước nhảy bất thường ({med:.0f}→{hr:.0f})"
        self.rej_streak, self.last_rej = 0, None
        self.accepted.append(hr)
        return hr, None

    # ------------------------------------------------------------------ một bước (1 phút)
    def step(self, minute, obs):
        cfg = self.cfg
        reasons, flags = [], []
        hr_raw = obs.get("hr")
        hr_ok, qc_reason = self._qc(hr_raw, obs.get("hr_quality"), obs.get("cadence"))
        e = cfg["ectemp"]
        hr_used = None if hr_ok is None else min(max(hr_ok, e["hr_clip_min"]), e["hr_clip_max"])
        self.hr_series.append(hr_used)
        self.missing_streak = self.missing_streak + 1 if hr_used is None else 0

        # --- ECTemp (thư viện skill) — chạy lại toàn chuỗi (n ≤ vài trăm phút, rẻ) ---
        tc, var = hs.ectemp(self.hr_series, params={"v0": self.v0}, tc0=self.tc0)[-1]
        sd = math.sqrt(var)
        self.etc_raw.append(tc)
        k = e["smoothing_min"]
        etc = sum(self.etc_raw[-k:]) / len(self.etc_raw[-k:])
        self.etc_s.append(etc)
        if hr_used is not None and hr_ok > e["low_confidence_hr_above"]:
            flags.append(f"HR {hr_ok:.0f} > {e['low_confidence_hr_above']}: eTc độ tin cậy thấp (vùng bão hoà parabol)")

        # --- tầng thiết bị ---
        lv_etc, src_etc = 0, None
        decision = etc + cfg["etc_safety_offset_c"] + self.rf_offset
        for row in cfg["etc_levels"]:
            if decision >= row["threshold"] and row["level"] >= lv_etc:
                lv_etc, src_etc = row["level"], row["id"]
        lv_etc_raw = max([r["level"] for r in cfg["etc_levels"] if etc + self.rf_offset >= r["threshold"]] or [0])
        if lv_etc:
            reasons.append(f"{src_etc}: eTc {etc:.2f}±{sd:.2f} °C (ngưỡng quyết định {decision:.2f} sau bù R5/R6)")

        recent = [h for h in self.hr_series[-2:] if h is not None]
        hr_s = sum(recent) / len(recent) if recent else None
        psi_v = apsi_v = None
        lv_psi = lv_apsi = 0
        if hr_s is not None:
            pc = cfg["psi"]
            hrmax_psi = self.hr_max if pc["use_personal_hrmax"] else 180.0
            psi_v = hs.psi(etc, hr_s, self.tc0, self.hr_rest, tc_max=pc["tc_max"], hr_max=hrmax_psi)
            for r in pc["levels"]:
                if psi_v >= r["threshold"] - self.rf_psi_offset:
                    lv_psi = max(lv_psi, r["level"])
                    tag = r["id"]
            if lv_psi:
                reasons.append(f"{tag}: PSI {psi_v:.1f}")
            ac = cfg["apsi"]
            tsk = obs.get("t_skin")
            if ac["enabled"] and tsk is not None:
                tc_crit = ac["tc_crit_base"] + ((etc - tsk) - ac["gradient_ref"]) / ac["gradient_div"]
                tc_crit = min(max(tc_crit, ac["tc_crit_min"], self.tc0 + 0.5), ac["tc_crit_max"])
                hr_crit = ac["hr_crit_frac"] * (220 - self.p["age"])
                apsi_v = hs.psi(etc, hr_s, self.tc0, self.hr_rest, tc_max=tc_crit, hr_max=hr_crit)
                for r in ac["levels"]:
                    if apsi_v >= r["threshold"] - self.rf_psi_offset:
                        lv_apsi = max(lv_apsi, r["level"])
                        tag = r["id"]
                if lv_apsi:
                    reasons.append(f"{tag}: aPSI {apsi_v:.1f} (Tsk {tsk:.1f}; công thức ❓ chưa kiểm chứng)")

        g = cfg["gait"]
        gi = obs.get("gait")
        self.gait_streak = self.gait_streak + 1 if (gi is not None and gi >= g["index_threshold"]) else 0
        lv_gait = g["level"] if self.gait_streak >= g["min_minutes"] else 0
        if lv_gait:
            reasons.append(f"{g['id']}: dáng chạy mất ổn định {self.gait_streak} phút (chỉ số {gi:.2f}) → coi như nghi TKTW (R2)")
        if obs.get("collapse") and hr_used is not None:
            lv_gait = max(lv_gait, 3)
            reasons.append("SCR-G1: gục ngã/dừng đột ngột (gia tốc kế/GPS), còn tín hiệu tim")

        # tín hiệu phụ: tốc độ tăng (chỉ khi eTc đã ≥ sàn, tránh báo ở pha khởi động), HR kéo dài
        rr = cfg["rise_rate"]
        rise = etc - self.etc_s[-1 - rr["window_min"]] if len(self.etc_s) > rr["window_min"] else 0.0
        rising = rise >= rr["delta_c"] and etc >= rr["apply_above_etc"]
        hs_cfg = cfg["hr_sustained"]
        self.hr_high_streak = self.hr_high_streak + 1 if (hr_ok is not None and hr_ok >= hs_cfg["pct_hrmax"] * self.hr_max) else 0
        hr_long = self.hr_high_streak > hs_cfg["min_minutes"]

        # môi trường
        wbgt = obs.get("wbgt")
        env_level, env_flag = 0, "?"
        if wbgt is not None:
            for r in cfg["wbgt_flags"]:
                if wbgt >= r["min"]:
                    env_level, env_flag = r["level"], r["flag"]

        # (a) mức "căng thẳng" (strain): eTc có bù R5/R6, PSI/aPSI, + các bậc cộng — trần = strain_cap (2)
        L3 = cfg["level3_rule"]
        strain = max(lv_etc, lv_psi, lv_apsi)
        strain = min(strain, L3["strain_cap"])
        if rising and strain < L3["strain_cap"]:
            strain = min(strain + rr["bump"], L3["strain_cap"])
            reasons.append(f"{rr['id']}: eTc tăng {rise:.2f} °C/{rr['window_min']} phút (+1)")
        if hr_long and strain < L3["strain_cap"]:
            strain = min(strain + hs_cfg["bump"], hs_cfg["cap"], L3["strain_cap"])
            reasons.append(f"{hs_cfg['id']}: HR ≥{hs_cfg['pct_hrmax']:.0%} HRmax {self.hr_high_streak} phút (+1)")
        wb = cfg["wbgt_bump"]
        if env_level >= wb["min_env_level"] and strain >= wb["only_if_personal_level_at_least"] and strain < L3["strain_cap"]:
            strain = min(strain + wb["bump"], wb["cap"], L3["strain_cap"])
            reasons.append(f"R7: WBGT {wbgt:.1f} °C (cờ {env_flag}) +1")

        # (b) mức 3 từ thiết bị: 1 tín hiệu "cứng" HOẶC ≥ N tín hiệu độc lập (R8 – đề xuất ❓)
        hard = []
        if lv_gait >= 3:
            hard.append("dáng đi/gục (R2)")
        if lv_etc_raw >= 3:
            hard.append(f"eTc thô {etc:.2f} ≥ SCR-T3")
        votes = []
        if lv_etc >= 3:
            votes.append(f"eTc+bù {decision:.2f} ≥ 39,5")
        if lv_psi >= 3 or lv_apsi >= 3:
            votes.append("PSI/aPSI ≥ 9")
        if rising:
            votes.append("eTc tăng nhanh")
        if hr_long:
            votes.append("HR ≥95 % HRmax kéo dài")
        if env_level >= L3["env_vote_min_level"]:
            votes.append(f"WBGT cờ {env_flag}")
        if hard or len(votes) >= L3["min_votes"]:
            base = 3
            reasons.append("R8 mức 3: " + ("; ".join(hard) if hard else f"{len(votes)} tín hiệu độc lập: " + ", ".join(votes)))
        else:
            base = strain
            if votes and strain == L3["strain_cap"]:
                reasons.append(f"R8: {len(votes)}/{L3['min_votes']} tín hiệu mức 3 ({', '.join(votes)}) → giữ mức {strain}")

        dev = min(base, cfg["device_level_cap"])  # R3

        # nghi ngừng tim (R4) — ngoại lệ duy nhất cho thiết bị lên mức 4
        cardiac = bool(obs.get("collapse") and obs.get("immobile") and hr_used is None)
        if cardiac:
            dev = 4
            reasons.append("SCR-H2/R4: gục + bất động + mất tín hiệu tim")

        # trễ hạ mức
        if dev >= self.dev_level:
            self.dev_level, self.below = dev, 0
        else:
            self.below += 1
            if self.below >= cfg["deescalate_after_min"]:
                self.dev_level, self.below = dev, 0
            else:
                reasons.append(f"giữ mức thiết bị {self.dev_level} (trễ hạ mức {self.below}/{cfg['deescalate_after_min']})")

        # tín hiệu kỹ thuật
        q = cfg["signal_qc"]
        tech = None
        if qc_reason and hr_raw is not None:
            flags.append(f"QC loại mẫu HR: {qc_reason}")
        if self.missing_streak >= q["long_gap_min"]:
            tech = f"MẤT TÍN HIỆU HR {self.missing_streak} phút: eTc chỉ dự báo (SD {sd:.2f}); quan sát viên kiểm tra trực tiếp VĐV + thiết bị"
        elif self.missing_streak >= q["signal_lost_after_min"]:
            tech = f"MẤT TÍN HIỆU HR {self.missing_streak} phút: giữ mức cũ, không hạ mức"

        # ------------------------------------------------ tầng con người (R1, R2) + chẩn đoán
        for key in ("cns", "exhaustion", "vomiting", "unresponsive_not_breathing", "muscle_symptoms", "headache"):
            if obs.get(key):
                self.human[key] = minute
        if obs.get("weight_change_pct") is not None:
            self.human["weight_change_pct"] = obs["weight_change_pct"]
        if obs.get("na") is not None:
            self.human["na"] = obs["na"]
        if obs.get("tre") is not None:
            self.tre_log.append((minute, obs["tre"]))
        if obs.get("cooling_started"):
            self.cooling_start = minute
        if obs.get("clear"):
            self.human, self.tre_log, self.cooling_start = {}, [], None
            self.dev_level = dev

        c, ea = cfg["clinical"], cfg["eah"]
        H = self.human
        tre = self.tre_log[-1][1] if self.tre_log else None
        tre_max = max((t for _, t in self.tre_log), default=None)
        na = H.get("na")
        wgain = H.get("weight_change_pct")
        cns = "cns" in H or lv_gait >= 3 and bool(obs.get("collapse"))
        human_level, dx = 0, None
        eah_risk = bool(self.p.get("eah_risk_prior"))
        eah_flag = False
        if wgain is not None and wgain > ea["weight_gain_pct"]:
            human_level = max(human_level, 2)
            eah_flag = True
            reasons.append(f"SCR-W1: tăng cân {wgain:+.1f} % trong giải → nguy cơ EAH")
        if na is not None and na < ea["na_low"]:
            eah_flag = True
            human_level = max(human_level, 2)
            reasons.append(f"LAB-NA1: Na⁺ {na} mmol/L")
        if "exhaustion" in H:
            human_level = max(human_level, 2)
            reasons.append("CLN-3: kiệt sức, không TKTW")
        if "muscle_symptoms" in H:
            human_level = max(human_level, 2)
            reasons.append("CLN-4: triệu chứng cơ → làm CK")
        if "cns" in H:
            human_level = max(human_level, 3)
            dx = "CNS_UNEXPLAINED"
            reasons.append("CLN-1/R2: dấu hiệu TKTW do người quan sát báo")
            tre_mild = tre is not None and tre < ea["tre_normal_or_mild_upper"]
            eah_clues = eah_flag or "vomiting" in H or "headache" in H
            if tre is not None and tre_max >= c["tre_ehs"]:
                human_level, dx = 4, "EHS"
                reasons.append(f"DX-T1: Tre {tre_max:.1f} °C ≥ {c['tre_ehs']} + TKTW → EHS")
            elif (na is not None and na < ea["na_low"]) or (na is not None and na < ea["na_severe"]):
                human_level, dx = 4, "EAH_SEVERE"
                reasons.append(f"LAB-NA2: TKTW + Na⁺ {na} → EAH nặng")
            elif na is None and tre_mild and eah_clues:
                human_level, dx = 4, "EAH_SEVERE"
                reasons.append(f"LAB-NA2: TKTW, chưa có Na⁺, Tre {tre:.1f} bình thường/tăng nhẹ + dấu hiệu EAH → xử trí như EAH nặng")
            elif tre is not None:
                human_level, dx = 3, "HEAT_CNS_TRE_LT_EHS"
                reasons.append(f"DX-T2: Tre {tre:.1f} < {c['tre_ehs']} + TKTW")
        if na is not None and na < ea["na_severe"] and dx != "EAH_SEVERE":
            human_level, dx = 4, "EAH_SEVERE"
            reasons.append(f"LAB-NA3: Na⁺ {na} < {ea['na_severe']}")
        if "unresponsive_not_breathing" in H:
            human_level, dx = 4, "CARDIAC"
            reasons.append("CLN-2: không đáp ứng + không thở bình thường")
        if cardiac:
            dx = "CARDIAC"

        # theo dõi làm mát (DX-T3/T5)
        cooling_note = None
        if dx == "EHS" and self.cooling_start is not None and tre is not None:
            if tre <= c["tre_stop_cooling"]:
                cooling_note = f"DX-T3: Tre {tre:.1f} ≤ {c['tre_stop_cooling']} → NGỪNG làm mát, lau khô, theo dõi Tre ≥15 phút, ngâm lại nếu tăng; chuẩn bị chuyển viện (DX-T6)"
                human_level = max(min(human_level, 4), 3)
                human_level = 3 if human_level == 4 else human_level
            elif minute - self.cooling_start >= c["cooling_rate_grace_min"]:
                pts = [(m, t) for m, t in self.tre_log if m >= self.cooling_start]
                if len(pts) >= 2 and pts[-1][0] > pts[0][0]:
                    peak = max(pts, key=lambda x: x[1])
                    rate = (peak[1] - pts[-1][1]) / max(pts[-1][0] - peak[0], 1)
                    if rate < c["cooling_rate_min_c_per_min"]:
                        cooling_note = f"DX-T5: tốc độ làm mát {rate:.2f} °C/phút < {c['cooling_rate_min_c_per_min']} → kiểm tra nước đủ lạnh, ngâm thân, khuấy"
                    else:
                        cooling_note = f"Làm mát đạt {rate:.2f} °C/phút; tiếp tục tới Tre {c['tre_stop_cooling']}"
            if cooling_note:
                reasons.append(cooling_note)

        final = max(self.dev_level, human_level)  # R1: thiết bị không bao giờ hạ mức do người đặt
        if final == 4 and dx is None:
            dx = "CARDIAC" if cardiac else dx

        # ------------------------------------------------ hướng dẫn dịch
        if "cns" in H or dx in ("EAH_SEVERE", "EHS", "CARDIAC", "CNS_UNEXPLAINED", "HEAT_CNS_TRE_LT_EHS") or lv_gait >= 3:
            fluid = "NPO"
        elif eah_flag:
            fluid = "RESTRICT"
        elif eah_risk:
            fluid = "THIRST_EAH_RISK"
        else:
            fluid = "THIRST"

        # ------------------------------------------------ thông điệp
        if final >= 4 and dx in DX_ACTION:
            action, target = DX_ACTION[dx]
            who = "Toàn chuỗi cứu sống + EMS"
        elif dx in DX_ACTION and final == 3:
            action, target = DX_ACTION[dx]
            who = "Đội cơ động + khu xử trí nhiệt"
        else:
            action, target = DASH_ACTION.get(final, ("Theo dõi nền", "—"))
            who = {0: "—", 1: "VĐV", 2: "VĐV + người quan sát", 3: "Đội cơ động"}.get(final, "—")
        if cooling_note and dx == "EHS":
            action = cooling_note
        athlete_msg = ATHLETE_MSG[final]
        if final >= 1 or fluid != "THIRST":
            athlete_msg = (athlete_msg + " " + FLUID_TEXT[fluid]).strip()

        out = {
            "minute": minute, "hr_raw": hr_raw, "hr_used": hr_used, "etc": round(etc, 2), "etc_sd": round(sd, 3),
            "psi": None if psi_v is None else round(psi_v, 1), "apsi": None if apsi_v is None else round(apsi_v, 1),
            "wbgt": wbgt, "env_flag": env_flag, "device_level": self.dev_level, "human_level": human_level,
            "level": final, "level_name": LEVEL_NAME[final], "dx": dx, "fluid": fluid,
            "athlete_msg": athlete_msg, "dashboard_action": action, "who": who, "target_time": target,
            "reasons": reasons, "flags": flags, "tech": tech,
        }
        # sự kiện dashboard khi đổi trạng thái
        tech_kind = None if tech is None else ("long" if self.missing_streak >= q["long_gap_min"] else "short")
        clin_key = tuple(sorted({r.split(":")[0] for r in reasons if r.startswith(("DX-", "LAB-", "CLN-", "SCR-W"))}))
        changed = (final != self.prev["level"] or dx != self.prev["dx"] or fluid != self.prev["fluid"]
                   or tech_kind != self.prev["tech"] or clin_key != self.prev.get("clin"))
        if changed:
            self.events.append(out)
        self.prev = {"level": final, "dx": dx, "tech": tech_kind, "fluid": fluid, "clin": clin_key}
        return out


# ==============================================================================================
# Kịch bản mô phỏng (dữ liệu TỔNG HỢP; "Tc thật" là quỹ đạo giả định để so sánh, không phải dữ liệu đo)
# ==============================================================================================
def _noise(rng, sd):
    return rng.gauss(0, sd)


def scenario_normal(rng):
    """S1 — Chạy bán marathon bình thường, nóng ẩm (WBGT 26–28 °C), VĐV phong trào khoẻ."""
    prof = {"id": "S1-A0123", "age": 35, "hr_rest": 62, "hr_max": 186, "risk_factors": []}
    rows, truth = [], []
    for m in range(0, 121):
        if m < 10:
            hr = 70 + (148 - 70) * m / 10
        else:
            hr = 148 + 0.10 * (m - 10)
        tc = 37.2 + min(m, 50) * 0.030 + max(0, m - 50) * 0.004
        tsk = 33.8 + min(m, 30) * 0.03
        rows.append({"hr": round(hr + _noise(rng, 2.5)), "t_skin": round(tsk + _noise(rng, 0.15), 2),
                     "gait": round(abs(_noise(rng, 0.12)), 2), "cadence": 168, "wbgt": round(26.0 + 2.0 * m / 120, 1)})
        truth.append(tc)
    rows[118]["weight_change_pct"] = -1.6
    return prof, rows, truth


def scenario_ehs(rng):
    """S2 — VĐV ưu tú 10 km/21 km tốc độ cao, Tc tăng tới 41,3 °C trong khi HR bão hoà ~186–190 bpm."""
    prof = {"id": "S2-E0007", "age": 24, "hr_rest": 50, "hr_max": 194, "risk_factors": ["mới ốm tiêu chảy 3 ngày trước"],
            "notable": [30, 40, 50, 60, 67, 70, 75, 76, 80]}
    rows, truth = [], []
    for m in range(0, 101):
        if m < 8:
            hr = 70 + (168 - 70) * m / 8
        elif m < 50:
            hr = 168 + 0.45 * (m - 8)
        else:
            hr = min(187 + 0.05 * (m - 50), 190)  # bão hoà gần HRmax
        if m < 10:
            tc = 37.3 + 0.04 * m
        elif m < 50:
            tc = 37.7 + 0.045 * (m - 10)
        else:
            tc = 39.5 + 0.06 * (m - 50)
        tsk = 33.0 + min(m, 30) * 0.08 + max(0, m - 30) * 0.03
        gait = 0.15 + (0.0 if m < 70 else 0.09 * (m - 70))
        r = {"hr": round(hr + _noise(rng, 2.0)), "t_skin": round(tsk + _noise(rng, 0.15), 2),
             "gait": round(min(gait + abs(_noise(rng, 0.05)), 1.0), 2), "cadence": 185, "wbgt": 28.5}
        if m >= 80:  # gục ngã lúc phút 80, tim vẫn đập, HR giảm dần
            tc = 41.3 - 0.0 * (m - 80)
            r.update({"hr": round(175 - 1.5 * (m - 80) + _noise(rng, 2)), "gait": None, "cadence": None})
        rows.append(r)
        truth.append(tc)
    rows[77]["cns"] = True          # TNV thấy chạy loạng choạng, trả lời lộn xộn
    rows[80]["collapse"] = True
    rows[82]["tre"] = 41.3          # đo Tre tại khu xử trí nhiệt
    rows[83]["cooling_started"] = True
    tre_cwi = {84: 41.3, 86: 41.2, 88: 40.9, 90: 40.5, 92: 40.1, 94: 39.7, 96: 39.3, 98: 38.95}
    for mm, t in tre_cwi.items():
        rows[mm]["tre"] = t
    for mm in range(83, 101):
        truth[mm] = tre_cwi.get(mm, truth[mm - 1])
    return prof, rows, truth


def scenario_noise(rng):
    """S3 — Như S1 nhưng HR quang học cổ tay: gai nhiễu, khoá nhịp bước, mất tín hiệu 12 phút; cuối: gục + bất động + mất HR."""
    prof, rows, truth = scenario_normal(rng)
    prof = dict(prof, id="S3-A0456", notable=[14, 15, 16, 21, 22, 23, 24, 30, 31, 32, 39, 40, 42, 44, 45, 46, 54, 56, 60, 66, 67, 68, 89, 90])
    rows = [dict(r) for r in rows[:96]]
    truth = truth[:96]
    rows[15]["hr"] = 238            # gai ngoài miền
    rows[22]["hr"] = 0              # rơi về 0
    rows[31]["hr"] = 205            # gai trong miền
    for m in range(40, 45):         # khoá theo cadence 168
        rows[m]["hr"] = 168 + rng.choice([-1, 0, 1])
        rows[m]["hr_quality"] = 0.8
    for m in range(55, 67):         # mất tín hiệu 12 phút
        rows[m]["hr"] = None
    for m in range(90, 96):         # gục + bất động + mất tín hiệu tim
        rows[m].update({"hr": None, "collapse": True, "immobile": True, "gait": None, "cadence": None})
    return prof, rows, truth


def scenario_eah(rng):
    """S4 — Người chạy chậm, marathon đầu tiên, uống ở mọi trạm; tăng cân +1,8 % tại km 30; lú lẫn + nôn, Tre 38,4, Na⁺ 127."""
    prof = {"id": "S4-F0890", "age": 45, "hr_rest": 66, "hr_max": 175, "risk_factors": [],
            "eah_risk_prior": True, "eah_risk_reasons": ["marathon đầu tiên", "chạy chậm (~5 h 30)", "uống ở mọi trạm"]}
    rows, truth = [], []
    for m in range(0, 311):
        hr = 75 + (126 - 75) * m / 10 if m < 10 else 126 + 0.02 * (m - 10)
        if m > 285:
            hr = 115  # đi bộ
        tc = 37.1 + min(m, 40) * 0.025 + max(0, m - 40) * 0.0005
        rows.append({"hr": round(hr + _noise(rng, 2.5)), "t_skin": round(34.0 + _noise(rng, 0.2), 2),
                     "gait": round(abs(_noise(rng, 0.12)), 2), "cadence": 150, "wbgt": round(24.0 + 5.0 * m / 310, 1)})
        truth.append(tc)
    rows[200]["weight_change_pct"] = 1.8   # cân tại trạm km 30
    rows[290].update({"cns": True, "vomiting": True, "headache": True})
    rows[294]["tre"] = 38.4
    rows[299]["na"] = 127
    return prof, rows, truth


SCENARIOS = [
    ("S1 Chạy bán marathon bình thường, nóng ẩm", scenario_normal),
    ("S2 Tiến triển EHS, HR bão hoà", scenario_ehs),
    ("S3 Nhiễu/mất tín hiệu HR (+ gục, mất tín hiệu tim cuối)", scenario_noise),
    ("S4 Hạ natri máu do gắng sức (EAH)", scenario_eah),
]


def baseline_ectemp_only(prof, rows):
    """Hệ 'chỉ ECTemp' dùng nguyên heatstrain.run() (HR thô, không QC/clip, ngưỡng mặc định của thư viện)."""
    brow = [{"minute": i, "hr": "" if r.get("hr") is None else r["hr"]} for i, r in enumerate(rows)]
    return hs.run(brow, hr0=prof["hr_rest"], tc0=hs.ECTEMP_PARAMS["tc0"])


def first(seq, pred):
    return next((i for i, x in enumerate(seq) if pred(x)), None)


def run_scenario(name, fn, seed=7, cfg=None):
    rng = random.Random(seed)
    prof, rows, truth = fn(rng)
    eng = AlertEngine(prof, cfg)
    outs = [eng.step(m, r) for m, r in enumerate(rows)]
    base = baseline_ectemp_only(prof, rows)
    return {"name": name, "profile": prof, "rows": rows, "truth": truth, "outs": outs, "events": eng.events, "baseline": base}


def summarize(res):
    outs, truth, base = res["outs"], res["truth"], res["baseline"]
    lv = [o["level"] for o in outs]
    blv = [b["level"] for b in base]
    n = len(outs)
    pre = [i for i in range(n) if not res["rows"][i].get("collapse") and res["rows"][i].get("tre") is None]
    err = [outs[i]["etc"] - truth[i] for i in pre if res["rows"][i].get("hr") is not None or True]
    s = {
        "minutes": n,
        "max_level": max(lv), "max_level_baseline": max(blv),
        "minutes_at_level": {k: lv.count(k) for k in range(5)},
        "baseline_minutes_at_level": {k: blv.count(k) for k in range(5)},
        "first_lvl2": first(lv, lambda x: x >= 2), "first_lvl3": first(lv, lambda x: x >= 3),
        "first_lvl4": first(lv, lambda x: x >= 4),
        "baseline_first_lvl2": first(blv, lambda x: x >= 2), "baseline_first_lvl3": first(blv, lambda x: x >= 3),
        "true_tc_ge_39_5": first(truth, lambda t: t >= 39.5), "true_tc_ge_40_5": first(truth, lambda t: t >= 40.5),
        "true_tc_peak": round(max(truth), 2),
        "etc_peak": max(o["etc"] for o in outs), "baseline_etc_peak": round(max(b["tc_ectemp"] for b in base), 2),
        "bias_etc_minus_true": round(statistics.mean(err), 2),
        "rmse": round(math.sqrt(statistics.mean([x * x for x in err])), 2),
    }
    return s


def self_tests(results):
    """Kiểm tra bất biến an toàn (R1–R4, EAH)."""
    fails = []
    for res in results:
        for o in res["outs"]:
            if o["device_level"] > 3 and o["dx"] != "CARDIAC":
                fails.append(f"{res['name']} phút {o['minute']}: thiết bị lên 4 không phải ngừng tim (vi phạm R3)")
            if o["level"] < o["human_level"]:
                fails.append(f"{res['name']} phút {o['minute']}: mức cuối < mức người đặt (vi phạm R1)")
            if o["fluid"] in ("NPO", "RESTRICT"):
                txt = (o["athlete_msg"] + " " + o["dashboard_action"]).lower()
                # mọi cụm "uống ..." phải đi sau phủ định "không" (vd. "KHÔNG uống thêm nước lọc")
                for mt in re.finditer(r"uống", txt):
                    if "không" not in txt[max(0, mt.start() - 12):mt.start()]:
                        fails.append(f"{res['name']} phút {o['minute']}: có lời khuyên uống không bị phủ định khi đang {o['fluid']}: "
                                     f"'…{txt[max(0, mt.start() - 12):mt.end() + 15]}…'")
            if o["dx"] == "EAH_SEVERE" and "CWI" in o["dashboard_action"]:
                fails.append(f"{res['name']} phút {o['minute']}: EAH nhưng hướng dẫn CWI")
    return fails


def fmt_row(o):
    return (f"{o['minute']:>4} | HR {str(o['hr_raw']):>4}→{'—' if o['hr_used'] is None else int(o['hr_used']):>3} | "
            f"eTc {o['etc']:.2f}±{o['etc_sd']:.2f} | PSI {o['psi'] if o['psi'] is not None else '—':>4} | "
            f"aPSI {o['apsi'] if o['apsi'] is not None else '—':>4} | WBGT {o['wbgt']} | "
            f"mức {o['level']} ({o['level_name']}) TB {o['device_level']}/Người {o['human_level']} | dịch {o['fluid']}")


def print_report(results):
    for res in results:
        s = res["summary"]
        print("=" * 110)
        print(f"{res['name']}  — hồ sơ {res['profile']['id']} (tuổi {res['profile']['age']}, HRrest {res['profile']['hr_rest']}, "
              f"HRmax {res['profile']['hr_max']}, yếu tố nguy cơ {res['profile'].get('risk_factors')})")
        print("-- Dòng thời gian (mỗi 10 phút + mọi phút có sự kiện):")
        ev_min = {e["minute"] for e in res["events"]}
        for o in res["outs"]:
            if o["minute"] % 10 == 0 or o["minute"] in ev_min:
                print("  " + fmt_row(o))
        print("-- Sự kiện gửi DASHBOARD ban y tế:")
        for e in res["events"]:
            print(f"  [phút {e['minute']}] MỨC {e['level']} {e['level_name']}"
                  f"{' · ' + e['dx'] if e['dx'] else ''} · ai: {e['who']} · mục tiêu: {e['target_time']}")
            print(f"      hành động: {e['dashboard_action']}")
            print(f"      app VĐV  : {e['athlete_msg'] or '(không)'}")
            if e["reasons"]:
                print(f"      lý do    : {' | '.join(e['reasons'])}")
            if e["tech"]:
                print(f"      kỹ thuật : {e['tech']}")
            qc = [f for f in e["flags"] if f.startswith("QC")]
            if qc:
                print(f"      QC       : {' | '.join(qc)}")
        qc_all = [(o["minute"], f) for o in res["outs"] for f in o["flags"] if f.startswith("QC")]
        if qc_all:
            print("-- Mẫu HR bị QC loại: " + "; ".join(f"p{m}: {f.replace('QC loại mẫu HR: ', '')}" for m, f in qc_all))
        b = res["baseline"]
        print("-- So sánh với baseline 'chỉ ECTemp' (heatstrain.run: HR thô, không QC/clip, ngưỡng thư viện) + Tc 'thật' mô phỏng:")
        mins = sorted(set(res["profile"].get("notable", [])) | {e["minute"] for e in res["events"]})
        for m in mins:
            bb, o = b[m], res["outs"][m]
            print(f"  [phút {m:>3}] HR thô {str(res['rows'][m].get('hr')):>4} | Tc mô phỏng {res['truth'][m]:.2f} | "
                  f"engine eTc {o['etc']:.2f} mức {o['level']} | baseline eTc {bb['tc_ectemp']:.2f} PSI {bb['psi']} mức {bb['level']} '{bb['label'][:40]}'")
        print("-- Tóm tắt: " + json.dumps(s, ensure_ascii=False))


def print_variants(cfg):
    """Phân tích độ nhạy cấu hình: gánh nặng báo động (S1) vs thời gian cảnh báo sớm (S2)."""
    import copy
    variants = []
    v = copy.deepcopy(cfg)
    variants.append(("A. Mặc định (CSV clinical + R5 bù 0,5 + R7 đỏ/đen + R8)", v))
    v = copy.deepcopy(cfg); v["wbgt_bump"]["min_env_level"] = 3
    variants.append(("B. R7 chỉ cộng khi cờ ĐEN", v))
    v = copy.deepcopy(cfg); v["wbgt_bump"]["min_env_level"] = 3
    for k in ("psi", "apsi"):
        v[k]["levels"][0]["threshold"] = 8.0; v[k]["levels"][1]["threshold"] = 10.0
    variants.append(("C. B + PSI/aPSI ngưỡng 8/10 (VĐV)", v))
    v = copy.deepcopy(cfg); v["etc_safety_offset_c"] = 0.0
    variants.append(("D. Không bù R5 (offset 0)", v))
    v = copy.deepcopy(cfg); v["apsi"]["enabled"] = False
    variants.append(("E. Mặc định, tắt aPSI (thiết bị không có Tsk)", v))
    v = copy.deepcopy(cfg); v["apsi"]["enabled"] = False; v["gait"]["index_threshold"] = 9.9
    variants.append(("F. Chỉ HR (không Tsk, không gia tốc)", v))
    v = copy.deepcopy(cfg); v["level3_rule"]["env_vote_min_level"] = 99
    variants.append(("G. R8 không tính phiếu WBGT đen", v))
    v = copy.deepcopy(cfg); v["level3_rule"]["env_vote_min_level"] = 99; v["apsi"]["enabled"] = False; v["gait"]["index_threshold"] = 9.9
    variants.append(("H. Chỉ HR + R8 không tính WBGT", v))
    print("=" * 110)
    print("PHÂN TÍCH ĐỘ NHẠY CẤU HÌNH (S1: phút ở mức ≥2 / ≥3 trên 121 phút; S2: phút đầu tiên mức ≥2/≥3 và mức 3 TRƯỚC khi gục [phút 80];"
          " Tc mô phỏng ≥39,5 ở phút 50, ≥40,5 ở phút 67)")
    for name, vc in variants:
        r1 = run_scenario("S1", scenario_normal, cfg=vc)
        r2 = run_scenario("S2", scenario_ehs, cfg=vc)
        l1 = [o["level"] for o in r1["outs"]]
        l2 = [o["level"] for o in r2["outs"]]
        f3 = first(l2, lambda x: x >= 3)
        print(f"  {name:<58} S1 ≥2: {sum(x >= 2 for x in l1):>3} ph, ≥3: {sum(x >= 3 for x in l1):>3} ph | "
              f"S2 đầu ≥2: p{first(l2, lambda x: x >= 2)}, ≥3: p{f3} (sớm {80 - f3 if f3 is not None else '—'} ph trước gục)")


def main(argv):
    cfg = load_config()
    if argv and argv[0] == "csv":
        opts = dict(zip(argv[2::2], argv[3::2]))
        prof = {"id": os.path.basename(argv[1]), "age": int(opts.get("--age", 30)),
                "hr_rest": float(opts.get("--hr-rest", 60)), "hr_max": float(opts["--hr-max"]) if "--hr-max" in opts else None}
        eng = AlertEngine(prof, cfg)
        with open(argv[1], newline="") as f:
            for i, r in enumerate(csv.DictReader(f)):
                obs = {k: (float(v) if v not in ("", None) else None) for k, v in r.items() if k != "minute"}
                print(fmt_row(eng.step(int(float(r.get("minute", i))), obs)))
        return 0
    results = []
    for name, fn in SCENARIOS:
        res = run_scenario(name, fn, cfg=cfg)
        res["summary"] = summarize(res)
        results.append(res)
    print_report(results)
    print_variants(cfg)
    fails = self_tests(results)
    print("=" * 110)
    print(f"TỰ KIỂM TRA bất biến an toàn (R1, R3, không khuyên uống khi NPO/RESTRICT, không CWI cho EAH): "
          f"{'ĐẠT' if not fails else 'LỖI'} ({len(fails)} vi phạm)")
    for f_ in fails[:20]:
        print("  - " + f_)
    if "--json" in argv:
        path = argv[argv.index("--json") + 1]
        with open(path, "w", encoding="utf-8") as f:
            json.dump([{k: v for k, v in r.items() if k != "rows"} for r in results], f, ensure_ascii=False, indent=1)
        print(f"Đã ghi {path}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
