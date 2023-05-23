from setuptools import find_packages, setup

setup(
    name='triesus',
    version='0.1.0',
    description='Find the Smallest Unique Subset (SUS)',
    url='https://github.com/alussana/TrieSUS',
    author='Alessandro Lussana',
    author_email='alessandro.lussana@proton.me',
    license='MIT',
    packages=find_packages(),
    scripts=['bin/triesus']
)