# Proyecto base — Examen Final de Aseguramiento de la Calidad del Software

**Curso:** Aseguramiento de la Calidad del Software  
**Docente:** Ing. Jersson Castillo  
**Evaluación total:** 35 puntos / 120 minutos  

Este repositorio contiene **el punto de partida, no las soluciones del examen**.
Trabaja individualmente, sigue las actividades que te presente el evaluador y
entrega evidencia en cada paso. No avances hasta que se haya validado tu trabajo.

## Contenido

- `inventario/modelos.py`: estructuras de producto y ventas.
- `inventario/excepciones.py`: errores de negocio.
- `inventario/repositorio.py`: almacenamiento base en memoria.
- `inventario/servicio_inventario.py`: **P2, cuatro métodos por implementar**.
- `inventario/servicio_ventas.py`: **P3, registrar ventas por implementar**.
- `inventario/diagnostico.py`: **P4, defecto intencional a diagnosticar**.
- `tests/test_entorno.py`: prueba inicial para verificar el entorno.
- `tests/test_unitarias.py`: espacio para mínimo cuatro pruebas unitarias.
- `tests/test_integracion.py`: espacio para tres pruebas de integración.
- `tests/test_diagnostico.py`: espacio para demostrar el defecto y su corrección.
- `.github/workflows/sonarqube.yml`: guía incompleta para crear el workflow.
- `sonar-project.properties.example`: parámetros de ejemplo (sin credenciales).
- `docs/REQUISITOS.md`: contrato funcional a implementar.

## Instalación en Windows (PowerShell)

Desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m pytest -v
```

Si PowerShell bloquea la activación, utiliza el ejecutable directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest -v
```

## Instalación en macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m pytest -v
```

## Estado inicial esperado

`pytest` debe ejecutar **1 prueba de entorno exitosa**. Las demás pruebas están
pendientes de escribir: un resultado verde inicial **no significa** que las
actividades P2 y P3 estén resueltas. Los métodos pendientes lanzan
`NotImplementedError` hasta que los implementes.

## Secuencia del examen práctico

1. **P1 (1 pt):** preparar entorno y presentar evidencia de versiones/pytest.
2. **P2 (4 pts):** implementar cuatro métodos de `ServicioInventario` y al menos
   cuatro pruebas unitarias reales, con escenarios positivos/negativos/límite.
3. **P3 (3 pts):** implementar ventas y tres pruebas de integración entre
   componentes (`RepositorioProductos`, `ServicioInventario`, `ServicioVentas`).
4. **P4 (1 pt):** demostrar defecto con una prueba que falle, corregirlo y
   demostrar que pasa. Presentar capturas antes y después.
5. **S1 (2 pts):** crear y publicar ramas `produccion` y `desarrollo` en GitHub.
6. **S2 (2 pts):** analizar el repositorio en SonarQube Cloud e interpretar métricas.
7. **S3 (3 pts):** completar workflow para ejecutar análisis automático tras
   hacer `push` a `desarrollo`, y presentar evidencias.

## Evidencias recomendadas

Capturas con comandos y resultado de pytest; código de pruebas; commit y ramas;
ejecución de GitHub Actions; panel SonarQube Cloud, resultado y Quality Gate.
No compartas tokens de API ni credenciales. Mantén el repositorio privado si
incluyera datos no públicos (este proyecto no necesita ninguno).

## Antes del examen

Recomendación: disponer de Python >= 3.10, Git, GitHub y una cuenta de
SonarQube Cloud. El docente puede proporcionar un repositorio/organización ya
habilitados para agilizar la práctica dentro de las dos horas.

## Calificación

Este archivo no sustituye las instrucciones del evaluador. Cada actividad se
califica sobre su puntaje y puede recibir penalización si se solicitan pistas o
soluciones. Consulta el prompt del examen para la rúbrica completa.
