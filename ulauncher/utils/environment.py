"""
Module for detecting the display protocol.

These constants are in a standalone module to minimize the dependencies so that
ulauncher.utils.xinit can safely use it.
"""

from __future__ import annotations

import csv
import logging
import os
import pathlib
from typing import Literal

logger = logging.getLogger()

GDK_BACKEND = os.environ.get("GDK_BACKEND", "").upper()
XDG_SESSION_TYPE = os.environ.get("XDG_SESSION_TYPE", "").upper()
DESKTOP_NAME = os.environ.get("XDG_CURRENT_DESKTOP", "").upper() or "Unknown Desktop"
DISTRO = "Unknown Distro"
DESKTOP_ID: Literal["GNOME", "XFCE", "PLASMA"] | None = None
IS_X11 = XDG_SESSION_TYPE == "X11"
# This means either X11 or XWayland
IS_X11_COMPATIBLE = IS_X11 or (GDK_BACKEND and GDK_BACKEND.startswith("X11"))

if "XFCE" in DESKTOP_NAME:
    DESKTOP_ID = "XFCE"
elif "GNOME" in DESKTOP_NAME or "PANTHEON" in DESKTOP_NAME:
    DESKTOP_ID = "GNOME"
elif "KDE" in DESKTOP_NAME:
    DESKTOP_ID = "PLASMA"

try:
    with open(pathlib.Path("/etc/os-release")) as stream:
        reader = csv.reader(stream, delimiter="=")
        DISTRO = dict(reader).get("PRETTY_NAME", DISTRO)
except (FileNotFoundError, ValueError):
    logger.info("Distro does not provide any version info")
