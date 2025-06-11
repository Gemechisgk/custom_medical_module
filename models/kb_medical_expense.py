from odoo import models, fields, _

class MedicalExpense(models.Model):
    _name = 'kb.medical.expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Medical Expense')
    _order = 'date desc'

    record_id = fields.Many2one('kb.medical.record', string=_('Medical Record'), required=True)
    name = fields.Char(string=_('Patient Name'), related='record_id.name', store=True)
    date = fields.Date(string=_('Date'), required=True, default=fields.Date.context_today)
    payment_made = fields.Float(string=_('Payment Made'))
    particulars = fields.Char(string=_('Particulars of Payment'))
    remarks = fields.Text(string=_('Remarks')) 