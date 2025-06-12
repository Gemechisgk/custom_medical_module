from odoo.http import Controller, request, route
from datetime import datetime, date
import json

class MedicalRecordPostmanAPI(Controller):
	def _convert_date_to_string(self, dt):
		if isinstance(dt, datetime):
			return dt.strftime("%Y-%m-%d %H:%M:%S")
		elif isinstance(dt, date):
			return dt.strftime("%Y-%m-%d")

	def _recursive_convert_to_string(self, dictionary):
		for key, values in dictionary.items():
			if isinstance(values, dict):
				self._recursive_convert_to_string(values)
			if isinstance(values, (datetime, date)):
				dictionary[key] = self._convert_date_to_string(values)
			if isinstance(values, list):
				for item in values:
					if isinstance(item, dict):
						self._recursive_convert_to_string(item)

	def _generate_medical_record_json(self, record_id):
		# Definitions for keys and o2m relations
		medical_record_keys = ['id', 'company_id', 'name', 'address', 'mobile', 'date_of_birth', 'id_number', 'gender', 'occupation', 'history_ids', 'history_count', 'allergy_ids', 'medical_history']
		medical_history_keys = ['id', 'user_id', 'name', 'date', 'test_result', 'complaints', 'diagnosis', 'medical_advice', 'procedure_ids', 'drug_prescribed', 'accident_ids', 'treatment_ids', 'lab_tested']
		procedure_keys =  ['id', 'name', 'procedure']
		vaccination_keys =  ['id', 'name', 'vaccine']
		treatment_keys =  ['id', 'name', 'treatment']
		accident_keys =  ['id', 'accident_number', 'date_of_visit', 'place_of_treatment', 'type_of_disease', 'severity']

		medical_record_o2m = ["history_ids"]
		medical_history_o2m = ["procedure_ids", "accident_ids", "treatment_ids"]

		# Generate recursively
		data = record_id.read(medical_record_keys)[0]
		data['history_ids'] = request.env['kb.medical.history'].sudo().browse(data['history_ids']).read(medical_history_keys)
		for history in data['history_ids']:
			history['procedure_ids'] = request.env['kb.medical.history.procedure'].sudo().browse(history['procedure_ids']).read(procedure_keys)
			history['accident_ids'] = request.env['kb.medical.history.accident'].sudo().browse(history['accident_ids']).read(accident_keys)
			history['treatment_ids'] = request.env['kb.medical.history.treatment'].sudo().browse(history['treatment_ids']).read(treatment_keys)
		return data

	@route(route='/medical-record/<int:record_id>', type='http', auth='public')
	def fetch_medical_record_pdf(self, record_id, **kw):
		if not isinstance(record_id, int):
			record_id = int(record_id)
		record = request.env['kb.medical.record'].sudo().browse(record_id)
		if not record:
			return json.dumps({
				'result': '404',
				'message': 'Medical record not found. There is no medical record with ID %s' % record_id,
			})

		if kw.get('return', False) == 'pdf':
			pdf, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf('custom_medical_module.medical_record_report', res_ids=[record_id])
			pdf_http_headers = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
			return request.make_response(pdf, headers=pdf_http_headers)
		else: # Return JSON
			data = self._generate_medical_record_json(record)

			# Convert dates to strings with recursive iteration
			self._recursive_convert_to_string(data)
			return json.dumps(data)