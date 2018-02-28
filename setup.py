import sys

if sys.version_info < (2, 5):
    print >> sys.stderr, "ERROR: Naive Variant Caller requires python 2.5 or greater"
    sys.exit()

try:
    import setuptools
except ImportError:
    # Automatically download setuptools if not available
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages
from glob import glob

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

       
def main():
    setup(  name = "nvc",
            version = "0.0.3",
            scripts = ["nvc/naive_variant_caller.py"],
            author = "Daniel Blankenberg",
            author_email = "dan.blankenberg@gmail.com",
            description = 'The Naive Variant Caller',
            license = "GPLv2",
            install_requires = ['numpy', 'pyBamParser==0.0.3', 'pyBamTools==0.0.3'],
            url = "https://github.com/blankenberg/nvc",
            zip_safe = False,
            dependency_links = [],
            classifiers=[ "Development Status :: 4 - Beta",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)" ],
            **extra )

if __name__ == "__main__":
    main()
