
from odoo import fields, models, api

class Property(models.Model):
    _name = 'ud_estate.property.type'
    _description = 'Property Types'
    _order = 'sequence, name'

    name = fields.Char(string='Title',  required=True)
    sequence = fields.Integer(default=10)

    property_ids = fields.One2many('ud_estate.property', 'type_id', string='Properties')
    property_offer_ids = fields.One2many('ud_estate.property.offer', 'property_type_id', string='Property Types')
    # computed fields
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of type must be unique!',
    )

 # -------------------------------------------------------------------------
 # COMPUTE
 # -------------------------------------------------------------------------
    @api.depends('property_offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.property_offer_ids)