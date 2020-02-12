import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LEDdebug", # Replace with your own username
    version="0.0.1",
    author="Peter Milne",
    author_email="peter@ursaleo.com",
    description="UrsaLeo LEDdebug board package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UrsaLeo/LEDdebug",
    packages=setuptools.find_packages(exclude=['test','*.examples']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: APACHE SOFTWARE LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['smbus'],
)
