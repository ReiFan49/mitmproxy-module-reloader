import builtins
from typing import Sequence
import logging

from mitmproxy import ctx

log = logging.getLogger(__name__)

class Reloader:
  def __init__(self, *, names = [], prefixes = []):
    self.__determine_name()
    self._names = list(set(names))
    self._prefixes = list(set(prefixes))

  def __determine_name(self):
    name_prefix = self.__class__.__name__ + ':'
    import inspect
    if inspect.currentframe() is None:
      import traceback
      tb = traceback.extract_stack(limit=3)[0]
      self.name = name_prefix + tb.filename
    else:
      import sys
      try:
        frame = sys._getframe(2)
        frame_locals = frame.f_locals
        self.name = name_prefix + frame_locals['__file__']
      finally:
        del frame, frame_locals

  def __reload_modules(self):
    import sys, importlib
    reloadable = set(
      v for k, v in sys.modules.items()
      if (
        k in self._names or
        k in self._prefixes or
        any(k.startswith(prefix + '.') for prefix in self._prefixes)
      )
    )
    for module in reloadable:
      importlib.reload(module)
    if reloadable:
      log.info('Reloaded %d module(s).', len(reloadable))

  def done(self):
    self.__reload_modules()

builtins.ModuleReloader = Reloader
