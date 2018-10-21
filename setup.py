import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_model",
    version="0.0.5",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="biobb_model is the Biobb module collection to fetch data to be consumed by the rest of the Biobb building blocks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_model",
    project_urls={
        "Documentation": "http://biobb_model.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test', 'cwl', 'notebooks',]),
    install_requires=['mistune==0.7.4', 'jsonschema==2.6.0', 'biobb_common', 'biopython' ],
    python_requires='>=3.5',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
