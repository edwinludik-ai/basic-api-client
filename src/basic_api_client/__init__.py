import os
import sys

_VENDOR = os.path.join(os.path.dirname(__file__), "..", "_vendor")
if _VENDOR not in sys.path:
    sys.path.insert(0, _VENDOR)

from .auth import authenticate, build_authorization_url

__all__ = ["authenticate", "build_authorization_url"]
