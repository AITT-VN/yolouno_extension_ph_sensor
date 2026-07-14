// ============ PHAN 1: DANG KY BLOCK (luon chay truoc, khong phu thuoc gi) ============

Blockly.Blocks['ph_init'] = {
  init: function() {
    this.jsonInit({
      "type": "ph_init",
      "message0": "PH Init pH6.86? %1",
      "args0": [
        {
          type: "field_dropdown",
          name: "PIN",
          options: [
            ["A0", "A0"],
            ["A1", "A1"],
            ["A2", "A2"],
            ["A3", "A3"],
            ["A4", "A4"]
          ],
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#26A69A",
      "tooltip": "Khởi tạo cảm biến pH và lưu điểm chuẩn trung tính. Nhúng đầu dò vào dung dịch chuẩn pH 6.86 trước khi chạy khối này.",
      "helpUrl": ""
    });
  }
};

Blockly.Blocks['ph_calibrate'] = {
  init: function() {
    this.jsonInit({
      "type": "ph_calibrate",
      "message0": "Calibrate PH %1 %2",
      "args0": [
        {
          type: "field_dropdown",
          name: "BUFFER",
          options: [
            ["PH4.0", "4.0"],
            ["PH6.86", "6.86"],
            ["PH7.0", "7.0"],
            ["PH9.18", "9.18"],
            ["PH10.0", "10.0"]
          ],
        },
        {
          type: "field_dropdown",
          name: "PIN",
          options: [
            ["A0", "A0"],
            ["A1", "A1"],
            ["A2", "A2"],
            ["A3", "A3"],
            ["A4", "A4"]
          ],
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#26A69A",
      "tooltip": "Thêm 1 điểm hiệu chuẩn. Nhúng đầu dò vào dung dịch chuẩn đã chọn (vd pH4.0) rồi chạy khối. Hai điểm cho đường pH chính xác.",
      "helpUrl": ""
    });
  }
};

Blockly.Blocks['ph_get'] = {
  init: function() {
    this.jsonInit({
      "type": "ph_get",
      "message0": "Get PH %1",
      "args0": [
        {
          type: "field_dropdown",
          name: "PIN",
          options: [
            ["A0", "A0"],
            ["A1", "A1"],
            ["A2", "A2"],
            ["A3", "A3"],
            ["A4", "A4"]
          ],
        }
      ],
      "output": "Number",
      "colour": "#26A69A",
      "tooltip": "Đọc giá trị pH hiện tại (0-14) từ chân đã chọn",
      "helpUrl": ""
    });
  }
};

Blockly.Blocks['ph_get_calib'] = {
  init: function() {
    this.jsonInit({
      "type": "ph_get_calib",
      "message0": "Get PH Calibrate Values",
      "output": "String",
      "colour": "#26A69A",
      "tooltip": "Trả về hệ số hiệu chuẩn hiện tại (A=..., B=...) của công thức pH = A*V + B",
      "helpUrl": ""
    });
  }
};

Blockly.Blocks['ph_set_calib'] = {
  init: function() {
    this.jsonInit({
      "type": "ph_set_calib",
      "message0": "Set PH Calibrate Values A: %1 ,B: %2",
      "args0": [
        {
          type: "field_number",
          name: "A",
          value: 0
        },
        {
          type: "field_number",
          name: "B",
          value: 0
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#26A69A",
      "tooltip": "Đặt trực tiếp hệ số hiệu chuẩn A và B (pH = A*V + B) để khôi phục hiệu chuẩn đã lưu",
      "helpUrl": ""
    });
  }
};

// ============ PHAN 2: GENERATOR PYTHON (bao ve neu Blockly.Python chua san sang) ============

(function() {
  var PyGen = Blockly.Python;
  if (!PyGen) {                       // python.js cua app loi/ chua nap -> tao cho de khong vo script
    PyGen = Blockly.Python = {};
  }
  if (!PyGen.definitions_) PyGen.definitions_ = {};
  if (PyGen.ORDER_ATOMIC === undefined) PyGen.ORDER_ATOMIC = 0;

  PyGen['ph_init'] = function(block) {
    var pin = block.getFieldValue('PIN');
    Blockly.Python.definitions_['import_ph_sensor'] = 'from ph_sensor import *';
    var code = 'ph_init(' + pin + '_PIN, 6.86)\n';
    return code;
  };

  PyGen['ph_calibrate'] = function(block) {
    var buffer = block.getFieldValue('BUFFER');
    var pin = block.getFieldValue('PIN');
    Blockly.Python.definitions_['import_ph_sensor'] = 'from ph_sensor import *';
    var code = 'ph_calibrate(' + pin + '_PIN, ' + buffer + ')\n';
    return code;
  };

  PyGen['ph_get'] = function(block) {
    var pin = block.getFieldValue('PIN');
    Blockly.Python.definitions_['import_ph_sensor'] = 'from ph_sensor import *';
    var code = 'ph_get(' + pin + '_PIN)';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  PyGen['ph_get_calib'] = function(block) {
    Blockly.Python.definitions_['import_ph_sensor'] = 'from ph_sensor import *';
    var code = 'ph_get_calibrate_values()';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  PyGen['ph_set_calib'] = function(block) {
    var a = block.getFieldValue('A');
    var b = block.getFieldValue('B');
    Blockly.Python.definitions_['import_ph_sensor'] = 'from ph_sensor import *';
    var code = 'ph_set_calibrate_values(' + a + ', ' + b + ')\n';
    return code;
  };
})();
