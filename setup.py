from setuptools import setup, find_packages
import os
import sys
import platform
import requests

# Function to find the real path of the shared library
def find_real_lib_path():
    lib_folder = os.path.join('lib3mf')  # Adjust the path to where your libraries are
    for item in os.listdir(lib_folder):
        if item.startswith('lib3mf') and (item.endswith('.so') or item.endswith('.dll') or item.endswith('.dylib')):
            full_path = os.path.join(lib_folder, item)
            if os.path.islink(full_path):
                return os.path.realpath(full_path)
            return full_path  # Return the direct file if it's not a symlink
    return None

# Use the resolved real path in package_data
real_lib_path = find_real_lib_path()
if real_lib_path:
    print("Choosing ", real_lib_path)
    lib_name = os.path.basename(real_lib_path)
else:
    raise FileNotFoundError("The lib3mf shared library could not be found.")

# Restrict installation to only supported platforms and architectures
SUPPORTED_PLATFORMS = {
    "Linux": ["x86_64"],
    "Windows": ["AMD64"],
    "Darwin": ["x86_64", "arm64"]  # macOS universal (Intel & Apple Silicon)
}

current_platform = platform.system()
current_arch = platform.machine()

if current_platform not in SUPPORTED_PLATFORMS or current_arch not in SUPPORTED_PLATFORMS[current_platform]:
    raise RuntimeError(
        f"This package only supports Linux (amd64), Windows (x86_64), and macOS (universal). "
        f"Your platform ({current_platform} {current_arch}) is not supported."
    )

# Function to download a file from a URL
def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download file from {url}")

# Download the README file
readme_url = "https://raw.githubusercontent.com/3MFConsortium/lib3mf/release/2.3.2/README.md"
readme_content = download_file(readme_url)

# Read the example script content
with open("create_cube_example_complete.py", "r", encoding="utf-8") as file:
    create_cube_example_complete = file.read()

# Insert the example before the documentation section
readme_parts = readme_content.split("## Documentation")
readme_content = readme_parts[0] + "\n\n## Example (Create Cube)\n\n```python\n" + create_cube_example_complete + "\n```\n\n## Documentation" + readme_parts[1]

print(readme_content)

# Setup script
setup(
    name='lib3mf',
    version='2.3.4',
    description='lib3mf is an implementation of the 3D Manufacturing Format file standard',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
