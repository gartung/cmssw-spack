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

class Cmssw(Package):
    """CMSSW"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://cms-sw.github.io"
    url      = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_0_0_pre2.tar.gz"

    version('9.0.X',git='https://github.com/cms-sw/cmssw.git',branch='CMSSW_9_0_X')

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

    depends_on('scram')
    depends_on('gmake')
    depends_on('root')
    depends_on('tbb')
    depends_on('tinyxml')
    depends_on('clhep')
    depends_on('md5')
    depends_on('python')
    depends_on('vdt')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('boost')
    depends_on('bzip2')
    depends_on('clhep')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('giflib')
    depends_on('libuuid')
    depends_on('libxml2')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('xz')
    depends_on('zlib')


    def install(self, spec, prefix):
        scram=which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        scram_version='V'+str(spec['scram'].version)
        
        gcc=which(spack_cc)
        if spec.satisfies('%clang') and self.compiler.is_apple:
            gcc_prefix='/usr'
            gcc_machine=''
        else:
            gcc_prefix=re.sub('/bin/.*$','',self.compiler.cc)
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
        values['GMAKE_VER']=str(spec['gmake'].version)
        values['GMAKE_PREFIX']=str(spec['gmake'].prefix)
        values['FWLITEDATA_VER']='V07-05-01-cms'
        values['FWLITEDATA_PREFIX']='/Users/gartung/CMSSW/osx1011_amd64_gcc540/cms'
        values['SELF_LIB']=build_directory+'/'+cmssw_u_version+'/lib/osx1011_amd64_gcc540'
        values['SELF_INC']=build_directory+'/'+cmssw_u_version+'/src'

        with working_dir(build_directory, create=True):
            md=which('mkdir')
            rsync=which('rsync')
            md('-p','src')
            rsync('-au', '--exclude', '.git', '--exclude', 'config',
                  '--exclude', 'tools', '--exclude', 'spack-build.*',
                  source_directory+'/','src/')
            md('-p','config')
            rsync('-au', '--exclude', '.git', 
                  source_directory+'/config/','config/')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            md('-p','tools')
            rsync('-au', '--exclude', '.git', source_directory+'/tools/','tools/')
            xmlfiles = glob(join_path('tools','selected','*.xml'))
            for xmlfile in xmlfiles:
                print xmlfile
                fin = open(xmlfile,'r')
                tmpl = Template( fin.read() )
                fin.close()
                res = tmpl.substitute(values)
                print res
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
                 '--arch', 'osx1011_amd64_gcc540')
            curl=which('curl')
            curl('-O', 'https://raw.githubusercontent.com/cms-sw/cmsdist/IB/CMSSW_9_0_X/gcc530/fwlite_build_set.file')
            fin='config/bootsrc.xml'
            matchexp=re.compile(r"(\s*\<download.*)(file:src)(.*)(name=\"src)(\"/\>)")
            lines = [line.rstrip('\n') for line in open(fin,'r')]
            fout=open(fin,'w')
            print fin
            for line in lines:
                mobj=matchexp.match(line)
                if mobj:
                    replacement='#'+line+'\n'
                    print replacement
                    fout.write(replacement)
		    reps = [line.rstrip('\n') for line in open('fwlite_build_set.file','r')]
		    for rep in reps:
                         replacement=mobj.group(1)+mobj.group(2)+'/'+rep+mobj.group(3)+mobj.group(4)+'/'+rep+mobj.group(5)+'\n'
                         print replacement
                         fout.write(replacement)
                else:
                    replacement=line+'\n'
                    print replacement
                    fout.write(replacement)
            fout.close()
            scram('-a','osx1011_amd64_gcc540', 'project','-b','config/bootsrc.xml')
        with working_dir(join_path(build_directory,cmssw_u_version),create=False):
            scram('-a', 'osx1011_amd64_gcc540', 'build', '-v', '-k')
        with working_dir(join_path(prefix,cmssw_u_version),create=True):
            rsync=which('rsync')
            rsync('-au',build_directory+'/'+cmssw_u_version+'/','./')    
            scram=which('scram')
            scram('-a', 'osx1011_amd64_gcc540', 'build', '-v', 'ProjectRename')

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "https://github.com/cms-sw/cmssw/archive/CMSSW_%s.tar.gz" % version_underscore

