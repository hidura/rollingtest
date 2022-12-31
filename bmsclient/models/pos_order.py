from odoo import api, fields, models
import requests
import logging
import psycopg2
import datetime
from datetime import date


_logger = logging.getLogger(__name__)

from odoo.addons.point_of_sale.models.pos_order import PosOrder as OriginalPosOrder

class PosOrderLine(models.Model):
    
    _inherit = "pos.order.line"
    
    uuid = fields.Char("UUID", help="The Unique identifier of the line,"+
                      "this must be created in the process order, if it exist the line"+
                      " will be change, if not will be created and added, this is just for the restaurant")
    
    def _export_for_ui(self, order):
        result = super(PosOrderLine, self)._export_for_ui(order)
        result['uuid'] = order.uuid
        return result

class General:
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
                    

@api.model
def _process_order(self, order, draft, existing_order):
    """Create or update an pos.order from a given dictionary.

    :param dict order: dictionary representing the order.
    :param bool draft: Indicate that the pos_order is not validated yet.
    :param existing_order: order to be updated or False.
    :type existing_order: pos.order.
    :returns: id of created/updated pos.order
    :rtype: int
    """
    order = order['data']
    pos_session = self.env['pos.session'].browse(order['pos_session_id'])
    if pos_session.state == 'closing_control' or pos_session.state == 'closed':
        order['pos_session_id'] = self._get_valid_session(order).id

    pos_order = False
    
    if not existing_order:
        pos_order = self.create(self._order_fields(order))
    else:
        
        order_to_write=[]
        pos_order = existing_order
        if not pos_order.session_id.config_id.module_pos_restaurant:
            pos_order.lines.unlink()
        else:
            #Get the saved lines and just add the not present ones
            lines = order['lines']
            for newline in lines:
                if newline[2]['order_line_id'] != None:
                    order_to_write.append(newline[2])
                    lines.remove(newline)
            
                
            #Hay que agregar un uuid al momento de cargar los orderlines en JS y procurar que lo agregue como parte
            # de los datos del producto al momento de seleccionarlo en ambos lados a fin de que el producto pueda tener su
            # propio identificador con el cual saber si fue guardado o no en la base de datos. Probar que sube y baja el uuid ahora
            # for orderline in pos_order.lines:
                
            #     oldline=General().cleanerFields(orderline.read(list(set(self.env['pos.order.line']._fields))))
                
                
        order['user_id'] = pos_order.user_id.id
        order_info=self._order_fields(order)
        pos_order.write(order_info)
        for oldline in order_to_write:
            orderline = self.env['pos.order.line'].search([('id','=',oldline['order_line_id'])])
            del oldline['order_line_id']
            del oldline['id']
            del oldline['description']
            del oldline['price_extra']
            orderline.write(oldline)

    pos_order = pos_order.with_company(pos_order.company_id)
    self = self.with_company(pos_order.company_id)
    self._process_payment_lines(order, pos_order, pos_session, draft)

    if not draft:
        try:
            pos_order.action_pos_order_paid()
        except psycopg2.DatabaseError:
            # do not hide transactional errors, the order(s) won't be saved!
            raise
        except Exception as e:
            _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))
        pos_order._create_order_picking()
        pos_order._compute_total_cost_in_real_time()

    if pos_order.to_invoice and pos_order.state == 'paid':
        pos_order._generate_pos_order_invoice()

    return pos_order.id
    
OriginalPosOrder._process_order = _process_order

