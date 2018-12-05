from setuptools import setup, find_packages

setup(name='mosaik_fmume_test',
      version='0.1',
      description='Test adapter for FMUs for ME in mosaik',
      author='Cornelius Steinbrink',
      author_email='cornelius.steinbrink at offis.de',
      url='',
      install_requires=[
          'mosaik-api>=2.0',
      ],
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          'Private :: Do Not Upload',
      ],
)