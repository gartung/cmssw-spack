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


class Fwlite(Package):
    """CMSSW FWLite"""

    homepage = "http://cms-sw.github.io"
    url      = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_0_0_pre2.tar.gz"

#    version('9.0.X',git='https://github.com/gartung/cmssw.git',branch='CMSSW_9_0_X')
    version('9.0.X',git='https://github.com/gartung/cmssw.git',branch='macos-clang-fixes')

    config_tag='V05-05-20'

    resource(name='config',
             git='https://github.com/cms-sw/cmssw-config.git',
             tag=config_tag,
             destination='',
             placement='config'
    )
    
    resource(name='toolbox',
             git='https://github.com/gartung/scram-tool-templ.git',
             destination='',
             placement='tools'
    )

    depends_on('gcc~binutils')
    depends_on('scram')
    depends_on('gmake')
    depends_on('root')
    depends_on('tbb')
    depends_on('tinyxml')
    depends_on('clhep')
    depends_on('md5')
    depends_on('python')
    depends_on('vdt')
    depends_on('boost+python')
    depends_on('libuuid')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('bzip2')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('libpng')
    depends_on('giflib')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('xz')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('bzip2')
    depends_on('cfe-bindings')
    depends_on('fireworks-data')


    def install(self, spec, prefix):
        scram=which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        scram_version='V'+str(spec['scram'].version)
        
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
        values['LIBUUID_VER']=str(spec['libuuid'].version)
        values['LIBUUID_PREFIX']=str(spec['libuuid'].prefix)
        values['LIBUNGIF_VER']=str(spec['giflib'].version)
        values['LIBUNGIF_PREFIX']=str(spec['giflib'].prefix)
        values['LIBTIFF_VER']=str(spec['libtiff'].version)
        values['LIBTIFF_PREFIX']=str(spec['libtiff'].prefix)
        values['LIBPNG_VER']=str(spec['libpng'].version)
        values['LIBPNG_PREFIX']=str(spec['libpng'].prefix)
        values['LIBJPEG_VER']=str(spec['jpeg'].version)
        values['LIBJPEG_PREFIX']=str(spec['jpeg'].prefix)
        values['HEPMC_VER']=str(spec['hepmc'].version)
        values['HEPMC_PREFIX']=str(spec['hepmc'].prefix)
        values['GSL_VER']=str(spec['gsl'].version)
        values['GSL_PREFIX']=str(spec['gsl'].prefix)
        values['CLHEP_VER']=str(spec['clhep'].version)
        values['CLHEP_PREFIX']=str(spec['clhep'].prefix)
        values['BZ2_VER']=str(spec['bzip2'].version)
        values['BZ2_PREFIX']=str(spec['bzip2'].prefix)
        values['CFE_VER']=str(spec['cfe-bindings'].version)
        values['CFE_PREFIX']=str(spec['cfe-bindings'].prefix)
        values['GMAKE_VER']=str(spec['gmake'].version)
        values['GMAKE_PREFIX']=str(spec['gmake'].prefix)
        values['CPPUNIT_VER']=str(spec['cppunit'].version)
        values['CPPUNIT_PREFIX']=str(spec['cppunit'].prefix)
        values['FWLITEDATA_VER']=str(spec['fireworks-data'].version)
        values['FWLITEDATA_PREFIX']=str(spec['fireworks-data'].prefix)
        values['SELF_LIB']=prefix+'/'+cmssw_u_version+'/lib/osx1012_amd64_clang8'
        values['SELF_INC']=prefix+'/'+cmssw_u_version+'/src'

        with working_dir(build_directory, create=True):
            md=which('mkdir')
            rsync=which('rsync')
            md('-p','src')
            rsync('-a', '--exclude', '.git', '--exclude', 'config',
                  '--exclude', 'tools', '--exclude', 'spack-build.*',
                  source_directory+'/','src/')
            md('-p','config')
            rsync('-a', '--exclude', '.git', 
                  source_directory+'/config/','config/')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            md('-p','tools')
            rsync('-a', '--exclude', '.git', source_directory+'/tools/','tools/')
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
                 '-p', 'CMSSW', 
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc', 
                 '--keys', 'PROJECT_GIT_HASH='+cmssw_u_version,
                 '--arch', 'osx1012_amd64_clang8')
            fin='config/bootsrc.xml'
            matchexp=re.compile(r"(\s*\<download.*)(file:src)(.*)(name=\"src)(\"/\>)")
            lines = [line.rstrip('\n') for line in open(fin,'r')]
            fout=open(fin,'w')
            for line in lines:
                mobj=matchexp.match(line)
                if mobj:
                    replacement='#'+line+'\n'
                    fout.write(replacement)
                    reps = [line.rstrip('\n') for line in open('tools/fwlite_build_set.file','r')]
                    for rep in reps:
                         replacement=mobj.group(1)+mobj.group(2)+'/'+rep+mobj.group(3)+mobj.group(4)+'/'+rep+mobj.group(5)+'\n'
                         fout.write(replacement)
                else:
                    replacement=line+'\n'
                    fout.write(replacement)
            fout.close()
            scram('project','-d', prefix, '-b', 'config/bootsrc.xml')

    
        with working_dir(join_path(prefix,cmssw_u_version),create=False):
            rm=which('rm')
            matches = []
            matches.append('src/CommonTools/Utils/src/TMVAEvaluator.cc')
            matches.append('src/FWCore/MessageLogger/python/MessageLogger_cfi.py')
            matches.append('src/CommonTools/Utils/plugins/GBRForestWriter.cc')
            for f in glob('src/*/*/test/BuildFile.xml'):
                matches.append(f)
            for m in matches: 
                rm('-v',m,output=str)
            scram('build', '-v','-k','-j4')
            rm('-r', 'tmp')
            rm('external/osx1012_amd64_clang8/lib/libJPEG.dylib')
            rm('external/osx1012_amd64_clang8/lib/libPng.dylib')
            rm('external/osx1012_amd64_clang8/lib/libTIFF.dylib')
            rm('external/osx1012_amd64_clang8/lib/libGIF.dylib')
            mv=which('mv')
            md=which('mkdir')
            md('-p','external/osx1012_amd64_clang8/data/Fireworks/Geometry/data')
            matches = []
            for f in glob('external/osx1012_amd64_clang8/data/*.root'):
                matches.append(f)
            for m in matches: 
                mv(m,'external/osx1012_amd64_clang8/data/Fireworks/Geometry/data')
             
            


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/osx1012_amd64_clang8')


    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "https://github.com/cms-sw/cmssw/archive/CMSSW_%s.tar.gz" % version_underscore
