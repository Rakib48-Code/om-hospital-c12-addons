from odoo import api, models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment.wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string='Appointment Date')


# store wizard data
    def create_appointment(self):
        vals = {
            'patient_id' : self.patient_id.id,
            'appointment_date' : self.appointment_date
        }

        # self.env[modelname (jei model table a store hbe]
        self.env['hospital.appointment'].create(vals)
