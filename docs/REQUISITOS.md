# Requisitos funcionales para el examen

## RF-01 Agregar producto

Un producto incluye `codigo`, `nombre`, `precio` (Decimal) y `existencia` (int).
No admite códigos ni nombres vacíos, precio <= 0, existencia < 0 o código duplicado.
Ante una entrada inválida, se espera `ValueError` (o `InventarioError`, subtipo
compatible), sin modificar registros previos.

## RF-02 Consultar existencia

Recibe el código y devuelve las unidades disponibles. Para código inexistente,
se espera `ProductoNoEncontrado`.

## RF-03 Validar inventario

Recibe código y cantidad. La cantidad debe ser entero positivo; de lo contrario
`ValueError`. Si existe el producto, devuelve True/False según el stock disponible.
No altera el repositorio.

## RF-04 Calcular total

Recibe código y cantidad positiva. Devuelve `Decimal` con `precio * cantidad`.
No altera existencias; es un cálculo de cotización. Código inexistente produce
`ProductoNoEncontrado`; cantidad no positiva produce `ValueError`.

## RF-05 Registrar venta

Recibe `LineaVenta(codigo, cantidad)` y devuelve
`ResultadoVenta(total=Decimal, unidades=int)`.
Valida cantidad y existencia. Si no hay inventario, debe lanzar
`InventarioInsuficiente` y conservar el stock original. Si la venta se concreta,
descuenta las unidades una sola vez. Código inexistente produce
`ProductoNoEncontrado`.

## RF-06 Diagnóstico de descuento

`aplicar_descuento(precio, porcentaje)` acepta precio >= 0 y porcentaje entre
0 y 100. Debe devolver el precio con la reducción porcentual correspondiente.
El módulo de diagnóstico incluye un defecto deliberado que debe ser identificado
con una prueba, explicado y corregido por el estudiante.

## RNF-01 Calidad verificable

Pruebas reproducibles con pytest, aserciones significativas y resultados
consistentes. La prueba de entorno no cuenta como parte de las pruebas exigidas.

## RNF-02 Integración continua

Configurar control de versiones y análisis automático de código a partir de un
push a la rama `desarrollo`, con evidencias de GitHub Actions y SonarQube Cloud.
