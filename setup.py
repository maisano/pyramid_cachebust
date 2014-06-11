import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid>=1.0.2', # wsgiref server entry point
]

setup(name='pyramid_cachebust',
      version='0.1.1',
      description='Nascent cache busting for the Pyramid web framework',
      long_description=README,
      classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        ],
      keywords='web wsgi pylons pyramid cachebust',
      author="maisano",
      author_email="rickmaisano@gmail.com",
      maintainer="maisano",
      maintainer_email="rickmaisano@gmail.com",
      url="https://github.com/maisano/pyramid_cachebust",
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite="pyramid_cachebust.tests",
      )
