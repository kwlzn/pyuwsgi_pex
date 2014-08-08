from contextlib import contextmanager
import os

from twitter.common.contextutil import pushd, temporary_dir

import pkg_resources


UWSGI_BINARY_PATH = 'pex_uwsgi'
UWSGI_BOOTSTRAP_PATH = 'bootstrap.py'
UWSGI_RESOURCE_PATH = 'pyuwsgi.resources'


def write_resource(filename, resource_path=UWSGI_RESOURCE_PATH):
  with open(filename, 'wb') as fh:
    for chunk in pkg_resources.resource_stream(resource_path, filename):
      fh.write(chunk)


@contextmanager
def uwsgi_context(*args, **kwargs):
  """A context manager that provides a temporary directory with a pex-bootstrapped uwsgi.

     Usage:

       import os
       from pyuwsgi import UWSGI_BINARY_PATH, uwsgi_context

       with uwsgi_context() as uwsgi_path:
         uwsgi_bin_path = os.path.join(uwsgi_path, UWSGI_BINARY_PATH)
         p = subprocess.Popen([uwsgi_bin_path, '--arg1', '--arg2'])
         ...


       >>> with uwsgi_context() as uwsgi_path:
       ...   print uwsgi_path
       ...   os.listdir(uwsgi_path)
       ...
       /private/var/folders/3t/xkwqrkld4xxgklk2s4n41jb80000gn/T/tmpCY4JhN
       ['pex_uwsgi']

  """
  old_cwd = os.getcwd()
  with temporary_dir(*args, **kwargs) as temp_dir:
    with pushd(temp_dir):
      write_resource(UWSGI_BINARY_PATH)
      if pkg_resources.resource_exists(UWSGI_RESOURCE_PATH, UWSGI_BOOTSTRAP_PATH):
        # This will only be present/needed on OSX.
        write_resource(UWSGI_BOOTSTRAP_PATH)
      with pushd(old_cwd):
        yield temp_dir
