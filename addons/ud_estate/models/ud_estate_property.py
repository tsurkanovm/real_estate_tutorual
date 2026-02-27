from dateutil.relativedelta import relativedelta

from odoo import fields, models

class Property(models.Model):
    _name = 'ud_estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Title', nullable=False, required=True)
    active = fields.Boolean(string='Active')
    state = fields.Selection(
        [('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string='Property State',
        default='new'
    )
    description = fields.Text(string='Property Description')
    postcode = fields.Char(string='Postcode')
    price = fields.Float(string='Expected Price', nullable=False, required=True)
    best_offer = fields.Float(string='Best Offer')
    available_from = fields.Date(string='Available From',
                                 default=fields.Date.today() + relativedelta(months=3), copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades', default=2)
    living_area = fields.Integer(string='Living Area')
    garden_area = fields.Integer(string='Garden Area')
    total_area = fields.Integer(string='Total Area')
    garden = fields.Boolean(string='Garden')
    garage = fields.Boolean(string='Garage')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation'
    )

    # relational fields
    type_id = fields.Many2one('ud_estate.property.type', string='Property Type')
    partner_id = fields.Many2one('res.partner', string='Bayer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('ud_estate.property.tag', string='Tags')
    offer_ids = fields.One2many('ud_estate.property.offer', 'property_id', string='Offers')