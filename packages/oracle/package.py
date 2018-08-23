from spack import *
import glob
import sys,os

class Oracle(Package):
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-basic-linux.x64-12.1.0.2.0.zip"

    version('12.1.0.2.0', 'd5ef30bc0506e0b0dae4dc20c76b8dbe')
    resource(name='basiclite', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-basiclite-linux.x64-12.1.0.2.0.zip',
             md5='3964438a216d6b9b329bad8201175b83', placement='basiclite')
    resource(name='jdbc', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-jdbc-linux.x64-12.1.0.2.0.zip',
             md5='d3f4afd0dbf9b74c0b1e998dd69e6c9c', placement='jdbc')
    resource(name='odbc', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-odbc-linux.x64-12.1.0.2.0.zip',
             md5='30c72d4bca33084dcafe466ab1a7c399', placement='odbc')
    resource(name='sdk', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-sdk-linux.x64-12.1.0.2.0.zip',
             md5='d5eff6654c7901d2d5bccc87e386e192', placement='sdk')
    resource(name='sqlplus', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-sqlplus-linux.x64-12.1.0.2.0.zip',
             md5='f165280723ff1c96f825ba62c63b65cf', placement='sqlplus')
    resource(name='tools', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-tools-linux.x64-12.1.0.2.0.zip',
             md5='aff843e3748bf49cc063fa695cca9fd2', placement='tools')

    def install(self, spec, prefix):
        install_tree('sdk/sdk/include', prefix.include)
        mkdirp(self.prefix.lib)
        for f in glob.glob('*/lib*'):
            install(f, self.prefix.lib)
        mkdirp(self.prefix.bin)

        with working_dir(prefix.lib, create=False):
            for f in glob.glob('lib*.' + dso_suffix + '.[0-9]*'):
                dest = str(os.path.basename(f)).split(
                    '.')[0] + '.' + dso_suffix
                os.symlink(f, dest)

