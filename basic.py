#!/usr/bin/env python3
# -*- coding; utf-8 -*-

import sys
import os
from subprocess import call

arquivo, extensao = os.path.splitext(sys.argv[1])
if extensao != ".bpp":
    raise Exception("Arquivo com extensao inválida! Use .bpp")

path = ""
if "/" in arquivo:
    path = arquivo[:arquivo.rfind("/")+1]
    arquivo = arquivo[arquivo.rfind("/")+1:]

call("python " + "sintax.py " + f"{path}{arquivo}{extensao}", shell=True)

isempty = os.stat(f"./logs/erros_{arquivo}.txt").st_size == 0

if(isempty):
    call("python " + f"{arquivo}.py", shell=True)
else:
    print("(!) Erros sintáticos encontrados.")
    sys.exit(0)