# PH sensor extension (Yolo UNO)

Extension đọc cảm biến pH analog cho Yolo UNO (app.ohstem.vn), viết theo cấu trúc
giống `yolouno_extension_ai_vision_camera`.

## Các block

| Block | Ý nghĩa |
|-------|---------|
| **PH Init pH6.86? [pin]** | Khởi tạo cảm biến trên chân analog và lưu điểm chuẩn trung tính (nhúng đầu dò vào dung dịch pH 6.86 trước khi chạy). |
| **Calibrate PH [pH4.0 ▾] [pin]** | Thêm 1 điểm hiệu chuẩn với dung dịch chuẩn đã chọn (pH4.0 / 9.18…). ≥2 điểm → đường pH chính xác (hồi quy tuyến tính). |
| **Get PH [pin]** | Trả về giá trị pH hiện tại (0–14). |
| **Get PH Calibrate Values** | Trả về chuỗi hệ số `A=..., B=...` của công thức `pH = A*V + B`. |
| **Set PH Calibrate Values A, B** | Đặt trực tiếp hệ số A, B để khôi phục hiệu chuẩn đã lưu. |

## Nguyên lý

Điện áp đọc từ ADC được lọc trung vị (20 mẫu), rồi quy đổi ra pH theo đường thẳng
`pH = A * V + B`. Hai điểm hiệu chuẩn (vd pH 6.86 và pH 4.0) cho ra A, B bằng
hồi quy least-squares. Mặc định khi chưa calib: `A = -5.70`, `B = 21.34`.

## Kết nối phần cứng

- pH board VCC → 3V3/5V, GND → GND (chung với Yolo UNO)
- pH board OUT (analog) → chân analog đã chọn (A0…A5)

## Files

- `ph_sensor.py` — thư viện MicroPython (chạy trên thiết bị)
- `definition.js` — định nghĩa block + sinh code Python
- `toolbox.xml` — nhóm block trong toolbox
- `en.js` / `vi.js` — chuỗi ngôn ngữ
- `config.json` — khai báo extension