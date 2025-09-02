# WoW Sim Sod/WotLK/Cataclysm/MoP Auto-Updater

This script is designed to automatically update the World of Warcraft Simulator (WoW Sim) for Season of Discovery (Classic Era), Wrath of the Lich King (WotLK), Cataclysm and Mists of Pandaria (MoP). It checks for the latest release of the simulator from a specified GitHub repository, downloads it if it is newer than the current version, and then unzips and runs the simulator.

## Features

- Checks for the latest release version from the GitHub repository.
- Downloads the latest release if it is not already present or if there is a new version.
- Unzips the downloaded file.
- Automatically terminates the running WoW Sim process before updating.
- Starts the WoW Sim application.

## Requirements

Before running this script, ensure you have Python 3.x installed on your system. Additionally, you will need the dependencies listed in the `requirements.txt` file.

## Installation

1. Clone this repository or download the script to your local machine.
2. Install the required Python libraries by running:

```
pip install -r requirements.txt
```

The script will:

1. Fetch the latest release information from the GitHub repository.
2. Compare the latest release version with the local version (if present).
3. Download the new release if necessary.
4. Unzip the downloaded file.
5. Run the WoW Sim application.

## Configuration

The script uses the following default configuration:

- GitHub API URL for WoW Sim WotLK releases: `https://api.github.com/repos/wowsims/wotlk/releases/latest`
- Release file name pattern: `wowsimwotlk-windows.exe.zip`
- Executable file name: `wowsimwotlk-windows.exe`

If you need to update these values, modify the respective variables in the script.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your improvements.

## License

[MIT License](LICENSE)

## Acknowledgments

- Thanks to the maintainers of the WoW Sim project for providing the community with useful tools.

---

For more information, questions, or feedback, please open an issue in this repository.
