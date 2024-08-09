"""
This script downloads all packages of ssv2 module, from
this site:
https://developer.qualcomm.com/software/ai-datasets/something-something
"""

import subprocess
import requests
import os

def download_files(links, folder_path):
    download_succedded = True

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for link in links:
        filename = link.split('/')[-1]  # Gets filename from link
        filepath = os.path.join(folder_path, filename)

        for i in range(5):

            print(f"Downloading {filename}...")
            try:
                response = requests.get(link)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"{filename} correctly downloaded.")
                break
            except requests.exceptions.RequestException as e:
                print(f"Failed on download {filename}: {e} - {i} attempt")
                if i == 4:
                    print(f"Failed on download {filename} - desisted.")
                    download_succedded = False
                # Last attempt

    return download_succedded

def run_recommended_commands(self, cmds_list):
    for cmd in cmds_list:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)

def main():
    links = [
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-instructions?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-00?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-01?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-02?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-03?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-04?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-05?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-06?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-07?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-08?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-09?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-10?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-11?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-12?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-13?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-14?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-15?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-16?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-17?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-18?referrer=node/68935",
        "https://developer.qualcomm.com/downloads/20bn-something-something-download-package-19?referrer=node/68935",
    ]
    folder_path = './downloads' # Folder to save downloaded files

    download_result = download_files(links, folder_path)

    if download_result:
        # All files were successfully downloaded
        print("All files were successfully downloaded")
        run_recommended_commands([
            "unzip 20bn-something-something-v2-\??.zip",
            "cat 20bn-something-something-v2-?? | tar -xvzf –"
        ])

if __name__ == "__main__":
    main()