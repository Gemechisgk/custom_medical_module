from odoo import models, fields, api, exceptions, _
from datetime import date

class MedicalRecord(models.Model):
	_name = 'kb.medical.record'
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
	occupation = fields.Char(string=_("Occupation"))
	history_ids = fields.One2many("kb.medical.history", "record_id", string=_("Medical Histories"))
	history_count = fields.Integer(compute="_calculate_history_count")
	allergy_ids = fields.Many2many("kb.medical.allergy", string=_("Allergies"))
	medical_history = fields.Text(string=_("Medical History"))
	reg_no = fields.Char(string=_("Reg. No"), readonly=True, copy=False, default="New")

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

	@api.model
	def create(self, vals):
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
			
		# Generate registration number for new record
		if vals.get('reg_no', 'New') == 'New':
			vals['reg_no'] = self.env['ir.sequence'].next_by_code('kb.medical.record') or 'New'
			
		return super(MedicalRecord, self).create(vals)

	def write(self, vals):
		if vals.get('employee_id'):
			# Check if changing employee_id would create a duplicate
			for record in self:
				duplicate = self.search([
					('employee_id', '=', vals['employee_id']),
					('id', '!=', record.id),
					('company_id', '=', vals.get('company_id', record.company_id.id))
				])
				if duplicate:
					raise exceptions.ValidationError(_('Cannot update to employee %s as they already have a medical record!') % 
						self.env['hr.employee'].browse(vals['employee_id']).name)
		return super(MedicalRecord, self).write(vals)

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
							(self.employee_id.name, existing_record.reg_no)
					}
				}
			
			self.name = self.employee_id.name
			self.address = self.employee_id.address_id.street if self.employee_id.address_id else ''
			self.mobile = self.employee_id.mobile_phone or self.employee_id.work_phone or ''
			self.date_of_birth = self.employee_id.date_of_birth
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
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		args = args or []
		domain = []
		if name:
			domain = ['|', '|', '|',
				('name', operator, name),
				('employee_id.name', operator, name),
				('id_number', operator, name),
				('reg_no', operator, name)
			]
		return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

	@api.model
	def name_search(self, name='', args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', '|', '|',
				('name', operator, name),
				('employee_id.name', operator, name),
				('id_number', operator, name),
				('reg_no', operator, name)
			]
		return self.search(domain + args, limit=limit).name_get()