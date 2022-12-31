// © 2022 Diego Hidalgo <dhidalgo@oikoschain.com>


// This file is part of Restaurant manager.

odoo.define('bmsclient.pos_order', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var _super_order = models.Order.prototype;
    var _super_posmodel = models.PosModel.prototype;
    var rpc = require('web.rpc');

   
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function (attr, options) {
            this.server_id=null;
            _super_orderline.initialize.call(this, attr, options);
        },
        init_from_JSON: function (json) {
            _super_orderline.init_from_JSON.call(this, json);
            
            this.server_id=json.server_id;
        },
        getUUIDByName: function (name) {
            
        },
        generateUUID:function() { // Public Domain/MIT
            var d = new Date().getTime();//Timestamp
            var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16;//random number between 0 and 16
                if(d > 0){//Use timestamp until depleted
                    r = (d + r)%16 | 0;
                    d = Math.floor(d/16);
                } else {//Use microseconds since page-load if supported
                    r = (d2 + r)%16 | 0;
                    d2 = Math.floor(d2/16);
                }
                return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            })
        },
        export_as_JSON: function () {
            var json = _super_orderline.export_as_JSON.call(this);
            
            $.extend(json, {
                order_line_id:this.server_id
            });
            return json;
        },
    });

    return models;
});
