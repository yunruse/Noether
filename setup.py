import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="noether",
    version="0.1.3",
    author="Mia yun Ruse",
    author_email="mia@yunru.se",
    description="Work with physical measurements and constants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunruse/noether",
    project_urls={
        "Bug Tracker": "https://www.notion.so/yunruse/714348466a284bd1b0d1942c81688579",
    },
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved",
        "Topic :: Scientific/Engineering",
        "Development Status :: 3 - Alpha",
    ],
    keywords="physics unit measure constant measurement uncertainty",
    python_requires='>=3.6',
    install_requires=["nestedtext>=1.0.0"],
)
