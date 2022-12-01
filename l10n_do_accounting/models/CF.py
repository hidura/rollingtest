from odoo import api, fields, models


"""This is the handle of the Comprobantes fiscales, allows the user to
Invervine and change or alter the sequence of the CF in question"""


class cf_sequence(models.Model):
    _name = "sequence.cf"

    name = fields.Char("name")
    l10n_latam_document_type_id = fields.Many2one("l10n_latam.document.type", String="Comprobante fiscal")
    current_sequence = fields.Integer("current_sequence", String="Secuencia actual")
    limit = fields.Integer("Limit", String="Limite")
    alarm_ncf = fields.Integer("alarm_ncf", String="Enviar aviso al llegar al número")

    @api.model
    def create(self, vals_list):
        if vals_list['limit'] == vals_list['current_sequence']:
            raise Exception("El limite no puede ser igual a la secuencia")
        id = super(cf_sequence, self).create(vals_list)
        return id

    def write(self, vals_list):
        id = super(cf_sequence, self).write(vals_list)

        return id
    
    def getNCF(self, partner_id):
        partner = self.env['res.partner'].search([('id', '=', partner_id)])
        
        latam_document_type = self.env['l10n_latam.document.type']. \
            search([('l10n_do_ncf_type', '=',
                        partner._get_l10n_do_ncf_types_data()['issued'][partner.l10n_do_dgii_tax_payer_type][0])])
        cf_sequence = self.env['sequence.cf']. \
            search([('l10n_latam_document_type_id', '=', latam_document_type.id)])

        new_sequence = cf_sequence.current_sequence + 1
        l10n_latam_document_number = str(new_sequence).zfill(8)
        cf_sequence.write({'current_sequence': new_sequence})
        return {
            "l10n_latam_document_number": latam_document_type.doc_code_prefix + l10n_latam_document_number,
            'l10n_latam_use_documents': True,
            "l10n_latam_document_type_id": latam_document_type.id,
            "l10n_do_ncf_expiration_date": latam_document_type.l10n_do_ncf_expiration_date
        }


class SequenceMove(models.Model):
    _name = "sequence.cf.move"

    name = fields.Char("name")
    l10n_latam_document_type_id = fields.Many2one("l10n_latam.document.type", String="Comprobante fiscal")
    cf_sequence = fields.Many2one("cf.sequence")
    pos_order = fields.Many2one("pos.order")
    account_move = fields.Many2one("account.move")
