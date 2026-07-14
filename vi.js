// Tiếng Việt — Cảm biến pH (Yolo UNO)

// ==== CATEGORY & GROUPS ====
Blockly.Msg.PH_CAT = "PH";
Blockly.Msg.PH_GRP_SETUP = "Khởi tạo & Hiệu chuẩn";
Blockly.Msg.PH_GRP_READ = "Đọc giá trị";
Blockly.Msg.PH_GRP_CALIB = "Hệ số hiệu chuẩn";

// ==== BLOCKS ====
Blockly.Msg.PH_INIT = "%1 PH Init pH6.86? %2";
Blockly.Msg.PH_CALIBRATE = "%1 Calibrate PH %2 %3";
Blockly.Msg.PH_GET = "%1 Get PH %2";
Blockly.Msg.PH_GET_CALIB = "%1 Get PH Calibrate Values";
Blockly.Msg.PH_SET_CALIB = "%1 Set PH Calibrate Values A: %2 ,B: %3";

// ==== TOOLTIPS ====
Blockly.Msg.PH_INIT_TOOLTIP = "Khởi tạo cảm biến pH trên chân analog đã chọn và lưu điểm chuẩn trung tính. Nhúng đầu dò vào dung dịch chuẩn pH 6.86 trước khi chạy block này.";
Blockly.Msg.PH_CALIBRATE_TOOLTIP = "Thêm 1 điểm hiệu chuẩn. Nhúng đầu dò vào dung dịch chuẩn đã chọn (vd pH4.0 hoặc pH9.18) rồi chạy block. Hai điểm cho đường pH chính xác.";
Blockly.Msg.PH_GET_TOOLTIP = "Đọc giá trị pH hiện tại (0-14) từ chân đã chọn theo đường hiệu chuẩn.";
Blockly.Msg.PH_GET_CALIB_TOOLTIP = "Trả về chuỗi hệ số hiệu chuẩn hiện tại (A=..., B=...) của công thức pH = A*V + B.";
Blockly.Msg.PH_SET_CALIB_TOOLTIP = "Đặt trực tiếp hệ số hiệu chuẩn A và B (pH = A*V + B) để khôi phục hiệu chuẩn đã lưu mà không cần nhúng lại dung dịch chuẩn.";
