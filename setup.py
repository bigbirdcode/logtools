from setuptools import find_packages
from setuptools import setup

long_description = """
Log viewer application that displays separate runs from a log file
in separate tabs and enable fast searching pre-defined patterns.
"""

setup(
    name="logtools",
    version="0.1",
    url="https://github.com/bigbirdcode/logtools",
    license="MIT License",
    author="BigBirdCode",
    author_email="na",
    description="Log viewer application",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Desktop Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Development",
        "Topic :: Utilities",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "wxPython>=4.0",
        "strictyaml",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "pylint",
        ],
    },
    entry_points={"gui_scripts": ["logtools = logtools.main:main"]},
)
