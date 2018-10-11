# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import franchise
from . import sale


def register():
    Pool.register(
        franchise.Category,
        franchise.Franchise,
        franchise.FranchiseCategory,
        franchise.Party,
        sale.Sale,
        module='sale_franchise', type_='model')
