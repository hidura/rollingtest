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
                                    'price':product.list_price
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
                for variant in product_info[0]['lines']:
                    line=http.request.env['product.variant.line'].sudo().search([('id','=',variant)])
                    product_variant = line.read(list(set(http.request.env['product.variant.line']._fields)))
                    product_variant[0]['product_product']=[product_info[0]['product_id'][0],product_info[0]['product_id'][1]]
                    variants.append(product_variant)
                    
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
    
    
    @http.route('/bmsclient/createPOSORDERLine', type='json', auth='none',csrf=False)
    def createPOSORDERLine(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            for line in kw['products']:
                product_product = http.request.env['product.product'].sudo().search([('id', '=',line['product_id'])])
                for tax_id in product_product.taxes_id:
                    tax = http.request.env['account.tax'].sudo().search([('id', '=',tax_id['id'])])
                    product_tax = line['price_subtotal']*(tax.amount/100)
                    line['price_subtotal_incl']=product_tax+line['price_subtotal']
                    del line['save_server']
                    line['order_id']=line['order_id'][0]
            pos_order_line = http.request.env['pos.order.line'].sudo().create(kw['products'])
            posorderlines=[]
            for line in pos_order_line:
                posorderline=self.cleanerFields(line.read(list(set(http.request.env['pos.order.line']._fields))))
                
                http.request.env['pos.order.line.log'].sudo().create({
                        'name':posorderline[0]['name'],
                        'full_product_name':posorderline[0]['full_product_name'],
                        'display_name':posorderline[0]['display_name'],
                        'product_id':posorderline[0]['product_id'][0],
                        'currency_id':posorderline[0]['currency_id'][0],
                        'qty':posorderline[0]['qty'],
                        'order_id':posorderline[0]['order_id'][0],
                        'customer_note':posorderline[0]['customer_note'],
                        'note':posorderline[0]['customer_note'],
                        'price_unit':posorderline[0]['price_unit'],
                        'order_line_id':posorderline[0]['id'],
                        'price_subtotal':posorderline[0]['price_subtotal'],
                        'price_subtotal_incl':posorderline[0]['price_subtotal_incl']
                        })
                posorderlines.append(posorderline)
                
                
        return posorderlines
    
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
    
    
    
    
    @http.route('/bmsclient/getPOSOrderLines', type='json', auth='user',csrf=False)
    def getPOSOrderLines(self, **kw):
        """This function check the products and return it"""
        if self.checkKey():
            poslines=[]
            if 'orderlines' in kw:
                for id_line in kw['orderlines']:
                    pos_config = http.request.env['pos.order.line'].sudo().search([('id','=',id_line)])

                    for posconfig in pos_config:
                        posorderline=self.cleanerFields(posconfig.read(list(set(http.request.env['pos.order.line']._fields))))
                        
                        poslines.append(posorderline)
            elif 'orderlines' not in kw and 'order_id' in kw:
                for line in http.request.env['pos.order.line'].sudo().search([('order_id','=',kw['order_id'])]):
                    
                    for orderline in line:
                        posorderline=self.cleanerFields(orderline.read(list(set(http.request.env['pos.order.line']._fields))))
                        
                        poslines.append(posorderline)
            
        return poslines
    
    @http.route('/bmsclient/getTablesByFloor', type='json', auth='user',csrf=False)
    def getTablesByFloor(self, **kw):
        pos_table = http.request.env['restaurant.table'].sudo().search([('floor_id','=',int(kw['zone_id']))])
        
        postable=[]
        for table in pos_table:
            table_det=self.cleanerFields(table.read(list(set(http.request.env['restaurant.table']._fields))))
            order = http.request.env['pos.order'].sudo().search([('table_id','=',table.id)])
            if order:
                for order_av in order:
                    table_det[0]['order_id']=order_av.id
            else:
                table_det[0]['order_id']=False
            
            postable.append(table_det)
            
        return postable