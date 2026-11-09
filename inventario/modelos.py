"""Modelos sencillos para un sistema de inventario y ventas."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    precio: Decimal
    existencia: int


@dataclass(frozen=True)
class LineaVenta:
    codigo: str
    cantidad: int


@dataclass(frozen=True)
class ResultadoVenta:
    total: Decimal
    unidades: int
