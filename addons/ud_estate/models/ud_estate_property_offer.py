from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models

class Property(models.Model):
    _name = 'ud_estate.property.offer'
    _description = 'Property Offers'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')], string='Status')
    property_id = fields.Many2one('ud_estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Bayer', required=True)
    validity = fields.Integer(string='Validity', default=7)

    #computed fields
    date_deadline = fields.Datetime(string='Deadline',
                                    compute='_compute_date_deadline',
                                    inverse='_inverse_date_deadline')

    # -------------------------------------------------------------------------
    # COMPUTE AND INVERSE METHODS
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
