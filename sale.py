# This file is part sale_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Sale', 'ShipmentOut', 'ShipmentOutReturn']
__metaclass__ = PoolMeta


class FranchiseAddressMixin:
    _franchise_address_field = 'delivery_address'
    franchise_party = fields.Function(fields.Many2One('party.party',
            'Franchise Party'),
        'on_change_with_franchise_party')

    @classmethod
    def __setup__(cls):
        super(FranchiseAddressMixin, cls).__setup__()
        field = getattr(cls, cls._franchise_address_field)
        if 'franchise_party' not in field.depends:
            current_domain = field.domain
            field.domain = [
                'OR',
                current_domain,
                [('party', '=', Eval('franchise_party', 0))]
                ]
            field.depends.append('franchise_party')


class Sale(FranchiseAddressMixin):
    __name__ = 'sale.sale'
    _franchise_address_field = 'shipment_address'
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

    @fields.depends('franchise')
    def on_change_with_franchise_party(self, name=None):
        if self.franchise:
            return self.franchise.company_party.id


class ShipmentOut(FranchiseAddressMixin):
    __name__ = 'stock.shipment.out'

    @fields.depends('outgoing_moves')
    def on_change_with_franchise_party(self, name=None):
        pool = Pool()
        SaleLine = pool.get('sale.line')
        for move in self.outgoing_moves:
            if hasattr(move, 'origin') and isinstance(move.origin, SaleLine):
                sale = move.origin.sale
                if sale.franchise:
                    return sale.franchise.company_party.id


class ShipmentOutReturn(FranchiseAddressMixin):
    __name__ = 'stock.shipment.out.return'

    @fields.depends('incoming_moves')
    def on_change_with_franchise_party(self, name=None):
        pool = Pool()
        SaleLine = pool.get('sale.line')
        for move in self.incoming_moves:
            if isinstance(move.origin, SaleLine):
                sale = move.origin.sale
                if sale.franchise:
                    return sale.franchise.company_party.id
