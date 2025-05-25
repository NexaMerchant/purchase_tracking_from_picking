from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_carrier_tracking_refs = fields.Char(
        string="快递单号",
        compute='_compute_picking_carrier_tracking_refs',
        search='_search_picking_carrier_tracking_refs',
        store=False,
        readonly=True,
        help="所有相关收货单的快递单号，逗号分隔"
    )

    def _compute_picking_carrier_tracking_refs(self):
        for order in self:
            refs = []
            for picking in order.picking_ids:
                ref = getattr(picking, 'carrier_tracking_ref', False)
                if ref:
                    refs.append(ref)
            order.picking_carrier_tracking_refs = ', '.join(refs)

    def _search_picking_carrier_tracking_refs(self, operator, value):
        pickings = self.env['stock.picking'].search([('carrier_tracking_ref', operator, value)])
        order_ids = pickings.mapped('purchase_id').ids
        return [('id', 'in', order_ids)]