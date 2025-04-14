from odoo import models, fields, api, exceptions, _
from datetime import date

class MedicalRecord(models.Model):
	_name = 'kb.medical.record'
	_description = _('Medical Records')
	_order = "name desc"

	company_id = fields.Many2one("res.company", ondelete="restrict", default=lambda self: self.env.company)
	employee_id = fields.Many2one("hr.employee", string=_("Employee"), ondelete="restrict") 
	name = fields.Char(string=_("Patient"), required=True)
	address = fields.Char(string=_("Address"))
	mobile = fields.Char(string=_("Mobile Number"), required=True)
	date_of_birth = fields.Date(string=_("Birth Date"), required=True)
	age = fields.Integer(string=_("Age"), compute="_compute_age", store=True)  # New field
	id_number = fields.Char(string=_("ID Number"), required=True)
	gender = fields.Selection([
		('male', _('Male')),
		('female', _('Female'))
	], string=_("Gender"), required=True)
	religion = fields.Selection([
		('christian', _('Christian')),
		('islam', _('Islam')),
		('catholic', _('Catholic')),
		('other', _('Other'))
	], string=_("Religion"))
	occupation = fields.Char(string=_("Occupation"))
	history_ids = fields.One2many("kb.medical.history", "record_id", string=_("Medical Histories"))
	history_count = fields.Integer(compute="_calculate_history_count")
	allergy_ids = fields.Many2many("kb.medical.allergy", string=_("Allergies"))
	medical_history = fields.Text(string=_("Medical History"))
	reg_no = fields.Char(string=_("Reg. No"), readonly=True, copy=False, default="New")

	@api.depends("history_ids")
	def _calculate_history_count(self):
		for record in self:
			record.history_count = len(record.history_ids)

	@api.depends("date_of_birth")
	def _compute_age(self):
		"""Calculate age based on the date of birth."""
		today = date.today()
		for record in self:
			if record.date_of_birth:
				birth_date = record.date_of_birth
				record.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
			else:
				record.age = 0

	@api.onchange('employee_id')
	def _onchange_employee_id(self):
		"""Auto-fill fields based on the selected employee."""
		if self.employee_id:
			self.name = self.employee_id.name
			self.address = self.employee_id.address_id.street if self.employee_id.address_id else ''
			self.mobile = self.employee_id.mobile_phone or self.employee_id.work_phone or ''
			self.date_of_birth = self.employee_id.date_of_birth  # Fetch birthdate from employee
			self.gender = 'male' if self.employee_id.gender == 'male' else 'female'
			self.occupation = self.employee_id.job_id.name if self.employee_id.job_id else ''
			self.id_number = self.employee_id.id_number_generated or False

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

	@api.model
	def create(self, vals):
		if vals.get('reg_no', 'New') == 'New':
			vals['reg_no'] = self.env['ir.sequence'].next_by_code('kb.medical.record') or 'New'
		return super(MedicalRecord, self).create(vals)