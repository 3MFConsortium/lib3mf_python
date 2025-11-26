import os
import sys
import platform

# Turn lib_path into a global variable
global lib_path

# Determine the current operating system
system = platform.system().lower()

# Determine the platform and choose the right library extension
if system == "linux":
    lib_file = "lib3mf.so"
elif system == "darwin":
    lib_file = "lib3mf.dylib"
elif system == "windows":
    lib_file = "lib3mf.dll"
else:
    raise OSError("Unsupported operating system")

# Build the path to the library file
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(dir_path, lib_file)

if not os.path.exists(lib_path):
    raise ImportError(f"The required binary {lib_path} could not be found in {dir_path}")

# Add the path to the system path if necessary (useful for DLLs on Windows)
sys.path.append(dir_path)

# Import generated bindings
from .Lib3MF import *


# ---------------------------
# Public helpers
# ---------------------------

def get_library_path():
    global lib_path
    return lib_path


def get_library_path_for_wrapper():
    global lib_path
    path_str = str(lib_path)

    if system == "linux" and path_str.endswith(".so"):
        return path_str[:-3]
    if system == "windows" and path_str.endswith(".dll"):
        return path_str[:-4]
    if system == "darwin" and path_str.endswith(".dylib"):
        return path_str[:-6]

    base, _ext = os.path.splitext(path_str)
    return base


def get_wrapper():
    from . import Lib3MF as _Lib3MF
    try:
        return _Lib3MF.Wrapper(get_library_path_for_wrapper())
    except _Lib3MF.ELib3MFException as e:
        print("Failed to initialize the Lib3MF wrapper: ", e)
        raise


# ---------------------------------------------------------------------------
# PYTHON 3.13 SHUTDOWN SAFETY MONKEY PATCH
#
# Fixes:
#   Exception ignored in: Base.__del__
#   AttributeError: 'NoneType' object has no attribute 'SUCCESS'
#
# Root cause:
#   During interpreter shutdown, Lib3MF.ErrorCodes becomes None.
#   Base.__del__ -> Wrapper.Release -> checkError -> ErrorCodes.SUCCESS
#
# Solution:
#   Patch Wrapper.checkError to NO-OP if ErrorCodes is already None.
#
# This preserves full runtime behavior and only affects shutdown.
# ---------------------------------------------------------------------------

try:
    from . import Lib3MF as _Lib3MF

    _original_checkError = _Lib3MF.Wrapper.checkError

    def _patched_checkError(self, instance, errorCode):
        ec = getattr(_Lib3MF, "ErrorCodes", None)
        if ec is None:
            # Interpreter shutdown: suppress destructor noise
            return
        return _original_checkError(self, instance, errorCode)

    _Lib3MF.Wrapper.checkError = _patched_checkError

except Exception:
    # Never block import if bindings differ slightly
    pass
