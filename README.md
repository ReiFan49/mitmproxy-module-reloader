# mitmproxy Module Reloader

Attempts to reload modules in a modular way.

## Caveats

This module **pollutes** `builtins` module to easily pass reference as non-addon script.
