import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_model",
    version="4.2.1",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="Biobb_model is the Biobb module collection to check and model 3d structures, create mutations or reconstruct missing atoms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_model",
    project_urls={
        "Documentation": "http://biobb-model.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    install_requires=[
        'biobb_common==4.2.0',
        'biobb_structure_checking>=3.13.4',
        'xmltodict'
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "checking_log = biobb_model.model.checking_log:main",
            "fix_chirality = biobb_model.model.fix_chirality:main",
            "fix_amides = biobb_model.model.fix_amides:main",
            "fix_altlocs = biobb_model.model.fix_altlocs:main",
            "fix_ssbonds = biobb_model.model.fix_ssbonds:main",
            "fix_backbone = biobb_model.model.fix_backbone:main",
            "fix_side_chain = biobb_model.model.fix_side_chain:main",
            "mutate = biobb_model.model.mutate:main",
            "fix_pdb = biobb_model.model.fix_pdb:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ],
)
