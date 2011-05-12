# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = '4.0b3'

setup(name='Products.PloneHelpCenter',
      version=version,
      description="A simple help-desk style documentation product for Plone.",
      long_description= open("README.txt").read() + '\n' +
                        open(os.path.join("docs", "INSTALL.txt")).read() + '\n' +
                        open(os.path.join("docs", "HISTORY.txt")).read() + '\n' +
                        open(os.path.join("docs", "CREDITS.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone help documentation',
      author='Plone Documentation Team',
      author_email='plone-docs@lists.sourceforge.net',
      maintainer='Israel Saeta Pérez',
      maintainer_email='dukebody@gmail.com',
      url='http://svn.plone.org/svn/collective/Products.PloneHelpCenter/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/plonehelpcenter',
      install_requires=[
        'setuptools',
        'lxml',
        'Plone',
        'plone.i18n',
        'Products.contentmigration',
      ],
)
