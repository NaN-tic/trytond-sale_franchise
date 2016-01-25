# This file is part sale_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'
    franchise = fields.Many2One('sale.franchise', 'Franchise',
        states={
            'readonly': Eval('state') != 'draft',
            },
        depends=['state'])

    @fields.depends('franchise')
    def on_change_franchise(self):
        changes = {}
        if self.franchise and self.franchise.address:
            changes['shipment_address'] = self.franchise.address.id
        return changes
