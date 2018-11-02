from setuptools import setup

version = "0.2.1"

setup(
    name="xmler",
    version=version,
    description="Converts a Python dictionary into a XML string with namespace support.",
    long_description="Long description and usage instructions can be found at https://github.com/dimitern/xmler",
    author="Chris Watson",
    author_email="chris@marginzero.co",
    maintainer="Dimiter Naydenov",
    maintainer_email="dimiter@naydenov.net",
    license="LICENCE",
    url="https://github.com/dimitern/xmler",
    py_modules=["xmler"],
    download_url="https://test.pypi.python.org/packages/source/d/xmler/xmler-%s.tar.gz?raw=true"
    % (version),
    platforms="Cross-platform",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
