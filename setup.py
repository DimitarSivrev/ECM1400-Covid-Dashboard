import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid 19 Dashboard",
    version ="0.0.1",
    author="Dimitar Sivrev",
    author_email="sivrevd@gmail.com",
    description="A dashboard for covid 19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DimitarSivrev/ECM1400-Covid-Dashboard",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.9"
)