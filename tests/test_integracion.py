"""Actividad P3: pruebas de integración.

Integran componentes REALES (sin mocks):
RepositorioProductos + ServicioInventario + ServicioVentas,
compartiendo el mismo repositorio.

Flujos requeridos:
1. Alta de producto -> consulta de inventario.
2. Alta -> venta -> descuento de existencias -> total.
3. Alta -> intento de venta insuficiente -> rechazo sin modificar stock.
"""
from decimal import Decimal

import pytest

from inventario.excepciones import InventarioInsuficiente
from inventario.modelos import LineaVenta, ResultadoVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.servicio_ventas import ServicioVentas


@pytest.fixture
def sistema():
    """Arma el sistema real: UN repositorio compartido por los dos servicios."""
    repo = RepositorioProductos()
    inventario = ServicioInventario(repo)
    ventas = ServicioVentas(inventario, repo)
    return repo, inventario, ventas


def test_alta_de_producto_y_consulta_de_inventario(sistema):
    """Flujo 1: lo que registra ServicioInventario queda en el repositorio
    y se puede consultar de vuelta."""
    repo, inventario, _ = sistema

    inventario.agregar_producto("P-10", "Martillo", Decimal("85.00"), 10)

    assert inventario.consultar_existencia("P-10") == 10
    guardado = repo.obtener("P-10")
    assert guardado.nombre == "Martillo"
    assert guardado.precio == Decimal("85.00")


def test_venta_descuenta_existencias_y_calcula_total(sistema):
    """Flujo 2: la venta calcula el total y descuenta el stock una sola vez."""
    _, inventario, ventas = sistema
    inventario.agregar_producto("P-20", "Cuaderno", Decimal("12.50"), 10)

    resultado = ventas.registrar_venta(LineaVenta("P-20", 3))

    assert resultado == ResultadoVenta(total=Decimal("37.50"), unidades=3)
    assert inventario.consultar_existencia("P-20") == 7  # 10 - 3, no 4 ni 10


def test_venta_insuficiente_se_rechaza_sin_modificar_stock(sistema):
    """Flujo 3: pedir 6 con 5 en existencia se rechaza y el stock no cambia."""
    _, inventario, ventas = sistema
    inventario.agregar_producto("P-30", "Lapicero", Decimal("7.25"), 5)

    with pytest.raises(InventarioInsuficiente, match="insuficientes"):
        ventas.registrar_venta(LineaVenta("P-30", 6))

    assert inventario.consultar_existencia("P-30") == 5


def test_venta_de_todas_las_existencias_deja_stock_en_cero(sistema):
    """Límite (extra): vender exactamente lo disponible se acepta y deja 0."""
    _, inventario, ventas = sistema
    inventario.agregar_producto("P-40", "Regla", Decimal("5.00"), 5)

    resultado = ventas.registrar_venta(LineaVenta("P-40", 5))

    assert resultado.total == Decimal("25.00")
    assert inventario.consultar_existencia("P-40") == 0