from spack.compiler import *
from spack.util.executable import *
import re

class CrayWrapper(object):
    cray_wrapper = True
    vendor_name = None
    # Subclasses use possible names of C compiler
    cc_names = ['cc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['CC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ftn']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ftn']

    # Named wrapper links within spack.build_env_path
    link_paths = { 'cc'  : 'craype/cc',
                   'cxx' : 'case-insensitive/CC',
                   'f77' : 'craype/ftn',
                   'fc'  : 'craype/ftn' }
    
    @classmethod
    def default_version(cls, comp):
        """The '-help' option gets information about the cray wrapper, not the
           underlying compiler
           Output looks like this::

           Usage: cc [options] file...
        """
        compiler = Executable(comp)
        output = compiler('-help', output=str, error=str)
        match = re.search(r'(Usage: cc|CC|ftn \[options\] file)\.*.*', output)
        if match.group(0) is not None:
            return super(CrayWrapper, cls).default_version(comp)

