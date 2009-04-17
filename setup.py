from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='explore.theme',
      version=version,
      description="A Plone 3 theme for the Explore site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone theme',
      author='JCU eResearch Centre',
      author_email='david.breitkreutz@jcu.edu.au',
      url='http://eresearch.jcu.edu.au/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['explore'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
