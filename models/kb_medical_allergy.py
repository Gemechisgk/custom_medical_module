from odoo import models, fields, api, exceptions, _

class AllergyHistory(models.Model):
	_name = 'kb.medical.allergy'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = _('Allergy List')
	_order = "name asc"

	name = fields.Char(string=_("Allergy"))