from setuptools import setup, find_packages
import codecs
import os.path


# from https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
  name="ubirtc",
  version="0.0.1",
  packages=['ubirtc'],
  author='Miguel Won',
  install_requires=[
    "websockets",
    "asyncio",
    ],
  description="Ubiquo: Live streaming and remote control",
  keywords=["Ubiquo","UbiOne","IoT","WebRTC","Raspberry Pi","GStreamer"],
  url="",
  classifiers=[
    'Programming Language :: Python :: 3 :: Only' # https://pypi.org/classifiers/
  ]
)
