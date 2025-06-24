from setuptools import setup, find_packages

setup(
    name="piperss",
    version="0.1.5",
    author="Keith Henderson",
    description="PipeRSS is minimalistic terminal-based RSS reader.",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["piperss = piperss.main:main"]},
    python_requires=">=3.7",
)
