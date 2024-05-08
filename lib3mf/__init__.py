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

# Ensure that your Lib3MF.py wraps around the shared library correctly
from .Lib3MF import *  # Import necessary classes/functions from your Lib3MF.py

# Returns the raw library path
def get_library_path():
    global lib_path
    return lib_path

# For existing codes that use Wrapper class directly
def get_library_path_for_wrapper():
    global lib_path
    if system == "linux":
        if str(lib_path).endswith(".so"):
            return lib_path[:-3]
    if system == "windows":
        if str(lib_path).endswith(".dll"):
            return lib_path[:-4]
    if system == "darwin":
        if str(lib_path).endswith(".dylib"):
            return lib_path[-6]

# Your existing logic to use the library
def get_wrapper():
    global lib_path
    try:
        # No need to modify lib_path here; just use it directly in your wrapper
        return Wrapper(get_library_path_for_wrapper())
    except ELib3MFException as e:
        print("Failed to initialize the Lib3MF wrapper: ", e)
        raise