import requests
import os
import zipfile
import psutil


def file_exists(file_path):
    # check if given file exists
    return os.path.exists(file_path)


def fetch_release_info(repo_url):
    # Fetches the release information from the given GitHub repository URL.
    response = requests.get(repo_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch latest release. Status Code: {response.status_code}")
        return None


def get_download_url(release_info, file_name):
    # Gets the download URL for the specified file from the release information.
    for asset in release_info['assets']:
        if asset['name'].lower() == file_name.lower():
            return asset['browser_download_url']
    return None


def download_file(url, file_name, file_version):
    # Downloads the file from the given URL and writes it to disk.
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        with open('version.txt', 'w') as version:
            version.write(file_version)
        return True
    else:
        print(f"Failed to download the file. Status Code: {response.status_code}")
        return False


def unzip_file(file):
    if file_exists(file):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()


def run_sim(file):
    if file_exists(file):
        os.startfile(file)


if __name__ == "__main__":
    # GitHub API URL for the latest release.
    api_repo_url = 'https://api.github.com/repos/wowsims/wotlk/releases/latest'
    release_file_name = 'wowsimwotlk-windows.exe.zip'
    file_name = 'wowsimwotlk-windows.exe'

    # Fetch the latest release information from the GitHub repository.
    release_info = fetch_release_info(api_repo_url)
    if release_info:
        # Extract the release tag/version number from the release information.
        release_tag = release_info['tag_name']
        # Get the download URL for the specified file from the release information.
        download_url = get_download_url(release_info, release_file_name)

        if download_url:
            if file_exists(release_file_name):
                # Check if the local version number matches the latest release tag.
                with open('version.txt') as version:
                    version_number = version.read()
                    if version_number != release_tag:
                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'wowsimwotlk-windows.exe':
                                proc.kill()
                        print(f"Downloading latest {release_file_name} from Github. {release_tag}")
                        # Download the file and update the local version number.
                        if download_file(download_url, release_file_name, release_tag):
                            print("Download complete.")
                            # Unzip downloaded file
                            unzip_file(release_file_name)
                        else:
                            print("Failed to download the file.")
                    else:
                        print(f"You already have the latest version {version_number}.")
            else:
                print(f"Downloading latest {release_file_name} from Github. {release_tag}")
                # Download the file and update the local version number.
                if download_file(download_url, release_file_name, release_tag):
                    print("Download complete.")
                    # Unzip downloaded file
                    unzip_file(release_file_name)

        run_sim(file_name)
