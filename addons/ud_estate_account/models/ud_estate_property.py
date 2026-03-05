from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _inherit = 'ud_estate.property'

    def action_set_sold(self):
        #@todo - needs to refactor
        main_line = Command.create({
                    "name": self.description,
                    "quantity": 1,
                    "price_unit": self.price,
                })
        tax_price = Command.create({
                    "name": 'Administrative fees',
                    "quantity": 1,
                    "price_unit": 100,
                })

        values = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'name': _('Invoice for property: ') + self.name,
            'invoice_line_ids': [main_line, tax_price]
        }
        self.env['account.move'].create(values)
        return super().action_set_sold()
