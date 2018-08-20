from spack import *
from llnl.util.filesystem import *

def write_scram_toolfile(tmplstr, vals, fname, prefix):
    """Create contents of scram tool config files for this package."""
    from string import Template
    mkdirp(join_path(prefix, 'scram.d'))
    filename=join_path(prefix, 'scram.d', fname)
    template = Template(tmplstr)
    contents = template.substitute(vals)
    with open(filename, 'w') as f:
        f.write(contents)
        f.close()


def relrelink(top):
    import os
    for root, dirs, files in os.walk(top, topdown=False):
        for x in files:
            p = os.path.join(root, x)
            f = os.path.abspath(p)
            if os.path.islink(f):
                linkto = os.path.realpath(f)
                if not os.path.commonprefix((f, linkto)) == '/':
                    rel = os.path.relpath(linkto, start=os.path.dirname(f))
                    os.remove(p)
                    os.symlink(rel, p)
        for y in dirs:
            p = os.path.join(root, y)
            f = os.path.abspath(p)
            if os.path.islink(f):
                linkto = os.path.realpath(f)
                if not os.path.commonprefix((f, linkto)) == '/':
                    rel = os.path.relpath(linkto, start=os.path.dirname(f))
                    os.remove(p)
                    os.symlink(rel, p)



