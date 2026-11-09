"""Excepciones de negocio para las validaciones del examen."""


class InventarioError(ValueError):
    """Error de dominio general."""


class ProductoNoEncontrado(InventarioError):
    """Se solicitó un producto inexistente."""


class InventarioInsuficiente(InventarioError):
    """No hay existencias para completar una venta."""
