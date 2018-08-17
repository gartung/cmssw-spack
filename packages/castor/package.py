from spack import *
import shutil
from datetime import date
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))


class Castor(Package):

    url = "http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/2.1.13-*/2.1.13-9/castor-2.1.13-9.tar.gz"


    version('2.1.13-9', '44084334e0ec70f71b5d366dcd70c959')
    #version('2.1.16-13', '5a2cf6992ac4c1a2dcf7eb90e14233e5')
    #version('2.1.16-18', '51ed4ad6c76c9f7ecd9bbaae6fbc57ba')

    depends_on('uuid-cms')

    patch('castor-2.1.13.6-fix-memset-in-showqueues.patch')
    patch('castor-2.1.13.9-fix-link-libuuid.patch')


    def patch(self):
        filter_file('-Werror','','config/Imake.tmpl')
        filter_file('--no-undefined', '', 'config/Imake.rules')
        perl=which('perl')
        perl('-pi', '-e', 's/\ \ __MAJORVERSION__/%s/'%self.version[0], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MINORVERSION__/%s/'%self.version[1], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MAJORRELEASE__/%s/'%self.version[2], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MINORRELEASE__/%s/'%self.version[3], 'h/patchlevel.h')
        perl('-p', '-i', '-e', 's!__PATCHLEVEL__!%s!;s!__BASEVERSION__!\"%s\"!;s!__TIMESTAMP__!%s!'
             %(self.version.up_to(-1),self.version.up_to(3),date.today().isoformat()),' h/patchlevel.h')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('CASTOR_NOSTK','yes')
        spack_env.append_flags('LDFLAGS', '-L%s' % self.spec['uuid-cms'].prefix.lib)
        spack_env.append_flags('CXXFLAGS', '-I%s' % self.spec['uuid-cms'].prefix.include)

    def install(self, spec, prefix):
        configure()
        make('client')
        make('installclient'
                ,'MAJOR_CASTOR_VERSION=%s' % self.version.dotted.up_to(2)
                ,'MINOR_CASTOR_VERSION=%s' % self.version.dotted.up_to(-2)
                ,'EXPORTLIB=/'
                ,'DESTDIR=%s'%prefix
                ,'PREFIX= '
                ,'CONFIGDIR=etc'
                ,'FILMANDIR=usr/share/man/man4'
                ,'LIBMANDIR=usr/share/man/man3'
                ,'MANDIR=usr/share/man/man1'
                ,'LIBDIR=lib'
                ,'BINDIR=bin'
                ,'LIB=lib'
                ,'BIN=bin'
                ,'DESTDIRCASTOR=include/shift'
                ,'TOPINCLUDE=include'
                 )
        shutil.move(prefix.usr.bin, prefix.bin)

    def url_for_version(self, version):
        url = "http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/%s-*/%s/castor-%s.tar.gz" % (version.up_to(3), version.string, version.string)
        return url
