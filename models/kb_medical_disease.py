from odoo import models, fields, _

class MedicalDisease(models.Model):
    _name = 'kb.medical.disease'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Disease List')
    _order = 'name asc'

    name = fields.Char(string=_('Disease'), required=True)

class MedicalDiseaseOccurrence(models.Model):
    _name = 'kb.medical.disease.occurrence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Disease Occurrence')
    _order = 'date desc'

    type_of_disease = fields.Char(string=_('Type of Disease'), required=True)
    number_of_occurrences = fields.Integer(string=_('Number of Occurrences'), required=True)
    remarks = fields.Text(string=_('Remarks'))
    date = fields.Date(string=_('Date'), required=True, default=fields.Date.context_today) 