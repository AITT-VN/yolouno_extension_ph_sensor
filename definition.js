const PHColorBlock = "#00a86b";

// Danh sach chan analog cho cam bien pH: CHI cho chon A0..A4.
var PH_AnalogPins = [
  ["A0", "A0"],
  ["A1", "A1"],
  ["A2", "A2"],
  ["A3", "A3"],
  ["A4", "A4"],
];

// -----------------------------------------------------------
// 1) KHOI TAO cam bien pH tren 1 chan analog
//    -> tao doi tuong toan cuc 'ph_sensor'
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_create"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_create",
      message0: "khởi tạo cảm biến pH chân %1",
      args0: [
        {
          type: "field_dropdown",
          name: "PIN",
          options: PH_AnalogPins, // chi cho chon A0..A4
        },
      ],
      previousStatement: null,
      nextStatement: null,
      colour: PHColorBlock,
      tooltip: "Khởi tạo cảm biến pH trên chân analog đã chọn",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_create"] = function (block) {
  var pin = block.getFieldValue("PIN");
  Blockly.Python.definitions_["import_ph_sensor"] = "from ph_meter import *";
  Blockly.Python.definitions_["init_ph_sensor"] =
    "ph_sensor = PHMeter(ph_pin=" + pin + "_PIN)";
  return "";
};

// -----------------------------------------------------------
// 2) DOC gia tri pH (so) - da loc nhieu, ap dung duong hieu chinh
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_read"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_read",
      message0: "đọc giá trị pH",
      colour: PHColorBlock,
      output: "Number",
      tooltip: "Đọc giá trị pH hiện tại (đã lọc nhiễu, áp dụng hiệu chỉnh)",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_read"] = function (block) {
  return ["ph_sensor.read_ph()", Blockly.Python.ORDER_FUNCTION_CALL];
};

// -----------------------------------------------------------
// 3) DOC dien ap tho tren chan pH (V) - de kiem tra / debug
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_read_voltage"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_read_voltage",
      message0: "đọc điện áp pH (V)",
      colour: PHColorBlock,
      output: "Number",
      tooltip: "Đọc điện áp (V) trên chân cảm biến pH",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_read_voltage"] = function (block) {
  return ["ph_sensor.read_voltage()", Blockly.Python.ORDER_FUNCTION_CALL];
};

// -----------------------------------------------------------
// 4) HIEU CHINH: them 1 diem calib voi pH chuan cho truoc
//    (nhung dau do vao dung dich chuan roi goi khoi nay)
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_add_point"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_add_point",
      message0: "hiệu chỉnh pH: thêm điểm với pH chuẩn %1",
      args0: [
        {
          type: "input_value",
          name: "PH",
          check: "Number",
        },
      ],
      previousStatement: null,
      nextStatement: null,
      inputsInline: true,
      colour: PHColorBlock,
      tooltip:
        "Nhúng đầu dò vào dung dịch chuẩn rồi gọi khối này để lưu 1 điểm hiệu chỉnh",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_add_point"] = function (block) {
  var ph =
    Blockly.Python.valueToCode(block, "PH", Blockly.Python.ORDER_ATOMIC) || "7";
  return "ph_sensor.add_calib_point_now(" + ph + ")\n";
};

// -----------------------------------------------------------
// 5) SO diem hieu chinh da luu (so)
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_num_points"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_num_points",
      message0: "số điểm hiệu chỉnh pH",
      colour: PHColorBlock,
      output: "Number",
      tooltip: "Số điểm hiệu chỉnh (calib) đang lưu",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_num_points"] = function (block) {
  return ["ph_sensor.n_pts", Blockly.Python.ORDER_MEMBER];
};

// -----------------------------------------------------------
// 6) XOA toan bo hieu chinh
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_reset"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_reset",
      message0: "đặt lại hiệu chỉnh pH",
      previousStatement: null,
      nextStatement: null,
      colour: PHColorBlock,
      tooltip: "Xóa toàn bộ điểm hiệu chỉnh đã lưu",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_reset"] = function (block) {
  return "ph_sensor.reset_calib()\n";
};

// -----------------------------------------------------------
// 7) IN thong tin hieu chinh (duong + cac diem calib) ra Serial
// -----------------------------------------------------------
Blockly.Blocks["uno_ph_describe"] = {
  init: function () {
    this.jsonInit({
      type: "uno_ph_describe",
      message0: "in thông tin hiệu chỉnh pH ra Serial",
      previousStatement: null,
      nextStatement: null,
      colour: PHColorBlock,
      tooltip: "In đường pH đang dùng và các điểm hiệu chỉnh đã lưu ra Serial",
      helpUrl: "",
    });
  },
  getDeveloperVars: function () {
    return ["ph_sensor"];
  },
};

Blockly.Python["uno_ph_describe"] = function (block) {
  return "ph_sensor.describe()\n";
};
