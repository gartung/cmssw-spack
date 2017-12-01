##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
#     spack install evtgen
#
# You can edit this file again by typing:
#
#     spack edit evtgen
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Evtgen(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/evtgen/evtgen-1.6.0-src.tgz"

    version('1.6.0', '6f81a213c03ed41f9a7f2e6225e42330')
    version('1.5.0', 'e979afdf58858a3f2f760594304cd9f3')

    depends_on('hepmc')
    depends_on('pythia8')
    depends_on('tauolapp')
    depends_on('photospp')

    def configures_args(self):
        args = ['--hepmcdir=%s' % self.spec['hepmc'].prefix,
                '--pythiadir=%s' % self.spec['pythia8'].prefix, 
                '--tauoladir=%s' % self.spec['tauolapp'].prefix,
                '--photosdir=%s' % self.spec['photospp'].prefix
               ]
        return args
