from odoo import api, fields, models

class User(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('ud_estate.property', 'user_id', string='Properties')