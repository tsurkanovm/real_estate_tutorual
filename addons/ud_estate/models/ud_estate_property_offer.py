from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class Property(models.Model):
    _name = 'ud_estate.property.offer'
    _description = 'Property Offers'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')], string='Status')
    property_id = fields.Many2one('ud_estate.property', string='Property', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Bayer', required=True)
    validity = fields.Integer(string='Validity', default=7)

    #computed fields
    property_type_id = fields.Many2one(related='property_id.type_id', store=True)
    date_deadline = fields.Datetime(string='Deadline',
                                    compute='_compute_date_deadline',
                                    inverse='_inverse_date_deadline')

    #constraints
    _check_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'Price must be positive.',
    )


    # -------------------------------------------------------------------------
    # COMPUTE AND INVERSE
    # -------------------------------------------------------------------------
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Datetime.now() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            deadline = offer.date_deadline
            if isinstance(deadline, int):
                deadline = datetime.fromtimestamp(deadline)

            now = fields.Datetime.now()
            offer.validity = (deadline - now).days

    # -------------------------------------------------------------------------
    # ONCHANGE
    # -------------------------------------------------------------------------
    @api.onchange('status')
    def _onchange_status(self):
        #todo - block to reject accepted offer
        if self.status == 'accepted':
            if self._property_already_has_accepted_offer(self):
                raise UserError('Another offer has already been accepted for this property.')


    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    def action_set_accept(self):
        for record in self:
            if self._property_already_has_accepted_offer(record):
                raise UserError('Another offer has already been accepted for this property.')

            record.write({'status': 'accepted'})
            record.property_id.write({'state': 'accepted', 'price': record.price, 'partner_id': record.partner_id.id})

        return True

    def action_set_reject(self):
        for record in self:
            record.write({'status': 'rejected'})

        return True

    def _property_already_has_accepted_offer(self, offer):
        return any(status == 'accepted' for status in offer.property_id.offer_ids.mapped('status'))

    # -------------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------------
    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id:
                property_record = self.env['ud_estate.property'].browse(property_id)
                max_offer_price = max(property_record.offer_ids.mapped('price'), default=0)
                if property_record.state == 'new':
                    property_record.write({'state': 'received'})
                if max_offer_price and vals['price'] <= max_offer_price:
                    raise ValidationError(_('Offer price must be higher than the current offer price.'))
        return super().create(vals_list)
