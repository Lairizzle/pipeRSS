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

## Installation

### Source Code 
Clone this repo and install dependencies:

```bash
git clone https://github.com/lairizzle/piperss.git
cd piperss
pip install -r requirements.txt
```
### Install with pip
```
pip install piperss
```
### Arch Based
PipeRSS is not on the AUR so if you are on Arch do the following:

```
mkdir piperss-pkgbuild
cd piperss-pkgbuild
curl -O https://raw.githubusercontent.com/Lairizzle/pipeRSS/master/PKGBUILD
makepkg -si
```

### Debian Based
```
sudo dpkg -i piperss_0.1.3_all.deb
piperss --version
```

## RPM Based
```
sudo rpm -i piperss-0.1.3-1.noarch.rpm
piperss --version
```
