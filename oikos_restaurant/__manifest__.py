# -*- coding: utf-8 -*-
{
    'name': "Oikos Restaurant",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "OikosChain, SRL",
    'website': "http://www.oikoschain.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'pos_restaurant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/variants.xml'
    ],
   
}
