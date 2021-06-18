# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from itertools import groupby
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_descuento_1 = fields.Integer("Descuento General(%)")
    x_descuento_value = fields.Integer(string="Descuento General ($)",readonly=True)
    representate_legal = fields.Many2one('res.partner', string='Representante Legal')
    # tipo_cambio = fields.Float(string='Tipo de Cambio')


    # @api.depends('order_line.price_total')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for order in self:
    #         descuento_value = order.x_descuento_1
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             line.discount = descuento_value
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         # descuento = (amount_untaxed * descuento_value) / 100
    #         order.update({
    #             # 'x_descuento_value': descuento,
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax': amount_tax,
    #             # 'amount_total': (amount_untaxed-descuento) + amount_tax,
    #             'amount_total': amount_untaxed + amount_tax,
    #         })

    def discount_global(self):
         for order in self:
            descuento_value = order.x_descuento_1
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line.discount = descuento_value
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            # descuento = (amount_untaxed * descuento_value) / 100
            order.update({
                # 'x_descuento_value': descuento,
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                # 'amount_total': (amount_untaxed-descuento) + amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

