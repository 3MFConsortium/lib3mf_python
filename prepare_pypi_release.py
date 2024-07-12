import os
import sys
import requests
import zipfile
import io
import shutil
import subprocess

# Download SDK directly to zip object
def download_sdk_zip(url):
    response = requests.get(url)
    if response.status_code == 200:
        return zipfile.ZipFile(io.BytesIO(response.content))
    else:
        raise Exception(f"Failed to download SDK zip from {url}")


# Clean up and remove unnecessary stuff from lib3mf directory
def clean_lib3mf_directory(lib3mf_dir):
    valid_extensions = {'.so', '.dylib', '.dll', 'Lib3MF.py', '__init__.py'}
    before_path = os.getcwd()
    os.chdir(lib3mf_dir)
    for item in os.listdir():
        if not any(item.endswith(ext) for ext in valid_extensions):
            os.unlink(item)
    os.chdir(before_path)
    print("Remove unnecessary files and cleaned up the lib3mf directory")


# Extract the libraries and necessary files to the lib3mf directory
def extract_bin_and_bindings(zip_file, lib3mf_dir):
    bin_dir = None
    bindings_python_file = None

    for file in zip_file.namelist():
        if 'Bin/' in file and bin_dir is None:
            bin_dir = os.path.dirname(file)
        if 'Bindings/Python/Lib3MF.py' in file:
            bindings_python_file = file

    if bin_dir is None or bindings_python_file is None:
        raise FileNotFoundError("Required directories or files not found in the SDK zip")

    for file in zip_file.namelist():
        if file.startswith(bin_dir) and not file.endswith('/'):
            destination_path = os.path.join(lib3mf_dir, os.path.basename(file))
            with zip_file.open(file) as source, open(destination_path, "wb") as target:
                shutil.copyfileobj(source, target)
        if str(file).endswith('Lib3MF.py'):
            destination_path = os.path.join(lib3mf_dir, os.path.basename(file))
            with zip_file.open(file) as source, open(destination_path, "wb") as target:
                shutil.copyfileobj(source, target)

    print(f"Copied the latest version of bindings to the lib3mf directory")
    clean_lib3mf_directory(lib3mf_dir)


# Update the contents of setup.py folder
def update_setup_file(version):
    setup_file = "setup.py"
    new_readme_url = f"https://raw.githubusercontent.com/3MFConsortium/lib3mf/release/{version}/README.md"
    new_version = version

    with open(setup_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(setup_file, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip().startswith("readme_url = "):
                line = f'readme_url = "{new_readme_url}"\n'
            if line.strip().startswith("version="):
                line = f"    version='{new_version}',\n"
            file.write(line)

    print(f"Updated {setup_file} with version {new_version} and README URL {new_readme_url}")

# Is it there already ?
def check_version_exists_on_pypi(package_name, version):
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    response = requests.get(url)
    return response.status_code == 200

# Deal with git also here
def git_commit_and_push(version, update_existing=False):
    try:
        commit_message = f"Updating Release version {version}" if update_existing else f"Release version {version}"
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        print(f"Successfully committed and pushed: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to commit and push: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_pypi_release.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    update_setup_file(version)
    sdk_url = f"https://github.com/3MFConsortium/lib3mf/releases/download/v{version}/lib3mf_sdk_v{version}.zip"

    zip_file = download_sdk_zip(sdk_url)

    lib3mf_dir = os.path.join(os.path.dirname(__file__), 'lib3mf')
    if not os.path.exists(lib3mf_dir):
        os.makedirs(lib3mf_dir)

    extract_bin_and_bindings(zip_file, lib3mf_dir)

    package_name = "lib3mf"
    update_existing = check_version_exists_on_pypi(package_name, version)
    git_commit_and_push(version, update_existing)