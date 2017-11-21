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
    
    config_tag='V05-05-21'
    resource(name='scram-config',
             url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/coral/CORAL_2_3_21/%s.tar.gz'%config_tag,
             md5='cfd1645786bb86ebe61221be6c3b2b9e',
             destination='.',
             placement='scram-config'
    )

    patch('coral-CORAL_2_3_20-hide-strict-aliasing.patch')
    patch('coral-CORAL_2_3_20-boost150-fix.patch')
 

    scram_arch='linux_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch='osx10_amd64_clang'
 
    depends_on('scram')
    depends_on('gmake')
    depends_on('python+shared')
    depends_on('boost@1.63.0+python+shared^python+shared')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite@3.16.02')
    depends_on('bzip2')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('uuid-cms')
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

        with working_dir(build_directory, create=True):
            rsync=which('rsync')
            mkdirp('src')
            rsync('-a', '--exclude', '.git', '--exclude', 'scram-config',
                  '--exclude', 'spack-build.*',
                  source_directory+'/','src/')
            mkdirp('config')
            rsync('-a', '--exclude', '.git', 
                  source_directory+'/scram-config/','config/')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():      
                xmlfiles = glob(join_path(dep.prefix.etc,'scram.d','*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile,'tools/selected')

            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close() 
            perl=which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CORAL', 
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc', 
                 '--keys', 'PROJECT_GIT_HASH='+cmssw_u_version,
                 '--arch', self.scram_arch)
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
            scram.add_default_env('LD_LIBRARY_PATH', project_dir+'/lib/'+self.scram_arch)
            scram('build', '-v', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')
           


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version='CORAL_'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('CORAL_RELEASE_BASE', self.prefix)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+self.scram_arch)


    def setup_environment(self, spack_env, run_env):
        cmssw_version='CORAL.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+self.scram_arch)

    def url_for_version(self, version):
        """Handle CORAL's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/coral/CORAL_%s/src.tar.gz" % version_underscore
