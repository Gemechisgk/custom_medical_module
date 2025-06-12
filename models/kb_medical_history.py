from odoo import models, fields, api, exceptions, _
from datetime import datetime

class MedicalHistory(models.Model):
	_name = 'kb.medical.history'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = _('Medical Histories')
	_order = "date desc"

	record_id = fields.Many2one("kb.medical.record", ondelete="cascade", string=_("Medical Record"), required=True)
	user_id = fields.Many2one("res.users", ondelete="restrict", string=_("Doctor in Charge"), required=True, default=lambda self: self.env.uid)
	name = fields.Char(string=_("Reference"), default=_("New"))
	date = fields.Datetime(string=_("Date"), default=lambda *a: datetime.now())
	test_result = fields.Text(string=_("Test Result"))
	complaints = fields.Text(string=_("Complaints"))
	diagnosis = fields.Text(string=_("Diagnosis"))
	medical_advice = fields.Text(string=_("Medical Advice"))
	procedure_ids = fields.One2many("kb.medical.history.procedure", "history_id", string=_("Procedures"))
	drug_prescribed = fields.Text(string=_("Drugs Presrcibed"))
	treatment_ids = fields.One2many("kb.medical.history.treatment", "history_id", string=_("Treatments"))
	lab_tested = fields.Text(string=_("Lab Tests"))
	accident_ids = fields.One2many('kb.medical.accident', 'history_id', string=_('Accidents'))

	@api.model_create_multi
	def create(self, vals_list):
		for values in vals_list:
			values['name'] = self.env['ir.sequence'].sudo().next_by_code('%s.sequence' % self._name)
		return super(MedicalHistory, self).create(vals_list)

	def create_procedure_histories(self):
		for history in self:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Create New Procedure History',
				'res_model': 'kb.medical.history.procedure',
				'view_mode': 'form',
				'target': 'new',
				'context': {
					'default_history_id': history.id,
				}
			}

	def create_treatment_histories(self):
		for history in self:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Create New Treatment History',
				'res_model': 'kb.medical.history.treatment',
				'view_mode': 'form',
				'target': 'new',
				'context': {
					'default_history_id': history.id,
				}
			}

	def create_accident_histories(self):
		for history in self:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Create New Accident',
				'res_model': 'kb.medical.accident',
				'view_mode': 'form',
				'target': 'new',
				'context': {
					'default_history_id': history.id,
				}
			}

class MedicalHistoryProcedure(models.Model):
	_name = "kb.medical.history.procedure"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = _("Procedure Histories")
	_order = "create_date desc"

	history_id = fields.Many2one("kb.medical.history", ondelete="cascade")
	name = fields.Char(string=_("Reference"), default=_("New"), readonly=True, copy=False)
	procedure = fields.Char(string=_("Procedure"), required=True)

	@api.model_create_multi
	def create(self, vals_list):
		for values in vals_list:
			values['name'] = self.env['ir.sequence'].sudo().next_by_code('%s.sequence' % self._name)
		return super(MedicalHistoryProcedure, self).create(vals_list)

class MedicalHistoryTreatment(models.Model):
	_name = "kb.medical.history.treatment"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = _("Treatment Histories")
	_order = "create_date desc"

	history_id = fields.Many2one("kb.medical.history", ondelete="cascade")
	name = fields.Char(string=_("Reference"), default=_("New"), readonly=True, copy=False)
	treatment = fields.Char(string=_("Treatment"), required=True)
	
	@api.model_create_multi
	def create(self, vals_list):
		for values in vals_list:
			values['name'] = self.env['ir.sequence'].sudo().next_by_code('%s.sequence' % self._name)
		return super(MedicalHistoryTreatment, self).create(vals_list)