{
    'name': 'Real Estate Ads',
    'version': '18.0.1.0.0',
    'category': 'Real Estate/Brokerage',
    'description': """
        The Real Estate Ads module.
        ========================================
    """,
    'application': True,
    'depends': ['base'],
    'data': [
        'security/ud_security.xml',
        'security/ir.model.access.csv',
        'data/ud_estate_property_type_data.xml',
        'data/ud_estate_property_tag_data.xml',
        'data/ud_estate_dashboard_data.xml',

        'views/ud_estate_property_views.xml',
        'views/ud_estate_property_menus.xml',
    ],
    "demo": [
        "demo/ud_estate_property_demo.xml",
    ],
    'author': 'Mykhailo Tsurkanov',
    'license': 'LGPL-3',
}
