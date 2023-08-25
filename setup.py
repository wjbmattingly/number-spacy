from setuptools import setup, find_packages

setup(
    name="number_spacy",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0",
        "word2number"
    ],
    author="WJB Mattingly",
    description="A spaCy extension for enhanced number entity recognition and extraction as structured data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wjbmattingly/number-spacy",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
