# -*- coding: utf-8 -*-

from odoo import models, fields, api


class patner_dgii(models.Model):
    _name = 'partner.dgii'
    _description = 'Partner information of the dgii full'

    name = fields.Char("name")
    sector=fields.Char("sector")
    street_number=fields.Char("street_number")
    street=fields.Char("street")
    economic_activity=fields.Char("economic_activity")
    phone=fields.Char("phone")
    state=fields.Char("state")
    business_name=fields.Char("business_name")
    rnc=fields.Char("rnc")
    payment_regime=fields.Char("payment_regime")
    constitution_date=fields.Date("constitution_date")

