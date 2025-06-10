-- Delete any references to the disease.occurrence model
DO $$
BEGIN
    -- Delete related records using the model name
    DELETE FROM ir_model_data WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_model_fields WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_model_constraint WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_model_relation WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_model_selection WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_ui_view WHERE model = 'kb.medical.disease.occurrence';
    DELETE FROM ir_rule WHERE model = 'kb.medical.disease.occurrence';
    
    -- Delete the model itself
    DELETE FROM ir_model WHERE model = 'kb.medical.disease.occurrence';
END $$;

-- Delete any menu items or actions referencing the model
DELETE FROM ir_ui_menu WHERE action LIKE '%kb.medical.disease.occurrence%';
DELETE FROM ir_actions_act_window WHERE res_model = 'kb.medical.disease.occurrence';
DELETE FROM ir_actions_act_window_view WHERE view_mode LIKE '%kb.medical.disease.occurrence%'; 