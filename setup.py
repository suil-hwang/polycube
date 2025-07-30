import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polycube",
    version="0.1.0",  
    author="Donald R. Sheehy",
    author_email="don.r.sheehy@gmail.com",
    description="A package for constructing polycube models with mesh I/O support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/polycube",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  
    install_requires=[
        'solidpython',
        'trimesh>=3.9.0',
        'pyvista>=0.32.0',
        'numpy>=1.19.0',
        'scipy>=1.5.0',  
    ],
)