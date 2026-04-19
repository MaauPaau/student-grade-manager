"""
data.py — Capa de persistencia
================================
Solo lee y escribe en disco. Sin lógica, sin prints de negocio.
"""

import json
import os

ARCHIVO_DATOS = "estudiantes.json"

# Tipo concreto: el diccionario siempre es str → list[float]
Estudiantes = dict[str, list[float]]


def cargar_datos(ruta: str = ARCHIVO_DATOS) -> Estudiantes:
    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"⚠  '{ruta}' está corrupto. Se inicia con datos vacíos.")
        return {}
    except OSError as e:
        print(f"⚠  No se pudo leer '{ruta}': {e}")
        return {}


def guardar_datos(estudiantes: Estudiantes, ruta: str = ARCHIVO_DATOS) -> bool:
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(estudiantes, f, indent=2, ensure_ascii=False)
        return True
    except OSError as e:
        print(f"⚠  No se pudo guardar en '{ruta}': {e}")
        return False
