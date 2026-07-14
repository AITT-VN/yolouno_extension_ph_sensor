# ============================================================
#  THU VIEN CAM BIEN pH - Yolo:Uno (ESP32-S3, MicroPython)
# ============================================================
#  Dung cho extension "Cam bien pH" (khoi lenh keo-tha).
#  - Doc dien ap chan analog (loc trung vi loai nhieu).
#  - Hieu chinh (calib) nhieu diem -> hoi quy tuyen tinh least-squares.
#  - Luu diem calib vao flash (file JSON) -> khong mat khi tat nguon.
#  KHONG phu thuoc man hinh: phan hien thi do khoi lenh khac lo.
# ============================================================

import json
from machine import Pin, ADC

# --- Duong pH mac dinh (khi CHUA co diem calib nao) ---
# pH = PH_SLOPE_DEFAULT * V + PH_OFFSET_DEFAULT
# Khop tu 2 diem do thuc te:
#   #1: V=1.467 -> pH 8.87
#   #2: V=2.239 -> pH 3.90
# => slope = (3.90 - 8.87) / (2.239 - 1.467) = -6.4391
#    offset = 8.87 - (-6.4391 * 1.467)        =  18.3184
PH_SLOPE_DEFAULT = -6.4391
PH_OFFSET_DEFAULT = 18.3184


class PHMeter:
    """Doc & hieu chinh cam bien pH analog."""

    def __init__(self, ph_pin, sample_count=20, calib_file="ph_calib.json", max_pts=6,
                 ema_alpha=0.25, ema_jump_v=0.5):
        self.sample_count = sample_count     # so mau moi lan doc (median)
        self.calib_file = calib_file         # file luu diem calib
        self.max_pts = max_pts               # so diem calib toi da

        # --- Loc lam muot EMA (trung binh truot mu) tren dien ap ---
        # alpha cang NHO -> cang muot/on dinh nhung phan ung cham hon.
        # Neu dien ap doi lon hon ema_jump_v (nhac ra / nhung vao) -> nhay theo
        # ngay de phan ung nhanh, khong bi tre.
        self.ema_alpha = ema_alpha
        self.ema_jump_v = ema_jump_v
        self._v_ema = None                   # trang thai EMA (None = chua khoi tao)

        # ADC: dai do 0..3.3V (ATTN_11DB)
        self.adc = ADC(Pin(ph_pin, Pin.IN))
        try:
            self.adc.atten(ADC.ATTN_11DB)
        except AttributeError:
            pass

        # He so duong pH dang dung
        self.slope = PH_SLOPE_DEFAULT
        self.offset = PH_OFFSET_DEFAULT

        # Diem calib: danh sach [v, ph], sap tang dan theo V
        self.pts = []
        self.load_calib()

    # ------------------------------------------------------------
    #  DOC DIEN AP (V) - loc TRUNG VI (median)
    # ------------------------------------------------------------
    def read_voltage(self):
        buf = []
        for _ in range(self.sample_count):
            buf.append(self._read_uv())
        buf.sort()
        n = self.sample_count
        if n & 1:
            uv = buf[n // 2]
        else:
            uv = (buf[n // 2 - 1] + buf[n // 2]) / 2.0
        return uv / 1_000_000.0   # microvolt -> V

    def read_voltage_smooth(self):
        """Doc dien ap (V) da lam muot bang EMA.
        Neu thay doi lon hon ema_jump_v (nhac dau do ra/ nhung vao) -> nhay
        theo ngay de phan ung nhanh; con lai thi loc muot."""
        v = self.read_voltage()
        if self._v_ema is None or abs(v - self._v_ema) > self.ema_jump_v:
            self._v_ema = v
        else:
            a = self.ema_alpha
            self._v_ema = (1.0 - a) * self._v_ema + a * v
        return self._v_ema

    def reset_smooth(self):
        """Xoa trang thai EMA (lan doc ke tiep se khoi tao lai)."""
        self._v_ema = None

    def _read_uv(self):
        # Uu tien read_uv() (da hieu chinh eFuse); neu firmware khong co -> quy doi tho.
        try:
            return self.adc.read_uv()
        except AttributeError:
            try:
                return int(self.adc.read_u16() * 3.3 / 65535 * 1_000_000)
            except AttributeError:
                return int(self.adc.read() * 3.3 / 4095 * 1_000_000)

    # ------------------------------------------------------------
    #  TINH pH
    # ------------------------------------------------------------
    def calc_ph(self, v):
        """Doi dien ap (V) -> pH theo duong da khop, gioi han 0..14."""
        ph = self.slope * v + self.offset
        if ph < 0:
            ph = 0.0
        elif ph > 14:
            ph = 14.0
        return ph

    def read_ph(self):
        """Doc pH hien tai (median + EMA lam muot + ap dung hieu chinh)."""
        return self.calc_ph(self.read_voltage_smooth())

    def read_ph_raw(self):
        """Doc pH tuc thoi, CHI median (khong EMA) - de kiem tra / phan ung nhanh."""
        return self.calc_ph(self.read_voltage())

    def update_regression(self):
        """Khop duong thang least-squares (pH theo V) qua cac diem calib.
        >=2 diem: hoi quy; 1 diem: dich offset; 0 diem: dung mac dinh."""
        n = len(self.pts)
        if n <= 0:
            self.slope = PH_SLOPE_DEFAULT
            self.offset = PH_OFFSET_DEFAULT
            return
        if n == 1:
            v, ph = self.pts[0]
            self.slope = PH_SLOPE_DEFAULT
            self.offset = ph - self.slope * v
            return
        sx = sy = sxx = sxy = 0.0
        for v, ph in self.pts:
            sx += v
            sy += ph
            sxx += v * v
            sxy += v * ph
        denom = n * sxx - sx * sx
        if abs(denom) < 1e-9:
            return
        self.slope = (n * sxy - sx * sy) / denom
        self.offset = (sy - self.slope * sx) / n

    # ------------------------------------------------------------
    #  HIEU CHINH (CALIB)
    # ------------------------------------------------------------
    def add_calib_point(self, v, ph):
        """Them 1 diem calib (v, ph). Ghi de neu da co diem rat gan (theo V).
        Neu day -> thay diem gan nhat. Sau do sap xep & luu flash."""
        for p in self.pts:
            if abs(p[0] - v) < 0.03:
                p[0] = v
                p[1] = ph
                self._finish_calib()
                return
        if len(self.pts) >= self.max_pts:
            nearest = min(self.pts, key=lambda q: abs(q[0] - v))
            nearest[0] = v
            nearest[1] = ph
        else:
            self.pts.append([v, ph])
        self._finish_calib()

    def add_calib_point_now(self, ph):
        """Doc dien ap hien tai va them lam 1 diem calib voi pH chuan 'ph'.
        (Nhung dau do vao dung dich chuan roi goi ham nay.)"""
        v = self.read_voltage()
        self.add_calib_point(v, ph)
        return v

    def _finish_calib(self):
        self.pts.sort(key=lambda q: q[0])
        self.save_calib()
        self.update_regression()

    @property
    def n_pts(self):
        return len(self.pts)

    def reset_calib(self):
        """Xoa toan bo diem calib."""
        self.pts = []
        self.save_calib()
        self.update_regression()

    # ------------------------------------------------------------
    #  LUU / NAP FLASH (file JSON)
    # ------------------------------------------------------------
    def save_calib(self):
        try:
            with open(self.calib_file, "w") as f:
                json.dump(self.pts, f)
        except OSError as e:
            print("!! Loi luu calib pH:", e)

    def load_calib(self):
        try:
            with open(self.calib_file, "r") as f:
                pts = json.load(f)
            self.pts = [[float(a), float(b)] for a, b in pts][: self.max_pts]
            self.pts.sort(key=lambda q: q[0])
        except (OSError, ValueError):
            self.pts = []
        self.update_regression()
