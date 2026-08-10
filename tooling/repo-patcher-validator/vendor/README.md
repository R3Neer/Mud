# Dependencia Windows fijada

Este directorio contiene el wheel que usa el workflow normativo sin acceder a
PyPI durante cada validación:

```text
pyyaml-6.0.3-cp313-cp313-win_amd64.whl
SHA-256: 79005a0d97d5ddabfeeea4cf676af11e647e41d81c9a7722a193022accdb6b7c
Tamaño: 154090 bytes
Origen: https://files.pythonhosted.org/
```

Los metadatos y el digest se verificaron contra la respuesta oficial de
`https://pypi.org/pypi/PyYAML/6.0.3/json` el 2026-08-10. El instalador vuelve a
comprobar el SHA-256 antes de invocar `pip --no-index --no-deps`.

El wheel se limita deliberadamente a CPython 3.13, Windows AMD64: coincide con
`windows-latest` y `actions/setup-python`. Cambiar Python o el entorno normativo
requiere reemplazar el wheel, actualizar el digest y repetir el E2E.
