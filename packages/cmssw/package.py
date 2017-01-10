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
#     spack install cmssw
#
# You can edit this file again by typing:
#
#     spack edit cmssw
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from glob import glob
from string import Template
import os.path

class Cmssw(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://cms-sw.github.io"
    url      = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_0_0_pre2.tar.gz"

    version('9.0.0.pre2', '070cc64e73a3a3ac5def459a3037c23d')

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
#    depends_on('sigcpp')
    depends_on('xrootd')
    depends_on('xz')
    depends_on('zlib')
#    depends_on('db6')
#    depends_on('davix')
#    depends_on('gdbm')


    def install(self, spec, prefix):
        scram=which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        scram_version='V'+str(spec['scram'].version)
	values = {}
        values['ROOT_VER']=str(spec['root'].version)
        values['DB6_VER']=str(spec['db6'].version)
        values['ROOT_PREFIX']=str(spec['root'].prefix)
        values['DB6_PREFIX']=str(spec['db6'].prefix)


        with working_dir(build_directory, create=True):
            ln=which('ln')
            rsync=which('rsync')
            mkdir('config')
            rsync('-au', '--exclude', '.git', source_directory+'/config/','config/')
            ln('-s', source_directory,'src')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            mkdir('tools')
            rsync('-au', '--exclude', '.git', source_directory+'/tools/','tools/')
            xmlfiles = glob(join_path('tools','*','*.xml.tmpl'))
            for xmlfile in xmlfiles:
                print xmlfile
                fin = open(xmlfile,'r')
                tmpl = Template( fin.read() )
                res = tmpl.substitute(values)
                outfile = os.path.splitext(xmlfile)[0]
                print outfile
                fout = open(outfile,'w')
                fout.write(res)
                fout.close() 
                fin.close()
            
            perl=which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CMSSW', 
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', 'tools',
                 '--keys', 'SCRAM_COMPILER=gcc', 
                 '--keys', 'PROJECT_GIT_HASH='+cmssw_u_version,
                 '--arch', 'osx1011_amd64_gcc540')
            scram('-a','osx1011_amd64_gcc540', 'project','-b','config/bootsrc.xml')
        with working_dir(join_path(build_directory,cmssw_u_version),create=False):
            scram('-a', 'osx1011_amd64_gcc540', 'build', '-v', '-k', '-j4')
        with working_dir(join_path(prefix,cmssw_u_version),create=True):
            rsync=which('rsync')
            rsync('-au',build_directory+'/'+cmssw_u_version+'/','./')    

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "https://github.com/cms-sw/cmssw/archive/CMSSW_%s.tar.gz" % version_underscore

