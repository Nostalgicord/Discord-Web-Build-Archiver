# Discord Web Build Archiver
![GitHub release (latest by date)](https://img.shields.io/github/downloads/Nostalgicord/Discord-Web-Build-Archiver/latest/total)
![GitHub](https://img.shields.io/github/license/Nostalgicord/Discord-Web-Build-Archiver)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md) 

Archive Discord web builds by only using the build's index.html file, using Python and Regex.

## Roadmap
1. Speed up download assets.
2. Decrease false positive regex matches.

## How to use
1. Install libraries from `requirements.txt`
2. Run `main.py` 
3. Insert you Discord web build's index.html inside `project root/build`
4. Insert the number of times to download assets. (Sometimes the JS files downloads other JS files which include other assets, this just maximize the files range.)
5. Sit back for 2-5 hours and that's it!

## Contribution
Check `code_of_conduct.md` for details.

## License 
Discord Web Build Archiver is licensed under GPTv3, please don't copy any code without any credit, or copy any code to a closed sourced project.
