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
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys
import shutil

def relrelink(top):
    for root, dirs, files in os.walk(top,topdown=False):
       for x in files:
           p = os.path.join(root,x)
           f = os.path.abspath(p)
           if os.path.islink(f):
               linkto=os.path.realpath(f)
               if not os.path.commonprefix((f,linkto)) == '/':
                   rel=os.path.relpath(linkto,start=os.path.dirname(f))
                   os.remove(p)
                   os.symlink(rel, p)
       for y in dirs:
           p = os.path.join(root,y)
           f = os.path.abspath(p)
           if os.path.islink(f):
               linkto=os.path.realpath(f)
               if not os.path.commonprefix((f,linkto)) == '/':
                   rel=os.path.relpath(linkto,start=os.path.dirname(f))
                   os.remove(p)
                   os.symlink(rel, p)

class Coral(Package):
    """CORAL built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/coral/CORAL_2_3_21/src.tar.gz"

    version('2.3.21','cad0b744fd18efc3a4aa045dc266fdb3')

    config_tag='V05-05-56'

    resource(name='scram-config',
             git='https://github.com/gartung/cmssw-config.git',
             branch='macos',
             destination='.',
             placement='scram-config'
    )
    
    resource(name='toolbox',
             git='https://github.com/gartung/scram-tool-templ.git',
             commit='a92faa1',
             destination='.',
             placement='scram-tool-templ'
    )

    depends_on('scram')
    depends_on('gmake')
    depends_on('root@6.10.08^python+shared^fftw~mpi')
    depends_on('tbb')
    depends_on('tinyxml^boost+python+shared^python+shared')
    depends_on('clhep@2.3.1.1~cxx11+cxx14')
    depends_on('md5')
    depends_on('python+shared')
    depends_on('vdt')
    depends_on('boost@1.63.0+python+shared^python+shared')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite@3.16.02')
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
    depends_on('libxml2^python+shared')
    depends_on('bzip2')
    depends_on('fireworks-data')
    depends_on('cmssw.llvm@4.0.1~gold~libcxx+python+shared_libs')
    depends_on('cfe-bindings@4.0.1')
    depends_on('libuuid')
    depends_on('valgrind')
    depends_on('geant4~qt')
    depends_on('expat')
    depends_on('protobuf')
    depends_on('eigen')
    depends_on('curl')
    depends_on('classlib')
    depends_on('davix')
    depends_on('gperftools')
    depends_on('meschach')
    depends_on('fastjet')
    depends_on('fftjet')
    depends_on('pythia6')
    depends_on('pythia8')
    depends_on('oracle')
    depends_on('frontier-client')

    def install(self, spec, prefix):
        scram=which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version='CORAL.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        scram_version='V'+str(spec['scram'].version)
        project_dir=join_path(prefix,cmssw_u_version)
        
        gcc=which(spack_f77)
        gcc_prefix=re.sub('/bin/.*$','',self.compiler.f77)
        gcc_machine=gcc('-dumpmachine',output=str)
        gcc_ver=gcc('-dumpversion',output=str)

        values = {}
        values['SELF_LIB']=project_dir+'/lib/'+str(spec.architecture)
        values['SELF_INC']=project_dir+'/src'
        values['GCC_VER']=gcc_ver.rstrip()
        values['GCC_PREFIX']=gcc_prefix
        values['GCC_MACHINE']=gcc_machine.rstrip()
        values['ROOT_VER']=str(spec['root'].version)
        values['ROOT_PREFIX']=str(spec['root'].prefix)
        values['XROOTD_VER']=str(spec['xrootd'].version)
        values['XROOTD_PREFIX']=str(spec['xrootd'].prefix)
        values['BOOST_VER']=str(spec['boost'].version)
        values['BOOST_PREFIX']=str(spec['boost'].prefix)
        values['TBB_VER']=str(spec['tbb'].version)
        values['TBB_PREFIX']=str(spec['tbb'].prefix)
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
        values['CFE_VER']=str(spec['cfe-bindings'].version)
        values['CFE_PREFIX']=str(spec['cfe-bindings'].prefix)
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
        values['FWLITEDATA_VER']=str(spec['fireworks-data'].version)
        values['FWLITEDATA_PREFIX']=str(spec['fireworks-data'].prefix)
        values['VALGRIND_VER']=str(spec['valgrind'].version)
        values['VALGRIND_PREFIX']=str(spec['valgrind'].prefix)
        values['GEANT4CORE_VER']=str(spec['geant4'].version)
        values['GEANT4CORE_PREFIX']=str(spec['geant4'].prefix)
        values['GEANT4_VER']=str(spec['geant4'].version)
        values['GEANT4_PREFIX']=str(spec['geant4'].prefix)
        values['GOOGLE_PERFTOOLS_VER']=str(spec['gperftools'].version)
        values['GOOGLE_PERFTOOLS_PREFIX']=str(spec['gperftools'].prefix)
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

        with working_dir(build_directory, create=True):
            rsync=which('rsync')
            mkdirp('src')
            rsync('-a', '--exclude', '.git', '--exclude', 'scram-config',
                  '--exclude', 'scram-tool-templ', '--exclude', 'spack-build.*',
                  source_directory+'/','src/')
            mkdirp('config')
            rsync('-a', '--exclude', '.git', 
                  source_directory+'/scram-config/','config/')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            mkdirp('tools')
            rsync('-a', '--exclude', '.git', source_directory+'/scram-tool-templ/','tools/')
            xmlfiles = glob(join_path('tools','selected','*.xml'))
            for xmlfile in xmlfiles:
                fin = open(xmlfile,'r')
                tmpl = Template( fin.read() )
                fin.close()
                res = tmpl.substitute(values)
                fout = open(xmlfile,'w')
                fout.write(res)
                fout.close() 
            perl=which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CORAL', 
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc', 
                 '--keys', 'PROJECT_GIT_HASH='+cmssw_u_version,
                 '--arch', str(spec.architecture))
            scram('project','-d', prefix, '-b', 'config/bootsrc.xml')


        with working_dir(project_dir,create=False):
            matches = []

            for f in glob('src/*/*/test/BuildFile*'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)

            scram.add_default_env('LOCALTOP', project_dir)
            scram.add_default_env('CORAL_BASE', project_dir)
            scram.add_default_env('LD_LIBRARY_PATH', project_dir+'/lib/'+str(self.spec.architecture))
            scram('build', '-v', '-k', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')
           


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version='CORAL_'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('CORAL_RELEASE_BASE', self.prefix)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+str(self.spec.architecture))


    def setup_environment(self, spack_env, run_env):
        cmssw_version='CORAL.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+str(self.spec.architecture))

    def url_for_version(self, version):
        """Handle CORAL's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/coral/CORAL_%s/src.tar.gz" % version_underscore
