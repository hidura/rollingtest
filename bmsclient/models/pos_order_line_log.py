import json
from odoo import api, fields, models
import requests

class PosOrderLineLog(models.Model):
    _name ="pos.order.line.log"
    
    status_order=[('Added','added'),
                    ('In process','in-process'),
                    ('Served','Served'),
                    ('Deleted','deleted')]
    
    
    name = fields.Char(string='Line No', required=True, copy=False)
    notice = fields.Char(string='Discount Notice')
    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string='Unit Price', digits=0)
    qty = fields.Float('Quantity', digits='Product Unit of Measure', default=1)
    price_subtotal = fields.Float(string='Subtotal w/o Tax', digits=0,
        readonly=True, required=True)
    price_subtotal_incl = fields.Float(string='Subtotal', digits=0,
        readonly=True, required=True)
    discount = fields.Float(string='Discount (%)', digits=0, default=0.0)
    order_id = fields.Integer('pos.order', required=True, index=True)
    order_line_id = fields.Integer("Order Line ID")
    currency_id = fields.Integer("Currency")
    full_product_name = fields.Char('Full Product Name')
    note = fields.Char('Note', help='This is a note destined to the customer')
    customer_note = fields.Char('Customer Note', help='This is a note destined to the customer')
    order_notes = fields.Char("Order Notes")
    status = fields.Selection(status_order)