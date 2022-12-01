# -*- coding: utf-8 -*-
# from odoo import http


# class OikosRestaurant(http.Controller):
#     @http.route('/oikos_restaurant/oikos_restaurant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oikos_restaurant/oikos_restaurant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('oikos_restaurant.listing', {
#             'root': '/oikos_restaurant/oikos_restaurant',
#             'objects': http.request.env['oikos_restaurant.oikos_restaurant'].search([]),
#         })

#     @http.route('/oikos_restaurant/oikos_restaurant/objects/<model("oikos_restaurant.oikos_restaurant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oikos_restaurant.object', {
#             'object': obj
#         })
