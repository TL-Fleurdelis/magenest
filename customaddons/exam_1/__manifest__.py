{
    'name': "Advanced Sale Management",
    'summary': """
    Advance Sales
""",
    'summary_vi_VN': """
Bán hàng nâng cao  
""",

    'description': """

    This is exam1
""",
    'author': "TL-Fleurdelis",
    'website': "https://github.com/TL-Fleurdelis",
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'l10n_de', 'website_sale', 'event_booth_sale'],
    # always loaded
    'data': [
        'security/new_customer_security.xml',
        'security/ir.model.access.csv',
        'views/new_sale_order_views.xml',
        'views/new_customer_views.xml',
        'views/new_menu_views.xml',
        'wizard/customer_wizard_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'exam_1/static/src/css/custom_style.css',
        ]},
}
