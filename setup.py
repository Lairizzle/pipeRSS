from setuptools import setup, find_packages

setup(
    name="piperss",
    version="0.1.0",
    author="Keith Henderson",
    description="PipeRSS is minimalistic terminal-based RSS reader.",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "feedparser",
        "requests",
        "readability-lxml",
        "beautifulsoup4",
        "rich",
        "html2text",
    ],
    entry_points={"console_scripts": ["piperss = piperss.main:main"]},
    python_requires=">=3.7",
)
