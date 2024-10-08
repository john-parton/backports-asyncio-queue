# This file is part of a backport of 'asyncio.queues' included with Python 3.13,
# exposed under the namespace of backports.lzma following the conventions
# laid down here: http://pypi.python.org/pypi/backports/1.0
# Backports homepage: http://bitbucket.org/brandon/backports

# A Python "namespace package" http://www.python.org/dev/peps/pep-0382/
# This always goes inside of a namespace package's __init__.py

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
