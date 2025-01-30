from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    # create override function
    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print('Yes')
        return res