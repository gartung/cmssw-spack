from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class UuidCms(Package):
    """Portable uuid C library"""

    homepage = "http://sourceforge.net/projects/libuuid/"
    url = "http://www.kernel.org/pub/linux/utils/util-linux/v2.22/util-linux-2.22.tar.gz"

    version('2.22', '9eb42d839abca59f01b81202580137ec')

    patch('libuuid-2.22.2-disable-get_uuid_via_daemon.patch')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--libdir=%s' % prefix.lib,
                  '--disable-silent-rules',
                  '--disable-tls',
                  '--disable-rpath',
                  '--disable-libblkid',
                  '--disable-libmount',
                  '--disable-mount',
                  '--disable-losetup',
                  '--disable-fsck',
                  '--disable-partx',
                  '--disable-mountpoint',
                  '--disable-fallocate',
                  '--disable-unshare',
                  '--disable-eject',
                  '--disable-agetty',
                  '--disable-cramfs',
                  '--disable-wdctl',
                  '--disable-switch_root',
                  '--disable-pivot_root',
                  '--disable-kill',
                  '--disable-utmpdump',
                  '--disable-rename',
                  '--disable-login',
                  '--disable-sulogin',
                  '--disable-su',
                  '--disable-schedutils',
                  '--disable-wall',
                  '--disable-makeinstall-setuid',
                  '--without-ncurses',
                  '--enable-libuuid')
        make('uuidd')

        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        for f in glob.glob('util-linux-*/.libs/libuuid.so*'):
            install(f, prefix.lib)
        make('install-uuidincHEADERS')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'uuid-cms.xml'
        contents = str("""<tool name="uuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

        fname = 'libuuid.xml'
        contents = str("""<tool name="libuuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
