# templatetags/filtros.py
from django import template

register = template.Library()

@register.filter
def total_con_iva(productos):
    total = 0
    for item in productos:
        total += item.subtotal_con_iva()
    return round(total, 2)
