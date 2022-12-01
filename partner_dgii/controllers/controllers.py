# -*- coding: utf-8 -*-
from odoo import http


# class PatnerDgii(http.Controller):
#     @http.route('/patner_dgii/patner_dgii', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

# @http.route('/patner_dgii/patner_dgii/objects', auth='public')
# def list(self, **kw):
#     return http.request.render('patner_dgii.listing', {
#         'root': '/patner_dgii/patner_dgii',
#         'objects': http.request.env['patner_dgii.patner_dgii'].search([]),
#     })

#     @http.route('/patner_dgii/patner_dgii/objects/<model("patner_dgii.patner_dgii"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('patner_dgii.object', {
#             'object': obj
#         })
