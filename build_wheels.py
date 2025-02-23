import json
import platform
import subprocess
import os

MANIFEST_FILE = "manifest.json"
TEMP_MANIFEST_IN = "MANIFEST.in"

def get_platform_tag():
    """Return the appropriate platform tag for wheel building."""
    system = platform.system()
    if system == "Linux":
        return "manylinux2014_x86_64"
    elif system == "Windows":
        return "win_amd64"
    elif system == "Darwin":
        return "macosx_10_9_universal2"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

def create_manifest():
    """Generate MANIFEST.in with the relevant platform-specific file."""
    with open(MANIFEST_FILE, "r") as f:
        data = json.load(f)

    system = platform.system().lower()
    file_to_include = data.get(system)

    if not file_to_include:
        raise RuntimeError(f"No relevant file found for platform: {system}")

    with open(TEMP_MANIFEST_IN, "w") as f:
        f.write(f"include {file_to_include}\n")

def build_wheel():
    """Build the wheel using the platform-specific command with --python-tag py3."""
    plat_name = get_platform_tag()
    command = f"python setup.py bdist_wheel --python-tag py3 --plat-name {plat_name}"
    
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def cleanup():
    """Remove the MANIFEST.in file after building."""
    if os.path.exists(TEMP_MANIFEST_IN):
        os.remove(TEMP_MANIFEST_IN)
        print(f"Removed {TEMP_MANIFEST_IN}")

if __name__ == "__main__":
    create_manifest()
    try:
        build_wheel()
    finally:
        cleanup()