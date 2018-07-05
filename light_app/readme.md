# compile
```
./build.sh

```

# salome
```python
context.setVariable(r"SALOME_MODULES", r"APP,GEOM,SMESH,HEXABLOCK,HOMARD,MED,PARAVIS,JOBMANAGER,YACS,CALCULATOR,light_app", overwrite=True)

#[light_app]
context.setVariable(r"light_app_ROOT_DIR", r"/home/superfun/fc/salome_app/app/light_app", overwrite=True)
context.setVariable(r"light_app_SRC_DIR", r"/home/superfun/fc/salome_app/src/light_app", overwrite=True)
context.addToPath(r"${light_app_ROOT_DIR}/bin/salome")
context.addToLdLibraryPath(r"${light_app_ROOT_DIR}/lib/salome")
context.addToPythonPath(r"${light_app_ROOT_DIR}/bin/salome:${light_app_ROOT_DIR}/lib/salome:${light_app_ROOT_DIR}/${PYTHON_LIBDIR0}/salome:${light_app_ROOT_DIR}/${PYTHON_LIBDIR1}/salome")
```
