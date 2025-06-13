from odoo import models, fields, api, exceptions, _
from datetime import date

class MedicalRecord(models.Model):
	_name = 'kb.medical.record'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = _('Medical Records')
	_order = "name desc"
	_sql_constraints = [
		('employee_uniq', 'unique(employee_id)', 'A medical record already exists for this employee!')
	]

	company_id = fields.Many2one("res.company", ondelete="restrict", default=lambda self: self.env.company)
	employee_id = fields.Many2one("hr.employee", string=_("Employee"), ondelete="restrict", required=True) 
	name = fields.Char(string=_("Patient"), required=True)
	address = fields.Char(string=_("Address"))
	mobile = fields.Char(string=_("Mobile Number"), required=True)
	date_of_birth = fields.Date(string=_("Birth Date"), required=True)
	age = fields.Integer(string=_("Age"), compute="_compute_age", store=True)  
	id_number = fields.Char(string=_("ID Number"), required=True)
	gender = fields.Selection([
		('male', _('Male')),
		('female', _('Female'))
	], string=_("Gender"), required=True)
	history_ids = fields.One2many("kb.medical.history", "record_id", string=_("Medical Histories"))
	history_count = fields.Integer(compute="_calculate_history_count")
	allergy_ids = fields.Many2many("kb.medical.allergy", string=_("Allergies"))
	medical_history = fields.Text(string=_("Medical History"))
	expense_ids = fields.One2many('kb.medical.expense', 'record_id', string=_('Expenses'))
	department_id = fields.Many2one('hr.department', string=_('Department'))
	patient_dead = fields.Boolean(string=_('Patient Dead'), default=False)
	cause_of_death = fields.Char(string=_('Cause of Death'))
	date_of_death = fields.Datetime(string=_('Date and Time of Death'))

	def action_redirect_to_existing(self):
		"""Redirect to existing record"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': _('Medical Record'),
			'res_model': 'kb.medical.record',
			'view_mode': 'form',
			'res_id': self.id,
			'target': 'current',
			'views': [[False, 'form']],
		}

	@api.constrains('employee_id')
	def _check_employee_unique(self):
		for record in self:
			if record.employee_id:
				duplicate = self.search([
					('employee_id', '=', record.employee_id.id),
					('id', '!=', record.id)
				])
				if duplicate:
					raise exceptions.ValidationError(_('A medical record already exists for employee %s!') % record.employee_id.name)

	@api.onchange('employee_id')
	def _onchange_employee_id(self):
		"""Auto-fill fields based on the selected employee."""
		if self.employee_id:
			# Check for existing record
			existing_record = self.search([
				('employee_id', '=', self.employee_id.id),
				('id', '!=', self.id or 0)
			], limit=1)
			
			if existing_record:
				return {
					'warning': {
						'title': _('Warning'),
						'message': _('Employee %s already has a medical record (ID: %s). Please search for the existing record instead of creating a new one.') % 
							(self.employee_id.name, existing_record.id_number)
					}
				}
			
			self.name = self.employee_id.name
			self.address = self.employee_id.address_id.street if self.employee_id.address_id else ''
			self.mobile = self.employee_id.mobile_phone or self.employee_id.work_phone or ''
			self.date_of_birth = self.employee_id.date_of_birth
			self.gender = 'male' if self.employee_id.gender == 'male' else 'female'
			self.id_number = self.employee_id.id_number_generated or False
			self.department_id = self.employee_id.department_id.id if self.employee_id.department_id else False

	@api.model_create_multi
	def create(self, vals_list):
		for vals in vals_list:
			if not vals.get('employee_id'):
				raise exceptions.ValidationError(_('Employee is required to create a medical record!'))
				
			# Check for existing record
			existing_record = self.search([
				('employee_id', '=', vals['employee_id']),
				('company_id', '=', vals.get('company_id', self.env.company.id))
			], limit=1)
			
			if existing_record:
				# If we're coming from the warning dialog, redirect to the existing record
				if self._context.get('redirect_to_existing'):
					return existing_record.action_redirect_to_existing()
				# Update existing record
				existing_record.write(vals)
				return existing_record
				
		return super(MedicalRecord, self).create(vals_list)

	def write(self, vals):
		res = super(MedicalRecord, self).write(vals)
		for record in self:
			if vals.get('patient_dead') and record.patient_dead:
				death_model = self.env['kb.medical.death']
				existing = death_model.search([('record_id', '=', record.id)], limit=1)
				if not existing:
					death_model.create({
						'record_id': record.id,
						'employee_name': record.name,
						'cause_of_death': '',
						'date_of_expiry': fields.Date.today(),
					})
		return res

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
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		args = args or []
		domain = []
		if name:
			domain = ['|', '|',
				('name', operator, name),
				('employee_id.name', operator, name),
				('id_number', operator, name)
			]
		return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

	@api.model
	def name_search(self, name='', args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', '|',
				('name', operator, name),
				('employee_id.name', operator, name),
				('id_number', operator, name)
			]
		return self.search(domain + args, limit=limit).name_get()

	@api.constrains('patient_dead', 'cause_of_death', 'date_of_death')
	def _check_death_fields_required(self):
		for record in self:
			if record.patient_dead:
				if not record.cause_of_death or not record.date_of_death:
					raise exceptions.ValidationError(_('Cause of Death and Date and Time of Death are required when Patient Dead is checked.'))

	@api.constrains('patient_dead')
	def _prohibit_new_history_if_dead(self):
		for record in self:
			if record.patient_dead and record.history_ids:
				for history in record.history_ids:
					if self.env.context.get('default_record_id') == record.id:
						raise exceptions.ValidationError(_('Cannot add new history for a deceased patient.'))