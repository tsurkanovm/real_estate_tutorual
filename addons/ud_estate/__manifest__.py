{
    'name': 'Real Estate Ads',
    'version': '1.0',
    'category': 'Sales',
    'description': """
        The Real Estate Ads module described in Odoo oficial documentation.
        ========================================
    """,
    'application': True,
    'depends': ['base'],
    'data': [
        'data/ir.model.access.csv',

        'views/ud_estate_property_views.xml',
        'views/ud_estate_property_menus.xml',
    ],
    'author': 'Mykhailo Tsurkanov',
    'license': 'LGPL-3',
}
