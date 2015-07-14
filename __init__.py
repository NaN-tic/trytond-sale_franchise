# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .franchise import *
from .sale import *


def register():
    Pool.register(
        Franchise,
        Party,
        Sale,
        ShipmentOut,
        ShipmentOutReturn,
        module='sale_franchise', type_='model')
