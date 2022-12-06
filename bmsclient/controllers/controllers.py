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
        
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if self.checkKey():
            products = http.request.env['product.product'].sudo().search([('available_in_pos','=',True)])
            productinfo=[]
            for product in products:
                productinfo.append({'name':product.name,
                                    'id':product.id,
                                    'category':[product.categ_id.id, product.categ_id.name,
                                                product.categ_id.printer_name],
                                    'description':product.description,
                                    'image':base_url + '/web/image?' + 'model=product.product&id=' + str(product.id) + '&field=image',
                                    'is_product_variant':product.is_product_variant,
                                    'price':product.price
                                    })
            
        return json.dumps(productinfo)

    
    @http.route('/bmsclient/getVariants', type='json', auth='user',csrf=False)
    def getVariants(self, **kw):
        """This function check the variant and return it"""
        if self.checkKey():
            products = http.request.env['product.variant'].sudo().search([])
            productinfo=[]
            for product in products:
                product_info=product.read(list(set(http.request.env['product.variant']._fields)))
                variants=[]
                print(product_info)
                for variant in product_info[0]['lines']:
                    line=http.request.env['product.variant.line'].sudo().search([('id','=',variant)])
                    variants.append(line.read(list(set(http.request.env['product.variant.line']._fields))))
                    
                product_info[0]['variants']=variants
                productinfo.append(self.cleanerFields(product_info))
               
        return productinfo
    
    @http.route('/bmsclient/getPOSConfig', type='json', auth='user',csrf=False)
    def getPOSConfig(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            pos_config = http.request.env['pos.config'].sudo().search([])
            posconfigs=[]
            for posconfig in pos_config:
                posconfigs.append(self.cleanerFields(posconfig.read(list(set(http.request.env['pos.config']._fields)))))
               
        return posconfigs
    
    
    
    @http.route('/bmsclient/getFloor', type='json', auth='user', csrf=False)
    def getFloor(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            pos_floor = http.request.env['restaurant.floor'].sudo().search([("pos_config_id","=",kw['pos'])])
            posfloor=[]
            for floor in pos_floor:
                posfloor.append(self.cleanerFields(floor.read(list(set(http.request.env['restaurant.floor']._fields)))))
               
        return posfloor

    @http.route('/bmsclient/getPOSSession', type='json', auth='user',csrf=False)
    def getPOSSession(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            sessions=[]
            for session in kw['sessions']:
                pos_session = http.request.env['pos.session'].sudo().search([('id','=',session)])
                for session_open in pos_session:
                    session_det=self.cleanerFields(session_open.read(list(set(http.request.env['pos.session']._fields))))
                    sessions.append(session_det)
                    
        return sessions
    
    
    @http.route('/bmsclient/createPOSORDER', type='json', auth='user',csrf=False)
    def createPOSORDER(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            session_id=kw['id_session']
            del kw['id_session']
            kw['session_id']=session_id
            pos_order = http.request.env['pos.order'].sudo().create(kw)
            posorder=[]
            for order in pos_order:
                posorder=self.cleanerFields(order.read(list(set(http.request.env['pos.order']._fields))))
                
        return posorder
    
    
    @http.route('/bmsclient/getPOSOrder', type='json', auth='user',csrf=False)
    def getPOSOrder(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            if "order_id" in kw:
                pos_config = http.request.env['pos.order'].sudo().search([('id','=',int(kw['order_id'])),
                                                                              ('state','=','draft')])
                posconfigs=[]
                for posconfig in pos_config:
                    posconfigs.append(self.cleanerFields(posconfig.read(list(set(http.request.env['pos.order']._fields)))))
            
            elif "session_ids" in kw:
                posconfigs=[]
                for sessionid in kw['session_ids']:
                    pos_config = http.request.env['pos.order'].sudo().search([('session_id','=',int(sessionid)),
                                                                              ('state','=','draft')])
                    print(pos_config)
                    for posconfig in pos_config:
                        posconfigs.append(self.cleanerFields(posconfig.read(list(set(http.request.env['pos.order']._fields)))))
            else:
                
                pos_config = http.request.env['pos.order'].sudo().search([('session_id','=',int(kw['pos_session'])),
                                                                              ('state','=','draft')])
                posconfigs=[]
                for posconfig in pos_config:
                    posconfigs.append(self.cleanerFields(posconfig.read(list(set(http.request.env['pos.order']._fields)))))
        return posconfigs
    
    @http.route('/bmsclient/getTablesByFloor', type='json', auth='user',csrf=False)
    def getTablesByFloor(self, **kw):
        pos_table = http.request.env['restaurant.table'].sudo().search([('floor_id','=',int(kw['zone_id']))])
        
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