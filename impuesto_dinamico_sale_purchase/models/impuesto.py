# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_contacto_ventas_iva = fields.Many2one('account.tax',string="Sale Tax")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_partner_iva = fields.Many2one(related="partner_id.x_contacto_ventas_iva",string="Impuesto de Venta")

    @api.onchange('order_line')
    def aplicar_iva_partner(self):
            for order in self:
                if order.x_partner_iva:
                    for line in order.order_line:
                        line.tax_id = order.x_partner_iva

class ResPartnerPurchase(models.Model):
    _inherit = "res.partner"

    x_contacto_compras_iva = fields.Many2one('account.tax',string="Purchase Tax")

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_partner_iva = fields.Many2one(related="partner_id.x_contacto_compras_iva",string="Impuesto de Compras")

    @api.onchange('order_line')
    def aplicar_iva_partner(self):
            for order in self:
                if order.x_partner_iva:
                    for line in order.order_line:
                        line.taxes_id = order.x_partner_iva
