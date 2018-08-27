from spack import *


class Tkonlinesw(Package):
    homepage = "http://www.example.com"
    url = "http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-4.2.0-1_gcc7.tgz"

    version('4.2.0-1_gcc7', sha256='e18649cb90d5dc867f8aedc35cd25fbd3f605e8aca86ed55c91f474d727d9d7d')

    depends_on('oracle')
    depends_on('xerces-c')
    depends_on('gmake')
    depends_on('root')

    patch('tkonlinesw-4.0-clang-hash_map.patch')

    def setup_environment(self, spack_env, run_env):
        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.2-tkonline'
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
        spack_env.set('ENV_CMS_TK_FED9U_ROOT_ROOT', '%s' % self.spec['root'].prefix)
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
                  '--with-root-path=%s' % spec['root'].prefix,
                  '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('FecSoftwareV3_0'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-root-path=%s' % spec['root'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('TrackerOnline/Fed9U/Fed9USoftware'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-root-path=%s' % spec['root'].prefix,
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        make('cmssw')
        make('cmsswinstall')

        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.2-tkonline'
        project_path = join_path(releasename, 'opt', projectname)
        install_tree(join_path(project_path, 'include'), prefix.include)
        install_tree(join_path(project_path, 'lib'), prefix.lib)

