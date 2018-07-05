app_name_=mesh_app
salome_root_dir_=/home/superfun/fc/SALOME-8.4.0
salome_app_root_dir_=/home/superfun/fc/salome_app
salome_app_install_dir_=$salome_app_root_dir_/app

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
