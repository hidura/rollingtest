# -*- coding: utf-8 -*-
from dataclasses import fields
from odoo import http
import json
import datetime
from datetime import date
class BMSClient(http.Controller):
    def checkKey(header):
        return True
    
    def cleanerFields(self,fields_dict_list):
        #This method clean all the fields that can produce an error
        
        for fields_dict in fields_dict_list:
            for piece in fields_dict:
               
                if type(fields_dict[piece]) is datetime.datetime:
                    _date = fields_dict[piece]
                    fields_dict[piece]=f"{_date.year}-{_date.month}-{_date.day}"
                if type(fields_dict[piece]) is date:
                    _date = fields_dict[piece]
                    fields_dict[piece]=f"{_date.year}-{_date.month}-{_date.day}"
        return fields_dict_list
                    
                    
    @http.route('/bmsclient/getProducts', type='json', auth='user',csrf=False)
    def getProducts(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            products = http.request.env['product.product'].sudo().search([('available_in_pos','=',True)])
            productinfo=[]
            for product in products:
                productinfo.append({'name':product.name,
                                    'id':product.id,
                                    'category':[product.categ_id.id, product.categ_id.name,
                                                product.categ_id.printer_name],
                                    'description':product.description,
                                    'image':product.image_128,
                                    'is_product_variant':product.is_product_variant,
                                    'price':product.price
                                    })
            
        return json.dumps(productinfo)

    
    @http.route('/bmsclient/getVariants', type='json', auth='public',csrf=False)
    def getVariants(self, **kw):
        """This function check the variant and return it"""
        if self.checkKey():
            products = http.request.env['pos.product.attribute.line'].sudo().search([])
            productinfo=[]
            for product in products:
                productinfo.append(self.cleanerFields(product.read(list(set(http.request.env['pos.product.attribute.line']._fields)))))
               
        return json.dumps(productinfo)
    
    @http.route('/bmsclient/getPOSConfig', type='json', auth='user',csrf=False)
    def getPOSConfig(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            pos_config = http.request.env['pos.config'].sudo().search([])
            posconfigs=[]
            for posconfig in pos_config:
                posconfigs.append(self.cleanerFields(posconfig.read(list(set(http.request.env['pos.config']._fields)))))
               
        return posconfigs
    
    
    @http.route('/bmsclient/getFloor', type='json', auth='public',csrf=False)
    def getFloor(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            pos_floor = http.request.env['restaurant.floor'].sudo().search([("pos_config_id","=",kw['pos'])])
            posfloor=[]
            for floor in pos_floor:
                posfloor.append(self.cleanerFields(floor.read(list(set(http.request.env['restaurant.floor']._fields)))))
               
        return posfloor

    @http.route('/bmsclient/getFloorTables', type='json', auth='public',csrf=False)
    def getFloorTables(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            
            pos_table = http.request.env['restaurant.table'].sudo().search([('floor_id','=',kw['zone_id'])])
            postable=[]
            for table in pos_table:
                table_det=self.cleanerFields(table.read(list(set(http.request.env['restaurant.table']._fields))))
                order = http.request.env['pos.order'].sudo().search([('table_id','=',table.id)])
                if order:
                    table_det[0]['order_id']=order.id
                else:
                    table_det[0]['order_id']=False
                
                postable.append(table_det)
               
        return postable
    
    
    @http.route('/bmsclient/createPOSORDER', type='json', auth='public',csrf=False)
    def getFloorTables(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            
            pos_table = http.request.env['restaurant.table'].sudo().search([('floor_id','=',kw['zone_id'])])
            postable=[]
            for table in pos_table:
                table_det=self.cleanerFields(table.read(list(set(http.request.env['restaurant.table']._fields))))
                order = http.request.env['pos.order'].sudo().search([('table_id','=',table.id)])
                if order:
                    table_det[0]['order_id']=order.id
                else:
                    table_det[0]['order_id']=False
                
                postable.append(table_det)
               
        return postable
    
    