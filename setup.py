import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="noether",
    version="1.0.0",
    author="Mia yun Ruse",
    author_email="mia@yunru.se",
    description="Work with physical measurements and constants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunruse/noether",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved",
        "Topic :: Scientific/Engineering",
        "Development Status :: 4 - Beta",
    ],
    keywords="physics unit measure constant measurement uncertainty",
    python_requires='>=3.10'
)
