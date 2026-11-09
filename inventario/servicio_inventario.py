"""Actividad P2: completar las reglas de negocio y sus pruebas unitarias."""
from decimal import Decimal
from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos
from inventario.excepciones import InventarioError, ProductoNoEncontrado


class ServicioInventario:
    def __init__(self, repositorio: RepositorioProductos) -> None:
        self.repositorio = repositorio

    def agregar_producto(self, codigo: str, nombre: str, precio: Decimal, existencia: int) -> Producto:
        """Registra un producto; valida código, nombre, precio y existencia.

        Requisitos: código/nombre no vacíos; precio > 0; existencia >= 0;
        no permitir códigos duplicados. Devolver el producto guardado.
        """
        # P2 implementado: validaciones (RF-01) y persistencia.
        if not isinstance(codigo, str) or not codigo.strip():
            raise InventarioError("El código no puede estar vacío")
        if not isinstance(nombre, str) or not nombre.strip():
            raise InventarioError("El nombre no puede estar vacío")
        if not isinstance(precio, Decimal) or not precio.is_finite() or precio <= 0:
            raise InventarioError("El precio debe ser un Decimal mayor que 0")
        if isinstance(existencia, bool) or not isinstance(existencia, int) or existencia < 0:
            raise InventarioError("La existencia debe ser un entero mayor o igual a 0")
        codigo = codigo.strip()
        nombre = nombre.strip()
        if self._existe(codigo):
            raise InventarioError(f"Código duplicado: {codigo}")

        producto = Producto(codigo, nombre, precio, existencia)
        self.repositorio.guardar(producto)
        return producto

    def consultar_existencia(self, codigo: str) -> int:
        """Devuelve existencias; si no existe, propaga ProductoNoEncontrado."""
        # P2 implementado (RF-02).
        return self.repositorio.obtener(codigo).existencia

    def validar_inventario(self, codigo: str, cantidad: int) -> bool:
        """Exige cantidad > 0 y producto existente.

        Devuelve True cuando hay suficientes unidades. Devuelve False si
        la existencia es insuficiente (no modifica el inventario).
        """
        # P2 implementado (RF-03).
        self._validar_cantidad(cantidad)
        producto = self.repositorio.obtener(codigo)
        return producto.existencia >= cantidad

    def calcular_total(self, codigo: str, cantidad: int) -> Decimal:
        """Devuelve precio * cantidad si cantidad > 0 y producto existe.

        No descuenta inventario. Una existencia insuficiente no invalida
        el cálculo de cotización; la venta real lo validará después.
        """
        # P2 implementado (RF-04).
        self._validar_cantidad(cantidad)
        producto = self.repositorio.obtener(codigo)
        return producto.precio * cantidad

    # --- Métodos auxiliares ---

    def _existe(self, codigo: str) -> bool:
        try:
            self.repositorio.obtener(codigo)
            return True
        except ProductoNoEncontrado:
            return False

    @staticmethod
    def _validar_cantidad(cantidad: int) -> None:
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
