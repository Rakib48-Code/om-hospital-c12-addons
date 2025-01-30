# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Odoo Development Tutorials',
    'version' : '12.0.0.1.1',
    'summary': 'odoo development tutorials',
    'sequence': 10,
    'author' : 'Rakib Hasan',
    'category': 'Tutorials',
    'depends' : ['mail','sale'],
    'data': [
        # security
        'security/ir.model.access.csv',

        # data
        'data/patient_sequence.xml',
        'data/appointment_sequence.xml',

        # views
        'views/menu.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/inherit_sales_module.xml',

        # reports
        'reports/report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
