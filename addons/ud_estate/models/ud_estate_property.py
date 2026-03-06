from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class Property(models.Model):
    _name = 'ud_estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc' # order in a list will override _order

    name = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active', default=True) # todo - delete?

    state = fields.Selection(
        [('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string='Property State',
        default='new'
    )

    postcode = fields.Char(string='Postcode')
    price = fields.Float(string='Selling Price', copy=False, readonly=True)
    expected_price = fields.Float(string='Expected Price', required=True)
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

    #constraints
    _check_price_positive = models.Constraint(
        'CHECK(price >= 0)',
        'Price must be positive.',
    )
    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'Price must be positive.',
    )
    _check_garden_area_positive = models.Constraint(
        'CHECK(garden_area >= 0)',
        'Garden area must be positive.',
    )
    _check_living_area_positive = models.Constraint(
        'CHECK(living_area > 0)',
        'Living area must be positive.',
    )
    _check_facades_positive = models.Constraint(
        'CHECK(facades > 0)',
        'Facades must be positive.',
    )
    _check_bedrooms_positive = models.Constraint(
        'CHECK(bedrooms > 0)',
        'Bedrooms must be positive.',
    )

    @api.constrains('expected_price', 'price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.price, precision_digits=2) and float_compare(record.expected_price * 0.9, record.price, precision_digits=2) > 0:
                raise ValidationError(_("Selling price must be higher than 90% of expected price."))

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


    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # works only on form context - do not trigger if created model programmatically
    # compute works in both cases
    # -------------------------------------------------------------------------
    @api.onchange('garden')
    def _onchange_garden(self):
        if self._origin.id: # if it not new record
            return {'warning': {
                'title': _("Warning"),
                'message': ('You are change existing property. Default values will not be set.'),}}

        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_area = 0
            self.garden_orientation = False


 # -------------------------------------------------------------------------
    # ACTION METHODS
# -------------------------------------------------------------------------
    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled' or record.state == 'new':
                raise UserError(_('You cannot sell a cancelled or new property.'))
            else:
                #record.state = 'sold' - just populate field, required to save in form
                # and if actions are can be used as API - needs to save here
                record.write({'state': 'sold'})
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('You cannot cancel a sold property.'))
            else:
                record.write({'state': 'cancelled'})

        return True

 # -------------------------------------------------------------------------
    # CRUD METHODS
# -------------------------------------------------------------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancel(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(_('You can delete only new or cancelled property.'))
        return True