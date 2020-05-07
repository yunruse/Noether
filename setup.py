import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

packages = setuptools.find_packages()

print(packages)

setuptools.setup(
    name="noether",
    version="0.1.1",
    author="Mia yun Ruse",
    author_email="mia@yunru.se",
    description="Work with physical measurements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunruse/noether",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved",
        "Topic :: Scientific/Engineering",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
