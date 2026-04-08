
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.tag'
    _description = 'Property Tags'
    _order = 'name desc' # asc by default

    name = fields.Char(string='Name',  required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name of tag must be unique!'),
    ]

