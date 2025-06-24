from setuptools import setup, find_packages
import re


def get_version():
    with open("piperss/__version__.py", "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*"(.+?)"', content)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find __version__ in piperss/__version__.py")


setup(
    name="piperss",
    version=get_version(),
    author="Keith Henderson",
    description="PipeRSS is minimalistic terminal-based RSS reader.",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "feedparser",
        "requests",
        "readability-lxml",
        "rich",
        "html2text",
    ],
    entry_points={"console_scripts": ["piperss = piperss.main:main"]},
    python_requires=">=3.7",
)
