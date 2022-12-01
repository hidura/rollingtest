from odoo import models


class IrSequence(models.Model):
    _inherit = "pos.order"

    def get_next_sequence(self):
        return {
            "ncf": self.next_by_id(),
            "expiration_date": self.expiration_date,
        }
