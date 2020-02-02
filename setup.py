import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daemon-process",
    version="0.9.1",
    author="J4CK VVH173",
    author_email="p78901234567890@gmail.com",
    description="The package for running daemonized processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/J4CKVVH173/python-daemonization.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Classifier: Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: Unix",
    ],
    python_requires='>=3',
)
