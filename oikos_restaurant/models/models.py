# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from random import random


class PosProductAttribute(models.Model):
    _name = "pos.product.attribute"
    _description = "Product Attribute"
    _order = 'sequence, name'

    variant_type=[('Companion','companion'),
                  ('Optional','optional'),
                  ('Suggested','suggested'),
                  ('Term','term')]
    
    name = fields.Char('Name', required=True, translate=True)
    price = fields.Float("Price", delfault=0.00)
    amount_to_choose = fields.Integer("Amount to choose")
    type = fields.Selection(variant_type,string="Tipo")
    value_ids = fields.One2many('pos.product.attribute.value', 'attribute_id', 'Values', copy=True)
    value_product_ids = fields.One2many('product.product', 'attribute_id', 'Values', copy=True)
    is_limited = fields.Boolean(string='Limited')
    is_required = fields.Boolean(string='Required')
    
    sequence = fields.Integer('Sequence', help="Determine the display order")


class PoProductAttributevalue(models.Model):
    _name = "pos.product.attribute.value"
    _order = 'sequence'

    name = fields.Char('Value', translate=True, related="product_id.name")
    sequence = fields.Integer('Sequence', help="Determine the display order")
    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade', required=True, domain=[("is_variant", "=", True)])
    price = fields.Float("Price", related="product_id.lst_price")
    attribute_id = fields.Many2one('pos.product.attribute', 'Attribute', ondelete='cascade')
    is_limited = fields.Boolean(string='Limited', related="attribute_id.is_limited")
    is_required = fields.Boolean(string='Required', related="attribute_id.is_required")

    _sql_constraints = [
        ('value_company_uniq', 'unique (name,attribute_id)', 'This attribute value already exists !')
    ]

    # @api.multi
    def name_get(self):
        if not self._context.get('show_attribute', True):  # TDE FIXME: not used
            return super(PoProductAttributevalue, self).name_get()
        return [(value.id, "%s: %s" % (value.attribute_id.name, value.name)) for value in self]


class pos_config(models.Model):
    _inherit = 'pos.config' 

    allow_product_varients = fields.Boolean('Allow Product Variants', default=True)


class PosProductAttributeLine(models.Model):
    _name = "pos.product.attribute.line"
    _rec_name = 'attribute_id'

    product_ids = fields.Many2one('product.product', 'Product', ondelete='cascade', required=True)
    value_ids = fields.Many2one('pos.product.attribute.value', string='Attribute Values')
    attribute_id = fields.Many2one('pos.product.attribute', 'Attribute', ondelete='restrict')
    is_limited = fields.Boolean(string='Limited', related="value_ids.is_limited")
    is_required = fields.Boolean(string='Required', related="value_ids.is_required")
    default_selected = fields.Boolean('Default selected')
    price = fields.Float("Price",related="value_ids.price")
    #order_line_id = fields.Many2one('pos.order', string='Orderline Ref', ondelete='cascade', required=True)


class product_product(models.Model):
    _inherit = 'product.product'
    
    has_variant = fields.Boolean('Tiene variante')
    is_variant = fields.Boolean('Es una variante')
    pos_product_varient_id = fields.One2many('pos.product.attribute.line','product_ids',string="Product Varient")
    attribute_id = fields.Many2one('pos.product.attribute', 'Attribute', ondelete='cascade')

class ProductVariant(models.Model):
    _name = 'product.variant'
    _rec_name = 'product_id'
    
    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade', required=True)
    lines = fields.One2many('product.variant.line', 'product_variant', 
                            string='Variants')
    

class PosProductAttributeLine(models.Model):
    _name = "product.variant.line"
    _description = "Product Attribute"
    _order = 'sequence, name'

    variant_type=[('companion','Companion'),
                  ('optional','Optional'),
                  ('suggested','Suggested'),
                  ('term','Term')]
    
    name = fields.Char('Name', required=True, translate=True)
    price = fields.Float("Price", delfault=0.00)
    amount_to_choose = fields.Integer("Amount to choose")
    type = fields.Selection(variant_type,string="Tipo")
    product_variant = fields.Many2one('product.variant', 'lines', ondelete='cascade')
    product_target = fields.Many2one('product.product', help="El producto que se mostrara como variante")
    is_limited = fields.Boolean(string='Limited')
    is_required = fields.Boolean(string='Required')
    sequence = fields.Integer('Sequence', help="Determine the display order")


    


class PosConfig(models.Model):
    _inherit = "pos.config"

    print_unique_id = fields.Char(string='Codigo Unico para Imprimir')
    print_title = fields.Char(string=u'Titulo')
    print_address = fields.Text(string=u'Dirección')




class RestaurantFloor(models.Model):

    _inherit = 'restaurant.floor'

    def _default_pricelist(self):
        return self.env['product.pricelist'].search([('company_id', 'in', (False, self.env.company.id)), ('currency_id', '=', self.env.company.currency_id.id)], limit=1)

    payment_method_id = fields.Many2many(comodel_name='pos.payment.method', string='Metodos de pago')
    pricelist_id = fields.Many2one('product.pricelist', 'Lista de Precio',  default=_default_pricelist)
    fiscal_position_id = fields.Many2one('account.fiscal.position', 'Posicion Fiscal por defecto')


class ProductCategory(models.Model):
    _inherit = "product.category"
    
    printer_name = fields.Char("Priner Name")
    
    