from setuptools import setup

setup(name='robin_stocks',
      version='0.1',
      description='Made to interact with the Robinhood API',
      url='https://github.com/jmfernandes/Robinhood',
      author='Josh Fernandes',
      author_email='joshfernandes@mac.com',
      license='MIT',
      python_requires='>=3',
      packages=['robin_stocks'],
      requires=['requests'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
