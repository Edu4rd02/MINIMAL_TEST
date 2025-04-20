from decimal import *

# Funcion para verificar si el precio es correcto
# Se asegura que el precio sea mayor o igual a 1 y que tenga dos decimales como máximo
def price_format(price):
    try:
        price = Decimal(price)
        if price >= 1 and price.as_tuple().exponent >= -2:
            return True
        else:
            return False
    except (ValueError, InvalidOperation):
        return False