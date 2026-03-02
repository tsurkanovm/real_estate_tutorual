
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.type'
    _description = 'Property Types'

    name = fields.Char(string='Title',  required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of type must be unique!',
    )
