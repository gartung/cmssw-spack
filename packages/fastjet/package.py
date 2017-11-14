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
from spack import *


class Fastjet(AutotoolsPackage):
    """."""

    homepage = "http://www.example.com"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/fastjet/3.1.0/fastjet-3.1.0.tgz"

    version('3.1.0', 'ca865ac0dfab9910dccd0ac4bd1ae7ea')


    def configure_args(self):
        args = [
                '--enable-shared',
                '--enable-atlascone',
                '--enable-cmsiterativecone',
                '--enable-siscone',
                '--enable-allcxxplugins'
               ]
        if 'CXXFLAGS' in env and env['CXXFLAGS']:
            env['CXXFLAGS'] += ' '+ '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
        else:
            env['CXXFLAGS'] = '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
        return args
