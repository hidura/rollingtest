// © 2015-2018 Eneldo Serrata <eneldo@marcos.do>
// © 2017-2018 Gustavo Valverde <gustavo@iterativo.do>
// © 2018 Jorge Hernández <jhernandez@gruponeotec.com>
// © 2018 Francisco Peñaló <frankpenalo24@gmail.com>
// © 2018 Kevin Jiménez <kevinjimenezlorenzo@gmail.com>
// © 2019-2020 Raul Ovalle <raulovallet@gmail.com>

// This file is part of NCF Manager.

// NCF Manager is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// NCF Manager is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with NCF Manager.  If not, see <https://www.gnu.org/licenses/>.


odoo.define('l10n_do_pos.screens', function (require) {
    "use strict";

    var RefundButton = require('point_of_sale.RefundButton');
    var PayButton = require('point_of_sale.ActionpadWidget');
    var gui = require('point_of_sale.Gui');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;

    // RefundButton.includes({
    //     _onClick(){
    //         alert("Logre hacer click")
    //         this._super.apply(this, arguments)
    //     }
    // })

});
