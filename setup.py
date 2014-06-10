import os

from setuptools import setup, find_packages


requires = [
    'pyramid>=1.0.2', # wsgiref server entry point
]

setup(name='pyramid_cachebust',
      version='0.1.1',
      description='Nascent cache busting for the Pyramid web framework',
      classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
      keywords='web wsgi pylons pyramid cachebust',
      author="maisano",
      author_email="rickmaisano@gmail.com",
      maintainer="maisano",
      maintainer_email="rickmaisano@gmail.com",
      url="https://github.com/maisano/pyramid_cachebust",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires
      )