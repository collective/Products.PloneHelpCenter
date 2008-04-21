from setuptools import setup, find_packages

version = '1.5b7'

setup(name='Products.PloneHelpCenter',
      version=version,
      description="A simple help-desk style documentation product for Plone.",
      long_description= open("Products/PloneHelpCenter/README.txt").read() + \
                        open("Products/PloneHelpCenter//INSTALL.txt").read() + \
                        open("Products/PloneHelpCenter//CREDITS.txt").read() + \
                        open("Products/PloneHelpCenter//HISTORY.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone help documentation',
      author='Plone Documentation Team',
      author_email='plone-docs@lists.sourceforge.net',
      maintainer='Steve McMahon',
      maintainer_email='steve@dcn.org',
      url='http://svn.plone.org/svn/collective/Products.PloneHelpCenter/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/plonehelpcenter',
      install_requires=[
        'setuptools',
        'plone.i18n',
      ],
)
