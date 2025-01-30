from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'patient_id'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('approve', 'Approved'),
        ('canceled', 'Canceled')
    ], 'Status', default='draft',)

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer(string='Age', related='patient_id.patient_age')
    notes = fields.Text(string='Registration Notes', )
    appointment_date = fields.Date(string='Appointment Date')


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'


    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'