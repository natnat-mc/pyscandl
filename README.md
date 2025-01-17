# pyscandl
**DISCLAIMER:** This project is just a technical demo, don't download scans and get the mangas from official retailers when they are accessible in your country

This modular program to be able to download manga and webtoon scans from the internet, it'll use an image fetcher specific for each website while respecting an API.  
The API will enable you to create your own image fetchers for other websites not supported yet by the program.

## dependence and installation
This is a python3 program that uses:
- `argparse` for the main
- [`selenium`](https://selenium-python.readthedocs.io/installation.html) for some of the default parsers
- `requests` for some other parsers
- `img2pdf` to create the pdfs of the scans
- `os`, `re` and `enum` are also needed

It is developed on a Debian 10 Buster computer so it is verified for Debian 10 and should work at least for the older debians and the debian-likes, provided that you have the dependencies listed up above.  
As for other linux distribution, windows and MacOSX I haven't tested the compatibility but it may work if you have all the dependencies.

To install the program clone or download the repository and either launch from command line the program or use it in python3 itself.

## command line interface
`python3 main.py [--keep-images|-k] [--quiet|-q] <--fetcher|-f fname> <--link|-l link | --manga|-m mname> [--chapter-start|-c chapnumber] [--all|-a | --download-number|-n number] [--output|-o path] [--start|-s number]`

- `--output` or `-o` **required**: the path (absolute or relative) to the folder where to save the data, the images will be stored in a subfolder `images` with inside one folder per chapter and the pdfs will be stored in a `pdf` subfolder 
- `--fetcher` or `-f` **required**: the name of the image links fetcher that will be used for the download
- `--link` or `-l` **required if not using `--manga` or `-m`**: gives the link to the page with all the chapter listed
- `--manga` or `-m` **required if not using `--link` or `-l`**: gives the manga name, the image fetcher will find the corresponding manga
- `--chapter-start` or `-c`: gives the chapter to start the download on (defaults at 1)
- `--download-number` or `-n`: gives the number of chapters to download (defaults at 1)
- `--all` or `-a`: downloads all the chapters from the starting point to the end
- `--keep-images` or `-k`: the images used for the pdf will be kept in their corresponding folder
- `--quiet` or `-q`: removes the verbose of the downloads
- `--skip` or `-s`: skips `n` images before starting to download the first chapter

## image fetcher API
- `.image` is a `string` with link to the image  
- `.next_image()` changes `.image` to the next in the chapter  
- `.next_chapter()` changes `.image` to the first in the next chapter
- `.is_last_image()` which returns `True` if it's the last page of the chapter
- `.is_last_chapter()` which returns `True` if it's the last chapter available 
- `.manga_name` is a `string` with the complete name of the manga or the webtoon of the current `.image`
- `.chapter_number` is an `int` (or a `float` if the chapter is an extra) containing the number of the chapter or the current `.image`
- `.chapter_name` is a `string` containing the title of the chapter of the current `.image` (the `string` is empty if no name is detected) 
- `.npage` is an `int` giving the current page of the fetcher
- `quit()` to close properly the fetcher

## Pyscandl()
`Pyscandl(self, fetcher, chapstart:int=1, output:str=".", keepimage:bool=False, all:bool=False, link:str=None, manga:str=None, download_number:int=1, quiet:bool=False, start:int=0)`

### args and kwargs
- `fetcher` will be the fetcher object used in this instance, there will be an `enum` with all the fetchers available (I strongly recommend if you make your own fetcher to place it in the enum too)
- `chapstart=` is an `int` (or a `float` in case of extra chapters) for the starting point of the fetching
- `output=` determines the output folder for the pdfs and the images (if kept)
- `keepimage=` determines if the images are downloaded instead of loaded into the RAM
- `all=` determines if you need to download all the available chapters or not
- `link=` **required if not using `manga=`**, is a `string` containing the link to the root page with the list of all the chapters
- `manga=` **required if not using `link=`**, is a `string` containing the complete manga name
- `download_number=` **required if `all=False`**, is an `int` containing the number of chapters we need to download
- `quiet=` deactivates the verbose while downloading

