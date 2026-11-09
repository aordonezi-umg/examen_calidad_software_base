"""Actividad P2: pruebas unitarias de ServicioInventario.

Cubren escenarios positivos, negativos (pytest.raises) y de límite
según RF-01 a RF-04 de docs/REQUISITOS.md.
"""
from decimal import Decimal

import pytest

from inventario.excepciones import InventarioError, ProductoNoEncontrado
from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario


@pytest.fixture
def servicio() -> ServicioInventario:
    """Servicio con un producto base: P-01, Q12.50, 5 unidades."""
    repo = RepositorioProductos()
    srv = ServicioInventario(repo)
    srv.agregar_producto("P-01", "Cuaderno", Decimal("12.50"), 5)
    return srv


# ---------- RF-01 Agregar producto ----------

def test_agregar_producto_valido_lo_guarda_y_lo_devuelve(servicio):
    """Positivo: el producto se devuelve y queda persistido en el repositorio."""
    producto = servicio.agregar_producto("P-02", "Lapicero", Decimal("7.25"), 20)

    assert producto == Producto("P-02", "Lapicero", Decimal("7.25"), 20)
    assert servicio.repositorio.obtener("P-02") == producto


@pytest.mark.parametrize(
    "codigo, nombre, precio, existencia",
    [
        ("", "Borrador", Decimal("3.00"), 1),        # código vacío
        ("   ", "Borrador", Decimal("3.00"), 1),     # código solo espacios
        ("P-03", "", Decimal("3.00"), 1),            # nombre vacío
        ("P-03", "Borrador", Decimal("0"), 1),       # precio = 0 (límite inválido)
        ("P-03", "Borrador", Decimal("-1.00"), 1),   # precio negativo
        ("P-03", "Borrador", Decimal("3.00"), -1),   # existencia negativa (límite)
    ],
    ids=["codigo_vacio", "codigo_espacios", "nombre_vacio",
         "precio_cero", "precio_negativo", "existencia_negativa"],
)
def test_agregar_producto_invalido_lanza_error(servicio, codigo, nombre, precio, existencia):
    """Negativo: cada dato inválido se rechaza y no se registra nada."""
    with pytest.raises(ValueError):
        servicio.agregar_producto(codigo, nombre, precio, existencia)

    assert len(servicio.repositorio.listar()) == 1  # solo el producto base


def test_agregar_codigo_duplicado_no_modifica_el_original(servicio):
    """Negativo: un código repetido se rechaza y conserva el registro previo."""
    with pytest.raises(InventarioError):
        servicio.agregar_producto("P-01", "Otro nombre", Decimal("99.99"), 100)

    original = servicio.repositorio.obtener("P-01")
    assert original.nombre == "Cuaderno"
    assert original.precio == Decimal("12.50")
    assert original.existencia == 5


def test_agregar_producto_con_valores_limite_validos(servicio):
    """Límite: existencia 0 y precio mínimo positivo (0.01) son válidos."""
    producto = servicio.agregar_producto("P-04", "Clip", Decimal("0.01"), 0)

    assert producto.existencia == 0
    assert producto.precio == Decimal("0.01")


# ---------- RF-02 Consultar existencia ----------

def test_consultar_existencia_devuelve_unidades(servicio):
    """Positivo: devuelve las unidades registradas."""
    assert servicio.consultar_existencia("P-01") == 5


def test_consultar_existencia_producto_inexistente(servicio):
    """Negativo: un código inexistente lanza ProductoNoEncontrado."""
    with pytest.raises(ProductoNoEncontrado):
        servicio.consultar_existencia("NO-EXISTE")


# ---------- RF-03 Validar inventario ----------

def test_validar_inventario_suficiente(servicio):
    """Positivo: 3 de 5 unidades disponibles."""
    assert servicio.validar_inventario("P-01", 3) is True


def test_validar_inventario_en_el_limite(servicio):
    """Límite: cantidad == existencia (5) se acepta; existencia + 1 (6) no."""
    assert servicio.validar_inventario("P-01", 5) is True
    assert servicio.validar_inventario("P-01", 6) is False
    assert servicio.consultar_existencia("P-01") == 5  # no altera el stock


@pytest.mark.parametrize("cantidad", [0, -1], ids=["cero", "negativa"])
def test_validar_inventario_cantidad_no_positiva(servicio, cantidad):
    """Negativo/límite: 0 y negativos lanzan ValueError."""
    with pytest.raises(ValueError):
        servicio.validar_inventario("P-01", cantidad)


def test_validar_inventario_producto_inexistente(servicio):
    """Negativo: producto inexistente lanza ProductoNoEncontrado."""
    with pytest.raises(ProductoNoEncontrado):
        servicio.validar_inventario("NO-EXISTE", 1)


# ---------- RF-04 Calcular total ----------

def test_calcular_total_precio_por_cantidad(servicio):
    """Positivo: 3 x 12.50 = 37.50 exacto (Decimal) y sin tocar el stock."""
    total = servicio.calcular_total("P-01", 3)

    assert total == Decimal("37.50")
    assert isinstance(total, Decimal)
    assert servicio.consultar_existencia("P-01") == 5


def test_calcular_total_permite_cotizar_mas_que_la_existencia(servicio):
    """Límite: cotizar 6 unidades con 5 en stock es válido (es solo cotización)."""
    assert servicio.calcular_total("P-01", 6) == Decimal("75.00")


def test_calcular_total_cantidad_cero_lanza_error(servicio):
    """Negativo/límite: cantidad 0 lanza ValueError."""
    with pytest.raises(ValueError):
        servicio.calcular_total("P-01", 0)


def test_calcular_total_producto_inexistente(servicio):
    """Negativo: producto inexistente lanza ProductoNoEncontrado."""
    with pytest.raises(ProductoNoEncontrado):
        servicio.calcular_total("NO-EXISTE", 1)
