from odoo import models, fields, _

class MedicalAccident(models.Model):
    _name = 'kb.medical.accident'
    _description = _('Medical Accident Case')
    _order = 'date_of_visit desc'

    record_id = fields.Many2one('kb.medical.record', string=_('Medical Record'), required=True)
    employee_name = fields.Char(string=_('Employee Name'), related='record_id.name', store=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string=_('Sex'), related='record_id.gender', store=True)
    date_of_visit = fields.Date(string=_('Date of Visit'), required=True, default=fields.Date.context_today)
    place_of_treatment = fields.Char(string=_('Place of Treatment'))
    type_of_disease = fields.Char(string=_('Type of Disease')) 