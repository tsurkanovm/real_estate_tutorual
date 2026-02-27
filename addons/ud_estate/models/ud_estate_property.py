from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class Property(models.Model):
    _name = 'ud_estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active')
    state = fields.Selection(
        [('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string='Property State',
        default='new'
    )

    postcode = fields.Char(string='Postcode')
    price = fields.Float(string='Expected Price', required=True)
    available_from = fields.Date(string='Available From',
                                 default=fields.Date.today() + relativedelta(months=3), copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades', default=2)
    living_area = fields.Integer(string='Living Area')
    garden_area = fields.Integer(string='Garden Area')
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


    # computed fields
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    description = fields.Text(string='Property Description', compute='_compute_description', store=True)
    best_offer = fields.Float(string='Best Offer', copy=False, compute='_compute_best_offer')

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('type_id.name', 'partner_id.name', 'total_area')
    def _compute_description(self):
        for property in self:
            property.description \
                = f"{property.type_id.name} for {property.partner_id.name} with total area {property.total_area} sqm"


    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_offer = max(property.offer_ids.mapped('price'))
            else:
                property.best_offer = 0.0