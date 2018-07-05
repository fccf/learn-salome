
INCLUDE(UseQtExt)

# additional include directories
INCLUDE_DIRECTORIES(
  ${QT_INCLUDES}
)

# --- scripts ---

# scripts / static
SET(_bin_SCRIPTS
  export_salome_mesh.py
  mesh_appGUI.py
)

# --- resources ---

# --- rules ---

SALOME_INSTALL_SCRIPTS("${_bin_SCRIPTS}" ${SALOME_INSTALL_SCRIPT_PYTHON})
