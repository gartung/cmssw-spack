from spack import *
from string import Template
import os

class ZlibToolfile(Package):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    fname = 'zlib.xml'
    homepage = "http://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = 'file://' + os.path.dirname(__file__) + '/' + fname
    sha1 = 'c4b943907d14c74c93ae121e7789e23148beb5f0'

    version('1.0.0', sha1, expand=False)
    depends_on('zlib')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['zlib'].version
        values['PFX'] = self.spec['zlib'].prefix
        fin = open(self.fname,'r')
        tmpl = Template( fin.read() )
        fin.close()
        contents = tmpl.substitute(values)
        mkdirp(join_path(prefix.etc,'scram.d'))
        fout = open(join_path(prefix.etc,'scram.d',self.fname), 'w')
        fout.write(contents)
        fout.close()
