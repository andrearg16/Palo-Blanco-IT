from odoo import models, api, fields
from collections import defaultdict

class Product(models.Model):
    _inherit = 'product.product'

    def _inverse_fsm_quantity(self):
        task = self._get_contextual_fsm_task()
        if task:
            SaleOrderLine_sudo = self.env['sale.order.line'].sudo()
            sale_lines_read_group = SaleOrderLine_sudo.read_group([
                ('order_id', '=', task.sale_order_id.id),
                ('product_id', 'in', self.ids),
                ('task_id', '=', task.id)],
                ['product_id', 'sequence', 'ids:array_agg(id)'],
                ['product_id', 'sequence'],
                lazy=False)
            sale_lines_per_product = defaultdict(lambda: self.env['sale.order.line'])
            for sol in sale_lines_read_group:
                sale_lines_per_product[sol['product_id'][0]] |= SaleOrderLine_sudo.browse(sol['ids'])
            for product in self:
                sale_lines = sale_lines_per_product.get(product.id, self.env['sale.order.line'])
                all_editable_lines = sale_lines.filtered(lambda l: l.qty_delivered == 0 or l.qty_delivered_method == 'manual' or l.state != 'done')
                diff_qty = product.fsm_quantity - sum(sale_lines.mapped('product_uom_qty'))
                if all_editable_lines:  # existing line: change ordered qty (and delivered, if delivered method)
                    if diff_qty > 0:
                        qty_var = all_editable_lines[0].product_uom_qty + diff_qty
                        try:
                            vals = {
                                'product_uom_qty': qty_var,
                                'ctn': qty_var / product.rate_ctn,
                                'inner': qty_var / product.inner_qty,
                                'pb_kgs': (qty_var / product.rate_ctn)/product.weight,
                                'cbm': (qty_var / product.rate_ctn)/product.volume,                             
                            }   
                        except ZeroDivisionError:
                            vals = {
                                'product_uom_qty': qty_var,
                                'ctn': 0,
                                'inner': 0,
                                'pb_kgs': (qty_var / product.rate_ctn)/product.weight,
                                'cbm': (qty_var / product.rate_ctn)/product.volume,  
                            }
                        if all_editable_lines[0].qty_delivered_method == 'manual':
                            vals['qty_delivered'] = all_editable_lines[0].product_uom_qty + diff_qty
                        all_editable_lines[0].with_context(fsm_no_message_post=True).write(vals)
                        all_editable_lines[0].product_uom_change()
                        continue
                    # diff_qty is negative, we remove the quantities from existing editable lines:
                    for line in all_editable_lines:
                        new_line_qty = max(0, line.product_uom_qty + diff_qty)
                        diff_qty += line.product_uom_qty - new_line_qty
                        if line.product_uom_qty != new_line_qty:
                            vals = {
                                'product_uom_qty': new_line_qty
                            }
                            if line.qty_delivered_method == 'manual':
                                vals['qty_delivered'] = new_line_qty
                            line.with_context(fsm_no_message_post=True).write(vals)
                            line.product_uom_change()
                        if diff_qty == 0:
                            break
                elif diff_qty > 0:  # create new SOL
                    try:
                        vals = {
                            'order_id': task.sale_order_id.id,
                            'product_id': product.id,
                            'product_uom_qty': diff_qty,
                            'rate_ctn': product.rate_ctn,
                            'ctn': diff_qty / product.rate_ctn,
                            'inner': diff_qty/product.inner_qty,
                            'pb_kgs': (diff_qty / product.rate_ctn)/product.weight,
                            'cbm': (diff_qty / product.rate_ctn)/product.volume,
                            'product_uom': product.uom_id.id,
                            'task_id': task.id
                        }
                    except ZeroDivisionError:
                        vals = {
                            'order_id': task.sale_order_id.id,
                            'product_id': product.id,
                            'product_uom_qty': diff_qty,
                            'rate_ctn': product.rate_ctn,
                            'ctn': 0,
                            'inner': 0,
                            'pb_kgs': (diff_qty / product.rate_ctn)/product.weight,
                            'cbm': (diff_qty / product.rate_ctn)/product.volume,                            
                            'product_uom': product.uom_id.id,
                            'task_id': task.id
                        }
                    if product.service_type == 'manual':
                        vals['qty_delivered'] = diff_qty

                    if task.sale_order_id.pricelist_id.discount_policy == 'without_discount':
                        sol = SaleOrderLine_sudo.new(vals)
                        sol._onchange_discount()
                        vals.update({'discount': sol.discount or 0.0})
                    sale_line = SaleOrderLine_sudo.create(vals)
                    if not sale_line.qty_delivered_method == 'manual':
                        sale_line.qty_delivered = 0