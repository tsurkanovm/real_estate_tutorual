from odoo import http
from odoo.http import request


class PortfolioController(http.Controller):

    @http.route('/portfolio', auth='public', website=True, type='http')
    def portfolio(self, **kwargs):
        return request.render('portfolio.portfolio_page', {})
