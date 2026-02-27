
from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property.offer'
    _description = 'Property Offers'

    #name = fields.Char(string='Name',  required=True)
    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')], string='Status')
    property_id = fields.Many2one('ud_estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Bayer', required=True)