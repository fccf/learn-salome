# Copyright (C) 2009-2016  OPEN CASCADE
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

#  Author : Roman NIKOLAEV Open CASCADE S.A.S. (roman.nikolaev@opencascade.com)
#  Date   : 13/04/2009

#------------------------------------------------------------

AC_DEFUN([CHECK_mesh_app],[

AC_CHECKING(for mesh_app)

mesh_app_ok=no

mesh_app_LDFLAGS=""
mesh_app_CXXFLAGS=""

AC_ARG_WITH(gui,
	    --with-py-light=DIR root directory path of mesh_app installation,
	    mesh_app_DIR="$withval",mesh_app_DIR="")

if test "x$mesh_app_DIR" = "x" ; then

# no --with-light option used

  if test "x$mesh_app_ROOT_DIR" != "x" ; then

    # mesh_app_ROOT_DIR environment variable defined
    LIGHT_DIR=$mesh_app_ROOT_DIR

  else

    # search mesh_app binaries in PATH variable
    AC_PATH_PROG(TEMP, mesh_appGUI.py)
    if test "x$TEMP" != "x" ; then
      mesh_app_BIN_DIR=`dirname $TEMP`
      mesh_app_DIR=`dirname $mesh_app_BIN_DIR`
    fi

  fi
#
fi

if test -f ${mesh_app_DIR}/lib/salome/mesh_appGUI.py  ; then
  mesh_app_ok=yes
  AC_MSG_RESULT(Using mesh_app distribution in ${mesh_app_DIR})

  if test "x$mesh_app_ROOT_DIR" == "x" ; then
    mesh_app_ROOT_DIR=${mesh_app_DIR}
  fi
  AC_SUBST(mesh_app_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled mesh_app distribution")
fi
  
AC_MSG_RESULT(for mesh_app: $mesh_app_ok)

])dnl
