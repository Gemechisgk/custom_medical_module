from odoo import models, fields, _

class MedicalDeath(models.Model):
    _name = 'kb.medical.death'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Medical Death Record')
    _order = 'date_of_expiry desc'

    record_id = fields.Many2one('kb.medical.record', string=_('Medical Record'), required=True)
    employee_name = fields.Char(string=_('Employee Name'), related='record_id.name', store=True)
    cause_of_death = fields.Char(string=_('Cause of Death'))
    date_of_expiry = fields.Date(string=_('Date of Expiry'), required=True) 