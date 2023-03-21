import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polycube",
    version="0.0.1",
    author="Donald R. Sheehy",
    author_email="don.r.sheehy@gmail.com",
    description="A package for constructing polycube models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/polycube",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['solidpython'],
)
