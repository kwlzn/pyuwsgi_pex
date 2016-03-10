import os
import sys

if sys.version_info[0] >= 3:
    from importlib import reload
else:
    from imp import reload


def activate_pex():
  sys.stderr.write('[pex_uwsgi] bootstrapping..\n')

  entry_point = os.environ.get('UWSGI_PEX')
  if not entry_point:
    sys.stderr.write(
      '[pex_uwsgi] couldnt determine pex from UWSGI_PEX environment variable, bailing!\n'
    )
    sys.exit(1)

  sys.stderr.write('[pex_uwsgi] entry_point=%s\n' % entry_point)

  sys.path[0] = os.path.abspath(sys.path[0])
  sys.path.insert(0, entry_point)
  sys.path.insert(0, os.path.abspath(os.path.join(entry_point, '.bootstrap')))

  from _pex import pex_bootstrapper

  if hasattr(pex_bootstrapper, 'bootstrap_pex_env'):
    # New-style pex bootstrapping.
    pex_bootstrapper.bootstrap_pex_env(entry_point)
  else:
    # Old and even older-style pex bootstrapping.
    from _pex.environment import PEXEnvironment
    from _pex.pex_info import PexInfo

    try:
      pex_bootstrapper.monkeypatch_build_zipmanifest()
    except AttributeError:
      pass

    try:
      from _pex.finders import register_finders
      register_finders()
    except (ImportError, NameError):
      pass

    pex_info = PexInfo.from_pex(entry_point)
    env = PEXEnvironment(entry_point, pex_info)
    env.activate()

  # import & reload in our newly bootstrapped environment
  import pkg_resources
  reload(pkg_resources)

  sys.stderr.write('[pex_uwsgi] sys.path=%s\n\n' % sys.path)
  return


activate_pex()
