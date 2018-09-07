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
        for f in glob.glob('.libs/libuuid.so*'):
            install(f, prefix.lib)
        make('install-uuidincHEADERS')

