# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import math

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_to_text_mxn = fields.Char("MXN", store=True)
    amount_to_text_usd = fields.Char("USD", store=True)

    @api.onchange('tax_totals_json')
    def amount_to_text(self):
        for order in self:
            if order.currency_id:
                parte_decimal, parte_entera = math.modf(order.amount_total)
                decimal = float(order.amount_total) - parte_entera
                decimal = round(decimal,2) * 100
                order.update({
                    'amount_to_text_mxn': "%s %s/100 M.N." %(order.currency_id.amount_to_text(parte_entera),int(decimal)),
                    'amount_to_text_usd': "%s %s/100 USD" %(order.currency_id.amount_to_text(parte_entera).replace("Pesos", "Dolares"),int(decimal)),
                })

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    amount_to_text_mxn_oc = fields.Char("MXN", store=True)
    amount_to_text_usd_oc = fields.Char("USD", store=True)

    @api.onchange('tax_totals_json')
    def amount_to_text(self):
        for order in self:
            parte_decimal, parte_entera = math.modf(order.amount_total)
            decimal = float(order.amount_total) - parte_entera
            decimal = round(decimal,2) * 100
            order.update({
                'amount_to_text_mxn_oc': "%s %s/100 M.N." %(order.currency_id.amount_to_text(parte_entera),int(decimal)),
                'amount_to_text_usd_oc': "%s %s/100 USD" %(order.currency_id.amount_to_text(parte_entera).replace("Pesos", "Dolares"),int(decimal)),
            })
            