"""Actividad P3: integrar inventario, repositorio y registro de ventas."""
from inventario.excepciones import InventarioInsuficiente
from inventario.modelos import LineaVenta, ResultadoVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario


class ServicioVentas:
    def __init__(self, inventario: ServicioInventario, repositorio: RepositorioProductos) -> None:
        self.inventario = inventario
        self.repositorio = repositorio

    def registrar_venta(self, linea: LineaVenta) -> ResultadoVenta:
        """Vende una línea de producto.

        Reglas: cantidad > 0, producto existente, existencias suficientes.
        Si no hay existencia, lanzar InventarioInsuficiente.
        Si se concreta la venta, descontar unidades exactamente una vez,
        devolver total y unidades. Ante error, no modificar existencias.
        """
        # P3 implementado.
        # 1) Validar ANTES de modificar nada.
        #    validar_inventario ya lanza ValueError si cantidad <= 0
        #    y ProductoNoEncontrado si el código no existe.
        if not self.inventario.validar_inventario(linea.codigo, linea.cantidad):
            existencia = self.inventario.consultar_existencia(linea.codigo)
            raise InventarioInsuficiente(
                f"Existencias insuficientes para {linea.codigo}: "
                f"solicitadas {linea.cantidad}, disponibles {existencia}"
            )

        # 2) Calcular el total (todavía sin tocar el inventario).
        total = self.inventario.calcular_total(linea.codigo, linea.cantidad)

        # 3) Descontar las unidades UNA sola vez (último paso).
        existencia_actual = self.inventario.consultar_existencia(linea.codigo)
        self.repositorio.actualizar_existencia(
            linea.codigo, existencia_actual - linea.cantidad
        )

        return ResultadoVenta(total=total, unidades=linea.cantidad)
