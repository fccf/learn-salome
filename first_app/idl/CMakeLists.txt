# Copyright (C) 2012-2016  CEA/DEN, EDF R&D, OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

INCLUDE(UseOmniORB)  # Provided by KERNEL

INCLUDE_DIRECTORIES(
  ${OMNIORB_INCLUDE_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}
  ${KERNEL_INCLUDE_DIRS}
)

SET(SalomeIDLfirst_app_IDLSOURCES
  first_app_Gen.idl
)

SET(_idl_include_dirs
  ${KERNEL_ROOT_DIR}/idl/salome
)

SET(_idl_link_flags
  ${KERNEL_SalomeIDLKernel}
)

OMNIORB_ADD_MODULE(SalomeIDLfirst_app "${SalomeIDLfirst_app_IDLSOURCES}" "${_idl_include_dirs}" "${_idl_link_flags}")
INSTALL(TARGETS SalomeIDLfirst_app EXPORT ${PROJECT_NAME}TargetGroup DESTINATION ${SALOME_INSTALL_LIBS})
