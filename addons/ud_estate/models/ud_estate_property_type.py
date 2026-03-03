
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.type'
    _description = 'Property Types'
    _order = 'sequence, name'

    name = fields.Char(string='Title',  required=True)
    sequence = fields.Integer(default=10)

    property_ids = fields.One2many('ud_estate.property', 'type_id', string='Properties')

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of type must be unique!',
    )
