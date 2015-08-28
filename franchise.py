# This file is part sale_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Category', 'Franchise', 'Party']


class Category(ModelSQL, ModelView):
    'Franchise Category'
    __name__ = 'sale.franchise.category'
    name = fields.Char('Name', required=True, select=True)


class Franchise(ModelSQL, ModelView):
    'Sale Franchise'
    __name__ = 'sale.franchise'

    code = fields.Char('code', required=True, select=True)
    name = fields.Char('Name', required=True, select=True)
    company = fields.Many2One('company.company', 'Company', required=True)
    company_party = fields.Function(fields.Many2One('party.party',
            'Company Party'),
        'on_change_with_company_party', searcher='search_company_party')
    address = fields.Many2One('party.address', 'Address',
        domain=[
            ('party', '=', Eval('company_party')),
            ],
        depends=['company_party'])
    category = fields.Many2One('sale.franchise.category', 'Category')
    supervisor = fields.Many2One('company.employee', 'Supervisor', select=True)

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    state = fields.Selection([
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ], 'State', required=True)

    @staticmethod
    def default_start_date():
        pool = Pool()
        Date = pool.get('ir.date')
        return Date.today()

    @staticmethod
    def default_state():
        return 'active'

    @fields.depends('company')
    def on_change_with_company_party(self, name=None):
        if self.company:
            return self.company.party.id

    @classmethod
    def search_company_party(cls, name, clause):
        return [('company.party',) + tuple(clause[1:])]


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    franchises = fields.One2Many('sale.franchise', 'company_party',
        'Franchises', readonly=True)
