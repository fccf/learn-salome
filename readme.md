# salome
[salome](http://www.salome-platform.org/)是由法国CEA,EDF开发的基于CAD的前后处理平台，其中集成了许多常用的CAE开源软件，主要模块如下

| 主要模块        | 功能            | 集成工具        |
| :------------- | :------------- |:------------- |
| Geometry       | 建立或导入CAD模型 | OpenCASCADE  |
| Mesh           | 网格剖分         | Tetgen, Gmsh ..|
| ParaVis        | 后处理           | ParaView     |
| Med            | 数据交换         |  ...         |


# salome app
salome是一个使用C和python等语言编写的平台，可以基于该平台编写自己的app。

# first app
参考 pyhello 模块，编写自己的 app。复制$SALOME_ROOT/SOURCES/PYHELLO到一个工作文件夹中，将所有的PYHELLO改为first_app，然后根据以下过程进行编译以及集成。

# 编译
salome使用cmake进行编译，编译自己的app时，需要预先加载salome环境以及指定环境变量 CONFIGURATION_ROOT_DIR
``` bash
source $SALOME_ROOT/env_launch.sh
export CONFIGURATION_ROOT_DIR=$SALOME_ROOT/SOURCES/CONFIGURATION/
```

然后通过cmake编译
```bash
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR ..
```

建立一个build.sh脚本进行编译,

```bash
app_name_=first_app
salome_root_dir_=
salome_first_app_ROOT_DIR_=
salome_app_install_dir_=$salome_first_app_ROOT_DIR_/app

source $salome_root_dir_/env_launch.sh
export CONFIGURATION_ROOT_DIR=$salome_root_dir_/SOURCES/CONFIGURATION/

if [[ ! -d "./build/" ]]; then
  #statements
  mkdir build
else
  rm -rf build
  mkdir build
fi
cd build
cmake -DCMAKE_INSTALL_PREFIX=$salome_app_install_dir_/$app_name_ ..
make
make install
cd ..
rm -rf build
```

# 集成
**新建应用的名称需要小写，大写不能集成到salome中，不知道为什么？可能是个bug？**
编译完成之后，需要将编译好的app集成到salome中， 修改 $SALOME_ROOT 中的 salome.py，设置环境变量。
```python
context.setVariable(r"SALOME_MODULES", r"APP,GEOM,SMESH,HEXABLOCK,HOMARD,MED,PARAVIS,JOBMANAGER,YACS,CALCULATOR,first_app", overwrite=True)

#[FIRST]
context.setVariable(r"first_app_ROOT_DIR", r"INSTALL_DIR", overwrite=True)
context.setVariable(r"APP_SRC_DIR", r"SRC_DIR", overwrite=True)
context.addToPath(r"${first_app_ROOT_DIR}/bin/salome")
context.addToLdLibraryPath(r"${first_app_ROOT_DIR}/lib/salome")
context.addToPythonPath(r"${first_app_ROOT_DIR}/bin/salome:${first_app_ROOT_DIR}/lib/salome:${first_app_ROOT_DIR}/${PYTHON_LIBDIR0}/salome:${first_app_ROOT_DIR}/${PYTHON_LIBDIR1}/salome")
```
其中 APP 是应用的名称， INSTALL_DIR 代表安装的位置， SRC_DIR 是源码的位置。
