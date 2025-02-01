from odoo import api, models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment.wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string='Appointment Date')