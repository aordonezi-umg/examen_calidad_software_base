"""Actividad P4: demostrar un defecto, corregirlo y volver a ejecutar."""
import pytest

from inventario.diagnostico import aplicar_descuento


def test_descuento_del_10_por_ciento_reduce_el_precio():
    """Defecto: un 10 % sobre Q100 debe dar Q90, no Q110."""
    assert aplicar_descuento(100, 10) == pytest.approx(90)


@pytest.mark.parametrize(
    "precio, porcentaje, esperado",
    [
        (100, 0, 100),    # límite inferior: sin descuento, precio igual
        (100, 100, 0),    # límite superior: descuento total, precio 0
        (50, 25, 37.5),   # caso intermedio
    ],
    ids=["sin_descuento", "descuento_total", "descuento_25"],
)
def test_descuento_en_limites(precio, porcentaje, esperado):
    """Límites del contrato: 0 % y 100 %."""
    assert aplicar_descuento(precio, porcentaje) == pytest.approx(esperado)


def test_precio_con_descuento_nunca_supera_el_original():
    """Propiedad: con cualquier porcentaje válido, el precio no puede subir."""
    for porcentaje in range(0, 101):
        assert aplicar_descuento(80, porcentaje) <= 80
