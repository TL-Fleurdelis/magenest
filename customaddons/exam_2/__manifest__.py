{
    'name': "Product Management",
    'name_vi_VN': "Quản lý Sản phẩm",

    'summary': """

""",
    'summary_vi_VN': """

""",

    'description': """


""",

    'author': "TL-Fleurdelis",
    'website': "https://github.com/TL-Fleurdelis",

    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'exam_1', 'product', 'website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/s_product_template_views.xml',
        'views/s_product_views_inherit.xml',
        'views/s_product_attribute_views_inherit.xml',
        'views/s_menu_views.xml',
        'wizard/product_template_add_warranty_wizard_views.xml',
        'views/s_product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'exam_2/static/src/css/custom_style.css',
        ]},
}
