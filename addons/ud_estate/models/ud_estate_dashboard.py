from odoo import api, fields, models

class EstateDashboard(models.Model):
    _name = 'ud_estate.dashboard'
    _description = 'Real Estate Dashboard'

    name = fields.Char(default='Dashboard')

    total_properties = fields.Integer(compute='_compute_metrics')
    new_properties = fields.Integer(compute='_compute_metrics')
    received_properties = fields.Integer(compute='_compute_metrics')
    accepted_properties = fields.Integer(compute='_compute_metrics')
    sold_properties = fields.Integer(compute='_compute_metrics')
    cancelled_properties = fields.Integer(compute='_compute_metrics')

    total_offers = fields.Integer(compute='_compute_metrics')
    accepted_offers = fields.Integer(compute='_compute_metrics')
    rejected_offers = fields.Integer(compute='_compute_metrics')

    avg_expected_price = fields.Float(compute='_compute_metrics')
    avg_selling_price = fields.Float(compute='_compute_metrics')

    @api.depends()
    def _compute_metrics(self):
        Property = self.env['ud_estate.property']
        Offer = self.env['ud_estate.property.offer']

        for rec in self:
            prop_groups = Property.read_group([], ['state'], ['state'])
            prop_map = {item['state']: item['state_count'] for item in prop_groups if item['state']}

            rec.new_properties = prop_map.get('new', 0)
            rec.received_properties = prop_map.get('received', 0)
            rec.accepted_properties = prop_map.get('accepted', 0)
            rec.sold_properties = prop_map.get('sold', 0)
            rec.cancelled_properties = prop_map.get('cancelled', 0)
            rec.total_properties = sum(prop_map.values())

            offer_groups = Offer.read_group([], ['status'], ['status'])
            offer_map = {item['status']: item['status_count'] for item in offer_groups if item['status']}

            rec.accepted_offers = offer_map.get('accepted', 0)
            rec.rejected_offers = offer_map.get('rejected', 0)
            rec.total_offers = sum(offer_map.values())

            props = Property.search([])
            sold_props = Property.search([('state', '=', 'sold')])

            rec.avg_expected_price = sum(props.mapped('expected_price')) / len(props) if props else 0.0
            rec.avg_selling_price = sum(sold_props.mapped('price')) / len(sold_props) if sold_props else 0.0

    def action_open_sold_properties(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sold Properties',
            'res_model': 'ud_estate.property',
            'view_mode': 'list,form',
            'domain': [('state', '=', 'sold')],
            'target': 'current',
        }

    def action_open_rejected_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rejected Offers',
            'res_model': 'ud_estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('status', '=', 'rejected')],
            'target': 'current',
        }