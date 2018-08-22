from spack import *
import shutil
import os
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Tkonlinesw(Package):
    homepage = "http://www.example.com"
    url = "http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-4.1.0-1.tgz"

    version('4.1.0-1', 'aa8c780611f0292d5ff534d992617b46')

    depends_on('oracle')
    depends_on('xerces-c')
    depends_on('gmake')
    depends_on('root')

    def setup_environment(self, spack_env, run_env):
        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.1-tkonline'
        spack_env.set('ENV_TRACKER_DAQ', releasename + '/opt/trackerDAQ')
        spack_env.set('XDAQ_ROOT', releasename + '/FecSoftwareV3_0/generic')
        spack_env.set('XDAQ_RPMBUILD', 'yes')
        spack_env.set('USBFEC', 'no')
        spack_env.set('PCIFEC', 'yes')
        spack_env.set('ENV_CMS_TK_BASE', releasename)
        spack_env.set('ENV_CMS_TK_DIAG_ROOT', releasename + '/DiagSystem')
        spack_env.set('ENV_CMS_TK_ONLINE_ROOT',
                      releasename + '/TrackerOnline/')
        spack_env.set('ENV_CMS_TK_COMMON', releasename +
                      '/TrackerOnline/2005/TrackerCommon/')
        spack_env.set('ENV_CMS_TK_XDAQ', releasename +
                      '/TrackerOnline/2005/TrackerXdaq/')
        spack_env.set('ENV_CMS_TK_APVE_ROOT',
                      releasename + '/TrackerOnline/APVe')
        spack_env.set('ENV_CMS_TK_FEC_ROOT', releasename + '/FecSoftwareV3_0')
        spack_env.set('ENV_CMS_TK_FED9U_ROOT', releasename +
                      '/TrackerOnline/Fed9U/Fed9USoftware')
        spack_env.set('ENV_CMS_TK_ICUTILS', releasename +
                      '/TrackerOnline/2005/TrackerCommon//ICUtils')
        spack_env.set('ENV_CMS_TK_LASTGBOARD', releasename + '/LAS')
        spack_env.set('ENV_CMS_TK_HAL_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_CAEN_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_SBS_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_TTC_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('XDAQ_OS', 'linux')
        spack_env.set('XDAQ_PLATFORM', 'x86_slc4')
        spack_env.set('CPPFLAGS', '-fPIC')
        spack_env.set('CFLAGS', '-O2 -fPIC')
        spack_env.set('CXXFLAGS', '-O2 -fPIC')

    def install(self, spec, prefix):
        filter_file('-Werror', '', 'FecSoftwareV3_0/generic/Makefile')
        mkdirp(join_path(prefix, 'dummy/Linux/lib'))
        configure('--with-xdaq-platform=x86_64',
                  '--with-oracle-path=%s' % spec['oracle'].prefix,
                  '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('FecSoftwareV3_0'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('TrackerOnline/Fed9U/Fed9USoftware'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        make('cmssw')
        make('cmsswinstall')

        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.1-tkonline'
        project_path = join_path(releasename, 'opt', projectname)
        install_tree(join_path(project_path, 'include'), prefix.include)
        install_tree(join_path(project_path, 'lib'), prefix.lib)

