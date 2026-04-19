"""
logic.py — Lógica pura
========================
Funciones sin efectos: reciben datos, retornan datos.
Sin prints, sin input(), sin I/O.

Regla: si una función tiene `print` o `input`, no pertenece aquí.
"""

from typing import TypedDict
from data import Estudiantes


# ── Tipos ─────────────────────────────────────────────────────────────────────

class ResumenEstudiante(TypedDict):
    nombre  : str
    notas   : list[float]
    promedio: float
    aprobado: bool


# ── Funciones puras ───────────────────────────────────────────────────────────

def calcular_promedio(notas: list[float]) -> float:
    """Promedio de una lista. Lanza ValueError si está vacía."""
    if not notas:
        raise ValueError("No se puede calcular el promedio de una lista vacía.")
    return sum(notas) / len(notas)


def construir_resumen(nombre: str, notas: list[float]) -> ResumenEstudiante:
    """
    Construye el ResumenEstudiante completo para un estudiante.
    Calcula el promedio UNA vez y lo reutiliza — sin redundancia.
    """
    prom = calcular_promedio(notas)
    return ResumenEstudiante(
        nombre   = nombre,
        notas    = notas,
        promedio = prom,
        aprobado = prom >= 51,
    )


# ── CRUD (lógica pura, sin persistencia) ─────────────────────────────────────

def crear_estudiante(
    estudiantes: Estudiantes,
    nombre: str,
    notas: list[float],
) -> tuple[bool, str]:
    """C — Valida y agrega. Retorna (éxito, mensaje)."""
    if not nombre:
        return False, "El nombre no puede estar vacío."
    if nombre in estudiantes:
        return False, f"'{nombre}' ya está registrado."
    if not notas:
        return False, "Debe ingresar al menos una nota."

    estudiantes[nombre] = notas
    return True, f"'{nombre}' registrado con {len(notas)} nota(s)."


def leer_estudiante(
    estudiantes: Estudiantes,
    nombre: str,
) -> ResumenEstudiante | None:
    """R — Retorna resumen de uno o None si no existe."""
    if nombre not in estudiantes:
        return None
    return construir_resumen(nombre, estudiantes[nombre])


def leer_todos(estudiantes: Estudiantes) -> list[ResumenEstudiante]:
    """R — Retorna lista ordenada alfabéticamente."""
    return [
        construir_resumen(nombre, notas)
        for nombre, notas in sorted(estudiantes.items())
    ]


def actualizar_notas(
    estudiantes: Estudiantes,
    nombre: str,
    notas_nuevas: list[float],
) -> tuple[bool, str]:
    """U — Reemplaza notas. Retorna (éxito, mensaje)."""
    if nombre not in estudiantes:
        return False, f"'{nombre}' no existe."
    if not notas_nuevas:
        return False, "La lista de notas nueva no puede estar vacía."

    estudiantes[nombre] = notas_nuevas
    return True, f"Notas de '{nombre}' actualizadas ({len(notas_nuevas)} nota(s))."


def eliminar_estudiante(
    estudiantes: Estudiantes,
    nombre: str,
) -> tuple[bool, str]:
    """D — Elimina. Retorna (éxito, mensaje)."""
    if nombre not in estudiantes:
        return False, f"'{nombre}' no existe."

    del estudiantes[nombre]
    return True, f"'{nombre}' eliminado correctamente."
