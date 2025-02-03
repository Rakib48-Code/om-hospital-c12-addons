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
    contact = fields.Char(string='Contact')
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
    active = fields.Boolean('Active', default=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    check_up_date = fields.Date(string='Checkup Date')
    pro = fields.Many2one('res.users', string='PRO')

    sl_no = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    ref = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))

    # name get function
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s %s' % (record.sl_no, record.patient_name)))
        return result



    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender


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
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('patient.ref') or _('New')
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
            'view_mode': 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    # count appointment
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count


    # send email with button action
    def action_send_email(self):
        print('Send Email')
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)


    # # cron job python code execution
    # @api.model
    # def patient_cron_job(self):
    #     ''' This method is called from a cron job. '''
    #     records = self.search([
    #         ('state', '=', 'posted'),
    #         ('auto_reverse', '=', True),
    #         ('reverse_date', '<=', fields.Date.today()),
    #         ('reverse_entry_id', '=', False)])
    #     for move in records:
    #         date = None
    #         company = move.company_id or self.env.user.company_id
    #         if move.reverse_date and (not company.period_lock_date or move.reverse_date > company.period_lock_date):
    #             date = move.reverse_date
    #         move.reverse_moves(date=date, auto=True)
