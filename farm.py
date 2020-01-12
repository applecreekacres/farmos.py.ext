"""Main farm access."""

import farmOS
import os

HOST = None
USER = None
PASS = None

if os.path.exists("farmos.cfg"):
    with open('farmos.cfg') as cfg:
        for line in cfg.readlines():
            if line.startswith("HOST"):
                HOST = line[line.index("=")+1:].strip()
            if line.startswith("USER"):
                USER = line[line.index("=")+1:].strip()
            if line.startswith("PASS"):
                PASS = line[line.index("=")+1:].strip()
    if not HOST:
        Exception("HOST key is not defined in farmos.cfg")
    if not USER:
        Exception("USER key is not defined in farmos.cfg")
    if not PASS:
        Exception("PASS key is not defined in farmos.cfg")

FARM = farmOS.farmOS(HOST, USER, PASS)
FARM.authenticate()


def farm():
    return FARM
