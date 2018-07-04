dnl Copyright (C) 2007-2016  CEA/DEN, EDF R&D, OPEN CASCADE
dnl
dnl Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
dnl CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
dnl
dnl This library is free software; you can redistribute it and/or
dnl modify it under the terms of the GNU Lesser General Public
dnl License as published by the Free Software Foundation; either
dnl version 2.1 of the License, or (at your option) any later version.
dnl
dnl This library is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
dnl Lesser General Public License for more details.
dnl
dnl You should have received a copy of the GNU Lesser General Public
dnl License along with this library; if not, write to the Free Software
dnl Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
dnl
dnl See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
dnl

#  Check availability of first_app binary distribution
#
#  Author : Marc Tajchman (CEA, 2002)
#------------------------------------------------------------

AC_DEFUN([CHECK_first_app],[

AC_CHECKING(for first_app)

first_app_ok=no

AC_ARG_WITH(first_app,
	    --with-py-hello=DIR root directory path of first_app installation,
	    first_app_DIR="$withval",first_app_DIR="")

if test "x$first_app_DIR" = "x" ; then

# no --with-py-hello option used

  if test "x$first_app_ROOT_DIR" != "x" ; then

    # first_app_ROOT_DIR environment variable defined
    first_app_DIR=$first_app_ROOT_DIR

  else

    # search first_app binaries in PATH variable
    AC_PATH_PROG(TEMP, first_appGUI.py)
    if test "x$TEMP" != "x" ; then
      first_app_BIN_DIR=`dirname $TEMP`
      first_app_DIR=`dirname $first_app_BIN_DIR`
    fi

  fi
#
fi

if test -f ${first_app_DIR}/bin/salome/first_appGUI.py  ; then
  first_app_ok=yes
  AC_MSG_RESULT(Using first_app distribution in ${first_app_DIR})

  if test "x$first_app_ROOT_DIR" == "x" ; then
    first_app_ROOT_DIR=${first_app_DIR}
  fi
  AC_SUBST(first_app_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled first_app distribution")
fi
  
AC_MSG_RESULT(for first_app: $first_app_ok)
 
])dnl
 
