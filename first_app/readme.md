# compile
```
./build.sh

```

# salome
```python
context.setVariable(r"SALOME_MODULES", r"APP,GEOM,SMESH,HEXABLOCK,HOMARD,MED,PARAVIS,JOBMANAGER,YACS,CALCULATOR,first_app", overwrite=True)

#[first_app]
context.setVariable(r"first_app_ROOT_DIR", r"/home/superfun/fc/salome_app/app/first_app", overwrite=True)
context.setVariable(r"first_app_SRC_DIR", r"/home/superfun/fc/salome_app/src/first_app", overwrite=True)
context.addToPath(r"${first_app_ROOT_DIR}/bin/salome")
context.addToLdLibraryPath(r"${first_app_ROOT_DIR}/lib/salome")
context.addToPythonPath(r"${first_app_ROOT_DIR}/bin/salome:${first_app_ROOT_DIR}/lib/salome:${first_app_ROOT_DIR}/${PYTHON_LIBDIR0}/salome:${first_app_ROOT_DIR}/${PYTHON_LIBDIR1}/salome")
```
