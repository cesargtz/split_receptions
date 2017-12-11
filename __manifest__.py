# -*- coding: utf-8 -*-
{
    'name': "split_receptions",


    'description': """
        Split truck receptions.
    """,

    'author': "yécora",
    'website': "yecora.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'vehicle', 'stock', 'truck_reception', 'vehicle_reception','pinup_price_purchase'],

    # always loaded
    'data': [
        'security/split_reception_access.xml',
        'security/ir.model.access.csv',
        'views/split_reception.xml',
    ],

}
