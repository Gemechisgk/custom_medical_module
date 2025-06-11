from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MedicalAccident(models.Model):
    _name = 'kb.medical.accident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Medical Accident Case')
    _order = 'date_of_visit desc'

    record_id = fields.Many2one('kb.medical.record', string=_('Medical Record'), required=True)
    employee_name = fields.Char(string=_('Employee Name'), related='record_id.name', store=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string=_('Sex'), related='record_id.gender', store=True)
    date_of_visit = fields.Date(string=_('Date of Visit'), required=True, default=fields.Date.context_today)
    place_of_treatment = fields.Char(string=_('Place of Treatment'))
    type_of_disease = fields.Char(string=_('Type of Disease'))
    accident_number = fields.Char(string=_('Accident Number'), readonly=True, copy=False, default=lambda self: _('New'))
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string=_('Severity'))
    history_id = fields.Many2one('kb.medical.history', string=_('Medical History'), ondelete='cascade', required=True)

    @api.model
    def create(self, vals):
        if vals.get('accident_number', _('New')) == _('New'):
            vals['accident_number'] = self.env['ir.sequence'].next_by_code('kb.medical.accident') or _('New')
        return super(MedicalAccident, self).create(vals) 