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
        'security/exam_1_security.xml',
        'security/ir.model.access.csv',
        'views/s_sale_order_views.xml',
        'views/s_res_partner_views.xml',
        'views/s_menu_views.xml',
        'wizard/res_partner_add_discount_wizard_views.xml',
        'views/s_cart_show_vip_code_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'exam_1/static/src/css/custom_style.css',
        ]},
}
