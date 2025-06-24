# PipeRSS

## What is PipeRSS?

PipeRSS is a fast, elegant, and fully terminal-based RSS reader designed for power users who want to stay updated without leaving their command line. 

Featuring:

- Clean, readable article rendering with smart paragraph handling
- Support for Markdown-like formatting including headers, bullet lists, and code blocks
- Interactive pagination with intuitive navigation commands
- Beautiful syntax highlighting for code, links, and inline elements
- Minimal dependencies
- Custom theme options in theme.conf

## Features

- Fetch and display full articles from RSS feeds
- Intelligent paragraph splitting and line wrapping
- Syntax highlighting for headers, bullet lists, numbered lists, code blocks, inline code, and URLs
- Centered article display for optimal readability
- Simple keyboard navigation: `[Enter]` next page, `[b]` back, `[m]` menu, `[q]` quit
- Fully customizable via Python code

## Installation

### Easy Install with pipx (Recommended) 
Requires: pipx

Arch:
```
sudo pacman -S python-pipx
pipx ensurepath
pipx install piperss
```
Debian
```
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install piperss

```
RHEL/Fedora
```
sudo dnf install pipx
pipx ensurepath
pipx install piperss
```

### Pip Install
```
pip install piperss
```

### Arch PACKAGEBUILD (will install python dependencies globally)
PipeRSS is not on the AUR so if you are on Arch and want to build the package do the following:

```
mkdir piperss-pkgbuild
cd piperss-pkgbuild
curl -O https://raw.githubusercontent.com/Lairizzle/pipeRSS/master/PKGBUILD
makepkg -si
```

## Feed List
Feeds are stored in ~/.config/piperss/feeds.txt
You can add them inside PipeRSS itself or you can add a list manually here.


## Themes
Themes use the standard rich colour values
You can set these with the names or the hex values
https://rich.readthedocs.io/en/stable/appendix/colors.html

This is a gruvbox style theme
```
#~/.config/piperss/theme.conf

[theme]
title = dark_orange     
header = light_goldenrod3  
border = grey37         
accent = yellow3     
error = indian_red
```


