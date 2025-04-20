def productos_bajo_stock(productos):
    alertas = []
    for producto in productos:
        if producto.cantidad <= producto.stock_minimo:
            alertas.append(producto.nombre)
    return alertas
