from setuptools import setup, find_packages

setup(
  name='coinhopper',
  version='0.0.1',
  description='coinhopper',
  py_modules=['coinhopper.coinhopper', 'coinhopper.api'],
  packages=find_packages(include=['src', 'src.*']),
  package_dir={'': 'src'},
  install_requires=[
    'aiogram',
    'aiohttp',
    'requests',
    'typing_extensions'
  ],
  entry_points={
    'console_scripts': [
        'coinhopper=coinhopper.coinhopper:main',
    ],
  }
)
