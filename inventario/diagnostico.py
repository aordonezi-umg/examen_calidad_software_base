"""Actividad P4: localizar, corregir y demostrar un defecto deliberado."""


def aplicar_descuento(precio: float, porcentaje: float) -> float:
    """Calcula el precio con descuento.

    Contrato: porcentaje entre 0 y 100; precio no negativo.
    Por ejemplo, un 10 % debe reducir el precio en una décima parte.
    """
    if precio < 0 or not 0 <= porcentaje <= 100:
        raise ValueError("Precio o porcentaje inválido")
    # CORREGIDO P4: el descuento se RESTA (antes se sumaba: precio + ...).
    return precio - precio * (porcentaje / 100)
