"""
tests.py — Tests unitarios
============================
Cubre logic.py y service.py completos.

Ejecutar:
    python tests.py

Cada función test_*:
  - Prepara datos de entrada
  - Llama a la función bajo prueba
  - Afirma el resultado esperado con assert

Si todas las aserciones pasan → OK.
Si alguna falla  → AssertionError con mensaje descriptivo.
"""

import os
import json
import tempfile

from logic import (
    calcular_promedio,
    construir_resumen,
    crear_estudiante,
    leer_estudiante,
    leer_todos,
    actualizar_notas,
    eliminar_estudiante,
)
from service import ServicioEstudiantes


# ── Helpers ───────────────────────────────────────────────────────────────────

def _svc_vacio() -> tuple[ServicioEstudiantes, str]:
    """Crea un servicio con archivo temporal vacío para cada test."""
    f = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    f.close()
    os.unlink(f.name)           # que no exista: simula primer arranque
    return ServicioEstudiantes(ruta=f.name), f.name


# =============================================================================
# TESTS de logic.py
# =============================================================================

def test_calcular_promedio_basico():
    assert calcular_promedio([80, 90, 70]) == 80.0, "Promedio básico incorrecto"


def test_calcular_promedio_un_elemento():
    assert calcular_promedio([55.0]) == 55.0, "Promedio de lista unitaria incorrecto"


def test_calcular_promedio_lista_vacia():
    try:
        calcular_promedio([])
        assert False, "Debería lanzar ValueError"
    except ValueError:
        pass    # comportamiento esperado ✅


def test_construir_resumen_aprobado():
    r = construir_resumen("Ana", [60, 70, 80])
    assert r["nombre"]   == "Ana"
    assert r["aprobado"] is True
    assert abs(r["promedio"] - 70.0) < 0.001, "Promedio calculado mal"


def test_construir_resumen_reprobado():
    r = construir_resumen("Luis", [30, 40, 45])
    assert r["aprobado"] is False
    assert r["promedio"] < 51


def test_construir_resumen_promedio_sin_doble_calculo():
    """
    Verifica que construir_resumen usa el mismo promedio para
    'promedio' y 'aprobado' (consistencia interna).
    """
    notas = [51.0]
    r = construir_resumen("Test", notas)
    assert r["aprobado"] == (r["promedio"] >= 51), "Inconsistencia entre promedio y aprobado"


def test_crear_estudiante_ok():
    datos: dict = {}
    ok, msg = crear_estudiante(datos, "Ana", [80, 90])
    assert ok is True
    assert "Ana" in datos
    assert datos["Ana"] == [80, 90]


def test_crear_estudiante_nombre_vacio():
    datos: dict = {}
    ok, _ = crear_estudiante(datos, "", [80])
    assert ok is False
    assert len(datos) == 0


def test_crear_estudiante_duplicado():
    datos = {"Ana": [80.0]}
    ok, _ = crear_estudiante(datos, "Ana", [90.0])
    assert ok is False
    assert datos["Ana"] == [80.0], "No debe sobreescribir el original"


def test_crear_estudiante_sin_notas():
    datos: dict = {}
    ok, _ = crear_estudiante(datos, "Ana", [])
    assert ok is False


def test_leer_estudiante_existente():
    datos = {"Ana": [70.0, 80.0]}
    r = leer_estudiante(datos, "Ana")
    assert r is not None
    assert r["nombre"] == "Ana"


def test_leer_estudiante_no_existente():
    datos = {"Ana": [70.0]}
    r = leer_estudiante(datos, "Luis")
    assert r is None


def test_leer_todos_orden_alfabetico():
    datos = {"Luis": [60.0], "Ana": [90.0], "Marta": [75.0]}
    resumen = leer_todos(datos)
    nombres = [r["nombre"] for r in resumen]
    assert nombres == sorted(nombres), "No está ordenado alfabéticamente"


def test_leer_todos_vacio():
    assert leer_todos({}) == []


def test_actualizar_notas_ok():
    datos = {"Ana": [60.0, 70.0]}
    ok, _ = actualizar_notas(datos, "Ana", [85.0, 90.0])
    assert ok is True
    assert datos["Ana"] == [85.0, 90.0]


def test_actualizar_notas_no_existente():
    datos: dict = {}
    ok, _ = actualizar_notas(datos, "Nadie", [80.0])
    assert ok is False


def test_actualizar_notas_lista_vacia():
    datos = {"Ana": [70.0]}
    ok, _ = actualizar_notas(datos, "Ana", [])
    assert ok is False
    assert datos["Ana"] == [70.0], "No debe borrar notas existentes"


def test_eliminar_existente():
    datos = {"Ana": [80.0]}
    ok, _ = eliminar_estudiante(datos, "Ana")
    assert ok is True
    assert "Ana" not in datos


def test_eliminar_no_existente():
    datos: dict = {}
    ok, _ = eliminar_estudiante(datos, "Nadie")
    assert ok is False


# =============================================================================
# TESTS de service.py
# =============================================================================

def test_service_crear_y_persistir():
    svc, ruta = _svc_vacio()
    ok, _ = svc.crear("Ana", [85.0, 90.0])
    assert ok is True
    assert svc.total == 1

    # Verificar que el archivo se creó con los datos correctos
    with open(ruta) as f:
        guardado = json.load(f)
    assert "Ana" in guardado
    os.unlink(ruta)


def test_service_cargar_desde_disco():
    """Al crear un nuevo servicio con la misma ruta, recupera los datos."""
    svc, ruta = _svc_vacio()
    svc.crear("Ana", [75.0])

    svc2 = ServicioEstudiantes(ruta=ruta)
    assert svc2.total == 1
    assert svc2.leer_uno("Ana") is not None
    os.unlink(ruta)


def test_service_eliminar_persiste():
    svc, ruta = _svc_vacio()
    svc.crear("Ana", [80.0])
    svc.eliminar("Ana")

    svc2 = ServicioEstudiantes(ruta=ruta)
    assert svc2.total == 0
    os.unlink(ruta)


def test_service_actualizar_persiste():
    svc, ruta = _svc_vacio()
    svc.crear("Ana", [60.0])
    svc.actualizar("Ana", [90.0, 95.0])

    svc2 = ServicioEstudiantes(ruta=ruta)
    datos = svc2.leer_uno("Ana")
    assert datos is not None
    assert datos["notas"] == [90.0, 95.0]
    os.unlink(ruta)


def test_service_archivo_corrupto(tmp_path):
    ruta = str(tmp_path / "corrupto.json")
    # Escribir en binario: \xe1 es un byte inválido en UTF-8
    with open(ruta, "wb") as f:
        f.write(b"{esto no es json \xe1\x21\x21\x21}")

    # No debe lanzar excepción — arranca vacío
    svc = ServicioEstudiantes(ruta=ruta)
    assert svc.total == 0


# =============================================================================
# RUNNER
# =============================================================================

def correr_tests() -> None:
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    pasados = fallados = 0

    print("=" * 50)
    print("  EJECUTANDO TESTS")
    print("=" * 50)

    for test in tests:
        nombre = test.__name__
        try:
            # tmp_path manual para el test que lo necesita
            if "tmp_path" in test.__code__.co_varnames:
                import pathlib, tempfile
                with tempfile.TemporaryDirectory() as td:
                    test(pathlib.Path(td))
            else:
                test()
            print(f"  ✅  {nombre}")
            pasados += 1
        except Exception as e:
            print(f"  ❌  {nombre}")
            print(f"       → {e}")
            fallados += 1

    print("=" * 50)
    print(f"  Resultado: {pasados} pasados  |  {fallados} fallados")
    print("=" * 50)


if __name__ == "__main__":
    correr_tests()
