# -*- coding: utf-8 -*-
{
    'name': "DGII Partner",

    'summary': """
       DGII partner information as is in the official file of the dgii
       """,

    'description': """
       DGII partner information as is in the official file of the dgii
       
    """,

    'author': "OikosChain, SRL",
    'website': "http://www.oikoschain.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/partner_dgii.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
