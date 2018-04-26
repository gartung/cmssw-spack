##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
#     spack install scram-tool-templ
#
# You can edit this file again by typing:
#
#     spack edit scram-tool-templ
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import re
import os
from glob import glob
from string import Template
import fnmatch


class CmsswToolConf(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    version('2.0', git='https://github.com/gartung/scram-tool-templ.git', branch='linux-link')

    depends_on('scram')
    depends_on('gmake')
    depends_on('root')
    depends_on('intel-tbb')
    depends_on('tinyxml')
    depends_on('clhep')
    depends_on('md5')
    depends_on('python')
    depends_on('vdt')
    depends_on('boost@1.63.0')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('bzip2')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('heppdt')
    depends_on('libpng')
    depends_on('giflib')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('xz')
    depends_on('libtiff')
    depends_on('libjpeg-turbo')
    depends_on('libxml2')
    depends_on('bzip2')
    depends_on('fireworks-geometry')
    depends_on('llvm')
    depends_on('uuid-cms')
    depends_on('valgrind')
    depends_on('geant4')
    depends_on('expat')
    depends_on('protobuf')
    depends_on('eigen')
    depends_on('curl')
    depends_on('classlib')
    depends_on('davix')
    depends_on('meschach')
    depends_on('fastjet')
    depends_on('fastjet-contrib')
    depends_on('fftjet')
    depends_on('pythia6')
    depends_on('pythia8')
    depends_on('oracle')
    depends_on('sqlite')
    depends_on('coral')
    depends_on('hector')
    depends_on('geant4-g4emlow')
    depends_on('geant4-g4ndl')
    depends_on('geant4-g4photonevaporation')
    depends_on('geant4-g4saiddata')
    depends_on('geant4-g4abla')
    depends_on('geant4-g4ensdfstate')
    depends_on('geant4-g4neutronsxs')
    depends_on('geant4-g4radioactivedecay')
    depends_on('libhepml')
    depends_on('lhapdf')
    depends_on('utm')
    depends_on('photospp')
    depends_on('rivet')
    depends_on('evtgen')
    depends_on('dcap')
    depends_on('tauolapp')
    depends_on('sherpa')
    depends_on('lwtnn')
    depends_on('yoda')
    depends_on('openloops')
    depends_on('qd') 
    depends_on('blackhat')
    depends_on('yaml-cpp')
    depends_on('jemalloc')
    depends_on('ktjet')
    depends_on('herwig')
    depends_on('photos')
    depends_on('tauola')
    depends_on('jimmy')
    depends_on('cascade')
    depends_on('csctrackfinderemulation')
    depends_on('mcdb')
    depends_on('fftw')
    depends_on('netlib-lapack')
    depends_on('libuuid')
    depends_on('frontier-client')

    def install(self, spec, prefix):
        gcc=which(spack_f77)
        gcc_prefix=re.sub('/bin/.*$','',self.compiler.f77)
        gcc_machine=gcc('-dumpmachine',output=str)
        gcc_ver=gcc('-dumpversion',output=str)


        values = {}
        values['GCC_VER']=gcc_ver.rstrip()
        values['GCC_PREFIX']=gcc_prefix
        values['GCC_MACHINE']=gcc_machine.rstrip()
        values['ROOT_VER']=str(spec['root'].version)
        values['ROOT_PREFIX']=str(spec['root'].prefix)
        values['XROOTD_VER']=str(spec['xrootd'].version)
        values['XROOTD_PREFIX']=str(spec['xrootd'].prefix)
        values['BOOST_VER']=str(spec['boost'].version)
        values['BOOST_PREFIX']=str(spec['boost'].prefix)
        values['TBB_VER']=str(spec['intel-tbb'].version)
        values['TBB_PREFIX']=str(spec['intel-tbb'].prefix)
        values['PYTHON_VER']=str(spec['python'].version)
        values['PYTHON_PREFIX']=str(spec['python'].prefix)
        values['XERCESC_VER']=str(spec['xerces-c'].version)
        values['XERCESC_PREFIX']=str(spec['xerces-c'].prefix)
        values['MD5_VER']=str(spec['md5'].version)
        values['MD5_PREFIX']=str(spec['md5'].prefix)
        values['TINYXML_VER']=str(spec['tinyxml'].version)
        values['TINYXML_PREFIX']=str(spec['tinyxml'].prefix)
        values['VDT_VER']=str(spec['vdt'].version)
        values['VDT_PREFIX']=str(spec['vdt'].prefix)
        values['XZ_VER']=str(spec['xz'].version)
        values['XZ_PREFIX']=str(spec['xz'].prefix)
        values['ZLIB_VER']=str(spec['zlib'].version)
        values['ZLIB_PREFIX']=str(spec['zlib'].prefix)
        values['SIGCPP_VER']=str(spec['libsigcpp'].version)
        values['SIGCPP_PREFIX']=str(spec['libsigcpp'].prefix)
        values['PCRE_VER']=str(spec['pcre'].version)
        values['PCRE_PREFIX']=str(spec['pcre'].prefix)
        values['OPENSSL_VER']=str(spec['openssl'].version)
        values['OPENSSL_PREFIX']=str(spec['openssl'].prefix)
        values['LIBXML2_VER']=str(spec['libxml2'].version)
        values['LIBXML2_PREFIX']=str(spec['libxml2'].prefix)
        values['CFE_VER']=str(spec['llvm'].version)
        values['CFE_PREFIX']=str(spec['llvm'].prefix)
        values['LIBUNGIF_VER']=str(spec['giflib'].version)
        values['LIBUNGIF_PREFIX']=str(spec['giflib'].prefix)
        values['LIBTIFF_VER']=str(spec['libtiff'].version)
        values['LIBTIFF_PREFIX']=str(spec['libtiff'].prefix)
        values['LIBPNG_VER']=str(spec['libpng'].version)
        values['LIBPNG_PREFIX']=str(spec['libpng'].prefix)
        values['LIBJPEG_VER']=str(spec['jpeg'].version)
        values['LIBJPEG_PREFIX']=str(spec['jpeg'].prefix)
        values['LIBUUID_VER']=str(spec['libuuid'].version)
        values['LIBUUID_PREFIX']=str(spec['libuuid'].prefix)
        values['HEPMC_VER']=str(spec['hepmc'].version)
        values['HEPMC_PREFIX']=str(spec['hepmc'].prefix)
        values['HEPPDT_VER']=str(spec['heppdt'].version)
        values['HEPPDT_PREFIX']=str(spec['heppdt'].prefix)
        values['GSL_VER']=str(spec['gsl'].version)
        values['GSL_PREFIX']=str(spec['gsl'].prefix)
        values['CLHEP_VER']=str(spec['clhep'].version)
        values['CLHEP_PREFIX']=str(spec['clhep'].prefix)
        values['BZ2_VER']=str(spec['bzip2'].version)
        values['BZ2_PREFIX']=str(spec['bzip2'].prefix)
        values['GMAKE_VER']=str(spec['gmake'].version)
        values['GMAKE_PREFIX']=str(spec['gmake'].prefix)
        values['CPPUNIT_VER']=str(spec['cppunit'].version)
        values['CPPUNIT_PREFIX']=str(spec['cppunit'].prefix)
        values['FWLITEDATA_VER']=str(spec['fireworks-geometry'].version)
        values['FWLITEDATA_PREFIX']=str(spec['fireworks-geometry'].prefix)
        values['VALGRIND_VER']=str(spec['valgrind'].version)
        values['VALGRIND_PREFIX']=str(spec['valgrind'].prefix)
        values['GEANT4CORE_VER']=str(spec['geant4'].version)
        values['GEANT4CORE_PREFIX']=str(spec['geant4'].prefix)
        values['GEANT4_VER']=str(spec['geant4'].version)
        values['GEANT4_PREFIX']=str(spec['geant4'].prefix)
        values['EXPAT_VER']=str(spec['expat'].version)
        values['EXPAT_PREFIX']=str(spec['expat'].prefix)
        values['LLVM_VER']=str(spec['llvm'].version)
        values['LLVM_PREFIX']=str(spec['llvm'].prefix)
        values['PROTOBUF_VER']=str(spec['protobuf'].version)
        values['PROTOBUF_PREFIX']=str(spec['protobuf'].prefix)
        values['EIGEN_VER']=str(spec['eigen'].version)
        values['EIGEN_PREFIX']=str(spec['eigen'].prefix)
        values['CURL_VER']=str(spec['curl'].version)
        values['CURL_PREFIX']=str(spec['curl'].prefix)
        values['CLASSLIB_VER']=str(spec['classlib'].version)
        values['CLASSLIB_PREFIX']=str(spec['classlib'].prefix)
        values['DAVIX_VER']=str(spec['davix'].version)
        values['DAVIX_PREFIX']=str(spec['davix'].prefix)
        values['MESCHACH_VER']=str(spec['meschach'].version)
        values['MESCHACH_PREFIX']=str(spec['meschach'].prefix)
        values['FASTJET_VER']=str(spec['fastjet'].version)
        values['FASTJET_PREFIX']=str(spec['fastjet'].prefix)
        values['FFTJET_VER']=str(spec['fftjet'].version)
        values['FFTJET_PREFIX']=str(spec['fftjet'].prefix)
        values['PYTHIA6_VER']=str(spec['pythia6'].version)
        values['PYTHIA6_PREFIX']=str(spec['pythia6'].prefix)
        values['PYTHIA8_VER']=str(spec['pythia8'].version)
        values['PYTHIA8_PREFIX']=str(spec['pythia8'].prefix)
        values['ORACLE_VER']=str(spec['oracle'].version)
        values['ORACLE_PREFIX']=str(spec['oracle'].prefix)
        values['FRONTIER_CLIENT_VER']=str(spec['frontier-client'].version)
        values['FRONTIER_CLIENT_PREFIX']=str(spec['frontier-client'].prefix)

        xmlfiles = glob('selected/*.xml')
        for xmlfile in xmlfiles:
            fin = open(xmlfile,'r')
            tmpl = Template( fin.read() )
            fin.close()
            res = tmpl.substitute(values)
            fout = open(xmlfile,'w')
            fout.write(res)
            fout.close() 

        install_tree(self.stage.source_path,prefix+'/tools')
