// English — PH sensor (Yolo UNO)

// ==== CATEGORY & GROUPS ====
Blockly.Msg.PH_CAT = "PH";
Blockly.Msg.PH_GRP_SETUP = "Setup & Calibrate";
Blockly.Msg.PH_GRP_READ = "Read value";
Blockly.Msg.PH_GRP_CALIB = "Calibration values";

// ==== BLOCKS ====
Blockly.Msg.PH_INIT = "%1 PH Init pH6.86? %2";
Blockly.Msg.PH_CALIBRATE = "%1 Calibrate PH %2 %3";
Blockly.Msg.PH_GET = "%1 Get PH %2";
Blockly.Msg.PH_GET_CALIB = "%1 Get PH Calibrate Values";
Blockly.Msg.PH_SET_CALIB = "%1 Set PH Calibrate Values A: %2 ,B: %3";

// ==== TOOLTIPS ====
Blockly.Msg.PH_INIT_TOOLTIP = "Initialize the pH sensor on the selected analog pin and store the neutral reference point. Dip the probe in pH 6.86 buffer before running this block.";
Blockly.Msg.PH_CALIBRATE_TOOLTIP = "Add one calibration point. Dip the probe in the selected standard buffer (e.g. pH4.0 or pH9.18) then run this block. Two points give an accurate pH line.";
Blockly.Msg.PH_GET_TOOLTIP = "Read the current pH value (0-14) from the selected pin using the calibration line.";
Blockly.Msg.PH_GET_CALIB_TOOLTIP = "Return the current calibration coefficients as a string (A=..., B=...) for pH = A*V + B.";
Blockly.Msg.PH_SET_CALIB_TOOLTIP = "Directly set the calibration coefficients A and B (pH = A*V + B) to restore a saved calibration without re-dipping standard buffers.";
