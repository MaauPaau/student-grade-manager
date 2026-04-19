"""
service.py — Capa de servicio
==============================
Orquesta lógica + persistencia.
La UI solo llama a service — nunca importa data directamente.

Flujo:  UI → Service → Logic + Data

Ventaja: si mañana cambiamos JSON por base de datos,
         solo tocamos data.py y service.py.
         ui.py no se entera del cambio.
"""

from data import Estudiantes, cargar_datos, guardar_datos, ARCHIVO_DATOS
from logic import (
    ResumenEstudiante,
    crear_estudiante,
    leer_estudiante,
    leer_todos,
    actualizar_notas,
    eliminar_estudiante,
)


class ServicioEstudiantes:
    """
    Punto único de acceso para todas las operaciones sobre estudiantes.
    Mantiene el estado en memoria y decide cuándo persistir.

    La UI instancia esta clase y solo llama a sus métodos.
    No conoce ni data.py ni logic.py.
    """

    def __init__(self, ruta: str = ARCHIVO_DATOS) -> None:
        self._ruta: str                = ruta
        self._datos: Estudiantes       = cargar_datos(ruta)

    # ── Información ──────────────────────────────────────────

    @property
    def total(self) -> int:
        """Cantidad de estudiantes en memoria."""
        return len(self._datos)

    # ── CRUD ─────────────────────────────────────────────────

    def crear(self, nombre: str, notas: list[float]) -> tuple[bool, str]:
        ok, msg = crear_estudiante(self._datos, nombre, notas)
        if ok:
            self._guardar()
        return ok, msg

    def leer_uno(self, nombre: str) -> ResumenEstudiante | None:
        return leer_estudiante(self._datos, nombre)

    def leer_todos(self) -> list[ResumenEstudiante]:
        return leer_todos(self._datos)

    def actualizar(self, nombre: str, notas: list[float]) -> tuple[bool, str]:
        ok, msg = actualizar_notas(self._datos, nombre, notas)
        if ok:
            self._guardar()
        return ok, msg

    def eliminar(self, nombre: str) -> tuple[bool, str]:
        ok, msg = eliminar_estudiante(self._datos, nombre)
        if ok:
            self._guardar()
        return ok, msg

    def existe(self, nombre: str) -> bool:
        return nombre in self._datos

    # ── Interno ───────────────────────────────────────────────

    def _guardar(self) -> None:
        """Persiste solo cuando una operación de escritura tiene éxito."""
        guardar_datos(self._datos, self._ruta)
