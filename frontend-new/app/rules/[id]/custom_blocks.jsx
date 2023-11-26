import Blockly from "blockly";
import {Order, pythonGenerator} from "blockly/python";

Blockly.Blocks['is_relative_difference_less_than'] = {
    init: function () {
        this.appendValueInput("NUMBER1")
            .setCheck("Number");
        this.appendValueInput("NUMBER2")
            .setCheck("Number")
        this.appendValueInput("PERCENTAGE")
            .setCheck("Number")
        this.setInputsInline(true);
        this.setOutput(true, "Boolean");
        this.setColour(300);
        this.setTooltip("This blocks checks if the difference between two numbers is less than provided percent");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['is_relative_difference_less_than'] = function (block, generator) {
    var value_number1 = generator.valueToCode(block, 'NUMBER1', Order.ATOMIC);
    var value_number2 = generator.valueToCode(block, 'NUMBER2', Order.ATOMIC);
    var value_percentage = generator.valueToCode(block, 'PERCENTAGE', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    var code = `abs(${value_number1} - ${value_number2}) / ${value_number1} * 100 < ${value_percentage}`;
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Order.NONE];
};

Blockly.Blocks['get_city_of_airport'] = {
    init: function () {
        this.appendValueInput("CODE")
            .setCheck("String")
            .appendField("get city of airport with code");
        this.setOutput(true, "String");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['get_city_of_airport'] = function (block, generator) {
    var iata_code = generator.valueToCode(block, 'CODE', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    var code = `get_city_of_airport(${iata_code})`;
    // TODO: Change ORDER_NONE to the correct strength.
    return [code, Order.NONE];
};

Blockly.Blocks['get_weight'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("get weight of");
        this.appendValueInput("LOGISTICS_OBJECT")
            .setCheck("LogisticsObject");
        this.setInputsInline(false);
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("Get weight from logistics object");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['get_weight'] = function (block, generator) {
    var logistics_object = generator.valueToCode(block, 'LOGISTICS_OBJECT', Order.ATOMIC);
    var code = 'get_gross_weight(' + logistics_object + ')';
    return [code, Order.NONE];
};

Blockly.Blocks['get_updated_logistics_object'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("updated LogisticsObject");
        this.setInputsInline(false);
        this.setOutput(true, "LogisticsObject");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['get_updated_logistics_object'] = function (block) {
    var code = '\nget_updated_logistics_object(change_request)';
    return [code, pythonGenerator.ORDER_NONE];
};

Blockly.Blocks['get_original_logistics_object'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("original LogisticsObject");
        this.setInputsInline(false);
        this.setColour(20);
        this.setOutput(true, "LogisticsObject");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['get_original_logistics_object'] = function (block, generator) {
    var code = '\nget_original_logistics_object(change_request)';
    return [code, pythonGenerator.ORDER_NONE];
};

Blockly.Blocks['decision_accepted'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Accept ChangeRequest");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(90);
        this.setTooltip("Returns a Recommendation object with decision 'ACCEPTED'.");
        this.setHelpUrl("");
    }
};

pythonGenerator['decision_accepted'] = function (block) {
    let code = 'return Recommendation(rule_id="RULE_ID", decision=Decision.ACCEPTED)\n';
    return code;
};

Blockly.Blocks['decision_rejected'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Reject ChangeRequest");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(350);
        this.setTooltip("Returns a Recommendation object with decision 'ACCEPTED'.");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['decision_rejected'] = function (block, generator) {
    let code = 'return Recommendation(rule_id="RULE_ID", decision=Decision.REJECTED)\n';
    return code;
};

Blockly.Blocks['decision_manual_check_required'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Manual check ChangeRequest");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(46);
        this.setTooltip("Returns a Recommendation object with decision 'ACCEPTED'.");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['decision_manual_check_required'] = function (block, generator) {
    let code = 'return Recommendation(rule_id="RULE_ID", decision=Decision.MANUAL_CHECK_REQUIRED)\n';
    return code;
};

Blockly.Blocks['is_typo_correction'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Is typo correction? (true/false)")
            .appendField("(Bing Spell Check API)");
        this.appendValueInput("ORIGINAL_STRING")
            .setCheck("String");
        this.appendValueInput("UPDATED_STRING")
            .setCheck("String");
        this.setInputsInline(false);
        this.setOutput(true, "Boolean");
        this.setColour(330);
        this.setTooltip("Check if the updated string is a typo correction of the original string");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['is_typo_correction'] = function (block, generator) {
    var original_string = generator.valueToCode(block, 'ORIGINAL_STRING', Order.ATOMIC);
    var updated_string = generator.valueToCode(block, 'UPDATED_STRING', Order.ATOMIC);
    var code = `is_typo_correction(${original_string}, ${updated_string})`;
    return [code, Order.NONE];
};

Blockly.Blocks['get_goods_description'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("get goods description of");
        this.appendValueInput("LOGISTICS_OBJECT")
            .setCheck("LogisticsObject");
        this.setInputsInline(false);
        this.setOutput(true, "String");
        this.setColour(230);
        this.setTooltip("Get goods description from logistics object");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['get_goods_description'] = function (block, generator) {
    var logistics_object = generator.valueToCode(block, 'LOGISTICS_OBJECT', Order.ATOMIC);
    var code = 'get_goods_description(' + logistics_object + ')';
    return [code, Order.NONE];
};
