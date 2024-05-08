from setuptools import setup, find_packages
import os

# Function to find the real path of the shared library
def find_real_lib_path():
    lib_folder = os.path.join('lib3mf')  # Adjust the path to where your libraries are
    for item in os.listdir(lib_folder):
        if item.startswith('lib3mf') and item.endswith('.so'):
            full_path = os.path.join(lib_folder, item)
            if os.path.islink(full_path):
                # Resolve the real path
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

setup(
    name='lib3mf',
    version='2.3.1',
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
