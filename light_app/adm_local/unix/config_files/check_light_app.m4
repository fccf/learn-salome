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

AC_DEFUN([CHECK_light_app],[

AC_CHECKING(for light_app)

light_app_ok=no

light_app_LDFLAGS=""
light_app_CXXFLAGS=""

AC_ARG_WITH(gui,
	    --with-py-light=DIR root directory path of light_app installation,
	    light_app_DIR="$withval",light_app_DIR="")

if test "x$light_app_DIR" = "x" ; then

# no --with-light option used

  if test "x$light_app_ROOT_DIR" != "x" ; then

    # light_app_ROOT_DIR environment variable defined
    LIGHT_DIR=$light_app_ROOT_DIR

  else

    # search light_app binaries in PATH variable
    AC_PATH_PROG(TEMP, light_appGUI.py)
    if test "x$TEMP" != "x" ; then
      light_app_BIN_DIR=`dirname $TEMP`
      light_app_DIR=`dirname $light_app_BIN_DIR`
    fi

  fi
#
fi

if test -f ${light_app_DIR}/lib/salome/light_appGUI.py  ; then
  light_app_ok=yes
  AC_MSG_RESULT(Using light_app distribution in ${light_app_DIR})

  if test "x$light_app_ROOT_DIR" == "x" ; then
    light_app_ROOT_DIR=${light_app_DIR}
  fi
  AC_SUBST(light_app_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled light_app distribution")
fi
  
AC_MSG_RESULT(for light_app: $light_app_ok)
 
])dnl
 
