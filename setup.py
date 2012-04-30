from setuptools import setup, find_packages
import os

_home_dir = os.path.join(os.path.dirname(__file__), 'jcu', 'theme')
version = file(os.path.join(_home_dir, 'version.txt'), 'r').read().strip()

setup(name='jcu.theme',
      version=version,
      description="A Plone theme based on the JCU style",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi
      #?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone theme zope web',
      author='JCU eResearch Centre',
      author_email='eresearch@jcu.edu.au',
      url='http://eresearch.jcu.edu.au',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['jcu'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=[
          'setuptools-git',
      ],
      install_requires=[
          'setuptools',
          'zope.annotation',
          'Products.CMFPlone>=4.1',
          'plone.app.caching',
          'plone.app.discussion',
          'plone.app.ldap',
          'plone.app.z3cform',
          'plone.formwidget.recaptcha',
          'Products.Collage',
          'Products.OpenXml',
          'Products.RedirectionTool',
          'Products.TinyMCE>=1.2.3',
          'collective.contentleadimage',
          'collective.fastview',
          'collective.recaptcha',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'unittest2',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
