import setuptools

# with open("../README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="aio",
    version="0.0.3",
    author="AIO",
    author_email="maintainer@aioneers.com",
    description="AIO tools",
    #    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aioneers/aio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytest",
        "pydata_sphinx_theme",
        "nbsphinx",
        "numpydoc",
        "numpy",
        "pandas",
    ],
)
