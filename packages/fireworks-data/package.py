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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fireworks-data
#
# You can edit this file again by typing:
#
#     spack edit fireworks-data
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from glob import glob


class FireworksData(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/cms-data/Fireworks-Geometry/archive/V07-05-01.tar.gz"

    version('07.05.01', '9f40fdf89286392d1d39d5ed52981051')
    version('07.05.02', '0277dd37c0ff7664ea733445445efb6a')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        matches=[]
        cp=which('cp')
        md=which('mkdir')
        instpath=prefix+'/data-Fireworks-Geometry/'+str(self.version)+'/Fireworks/Geometry/data/'
        md('-p',instpath)
        for f in glob('*.root'):
            matches.append(f)
        for m in matches:
            cp('-v',m,instpath,output=str)

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore=str(self.version).replace('.','-')
        return "https://github.com/cms-data/Fireworks-Geometry/archive/V%s.tar.gz" % version_underscore
