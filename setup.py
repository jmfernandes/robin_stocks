from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='robin_stocks',
      version='2.1.0',
      description='A Python wrapper around the Robinhood API',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/jmfernandes/robin_stocks',
      author='Josh Fernandes',
      author_email='joshfernandes@mac.com',
      keywords=['robinhood','robin stocks','finance app','stocks','options','trading','investing'],
      license='MIT',
      python_requires='>=3',
      packages=find_packages(),
      requires=['requests', 'pyotp', 'cryptography'],
      install_requires=[
          'requests',
          'pyotp',
          'python-dotenv',
          'cryptography'
      ],
      zip_safe=False)
