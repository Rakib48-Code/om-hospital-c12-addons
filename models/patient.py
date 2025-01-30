from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_name'
    _order = 'id desc'

    patient_name = fields.Char(string='Name', required=True, track_visibility='always')
    patient_age = fields.Integer(string='Age', track_visibility='always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Age Group', compute='set_age_group')
    image = fields.Binary(string='Image')
    email_id = fields.Char(string='Email', track_visibility='always')
    doctor_note = fields.Text(string='Doctor Prescription')
    pharmacy_note = fields.Text(string='Pharmacy')
    appointment_count = fields.Integer(string='Appointments', compute='get_appointment_count')

    sl_no = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.model
    def create(self, vals):
        if vals.get('sl_no', _('New')) == _('New'):
            vals['sl_no'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.constrains('patient_age')
    def _check_age(self):
        for rec in self:
            if rec.patient_age == 0:
                raise ValidationError(_('The age must be greater than zero!'))

    # smart button action type object
    @api.multi
    def open_patient_appointment(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_mode' : 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    # count appointment
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count