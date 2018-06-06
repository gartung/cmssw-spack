from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libxml2(AutotoolsPackage):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
       project (but usable outside of the Gnome platform), it is free
       software available under the MIT License."""
    homepage = "http://xmlsoft.org"
    url = "http://xmlsoft.org/sources/libxml2-2.9.2.tar.gz"

    version('2.9.4', 'ae249165c173b1ff386ee8ad676815f5')
    version('2.9.2', '9e6a9aca9d155737868b3dc5fd82f788')
    version('2.7.8', '8127a65e8c3b08856093099b52599c86')

    variant('python', default=True, description='Enable Python support')

    depends_on('python')
    depends_on('zlib')
    depends_on('xz')

    depends_on('pkg-config@0.9.0:', type='build')

    def configure_args(self):
        spec = self.spec

        args = ["--with-lzma=%s" % spec['xz'].prefix]

        if '+python' in spec:
            args.extend([
                '--with-python={0}'.format(spec['python'].home),
                '--with-python-install-dir={0}'.format(site_packages_dir)
            ])
        else:
            args.append('--without-python')

        return args


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'libxml2.xml'
        contents = str("""<tool name="libxml2" version="$VER">
  <info url="http://xmlsoft.org/"/>
  <lib name="xml2"/>
  <client>
    <environment name="LIBXML2_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBXML2_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBXML2_BASE/include/libxml2"/>
  </client>
  <runtime name="PATH" value="$$LIBXML2_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)
