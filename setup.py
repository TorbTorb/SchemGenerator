import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "SchemGenerator",
    version = "1.0.5",
    author = "Torb",
    description = "A Package for creating minecraft schematics",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/TorbTorb/SchemGenerator",
    project_urls = {
        "Bug Tracker": "https://github.com/TorbTorb/SchemGenerator/issues",
        "repository": "https://github.com/TorbTorb/SchemGenerator/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'NBT',
      ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.10"
)