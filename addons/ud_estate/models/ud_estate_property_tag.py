
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.tag'
    _description = 'Property Tags'

    name = fields.Char(string='Name',  required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of tag must be unique!',
    )

