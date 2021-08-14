# Copyright (C) 2021 Featyre
# 
# This file is part of Discord Web Build Archiver.
# 
# Discord Web Build Archiver is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Discord Web Build Archiver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Discord Web Build Archiver.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
import urllib.request
from bs4 import BeautifulSoup
import jsbeautifier
import cssbeautifier
import logging
import shutil
import datetime
from pytz import timezone

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

assetNameCheck = '[a-zA-Z0-9.]+\.(png|ico|mp3|svg|js|css|woff|woff2|webm|jpg|jpeg)'
jsFiles = None


def formatJSandCSS():
    print("Beautifying JS and CSS... (This can take a while)")
    logging.info("Beautifying JS and CSS...")
    assetFolderList = os.listdir(os.path.join(__location__, 'build', 'assets'))
    for assetFile in assetFolderList:
        if assetFile.endswith('.js') or assetFile.endswith('.css'):
            with open(os.path.join(__location__, 'build', 'assets', assetFile), 'r+', encoding='utf-8') as f:
                lines = f.read()
                f.seek(0)
                if assetFile.endswith('.js'):
                    f.write(jsbeautifier.beautify(lines))
                else:
                    f.write(cssbeautifier.beautify(lines))
                f.truncate()
    print("Done!")
    logging.info("Done!")


def downloadFile(assetFileName, assetFileNameLine, url, finalFilename):
    logging.info(f'Asset found in line {assetFileNameLine+1} in {assetFileName}')
    try:
        openURL = urllib.request.urlopen(urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'}))
    except Exception as e:
        logging.error(f"{str(e)} | Either your internet is broken, file doesn't exist in Discord's server or regex found a false positive.")
        logging.error(f'Asset in line is: {finalFilename}')
        return False
    logging.info(f'Downloading {finalFilename}')
    with open(os.path.join(__location__, 'build', 'assets', finalFilename), 'wb') as f:
        f.write(openURL.read())
        logging.info("Done!")
    return True


def readFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

# Some pretty thing idk

print("""                                                                                                        
  ____  _                       ___        __   _     ____        _ _     _    _             _     _                
 |  _ \(_)___  ___ ___  _ __ __| \ \      / /__| |__ | __ ) _   _(_) | __| |  / \   _ __ ___| |__ (_)_   _____ _ __ 
 | | | | / __|/ __/ _ \| '__/ _` |\ \ /\ / / _ \ '_ \|  _ \| | | | | |/ _` | / _ \ | '__/ __| '_ \| \ \ / / _ \ '__|
 | |_| | \__ \ (_| (_) | | | (_| | \ V  V /  __/ |_) | |_) | |_| | | | (_| |/ ___ \| | | (__| | | | |\ V /  __/ |   
 |____/|_|___/\___\___/|_|  \__,_|  \_/\_/ \___|_.__/|____/ \__,_|_|_|\__,_/_/   \_\_|  \___|_| |_|_| \_/ \___|_|   

By Featyre, as a part of the Nostalgicord Project.
https://github.com/Nostalgicord/Discord-Web-Build-Archiver
Version 1.0
""")

if not os.path.exists(os.path.join(__location__, 'logs')):
    os.makedirs(os.path.join(__location__, 'logs'))
if not os.path.exists(os.path.join(__location__, 'build')):
    os.makedirs(os.path.join(__location__, 'build'))

if not os.path.exists(os.path.join(__location__, 'build', 'assets')):
    os.makedirs(os.path.join(__location__, 'build', 'assets'))
else:
    shutil.rmtree(os.path.join(__location__, 'build', 'assets'))
    os.makedirs(os.path.join(__location__, 'build', 'assets'))

dateNow = datetime.datetime.now(timezone('UTC'))

logging.basicConfig(
    level=logging.NOTSET,
    filename=f'{__location__}/logs/DWBA-{dateNow.strftime("%d-%b-%Y-%H-%M-%S")}.log',
    filemode='w',
    format=f'{dateNow.strftime("%d-%b-%Y %H:%M:%S")} | %(levelname)s - %(message)s'
)

print("If you think you're stuck, check the logs inside the logs folder for anything unusual and report the bug.")
input("Please put your Discord web build's index.html inside the build folder and press the Enter key to begin.")
while True:
    if not os.path.exists(os.path.join(__location__, 'build', 'index.html')):
        input("Index.html not found, please try again.")
        logging.error("User did not input index.html.")
    else:
        break

passes = input("How many times does the downloader downloads assets? (Two is minimum, Three is recommended.) ")
while True:
    if int(passes) >= 2:
        break
    else:
        print("No number inserted or inserted number is below 2, please try again.")
        passes = input("How many times does the downloader downloads assets? (Two is minimum, Three is recommended.) ")
        logging.error("User did not input number or inserted number is below 2.")

logging.info(f"User inputed {passes}x download.")

# Read index.html, pretties it and then download the first batch of JS Files

with open(os.path.join(__location__, 'build', 'index.html'), 'r+', encoding='utf-8') as f:
    lines = f.read()
    f.seek(0)
    print("Beautifying HTML...")
    logging.info("Beautifying HTML...")
    f.write(BeautifulSoup(lines, features="html.parser").prettify())
    f.truncate()
    print("Done!")
    logging.info("Done!")

print("Downloading the first batch of JS and CSS files...")
logging.info("Downloading the first batch of JS and CSS files...")

for i, line in enumerate(readFile(os.path.join(__location__, 'build', 'index.html'))):
    assetName = re.search(assetNameCheck, line)
    if assetName:
        if not downloadFile('index.html', i, f'https://discord.com/assets/{assetName.group()}', assetName.group()):
            continue

print("Done!")
logging.info("Done!")

# Formats the JS Files and downloads the second batch of JS Files (and CSS Files)

print("Downloading the second batch of JS and CSS files...")
logging.info("Downloading the second batch of JS and CSS files...")

formatJSandCSS()

assetFolderList = os.listdir(os.path.join(__location__, 'build', 'assets'))
for assetFile in assetFolderList:
    if assetFile.endswith('.js'):
        for i, line in enumerate(readFile(os.path.join(__location__, 'build', 'assets', assetFile))):
            if re.search('= "/assets/"', line):
                jsFiles = assetFile
                logging.info(f"The all JS and CSS file list file is {jsFiles}")
                break

for i, line in enumerate(readFile(os.path.join(__location__, 'build', 'assets', jsFiles))):
    assetNameListCheck = re.search('[0-9]+: "[a-zA-Z0-9]+"', line)
    if assetNameListCheck:
        listNumber = re.search(
            '[0-9]+', re.search('[0-9]+:', assetNameListCheck.group()).group())
        assetName = re.search(
            '[a-zA-Z0-9]+', re.search('"[a-zA-Z0-9]+"', assetNameListCheck.group()).group())
        if assetName and not os.path.exists(os.path.join(__location__, 'build', 'assets', f'{listNumber.group()}.{assetName.group()}.css')) or not os.path.exists(os.path.join(__location__, 'build', 'assets', f'{assetName.group()}.css')) or not os.path.exists(os.path.join(__location__, 'build', 'assets', f'{listNumber.group()}.{assetName.group()}.js')) or not os.path.exists(os.path.join(__location__, 'build', 'assets', f'{assetName.group()}.js')):
            if not downloadFile(jsFiles, i, f'https://discord.com/assets/{listNumber.group()}.{assetName.group()}.css', f'{listNumber.group()}.{assetName.group()}.css'):
                if not downloadFile(jsFiles, i, f'https://discord.com/assets/{assetName.group()}.css', f'{assetName.group()}.css'):
                    if not downloadFile(jsFiles, i, f'https://discord.com/assets/{listNumber.group()}.{assetName.group()}.js', f'{listNumber.group()}.{assetName.group()}.js'):
                        if not downloadFile(jsFiles, i, f'https://discord.com/assets/{assetName.group()}.js', f'{assetName.group()}.js'):
                            continue

print("Done!")
logging.info("Done!")

# Downloads the rest, according to user selected passes

print("Downloading the rest of the assets... (This can take a while)")
logging.info("Downloading the rest of the assets...")

for t in range(int(passes)):
    print(f"Times: {t+1}")
    logging.info(f"Pass: {t+1}")
    formatJSandCSS()
    assetList = os.listdir(os.path.join(__location__, 'build', 'assets'))
    print("Downloading...")
    logging.info("Downloading the assets...")
    for asset in assetList:
        if asset.endswith('.js') or asset.endswith('.css'):
            for i, line in enumerate(readFile(os.path.join(__location__, 'build', 'assets', asset))):
                foundAsset = re.search(assetNameCheck, line)
                if foundAsset and not os.path.exists(os.path.join(__location__, 'build', 'assets', foundAsset.group())):
                    if not downloadFile(asset, i, f'https://discord.com/assets/{foundAsset.group()}', foundAsset.group()):
                        continue
    print("Done!")
    logging.info("Done!")

print("Finished archiving build! Enjoy your day!")
logging.info("Archive finished.")
