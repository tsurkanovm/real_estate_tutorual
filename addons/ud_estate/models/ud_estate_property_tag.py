
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.tag'
    _description = 'Property Tags'

    name = fields.Char(string='Name',  required=True)
