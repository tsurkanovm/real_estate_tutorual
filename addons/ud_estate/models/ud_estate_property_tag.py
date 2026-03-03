
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.tag'
    _description = 'Property Tags'
    _order = 'name desc' # asc by default

    name = fields.Char(string='Name',  required=True)
    color = fields.Integer(string='Color')

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of tag must be unique!',
    )

