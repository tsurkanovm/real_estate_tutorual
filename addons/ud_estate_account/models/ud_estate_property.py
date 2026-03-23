from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _inherit = 'ud_estate.property'

    def action_set_sold(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError(_("You must set a customer before selling the property."))

        invoice_vals = self._prepare_sale_invoice_vals()
        self.env['ud_estate.property'].check_access_rule('write')
        self.env['account.move'].sudo().create(invoice_vals)

        return super().action_set_sold()

    def _prepare_sale_invoice_vals(self):
        self.ensure_one()

        return {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create(self._prepare_property_invoice_line()),
                Command.create(self._prepare_admin_fee_invoice_line())
            ]
        }

    def _prepare_property_invoice_line(self):
        self.ensure_one()

        return {
            'name': self.description or self.name,
            'quantity': 1,
            'price_unit': self.price,
        }

    def _prepare_admin_fee_invoice_line(self):
        self.ensure_one()

        return {
            'name': _('Administrative fees'),
            'quantity': 1,
            'price_unit': 100,
        }