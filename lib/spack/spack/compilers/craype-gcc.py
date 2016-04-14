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

class CraypeGcc(Compiler):
    cray_wrapper = 'gnu'
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

    suffixes = [r'-mp-\d\.\d', r'-\d\.\d', r'-\d']

    @classmethod
    def cc_version(cls, cc):
        if CrayWrapper._detect_wrapper(cc, r'(Usage: cc \[options\] file)\.*'):
            return get_compiler_version(
                cc, '--version',
                r'gcc \(GCC\) (\d+\.\d+(?:\.\d+)?)')

    @classmethod
    def cxx_version(cls, cxx):
        if CrayWrapper._detect_wrapper(cxx, r'(Usage: CC \[options\] file)\.*'):
            return get_compiler_version(
                cxx, '--version',
                r'g\+\+ \(GCC\) (\d+\.\d+(?:\.\d+)?)')
