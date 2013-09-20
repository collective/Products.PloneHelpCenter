# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = '4.0'

setup(name='Products.PloneHelpCenter',
      version=version,
      description="A simple help-desk style documentation product for Plone.",
      long_description=(open("README.txt").read() + '\n' +
                        open(os.path.join("docs", "INSTALL.txt")).read() + '\n' +
                        open("CHANGES.rst").read() + '\n' +
                        open(os.path.join("docs", "CREDITS.txt")).read()),
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Zope2",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='Zope CMF Plone help documentation',
      author='Plone Documentation Team',
      author_email='plone-docs@lists.sourceforge.net',
      maintainer='Israel Saeta Pérez',
      maintainer_email='dukebody@gmail.com',
      url='https://github.com/collective/Products.PloneHelpCenter',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'lxml',
          'Plone',
          'plone.i18n',
          'Products.contentmigration',
      ],
      )
