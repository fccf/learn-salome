# compile
```
./build.sh

```

# salome
```python
context.setVariable(r"SALOME_MODULES", r"APP,GEOM,SMESH,HEXABLOCK,HOMARD,MED,PARAVIS,JOBMANAGER,YACS,CALCULATOR,fish_app", overwrite=True)

#[fish_app]
context.setVariable(r"fish_app_ROOT_DIR", r"/home/superfun/fc/salome_app/app/fish_app", overwrite=True)
context.setVariable(r"fish_app_SRC_DIR", r"/home/superfun/fc/salome_app/src/fish_app", overwrite=True)
context.addToPath(r"${fish_app_ROOT_DIR}/bin/salome")
context.addToLdLibraryPath(r"${fish_app_ROOT_DIR}/lib/salome")
context.addToPythonPath(r"${fish_app_ROOT_DIR}/bin/salome:${fish_app_ROOT_DIR}/lib/salome:${fish_app_ROOT_DIR}/${PYTHON_LIBDIR0}/salome:${fish_app_ROOT_DIR}/${PYTHON_LIBDIR1}/salome")
```
