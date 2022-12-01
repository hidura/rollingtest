odoo.define('l10n_henca_pos.receipt', function (require) {
    'use strict';
    const models = require('point_of_sale.models');
    models.load_fields('res.partner', 'vat');
    
    models.load_fields('pos.order', 'l10n_latam_document_type_id,l10n_do_is_return_order,l10n_do_return_order_id,l10n_do_ncf_expiration_date,l10n_do_origin_ncf,l10n_latam_document_number');
    

    
});