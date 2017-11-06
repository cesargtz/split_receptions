# -*- coding: utf-8 -*-

from odoo import models, fields, api

class split_receptions(models.Model):
    _inherit = ['mail.thread']
    _name = 'split.receptions'

    name = fields.Char('Split reception reference', required=True, select=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('reg_code_split'), help="Unique number of the Split reception")

    contract_id = fields.Many2one('purchase.order', required=True)
    partner_id = fields.Many2one('res.partner', 'Productor', readonly=True, related="contract_id.partner_id")

    contract_dest_id = fields.Many2one('purchase.order', required=True)
    partner_dest_id = fields.Many2one('res.partner', 'Productor', readonly=True, related="contract_dest_id.partner_id")

    hired = fields.Float('Contratado', compute="_compute_hired", readonly=True, store=False)
    hired_dest = fields.Float('Contratado', compute="_compute_hired_dest", readonly=True, store=False)

    delivered = fields.Float('Entregado', compute="_compute_delivered", readonly=True, store=False, digits=(12, 3))
    delivered_dest = fields.Float('Entregado', compute="_compute_delivered_dest", readonly=True, store=False, digits=(12, 3))

    tons_transfer = fields.Float(digits=(12, 3), required=True)

    state = fields.Selection([
        ('open', 'Abierto'),
        ('close', 'Cerrado'),
    ], default='open',readonly=True)



    @api.one
    @api.depends('contract_id')
    def _compute_hired(self):
        self.hired = sum(line.product_qty for line in self.contract_id.order_line)

    @api.one
    @api.depends('contract_dest_id')
    def _compute_hired_dest(self):
        self.hired_dest = sum(line.product_qty for line in self.contract_dest_id.order_line)

    @api.one
    @api.depends('contract_id')
    def _compute_delivered(self):
        self.delivered += self.contract_id.tons_reception

    @api.one
    @api.depends('contract_dest_id')
    def _compute_delivered_dest(self):
        self.delivered_dest += self.contract_dest_id.tons_reception


    @api.onchange('tons_transfer')
    def _onchange_tons(self):
        price = self.env['pinup.price.purchase'].search([('purchase_order_id', '=', self.contract_id.name),('state', '=', 'close')])
        if self.tons_transfer > (self.delivered - price.tons_priced):
            return {
                'warning': {
                    'title': "ATENCIÓN",
                    'message': "No cuentas con las toneladas necesarias.",
                }
            }

    @api.model
    def create(self, vals):
        vals['state'] = 'close'
        res = super(split_receptions, self).create(vals)
        return res
