# ============================================================
#  SCRIPT TEST CALIB pH - Yolo:Uno (MicroPython)
# ============================================================
#  Muc dich: calib 2 diem theo but do pH 5in1 (lam chuan) va
#  XEM gia tri pH thay doi ra sao TRUOC va SAU khi calib.
#
#  CACH DUNG:
#   1) Nap file nay + ph_meter.py len board.
#   2) Sua PH_PIN ben duoi cho dung chan dang cam cam bien.
#   3) Chay:  import test_ph_calib   (hoac nhan Run trong Thonny)
#   4) Lam theo huong dan in ra Serial:
#        - Nhung ca dau do + but 5in1 vao cung 1 coc dung dich.
#        - Doc pH tren but 5in1, go so do vao Serial roi Enter.
#        - Script tu doc dien ap, luu diem, in log so sanh.
# ============================================================

from ph_meter import PHMeter
import time

# --- CHON CHAN cam bien pH ---
# Neu chay tren Yolo:Uno co dinh nghia A0_PIN..A4_PIN thi dung truc tiep:
#   PH_PIN = A0_PIN
# Neu khong, dat so GPIO tuong ung voi chan analog dang cam.
try:
    PH_PIN = A0_PIN          # co san khi chay tren firmware Yolo:Uno
except NameError:
    PH_PIN = 1               # <-- SUA lai so GPIO cho dung neu bao loi


def doc_trung_binh(sensor, lan=10, nghi=0.2):
    """Doc pH va V nhieu lan roi lay trung binh cho on dinh khi log."""
    tong_v = 0.0
    tong_ph = 0.0
    for _ in range(lan):
        v = sensor.read_voltage_smooth()
        tong_v += v
        tong_ph += sensor.calc_ph(v)
        time.sleep(nghi)
    return tong_v / lan, tong_ph / lan


def nhap_so(nhac):
    """Doc 1 so tu Serial, lap lai neu go sai."""
    while True:
        s = input(nhac).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("  !! Khong phai so hop le, thu lai.")


def calib_1_diem(sensor, thu_tu):
    print("\n===== CALIB DIEM #{} =====".format(thu_tu))
    print("  - Nhung CA dau do va but 5in1 vao cung 1 coc dung dich.")
    print("  - Cho ca hai on dinh (~15-30 giay).")
    ph_chuan = nhap_so("  Doc pH tren but 5in1 va go vao day: ")

    # log truoc khi luu diem
    v_truoc, ph_truoc = doc_trung_binh(sensor)
    print("  [Truoc khi luu] V = {:.3f}  |  pH (duong hien tai) = {:.2f}".format(v_truoc, ph_truoc))
    print("  Chenh lech so voi but: {:+.2f} pH".format(ph_truoc - ph_chuan))

    # luu diem calib bang dien ap dang doc
    v_luu = sensor.add_calib_point_now(ph_chuan)
    print("  >> Da luu diem: V = {:.3f}  ->  pH chuan {:.2f}".format(v_luu, ph_chuan))

    # log sau khi cap nhat duong
    sensor.describe()
    v_sau, ph_sau = doc_trung_binh(sensor)
    print("  [Sau khi luu ] V = {:.3f}  |  pH (duong moi) = {:.2f}".format(v_sau, ph_sau))
    print("  Chenh lech so voi but: {:+.2f} pH".format(ph_sau - ph_chuan))


def main():
    sensor = PHMeter(ph_pin=PH_PIN)

    print("\n############################################")
    print("#   TEST CALIB pH - so sanh voi but 5in1   #")
    print("############################################")
    print("\n>>> Trang thai BAN DAU (truoc khi calib):")
    sensor.describe()
    v0, ph0 = doc_trung_binh(sensor)
    print("    V hien tai = {:.3f}  |  pH (mac dinh) = {:.2f}".format(v0, ph0))

    # tuy chon: xoa calib cu de test tu dau
    tra_loi = input("\nXoa calib cu de test lai tu dau? (y/n): ").strip().lower()
    if tra_loi == "y":
        sensor.reset_calib()
        print(">> Da xoa. Quay ve duong mac dinh.")
        sensor.describe()

    # calib 2 diem
    calib_1_diem(sensor, 1)
    calib_1_diem(sensor, 2)

    # ket qua cuoi
    print("\n============ KET QUA SAU 2 DIEM ============")
    sensor.describe()
    print("\n>>> Doc pH lien tuc de kiem tra (Ctrl+C de dung):")
    try:
        while True:
            v = sensor.read_voltage_smooth()
            print("   V = {:.3f}  |  pH = {:.2f}".format(v, sensor.calc_ph(v)))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n>> Da dung. Cac diem calib van luu trong ph_calib.json.")


main()
