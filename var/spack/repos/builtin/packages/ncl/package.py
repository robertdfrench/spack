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


class Ncl(Package):
    """a free interpreted language designed specifically for scientific data
       processing and visualization.
    """

    homepage = "http://ncl.ucar.edu/"
    url = "https://www.earthsystemgrid.org/download/fileDownload.html?logicalFileId=5995adf7-351e-11e4-a4b4-00c0f03d5b7c"

    version('6.2.1','74a2855695bccb51b6e301383ad4818c')
    
    depends_on('jpeg')
    depends_on('zlib')
    depends_on('cairo')
    depends_on('netcdf~mpi')
    depends_on('hdf')

    def install(self, spec, prefix):
        cd("config")
        make("-f","Makefile.ini")
        ymake = Executable("./ymake")
        yamke("-config", pwd)
