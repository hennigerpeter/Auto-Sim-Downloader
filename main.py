import requests
import os
import zipfile
import psutil
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d-%m-%y %H:%M:%S',
    filename='sim_downloader.log',
    filemode='w'
)

# Cataclysm
cata_api_repo_url = 'https://api.github.com/repos/wowsims/cata/releases/latest'
cata_release_file_name = 'wowsimcata-windows.exe.zip'
cata_file_name = 'wowsimcata-windows.exe'

# Wrath of the Lich King
wotlk_api_repo_url = 'https://api.github.com/repos/wowsims/wotlk/releases/latest'
wotlk_release_file_name = 'wowsimwotlk-windows.exe.zip'
wotlk_file_name = 'wowsimwotlk-windows.exe'

# Season of Discovery
sod_api_repo_url = 'https://api.github.com//wowsims/sod/releases/latest'
sod_release_file_name = 'wowsimsod-windows.zip'
sod_file_name = 'wowsimsod-windows.exe'


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
        logging.error(f"Failed to fetch latest release. Status Code: {response.status_code}")
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
        logging.error(f"Failed to download the file. Status Code: {response.status_code}")
        return False


def unzip_file(file):
    if file_exists(file):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall()
            zip_ref.close()


def run_sim(file):
    if file_exists(file):
        print(file)
        os.startfile(file)


def download_sim(api_repo_url, release_file_name, file_name):
    # Fetch the latest release information from the GitHub repository.
    release_info = fetch_release_info(api_repo_url)

    if release_info:
        # Extract the release tag/version number from the release information.
        release_tag = release_info['tag_name']
        # Get the download URL for the specified file from the release information.
        download_url = get_download_url(release_info, release_file_name)

        if download_url:
            version_number = None
            if file_exists('version.txt'):
                with open('version.txt') as version:
                    version_number = version.read()

            if version_number != release_tag:
                for proc in psutil.process_iter():
                    # check whether the process name matches
                    if proc.name() == file_name:
                        proc.kill()
                print(f"Downloading latest {release_file_name} from Github. {release_tag}")
                logging.info(f"Downloading latest {release_file_name} from Github. {release_tag}")
                # Download the file and update the local version number.
                if download_file(download_url, release_file_name, release_tag):
                    print("Download complete.")
                    logging.info("Download complete.")
                    # Unzip downloaded file
                    unzip_file(release_file_name)
                else:
                    print("Failed to download the file.")
                    logging.error("Failed to download the file.")
            else:
                print(f"You already have the latest version {version_number}.")
                logging.warning(f"You already have the latest version {version_number}.")
        else:
            print("Download URL not found.")
            logging.critical(f"Download URL {download_url} not found.")


def cataclysm():
    download_sim(cata_api_repo_url, cata_release_file_name, cata_file_name)
    run_sim(cata_file_name)


def wrath_of_the_lich_king():
    download_sim(wotlk_api_repo_url, wotlk_release_file_name, wotlk_file_name)
    run_sim(wotlk_file_name)


def season_of_discovery():
    download_sim(sod_api_repo_url, sod_release_file_name, sod_file_name)
    run_sim(sod_file_name)


if __name__ == "__main__":
    cataclysm()
