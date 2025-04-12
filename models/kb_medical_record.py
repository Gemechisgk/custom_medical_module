from odoo import models, fields, api, exceptions, _

class MedicalRecord(models.Model):
	_name = 'kb.medical.record'
	_description = _('Medical Records')
	_order = "name desc"

	company_id = fields.Many2one("res.company", ondelete="restrict", default=lambda self: self.env.company)
	name = fields.Char(string=_("Patient"), required=True)
	address = fields.Char(string=_("Address"))
	mobile = fields.Char(string=_("Mobile Number"), required=True)
	date_of_birth = fields.Date(string=_("Birth Date"), required=True)
	citizenship_number = fields.Char(string=_("NIK"))
	gender = fields.Selection([
		('male', _('Male')),
		('female', _('Female'))
	], string=_("Gender"), required=True)
	religion = fields.Selection([
		('buddha', _('Buddha')),
		('islam', _('Islam')),
		('hindu', _('Hindu')),
		('christian', _('Christian')),
		('catholic', _('Catholic')),
		('other', _('Other'))
	], string=_("Religion"))
	occupation = fields.Char(string=_("Occupation"))
	history_ids = fields.One2many("kb.medical.history", "record_id", string=_("Medical Histories"))
	history_count = fields.Integer(compute="_calculate_history_count")
	allergy_ids = fields.Many2many("kb.medical.allergy", string=_("Allergies"))
	medical_history = fields.Text(string=_("Medical History"))

	@api.depends("history_ids")
	def _calculate_history_count(self):
		for record in self:
			record.history_count = len(record.history_ids)

	def view_medical_histories(self):
		for record in self:
			return {
				'type': 'ir.actions.act_window',
				'name': '%s Medical Histories' % record.name,
				'res_model': 'kb.medical.history',
				'domain': "[('record_id', '=', %s)]" % record.id,
				'view_mode': 'list,form',
				'target': 'current',
			}

	def create_medical_histories(self):
		for record in self:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Create New Medical History',
				'res_model': 'kb.medical.history',
				'view_mode': 'form',
				'target': 'current',
				'context': {
					'default_record_id': record.id,
				}
			}