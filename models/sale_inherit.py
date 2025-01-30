from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_patient = fields.Char(string='Patient Name')