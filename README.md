# Cảm biến pH — Extension cho Yolo:Uno

Mục mở rộng (khối lệnh kéo–thả) giúp **đọc cảm biến pH analog** trên **Yolo:Uno (ESP32-S3)**.
Hỗ trợ **lọc nhiễu (median + EMA)**, **hiệu chỉnh nhiều điểm** bằng hồi quy tuyến tính, và **lưu điểm hiệu chỉnh vào flash** (không mất khi tắt nguồn).

---

## 1. Kết nối phần cứng

| Cảm biến pH | Yolo:Uno                        |
| ----------- | ------------------------------- |
| VCC (+)     | 3V3 (hoặc 5V nếu board cần)     |
| GND (−)     | GND                             |
| PH_OUT      | Một chân **analog**: A0 … A4    |

> Chỉ dùng được các chân analog **A0–A4**.

---

## 2. Bộ khối lệnh (6 khối)

| Khối                                           | Kiểu    | Chức năng                                              |
| ---------------------------------------------- | ------- | ------------------------------------------------------ |
| `khởi tạo cảm biến pH chân [A0]`               | lệnh    | Khởi tạo cảm biến — đặt ở **khi bắt đầu**              |
| `đọc pH`                                        | giá trị | pH hiện tại (median + EMA làm mượt + áp dụng hiệu chỉnh) |
| `đọc điện áp cảm biến pH (V)`                   | giá trị | Điện áp thô trên chân — để kiểm tra / debug            |
| `hiệu chỉnh pH: thêm điểm với pH chuẩn [6.86]` | lệnh    | Lưu 1 điểm hiệu chỉnh (V ↔ pH chuẩn)                   |
| `số điểm hiệu chỉnh pH`                         | giá trị | Số điểm hiệu chỉnh đang lưu                            |
| `xóa hiệu chỉnh pH`                             | lệnh    | Xóa toàn bộ điểm hiệu chỉnh                            |

---

## 3. Cách đo pH hoạt động

Mỗi lần gọi khối `đọc pH`, thư viện thực hiện:

1. **Đọc điện áp** chân analog (ưu tiên `read_uv()` đã hiệu chỉnh eFuse).
2. **Lọc median** 20 mẫu → loại nhiễu đột biến.
3. **Làm mượt EMA**: `V = 0.75·V_cũ + 0.25·V_mới`; nếu đổi > 0.5V (nhấc ra / nhúng vào) thì nhảy theo ngay để phản ứng nhanh.
4. **Quy đổi ra pH**: `pH = slope · V + offset`, giới hạn trong khoảng 0–14.

> **Mẹo:** EMA chỉ mượt khi khối `đọc pH` chạy **lặp lại liên tục** (trong `lặp lại mãi`). Nếu đọc đúng 1 lần thì giá trị bằng bản thô.

---

## 4. Đường mặc định (khi CHƯA hiệu chỉnh)

Khi chưa có điểm hiệu chỉnh nào, dùng đường:

```
pH = -6.4391 · V + 18.3184
```

Đường này khớp từ 2 điểm đo thực tế (V=1.467→pH 8.87 và V=2.239→pH 3.90) — **chỉ gần đúng**. Nên hiệu chỉnh lại bằng dung dịch chuẩn để chính xác.

---

## 5. Cách hiệu chỉnh (calib)

1. Nhúng đầu dò vào **dung dịch chuẩn** (vd pH 6.86).
2. Chờ ổn định vài giây, chạy khối `hiệu chỉnh pH: thêm điểm với pH chuẩn 6.86`.
3. Lặp lại với **≥2 dung dịch** khác nhau (vd 4.01, 6.86, 9.18) trải đều → đường pH chính xác nhất.

Cơ chế:

- **0 điểm** → dùng đường mặc định ở mục 4.
- **1 điểm** → giữ độ dốc mặc định, chỉ dịch offset qua điểm đó.
- **≥2 điểm** → khớp đường thẳng least-squares qua các điểm.

Điểm hiệu chỉnh được lưu vào file **`ph_calib.json`** trên flash của board → **giữ nguyên sau khi tắt/mở nguồn**. Dùng khối `xóa hiệu chỉnh pH` để xóa và quay về đường mặc định.

---

## 6. Ví dụ chương trình

```
khi bắt đầu:
    khởi tạo cảm biến pH chân A0

lặp lại mãi:
    hiển thị OLED  ⟵  ghép chuỗi "pH = " với  (đọc pH)
    đợi 0.25 giây
```

---

## 7. Cài đặt vào OhStem App / Yolo:Uno

1. Nén cả thư mục này thành `.zip` (hoặc trỏ tới URL repo Git).
2. Trong trình soạn thảo Yolo:Uno: **Mở rộng → Nhập extension** → chọn file `.zip` / dán URL.
3. Nhóm khối **"Cảm biến pH"** sẽ xuất hiện trong bảng khối, sẵn sàng kéo–thả.
