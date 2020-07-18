import setuptools

with open("README.md",'r') as file:
    description = file.read()


setuptools.setup(
    name="level2scraper-pkq-futurenowait",
    version="0.1",
    author="Lukas Petravicius",
    author_email="lkspetravicius@gmail.com",
    description="Software to collect level 2 data from crypto exchanges",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/futurenowait/level2Scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)