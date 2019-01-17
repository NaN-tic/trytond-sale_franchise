# This file is part sale_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond import backend
from trytond.transaction import Transaction

__all__ = ['Category', 'Franchise', 'FranchiseCategory', 'Party']


class Category(ModelSQL, ModelView):
    'Franchise Category'
    __name__ = 'sale.franchise.category'
    name = fields.Char('Name', required=True, select=True)
    franchises = fields.Many2Many('sale.franchise-sale.franchise.category',
        'category', 'franchise', 'Franchises')


class Franchise(ModelSQL, ModelView):
    'Sale Franchise'
    __name__ = 'sale.franchise'

    code = fields.Char('code', required=True, select=True)
    name = fields.Char('Name', required=True, select=True)
    company = fields.Many2One('company.company', 'Company')
    company_party = fields.Many2One('party.party', 'Company Party')
    address = fields.Many2One('party.address', 'Address',
        domain=[
            ('party', '=', Eval('company_party')),
            ],
        depends=['company_party'])
    categories = fields.Many2Many('sale.franchise-sale.franchise.category',
        'franchise', 'category', 'Categories')
    supervisor = fields.Many2One('company.employee', 'Supervisor', select=True)

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    state = fields.Selection([
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ], 'State', required=True)

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().connection.cursor()
        table = TableHandler(cls, module_name)
        sql_table = cls.__table__()
        pool = Pool()
        Company = pool.get('company.company')
        company = Company.__table__()

        created_company_party = not table.column_exist('company_party')
        category_exists = table.column_exist('category')

        super(Franchise, cls).__register__(module_name)

        # Migration from 3.4: drop required on company
        if created_company_party:
            value = company.select(company.party,
                    where=company.id == sql_table.company)
            cursor.execute(*sql_table.update([sql_table.company_party],
                    [value]))
        table.not_null_action('company', action='remove')
        # Migration from 3.4.0: drop category field (replaced by categories)
        if category_exists:
            table.drop_column('category')

    def get_rec_name(self, name):
        return '[%s] %s' % (self.code, self.name)

    @classmethod
    def search_rec_name(cls, name, clause):
        return [
            ['OR',
                ('code',) + tuple(clause[1:]),
                ('name',) + tuple(clause[1:]),
                ]]

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


class FranchiseCategory(ModelSQL):
    'Franchise - Category'
    __name__ = 'sale.franchise-sale.franchise.category'
    franchise = fields.Many2One('sale.franchise', 'Franchise',
        ondelete='CASCADE', required=True, select=True)
    category = fields.Many2One('sale.franchise.category', 'Category',
        ondelete='CASCADE', required=True, select=True)


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    franchises = fields.One2Many('sale.franchise', 'company_party',
        'Franchises', readonly=True)
