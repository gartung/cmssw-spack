from spack import *
import sys
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Graphviz(AutotoolsPackage):
    """Graph Visualization Software"""
    homepage = 'http://www.graphviz.org'
    url = 'http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.38.0.tar.gz'

    version('2.38.0', '5b6a829b2ac94efcd5fa3c223ed6d3ae')

    # We try to leave language bindings enabled if they don't cause
    # build issues or add dependencies.
    variant('sharp', default=False,
            description='Enable for optional sharp language bindings'
            ' (not yet functional)')
    variant('go', default=False,
            description='Enable for optional go language bindings'
            ' (not yet functional)')
    variant('guile', default=False,
            description='Enable for optional guile language bindings'
            ' (not yet functional)')
    variant('io', default=False,
            description='Enable for optional io language bindings'
            ' (not yet functional)')
    variant('java', default=False,  # Spack has no Java support
            description='Enable for optional java language bindings')
    variant('lua', default=False,
            description='Enable for optional lua language bindings'
            ' (not yet functional)')
    variant('ocaml', default=False,
            description='Enable for optional ocaml language bindings'
            ' (not yet functional)')
    variant('perl', default=False,    # Spack has no Perl support
            description='Enable for optional perl language bindings')
    variant('php', default=False,
            description='Enable for optional php language bindings'
            ' (not yet functional)')
    variant('python', default=False,    # Build issues with Python 2/3
            description='Enable for optional python language bindings'
            ' (not yet functional)')
    variant('r', default=False,
            description='Enable for optional r language bindings'
            ' (not yet functional)')
    variant('ruby', default=False,
            description='Enable for optional ruby language bindings'
            ' (not yet functional)')
    variant('tcl', default=False,
            description='Enable for optional tcl language bindings'
            ' (not yet functional)')

    variant('pangocairo', default=False,
            description='Build with pango+cairo support (more output formats)')
    variant('libgd', default=False,
            description='Build with libgd support (more output formats)')

    parallel = False

    # These language bindings have been tested, we know they work.
    tested_bindings = ('+java', )

    # These language bindings have not yet been tested.  They
    # likely need additional dependencies to get working.
    untested_bindings = (
        '+perl',
        '+sharp', '+go', '+guile', '+io',
        '+lua', '+ocaml', '+php',
        '+python', '+r', '+ruby', '+tcl')

    for b in tested_bindings + untested_bindings:
        depends_on('swig', when=b)

    depends_on('cairo', when='+pangocairo')
    depends_on('pango', when='+pangocairo')
    depends_on('libgd', when='+libgd')
    depends_on('ghostscript')
    depends_on('freetype')
    depends_on('expat')
    depends_on('libtool')
    depends_on('pkg-config', type='build')

    depends_on('java', when='+java')
    depends_on('python@2:2.8', when='+python')

    def patch(self):
        # Fix a few variable names, gs after 9.18 renamed them
        # See
        # http://lists.linuxfromscratch.org/pipermail/blfs-book/2015-October/056960.html
        if self.spec.satisfies('^ghostscript@9.18:'):
            kwargs = {'ignore_absent': False, 'backup': True, 'string': True}
            filter_file(' e_', ' gs_error_', 'plugin/gs/gvloadimage_gs.c',
                        **kwargs)

    def configure_args(self):
        spec = self.spec
        options = []

        need_swig = False

        for var in self.untested_bindings:
            if var in spec:
                raise InstallError(
                    "The variant {0} for language bindings has not been "
                    "tested.  It might or might not work.  To try it "
                    "out, run `spack edit graphviz`, and then move '{0}' "
                    "from the `untested_bindings` list to the "
                    "`tested_bindings` list.  Be prepared to add "
                    "required dependencies.  "
                    "Please then submit a pull request to "
                    "http://github.com/spack/spack".format(var))
            options.append('--disable-%s' % var[1:])

        for var in self.tested_bindings:
            if var in spec:
                need_swig = True
                options.append('--enable-{0}'.format(var[1:]))
            else:
                options.append('--disable-{0}'.format(var[1:]))

        if need_swig:
            options.append('--enable-swig=yes')
        else:
            options.append('--enable-swig=no')

        for var in ('+pangocairo', '+libgd'):
            if var in spec:
                options.append('--with-{0}'.format(var[1:]))
            else:
                options.append('--without-{0}'.format(var[1:]))

        # On OSX fix the compiler error:
        # In file included from tkStubLib.c:15:
        # /usr/include/tk.h:78:11: fatal error: 'X11/Xlib.h' file not found
        #       include <X11/Xlib.h>
        if sys.platform == 'darwin':
            options.append('CFLAGS=-I/opt/X11/include')

        # A hack to patch config.guess in the libltdl sub directory
        shutil.copyfile('./config/config.guess', 'libltdl/config/config.guess')

        return options

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'graphviz.xml'
        contents = str("""<tool name="graphviz" version="$VER">
  <info url="http://www.research.att.com/sw/tools/graphviz/"/>
  <client>
    <environment name="GRAPHVIZ_BASE" default="$PFX"/>
  </client>
  <runtime name="PATH" value="$$GRAPHVIZ_BASE/bin" type="path"/>
  <use name="expat"/>
  <use name="zlib"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
