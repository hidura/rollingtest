# -*- coding: utf-8 -*-
import logging
import json
from odoo import models, fields, api
import requests
_logger = logging.getLogger(__name__)


class BMSClient(models.Model):
    _name = 'bms.client'
    _description = 'The bmsclient connection'

    name = fields.Char("Name")
    key=fields.Char("key")
    granted_until=fields.Date("granted_until", readonly=True)
    status = fields.Boolean("Status", readonly=True)
    
    
    @api.model
    def create(self, vals):
        rec = super(BMSClient, self).create(vals)
        return rec
    
    def write(self, vals):
        # Once the system is called.
        rec = super(BMSClient, self).write(vals)
        return rec
    
    
    def action_validate(self):
        headers = {'odoo_uuid':self.env["ir.config_parameter"]
                    .sudo()
                    .get_param('database.uuid'),
                   'oikos_key':self.key}
        
        url =self.env["ir.config_parameter"].sudo().get_param('oikoschain_api_url')+"bmscore/keyauth"
        response_load = requests.post(url, headers=headers, data=json.dumps({}))
        
        if response_load.status_code == 200:
            keys_information=json.loads(response_load.content.decode())
            #{'status': 0, 'data': [{'active_until': '2023-12-31', 'status_account': True}]}
            if keys_information['status'] == 0:
                self.granted_until = keys_information['data'][0]['active_until']
                self.status = keys_information['data'][0]['status_account']
                self.env['bms.client'].search([('id','=',self.ids[0])]).\
                    write({'granted_until':keys_information['data'][0]['active_until'],
                           'status':keys_information['data'][0]['status_account']})


