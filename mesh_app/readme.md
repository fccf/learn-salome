# introduce

输出elmer格式的网格以及坐标文件，输出位置为当前 study 所在的目录。

```python
# 当前 study 所在的目录
os.path.dirname(salome.myStudy._get_URL())

```

# compile
```
./build.sh

```

# salome
```python
context.setVariable(r"SALOME_MODULES", r"APP,GEOM,SMESH,HEXABLOCK,HOMARD,MED,PARAVIS,JOBMANAGER,YACS,CALCULATOR,mesh_app", overwrite=True)

#[mesh_app]
context.setVariable(r"mesh_app_ROOT_DIR", r"/home/superfun/fc/salome_app/app/mesh_app", overwrite=True)
context.setVariable(r"mesh_app_SRC_DIR", r"/home/superfun/fc/salome_app/src/mesh_app", overwrite=True)
context.addToPath(r"${mesh_app_ROOT_DIR}/bin/salome")
context.addToLdLibraryPath(r"${mesh_app_ROOT_DIR}/lib/salome")
context.addToPythonPath(r"${mesh_app_ROOT_DIR}/bin/salome:${mesh_app_ROOT_DIR}/lib/salome:${mesh_app_ROOT_DIR}/${PYTHON_LIBDIR0}/salome:${mesh_app_ROOT_DIR}/${PYTHON_LIBDIR1}/salome")
```
