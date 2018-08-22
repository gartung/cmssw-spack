from spack import *
import tarfile
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Lhapdf(Package):
    homepage = "http://www.example.com"
    url = "http://www.hepforge.org/archive/lhapdf/LHAPDF-6.2.1.tar.gz"

    version('6.2.1', '9e05567d538fdb4862d4781cd076d7db')

    resource(name='cteq6l1', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/cteq6l1.tar.gz',
             md5='5611f1e9235151d9f67254aeb13bb65f')
    resource(name='CT10', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/CT10.tar.gz',
             md5='ec16da599329ad3525df040219c64538')
    resource(name='MSTW2008nlo68cl', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MSTW2008nlo68cl.tar.gz',
             md5='929cd57dbcd8bae900c2bf694c529d75')
    resource(name='MMHT2014lo68cl', url='https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014lo68cl.tar.gz',
             md5='25aae4cc0a0428de50fd6bdc5f7ff20b')
    resource(name='MMHT2014nlo68cl', url='https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014nlo68cl.tar.gz',
             md5='71688543dd0a624944e023be0171c6e3')

    def patch(self):
        install(join_path(os.path.dirname(__file__), "lhapdf_makeLinks.file"),
                "lhapdf_makeLinks")
        install(join_path(os.path.dirname(__file__), "lhapdf_pdfsetsindex.file"),
                "lhapdf_pdfsetsindex")


    depends_on('gmake', type='build')
    depends_on('boost@1.63.0')
    depends_on('cython', type='build')
    depends_on('python')
#    depends_on('yaml-cpp@0.5.1')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-boost=%s' % spec['boost'].prefix,
                  'PYTHON=%s/bin/python' % spec['python'].prefix,
                  'CYTHON=%s/bin/cython' % spec['cython'].prefix,
                  'PYTHONPATH=%s/lib/python2.7/site-packages' %
                  spec['cython'].prefix)
        make('all', 'PYTHONPATH=%s/lib/python2.7/site-packages' %
             spec['cython'].prefix)
        make('install', 'PYTHONPATH=%s/lib/python2.7/site-packages' %
                        spec['cython'].prefix)

        mkdirp(join_path(spec.prefix.share, 'LHAPDF'))
        for pdf in ['cteq6l1', 'CT10', 'MSTW2008nlo68cl', 'MMHT2014lo68cl', 'MMHT2014nlo68cl']:
            install_tree(pdf, join_path(spec.prefix.share, 'LHAPDF', pdf))
