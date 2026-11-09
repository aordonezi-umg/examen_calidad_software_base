"""Almacenamiento en memoria: componente inicial suministrado."""
from dataclasses import replace
from inventario.modelos import Producto
from inventario.excepciones import ProductoNoEncontrado


class RepositorioProductos:
    def __init__(self) -> None:
        self._productos: dict[str, Producto] = {}

    def guardar(self, producto: Producto) -> None:
        self._productos[producto.codigo] = producto

    def obtener(self, codigo: str) -> Producto:
        try:
            return self._productos[codigo]
        except KeyError as exc:
            raise ProductoNoEncontrado(f"Producto no encontrado: {codigo}") from exc

    def actualizar_existencia(self, codigo: str, nueva_existencia: int) -> None:
        producto = self.obtener(codigo)
        self.guardar(replace(producto, existencia=nueva_existencia))

    def listar(self) -> list[Producto]:
        return list(self._productos.values())
