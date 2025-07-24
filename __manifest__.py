# -*- coding: utf-8 -*-
{
    'name': "Medical Records",

    'summary': "Track Medical Records",

    'description': """
    Enable users to manage patient medical records.
    """,

    'author': "Kode-Bruh (Timotius Randy Putra Wiyono)",
    'website': "https://www.kode-bruh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'extended_employee_badge'],

    # always loaded
    'data': [
        'data/module_category.xml',
        'security/medical_doctor_report_groups.xml',
        'security/medical_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_sequence_accident.xml',
        'data/kb_medical_allergy.xml',
        'views/kb_medical_expense.xml',
        'views/kb_medical_accident.xml',
        'views/kb_medical_death.xml',
        'views/kb_medical_disease_occurrence.xml',
        'views/kb_medical_doctor_report_views.xml',
        'report/kb_medical_record.xml',
        'report/prescription_template.xml',
        'report/referral_template.xml',
        'views/kb_medical_record.xml',
        'views/kb_medical_allergy.xml',
        'views/kb_medical_disease.xml',
        'views/kb_medical_history.xml',
        'views/kb_medical_history_other.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/res_users.xml',
        'demo/ir_sequence.xml',
        'demo/kb_medical_record.xml',
        'demo/kb_medical_history.xml',
        'demo/kb_medical_history_procedure.xml',
        'demo/kb_medical_history_treatment.xml',
    ],
    'application': True,
}

