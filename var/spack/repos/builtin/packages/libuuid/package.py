##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Libuuid(Package):
    """Portable uuid C library"""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://sourceforge.net/projects/libuuid/"
    url      = "http://downloads.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flibuuid%2F&ts=1433881396&use_mirror=iweb"

    version('1.0.3', 'd44d866d06286c08ba0846aba1086d68')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
