from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError
import re

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_l10n_do_ncf_types_data(self):
        return {
            "issued": {
                "taxpayer": ["fiscal"],
                "non_payer": ["consumer", "unique"],
                "nonprofit": ["fiscal"],
                "special": ["special"],
                "governmental": ["governmental"],
                "foreigner": ["export", "consumer"],
            },
            "received": {
                "taxpayer": ["fiscal"],
                "non_payer": ["informal", "minor"],
                "nonprofit": ["special", "governmental"],
                "special": ["fiscal", "special", "governmental"],
                "governmental": ["fiscal", "special", "governmental"],
                "foreigner": ["import", "exterior"],
            },
        }

