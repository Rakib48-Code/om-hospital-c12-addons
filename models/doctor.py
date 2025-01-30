from odoo import api, fields, models

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor Record'

    name = fields.Char(string='Name')
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Gender")
    user_id = fields.Many2one('res.users', string='Related User')
    age = fields.Integer(string='Age')