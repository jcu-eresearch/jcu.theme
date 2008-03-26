from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='jcu.theme',
      version=version,
      description="A Plone theme based on the JCU style",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone theme zope web',
      author='Russell Sim',
      author_email='russell.sim@jcu.edu.au',
      url='http://www.hpc.jcu.edu.au/projects/plone',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['jcu'],
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
