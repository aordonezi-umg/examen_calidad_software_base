"""Prueba inicial para confirmar que pytest y los imports funcionan."""
from decimal import Decimal
from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos


def test_repositorio_guarda_y_recupera_producto() -> None:
    repo = RepositorioProductos()
    producto = Producto("P-01", "Cuaderno", Decimal("12.50"), 5)
    repo.guardar(producto)
    assert repo.obtener("P-01") == producto
