from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='Pictures Keywords Extractor',
      version='0.0.1',
      license='MIT',
      description="Horrible GUI wrapper for the great Exiftool by Phil Harvey. Extracts user generated keywords from the metadata of all pictures in a specific folder into a .csv",
      author="Corentin Dubois",
      author_email="corentindubois22@gmail.com",
      install_requires=requirements,
      packages=find_packages())
