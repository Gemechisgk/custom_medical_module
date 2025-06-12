from odoo import models, fields, api, tools, _

class DoctorReport(models.Model):
    _name = 'kb.medical.doctor.report'
    _description = _('Doctor Report')
    _auto = False

    doctor_id = fields.Many2one('res.users', string=_('Doctor'), readonly=True)
    doctor_name = fields.Char(string=_('Doctor Name'), readonly=True)
    total_patients = fields.Integer(string=_('Total Patients'), readonly=True)
    total_consultations = fields.Integer(string=_('Total Consultations'), readonly=True)
    total_procedures = fields.Integer(string=_('Total Procedures'), readonly=True)
    total_treatments = fields.Integer(string=_('Total Treatments'), readonly=True)
    total_accidents = fields.Integer(string=_('Total Accidents'), readonly=True)

    def init(self):
        # Create or replace the view directly
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s as (
                SELECT
                    row_number() OVER () as id,
                    h.user_id as doctor_id,
                    rp.name as doctor_name,
                    COUNT(DISTINCT h.record_id) as total_patients,
                    COUNT(DISTINCT h.id) as total_consultations,
                    COUNT(DISTINCT p.id) as total_procedures,
                    COUNT(DISTINCT t.id) as total_treatments,
                    COUNT(DISTINCT a.id) as total_accidents
                FROM kb_medical_history h
                LEFT JOIN res_users ru ON ru.id = h.user_id
                LEFT JOIN res_partner rp ON rp.id = ru.partner_id
                LEFT JOIN kb_medical_history_procedure p ON p.history_id = h.id
                LEFT JOIN kb_medical_history_treatment t ON t.history_id = h.id
                LEFT JOIN kb_medical_accident a ON a.history_id = h.id
                WHERE h.user_id IS NOT NULL
                GROUP BY h.user_id, rp.name
            )
        """ % self._table) 