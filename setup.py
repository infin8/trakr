from setuptools import setup, find_packages
import sys, os

version = '0.1'
NAME='trakr'
setup(name=NAME,
      version=version,
      description="tracking",
      long_description="""\
tracking without all the fluff""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='tracking analytics',
      author='n8',
      author_email='yo.its.n8@gmail.com',
      url='http://trakr.mobi',
      license='AGPL',
      packages=[NAME] + ['twisted.plugins'] + find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={'twisted': ['twisted/plugins/trakr_plugin.py']},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          filter(str, map(str.strip,
        """
            Twisted==13.0.0
            bottle==0.11.6
            pymongo==2.5.2
        """.splitlines()))
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
