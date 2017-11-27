##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import sys,re


class Root(CMakePackage):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url      = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"
    # Development versions
    version('6.11.02', '95e5705e203a5e0e70be7849c915f732')

    # Production versions
    version('6.10.08', '48f5044e9588d94fb2d79389e48e1d73', preferred=True)

    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkg-config',   type='build')
    depends_on("pcre")
    depends_on("fftw~mpi")
    depends_on("python+shared")
    depends_on("gsl")
    depends_on("libxml2+python^python+shared")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("giflib")
    depends_on("xz")
    depends_on("openssl")
    depends_on("xrootd")
    depends_on("freetype")

    def cmake_args(self):
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        options=[ '-Dcxx17=on'
                 ,'-Droofit=on'
                 ,'-Dx11=on'
                 ,'-Dminuit2=on'
                 ,'-DPCRE_CONFIG_EXECUTABLE=%s/bin/pcre-config' %
                   self.spec['pcre'].prefix
                 ,'-DPCRE_INCLUDE_DIR=%s/include' %
                   self.spec['pcre'].prefix
                 ,'-DPCRE_PCRE_LIBRARY=%s/lib/libpcre.%s' %
                  (self.spec['pcre'].prefix,dso_suffix)
                 ,'-DPCRE_PCREPOSIX_LIBRARY=%s/lib/libpcreposix.%s' %
                  (self.spec['pcre'].prefix,dso_suffix)
                 ,'-DLZMA_DIR=%s' %
                   self.spec['xz'].prefix
                 ,'-DLZMA_INCLUDE_DIR=%s/include' %
                   self.spec['xz'].prefix
                 ,'-DLZMA_LIBRARY=%s/lib/liblzma.%s' %
                  (self.spec['xz'].prefix,dso_suffix)
                 ,'-DXROOTD_ROOT_DIR=%s' %
                   self.spec['xrootd'].prefix
                 ,'-DPNG_INCLUDE_DIR=%s/include' %
                   self.spec['libpng'].prefix
                 ,'-DPNG_LIBRARY=%s/lib/libpng.%s' %
                  (self.spec['libpng'].prefix,dso_suffix)
                 ,'-DPYTHON_EXECUTABLE=%s/python' %
                  (self.spec['python'].prefix.bin)
                 ,'-DPYTHON_INCLUDE=%s' %
                  (self.spec['python'].prefix.include)
                 ,'-DPYTHON_LIBRARY=%s/libpython%s.%s' %
                  (self.spec['python'].prefix.lib,pyver,dso_suffix) ]               
        if sys.platform == 'darwin':
            darwin_options = [
                '-Dx11=off',
                '-Dcocoa=on',
                '-Dbonjour=on',
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF']
            options.extend(darwin_options)

        return options

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL','0')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('ROOT_VERSION', 'v6')
        spack_env.prepend_path('PYTHONPATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL','0')

    def url_for_version(self, version):
        """Handle ROOT's unusual version string."""
        return "https://root.cern.ch/download/root_v%s.source.tar.gz" % version

    def write_scram_toolfile(self,contents,filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc+'/scram.d/'+filename,'w') as f:
            f.write(contents)
            f.close()
        

    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        gcc=which(spack_f77)
        gcc_prefix=re.sub('/bin/.*$','',self.compiler.f77)
        gcc_machine=gcc('-dumpmachine',output=str)
        gcc_ver=gcc('-dumpversion',output=str)

        values={}
        values['VER']=self.spec.version
        values['PFX']=self.spec.prefix
        values['GCC_VER']=gcc_ver.rstrip()
        values['GCC_PREFIX']=gcc_prefix
        values['GCC_MACHINE']=gcc_machine.rstrip()

        fname='root_interface.xml'
        template=Template("""<tool name="root_interface" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOT_INTERFACE_BASE"     default="$PFX"/>
    <environment name="INCLUDE"                 default="$PFX/include"/>
    <environment name="LIBDIR"                  default="$PFX/lib"/>
  </client>
  <runtime name="PATH"                          value="$PFX/bin" type="path"/>
  <runtime name="PYTHONPATH"                    value="$PFX/lib" type="path"/>
  <runtime name="ROOTSYS"                       value="$PFX/"/>
  <runtime name="ROOT_TTREECACHE_SIZE"          value="0"/>
  <runtime name="ROOT_TTREECACHE_PREFILL"       value="0"/>
  <runtime name="ROOT_INCLUDE_PATH"             value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

        fname='root_cxxdefaults.xml'
        template=Template("""<tool name="root_cxxdefaults" version="$VER">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="$GCC_PREFIX" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/$GCC_MACHINE" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/backward" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

# rootcling toolfile
        fname='rootcling.xml'
        template=Template("""<tool name="rootcling" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Core"/>
  <client>
    <environment name="ROOTCLING_BASE" default="$PFX"/>
    <environment name="INCLUDE"        default="$PFX/include"/>
  </client>
  <use name="root_interface"/>
  <use name="sockets"/>
  <use name="pcre"/>
  <use name="zlib"/>
  <use name="xz"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

# rootrint toolfile
        fname='rootrint.xml'
        template=Template("""<tool name="rootrint" version="$VER'">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <use name="rootcling"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

# rootsmatrix toolfile
        fname='rootsmatrix.xml'
        template=Template("""<tool name="rootsmatrix" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Smatrix"/>
  <use name="rootcling"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootrio toolfile
        fname='rootrio.xml'
        template=Template("""<tool name="rootrio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RIO"/>
  <use name="rootcling"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootthread toolfile
        fname='rootthread.xml'
        template=Template("""<tool name="rootthread" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Thread"/>
  <use name="rootrio"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootxmlio toolfile
        fname='rootxmlio.xml'
        template=Template("""<tool name="rootxmlio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLIO"/>
  <use name="rootrio"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootmathcore toolfile
        fname='rootmathcore.xml'
        template=Template("""<tool name="rootmathcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MathCore"/>
  <use name="rootcling"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootcore toolfile
        fname='rootcore.xml'
        template=Template("""<tool name="rootcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <use name="rootmathcore"/>
  <use name="rootthread"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roothistmatrix toolfile
        fname='roothistmatrix.xml'
        template=Template("""<tool name="roothistmatrix" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="rootcore"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootspectrum toolfile
        fname='rootspectrum.xml'
        template=Template("""<tool name="rootspectrum" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Spectrum"/>
  <use name="roothistmatrix"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootphysics toolfile
        fname='rootphysics.xml'
        template=Template("""<tool name="rootphysics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
  <use name="roothistmatrix"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# root toolfile, alias for rootphysics. Using rootphysics is preferred.
        fname='root.xml'
        template=Template("""<tool name="root" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootphysics"/>
  <ifversion name="^[6-9]\.">
    <flags NO_CAPABILITIES="yes"/>
  </ifversion>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootgpad toolfile
        fname='rootgpad.xml'
        template=Template("""<tool name="rootgpad" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gpad"/>
  <lib name="Graf"/>
  <use name="roothistmatrix"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootgraphics toolfile, identical to old "root" toolfile
        fname='rootgraphics.xml'
        template=Template("""<tool name="rootgraphics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TreePlayer"/>
  <lib name="Graf3d"/>
  <lib name="Postscript"/>
  <use name="rootgpad"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rooteg toolfile, identical to old "root" toolfile
        fname='rooteg.xml'
        template=Template("""<tool name="rooteg" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="EG"/>
  <use name="rootgraphics"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootpy toolfile, identical to old "root" toolfile
        fname='rootpy.xml'
        template=Template("""<tool name="rootpy" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyROOT"/>
  <use name="rootgraphics"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootinteractive toolfile 
        fname='rootinteractive.xml'
        template=Template("""<tool name="rootinteractive" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
  <use name="rootrint"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootmath toolfile
        fname='rootmath.xml'
        template=Template("""<tool name="rootmath" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="rootcore"/>
  <use name="gsl"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootminuit toolfile
        fname='rootminuit.xml'
        template=Template("""<tool name="rootminuit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit"/>
  <use name="rootgpad"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootminuit2 toolfile
        fname='rootminuit2.xml'
        template=Template("""<tool name="rootminuit2" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit2"/>
  <use name="rootgpad"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootrflx toolfile
        fname='rootrflx.xml'
        template=Template("""<tool name="rootrflx" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOTRFLX_BASE" default="$PFX"/>
  </client>
  <flags GENREFLEX_GCCXMLOPT="-m64"/>
  <flags GENREFLEX_CPPFLAGS="-DCMS_DICT_IMPL -D_REENTRANT -DGNUSOURCE -D__STRICT_ANSI__"/>
  <flags GENREFLEX_ARGS="--deep"/>
  <runtime name="GENREFLEX" value="$PFX/bin/genreflex"/>
  <use name="root_interface"/>
  <use name="rootcling"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roothtml toolfile
        fname='roothtml.xml'
        template=Template("""<tool name="roothtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Html"/>
  <use name="rootgpad"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootmlp toolfile
        fname='rootmlp.xml'
        template=Template("""<tool name="rootmlp" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MLP"/>
  <use name="rootgraphics"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roottmva toolfile
        fname='roottmva.xml'
        template=Template("""<tool name="roottmva" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="rootmlp"/>
  <use name="rootminuit"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootxml toolfile
        fname='rootxml.xml'
        template=Template("""<tool name="rootxml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLParser"/>
  <use name="rootcore"/>
  <use name="libxml2"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootfoam toolfile
        fname='rootfoam.xml'
        template=Template("""<tool name="rootfoam" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Foam"/>
  <use name="roothistmatrix"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootgeom toolfile
        fname='rootgeom.xml'
        template=Template("""<tool name="rootgeom" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Geom"/>
  <use name="rootrio"/>
  <use name="rootmathcore"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootgeompainter toolfile
        fname='rootgeompainter.xml'
        template=Template("""<tool name="rootgeompainter" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GeomPainter"/>
  <use name="rootgeom"/>
  <use name="rootgraphics"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootrgl toolfile
        fname='rootrgl.xml'
        template=Template("""<tool name="rootrgl" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RGL"/>
  <use name="rootinteractive"/>
  <use name="rootgraphics"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rooteve toolfile
        fname='rooteve.xml'
        template=Template("""<tool name="rooteve" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Eve"/>
  <use name="rootgeompainter"/>
  <use name="rootrgl"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# rootguihtml toolfile
        fname='rootguihtml.xml'
        template=Template("""<tool name="rootguihtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GuiHtml"/>
  <use name="rootinteractive"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roofitcore toolfile
        fname='roofitcore.xml'
        template=Template("""<tool name="roofitcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$ROOFIT_BASE/lib"/>
    <environment name="INCLUDE" default="$$ROOFIT_BASE/include"/>
  </client>
  <runtime name="ROOFITSYS" value="$$ROOFIT_BASE/"/>
  <runtime name="PATH"      value="$$ROOFIT_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roofit toolfile
        fname='roofit.xml'
        template=Template("""<tool name="roofit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# roostats toolfile
        fname='roostats.xml'
        template=Template("""<tool name="roostats" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)


# histfactory toolfile
        fname='histfactory.xml'
        template=Template("""<tool name="histfactory" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistFactory"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="roostats"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootxml"/>
  <use name="rootfoam"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)
