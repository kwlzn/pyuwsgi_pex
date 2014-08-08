import sys

from setuptools import setup


if sys.platform == 'darwin':
  platform_opts = dict(platforms=['darwin'])
  extra_resources = ['resources/bootstrap.py']
elif 'linux' in sys.platform:
  platform_opts = dict(platforms=['linux'])
  extra_resources = []


setup(
  name='pyuwsgi_pex',
  version='2.0.6.3',
  description='python cli wrapper around an embedded, pex-bootstrapped uwsgi',
  author='@kwlzn',
  author_email='kwilson@twitter.com',
  url='http://github.com/kwlzn/pyuwsgi_pex',
  packages=['pyuwsgi'],
  data_files=[('pyuwsgi/resources',
               ['resources/pex_uwsgi', 'resources/__init__.py'] + extra_resources)],
  requires=['twitter.common.contextutil'],
  **platform_opts
)
