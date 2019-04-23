import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bot_utils",
    version="0.0.6",
    author="Marcus Deh",
    author_email="deh.marcus@outlook.de",
    description="package containing methods and classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theweekendgeek/bot_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
)