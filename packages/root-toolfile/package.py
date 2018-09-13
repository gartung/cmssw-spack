from spack import *
import sys,os,re
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class RootToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('root')

    def install(self, spec, prefix):
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['VER'] = spec['root'].version
        values['PFX'] = spec['root'].prefix
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()

        fname = 'root_interface.xml'
        contents = str("""<tool name="root_interface" version="$VER">
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
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'root_cxxdefaults.xml'
        if sys.platform == 'darwin':
          contents = str("""<tool name="root_cxxdefaults" version="$VER">
</tool>""")
          write_scram_toolfile(contents, values, fname, prefix)
        else:
          contents = str("""<tool name="root_cxxdefaults" version="$VER">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="$GCC_PREFIX" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/$GCC_MACHINE" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/backward" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path"/>
</tool>""")
          write_scram_toolfile(contents, values, fname, prefix)

# rootcling toolfile
        fname = 'rootcling.xml'
        contents = str("""<tool name="rootcling" version="$VER">
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
        write_scram_toolfile(contents, values, fname, prefix)

# rootrint toolfile
        fname = 'rootrint.xml'
        contents = str("""<tool name="rootrint" version="$VER'">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# rootsmatrix toolfile
        fname = 'rootsmatrix.xml'
        contents = str("""<tool name="rootsmatrix" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Smatrix"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrio toolfile
        fname = 'rootrio.xml'
        contents = str("""<tool name="rootrio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RIO"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootthread toolfile
        fname = 'rootthread.xml'
        contents = str("""<tool name="rootthread" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Thread"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootxmlio toolfile
        fname = 'rootxmlio.xml'
        contents = str("""<tool name="rootxmlio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLIO"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmathcore toolfile
        fname = 'rootmathcore.xml'
        contents = str("""<tool name="rootmathcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MathCore"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootcore toolfile
        fname = 'rootcore.xml'
        contents = str("""<tool name="rootcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <use name="rootmathcore"/>
  <use name="rootthread"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roothistmatrix toolfile
        fname = 'roothistmatrix.xml'
        contents = str("""<tool name="roothistmatrix" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="rootcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootspectrum toolfile
        fname = 'rootspectrum.xml'
        contents = str("""<tool name="rootspectrum" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Spectrum"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootphysics toolfile
        fname = 'rootphysics.xml'
        contents = str("""<tool name="rootphysics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# root toolfile, alias for rootphysics. Using rootphysics is preferred.
        fname = 'root.xml'
        contents = str("""<tool name="root" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootphysics"/>
  <ifversion name="^[6-9]\.">
    <flags NO_CAPABILITIES="yes"/>
  </ifversion>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgpad toolfile
        fname = 'rootgpad.xml'
        contents = str("""<tool name="rootgpad" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gpad"/>
  <lib name="Graf"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgraphics toolfile, identical to old "root" toolfile
        fname = 'rootgraphics.xml'
        contents = str("""<tool name="rootgraphics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TreePlayer"/>
  <lib name="Graf3d"/>
  <lib name="Postscript"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rooteg toolfile, identical to old "root" toolfile
        fname = 'rooteg.xml'
        contents = str("""<tool name="rooteg" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="EG"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootpy toolfile, identical to old "root" toolfile
        fname = 'rootpy.xml'
        contents = str("""<tool name="rootpy" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyROOT"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootinteractive toolfile
        fname = 'rootinteractive.xml'
        contents = str("""<tool name="rootinteractive" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
  <use name="rootrint"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmath toolfile
        fname = 'rootmath.xml'
        contents = str("""<tool name="rootmath" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="rootcore"/>
  <use name="gsl"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootminuit toolfile
        fname = 'rootminuit.xml'
        contents = str("""<tool name="rootminuit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootminuit2 toolfile
        fname = 'rootminuit2.xml'
        contents = str("""<tool name="rootminuit2" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit2"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrflx toolfile
        fname = 'rootrflx.xml'
        contents = str("""<tool name="rootrflx" version="$VER">
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
        write_scram_toolfile(contents, values, fname, prefix)


# roothtml toolfile
        fname = 'roothtml.xml'
        contents = str("""<tool name="roothtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Html"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmlp toolfile
        fname = 'rootmlp.xml'
        contents = str("""<tool name="rootmlp" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MLP"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roottmva toolfile
        fname = 'roottmva.xml'
        contents = str("""<tool name="roottmva" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="rootmlp"/>
  <use name="rootminuit"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootxml toolfile
        fname = 'rootxml.xml'
        contents = str("""<tool name="rootxml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLParser"/>
  <use name="rootcore"/>
  <use name="libxml2"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootfoam toolfile
        fname = 'rootfoam.xml'
        contents = str("""<tool name="rootfoam" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Foam"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgeom toolfile
        fname = 'rootgeom.xml'
        contents = str("""<tool name="rootgeom" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Geom"/>
  <use name="rootrio"/>
  <use name="rootmathcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgeompainter toolfile
        fname = 'rootgeompainter.xml'
        contents = str("""<tool name="rootgeompainter" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GeomPainter"/>
  <use name="rootgeom"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrgl toolfile
        fname = 'rootrgl.xml'
        contents = str("""<tool name="rootrgl" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RGL"/>
  <use name="rootinteractive"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rooteve toolfile
        fname = 'rooteve.xml'
        contents = str("""<tool name="rooteve" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Eve"/>
  <use name="rootgeompainter"/>
  <use name="rootrgl"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootguihtml toolfile
        fname = 'rootguihtml.xml'
        contents = str("""<tool name="rootguihtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GuiHtml"/>
  <use name="rootinteractive"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roofitcore toolfile
        fname = 'roofitcore.xml'
        contents = str("""<tool name="roofitcore" version="$VER">
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
        write_scram_toolfile(contents, values, fname, prefix)


# roofit toolfile
        fname = 'roofit.xml'
        contents = str("""<tool name="roofit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roostats toolfile
        fname = 'roostats.xml'
        contents = str("""<tool name="roostats" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# histfactory toolfile
        fname = 'histfactory.xml'
        contents = str("""<tool name="histfactory" version="$VER">
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
        write_scram_toolfile(contents, values, fname, prefix)
