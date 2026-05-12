{
    'name': 'Portfolio',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Personal portfolio page at /portfolio',
    'author': 'Tsurkanov Mykhailo',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/portfolio_project_views.xml',
        'views/portfolio_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'portfolio/static/src/css/portfolio.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
