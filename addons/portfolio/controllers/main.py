from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class PortfolioController(http.Controller):

    # @http.route('/portfolio', auth='public', website=True, type='http')
    # def portfolio(self, **kwargs):
    #     return request.render('portfolio.portfolio_page', {})

    @http.route('/portfolio/<string:url_key>', auth='public', website=True, type='http')
    def project_page(self, url_key, **kwargs):
        project = request.env['portfolio.project'].sudo().search([
            ('url_key', '=', url_key),
            ('website_published', '=', True),
        ], limit=1)
        if not project:
            raise NotFound()
        return request.render('portfolio.project_page', {'project': project})
