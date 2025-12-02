"""
Stub simple del módulo `pwd` para entornos Windows.

Algunas dependencias de `langchain_community` intentan importar `pwd`,
que solo existe en sistemas tipo Unix. Este archivo evita que falle el
`import pwd` en Windows. No se usa directamente en tu proyecto.
"""

import getpass
import os
from dataclasses import dataclass


@dataclass
class struct_passwd:
    pw_name: str
    pw_dir: str


def getpwuid(uid: int) -> struct_passwd:  # type: ignore[override]
    """
    Devuelve un objeto mínimo similar a pwd.struct_passwd.
    Solo se usa si alguna librería llama a pwd.getpwuid en Windows.
    """
    return struct_passwd(
        pw_name=getpass.getuser(),
        pw_dir=os.path.expanduser("~"),
    )


def getpwnam(name: str) -> struct_passwd:  # type: ignore[override]
    """
    Versión mínima de pwd.getpwnam para evitar errores si se llama.
    """
    return struct_passwd(
        pw_name=name,
        pw_dir=os.path.expanduser("~"),
    )


