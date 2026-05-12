from odoo import fields, models


class PortfolioProject(models.Model):
    _name = 'portfolio.project'
    _description = 'Portfolio Project'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    description = fields.Text()
    body = fields.Html()
    active = fields.Boolean(default=True)
    website_published = fields.Boolean(default=False)
    url_key = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('url_key_unique', 'unique(url_key)', 'URL key must be unique'),
    ]
