# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install hls
#
# You can edit this file again by typing:
#
#     spack edit hls
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import shutil

class Hls(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git_url      = "https://github.com/Xilinx/HLS_arbitrary_Precision_Types"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2019-200a9aecaadf471592558540dc5a88256cbf880f', git=git_url, branch='master', commit='200a9aecaadf471592558540dc5a88256cbf880f')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        with working_dir(join_path(self.stage.source_path, 'examples/ap_fixed')):
            make()
        with working_dir(join_path(self.stage.source_path, 'examples/ap_int')):
            make()
        shutil.move(join_path(self.stage.source_path, 'examples/ap_fixed', 'a.out'), join_path(self.stage.source_path, 'examples', 'ap_fixed.exe'))
        shutil.move(join_path(self.stage.source_path, 'examples/ap_int', 'a.out'), join_path(self.stage.source_path, 'examples', 'ap_int.exe'))
        install_tree(self.stage.source_path, self.prefix)
