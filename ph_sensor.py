"""
ph_sensor.py - Thu vien MicroPython cho cam bien pH (analog) tren Yolo UNO.

Cach dung:
  1) Nhung dau do vao dung dich chuan pH 6.86 -> goi ph_init(pin, 6.86)
     -> luu diem chuan trung tinh (diem calib #1).
  2) Nhung vao dung dich chuan khac (vd 4.0 hoac 9.18) -> goi ph_calibrate(pin, 4.0)
     -> luu them diem calib -> tinh duong thang pH = A*V + B (least-squares).
  3) ph_get(pin) tra ve gia tri pH hien tai (0..14).

Cong thuc: pH = A * dien_ap(V) + B
  - A, B la he so calib (dung chung cho ca thu vien).
  - Co the doc/ghi truc tiep bang ph_get_calibrate_values() / ph_set_calibrate_values(a, b)
    de luu lai va khoi phuc calib ma khong can nhung lai dung dich chuan.
"""

import machine
import time

# --- He so duong pH mac dinh (dung khi CHUA calib) ---
# pH = A * V + B. Nhieu board pH analog: ~ -5.7 pH/V, offset ~ 21.34 (V tai pH7 ~ 2.5V).
DEFAULT_A = -5.70
DEFAULT_B = 21.34

_adcs = {}          # pin (int GPIO) -> doi tuong ADC (khoi tao 1 lan)
_points = []        # cac diem calib: list cua (dien_ap, pH)
_A = DEFAULT_A      # he so goc duong pH dang dung
_B = DEFAULT_B      # he so tu do

SAMPLE_COUNT = 20   # so mau moi lan doc (loc trung vi de bo nhieu)


def _get_adc(pin):
    # Tao/lay ADC cho chan. Dai do 0..3.3V (ATTN_11DB), 12-bit.
    key = str(pin)
    if key not in _adcs:
        try:
            a = machine.ADC(machine.Pin(pin))   # pin la so GPIO
        except Exception:
            a = machine.ADC(pin)                # pin da la doi tuong Pin
        try:
            a.atten(machine.ADC.ATTN_11DB)
        except Exception:
            pass
        try:
            a.width(machine.ADC.WIDTH_12BIT)
        except Exception:
            pass
        _adcs[key] = a
    return _adcs[key]


def ph_read_voltage(pin, samples=SAMPLE_COUNT):
    # Doc dien ap (V) tren chan pH - loc TRUNG VI de loai nhieu dot bien.
    a = _get_adc(pin)
    buf = []
    for _ in range(samples):
        try:
            buf.append(a.read_uv() / 1000000.0)          # micro-volt -> V (tu hieu chinh eFuse)
        except Exception:
            buf.append(a.read() / 4095.0 * 3.3)          # du phong: 12-bit -> V
        time.sleep_ms(2)
    buf.sort()
    n = len(buf)
    if n == 0:
        return 0.0
    return buf[n // 2] if (n & 1) else (buf[n // 2 - 1] + buf[n // 2]) / 2.0


def _recompute():
    # Khop duong thang least-squares (pH theo V) qua cac diem calib da luu.
    global _A, _B
    n = len(_points)
    if n >= 2:
        sx = sy = sxx = sxy = 0.0
        for v, p in _points:
            sx += v; sy += p; sxx += v * v; sxy += v * p
        d = n * sxx - sx * sx
        if abs(d) > 1e-9:
            _A = (n * sxy - sx * sy) / d
            _B = (sy - _A * sx) / n
    elif n == 1:
        v, p = _points[0]
        _B = p - _A * v          # 1 diem: giu do doc, chi dich offset


def ph_init(pin, buffer_ph=6.86):
    # Khoi tao cam bien pH tren 'pin' va luu diem chuan trung tinh (vd 6.86).
    # Nhung dau do vao dung dich chuan buffer_ph TRUOC khi goi.
    global _points
    _get_adc(pin)
    v = ph_read_voltage(pin)
    _points = [(v, float(buffer_ph))]   # reset lai danh sach, lay diem nay lam moc
    _recompute()
    return v


def ph_calibrate(pin, buffer_ph):
    # Them 1 diem calib: nhung dau do vao dung dich chuan buffer_ph (vd 4.0 / 9.18) roi goi.
    v = ph_read_voltage(pin)
    for i in range(len(_points)):
        if abs(_points[i][0] - v) < 0.03:      # ghi de neu da co diem rat gan
            _points[i] = (v, float(buffer_ph))
            break
    else:
        _points.append((v, float(buffer_ph)))
    _points.sort(key=lambda pt: pt[0])         # sap xep tang dan theo dien ap
    _recompute()
    return v


def ph_get(pin):
    # Tra ve gia tri pH hien tai (0..14) doc tu 'pin' theo duong calib.
    v = ph_read_voltage(pin)
    ph = _A * v + _B
    if ph < 0:
        ph = 0.0
    elif ph > 14:
        ph = 14.0
    return round(ph, 2)


def ph_get_calibrate_values():
    # Tra ve chuoi he so calib hien tai "A=..., B=..." de xem / luu lai.
    return "A=%.4f, B=%.4f" % (_A, _B)


def ph_set_calibrate_values(a, b):
    # Dat truc tiep he so calib pH = A*V + B (khoi phuc calib da luu truoc do).
    global _A, _B
    _A = float(a)
    _B = float(b)
