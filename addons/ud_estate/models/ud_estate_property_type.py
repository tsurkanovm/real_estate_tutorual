
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.type'
    _description = 'Property Types'

    name = fields.Char(string='Title',  required=True)
