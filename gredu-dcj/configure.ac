#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT(gredu-dcj, 1.0, aks7832@psu.edu)
AM_INIT_AUTOMAKE([tar-pax])
AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.
AS_IF([test "s$BOOST_HOME" = "s"],[AC_MSG_ERROR([*** Please set environment variable BOOST_HOME ***])]) 

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 src/Makefile])

AC_OUTPUT
