# -*- coding: utf-8 -*-
# from odoo import http


# class IndustryFsmSaleExtends(http.Controller):
#     @http.route('/industry_fsm_sale_extends/industry_fsm_sale_extends', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/industry_fsm_sale_extends/industry_fsm_sale_extends/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('industry_fsm_sale_extends.listing', {
#             'root': '/industry_fsm_sale_extends/industry_fsm_sale_extends',
#             'objects': http.request.env['industry_fsm_sale_extends.industry_fsm_sale_extends'].search([]),
#         })

#     @http.route('/industry_fsm_sale_extends/industry_fsm_sale_extends/objects/<model("industry_fsm_sale_extends.industry_fsm_sale_extends"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('industry_fsm_sale_extends.object', {
#             'object': obj
#         })
