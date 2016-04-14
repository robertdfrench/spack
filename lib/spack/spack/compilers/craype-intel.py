##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.compiler import *

class CraypeIntel(Compiler):
    cray_wrapper = 'intel'
    # Subclasses use possible names of C compiler
    cc_names = ['cc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['CC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ftn']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ftn']

    # Named wrapper links within spack.build_env_path
    link_paths = { 'cc'  : 'craype/cc',
                   'cxx' : 'case-insensitive/CC',
                   'f77' : 'craype/ftn',
                   'fc'  : 'craype/ftn' }

    @property
    def cxx11_flag(self):
        if self.version < ver('11.1'):
            tty.die("Only intel 11.1 and above support c++11.")
        elif self.version < ver('13'):
            return "-std=c++0x"
        else:
            return "-std=c++11"


    @classmethod
    def default_version(cls, comp):
        """The '-help' option of cray wrapper cc returns:
            'Usage: cc [options] file...'

           The '--version' option seems to be the most consistent one
           for intel compilers.  Output looks like this::

               icpc (ICC) 12.1.5 20120612
               Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.

           or::

               ifort (IFORT) 12.1.5 20120612
               Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.
        """
        compiler = Executable(comp)
        output = compiler('-help', output=str, error=str)

        match = re.search(r'(Usage: cc|CC|ftn \[options\] file)\.*.*', output)
        if match.group(0) is not None:
            return get_compiler_version(
                comp, '--version', r'\((?:IFORT|ICC)\) ([^ ]+)')
        else:
            return 'unknown'


