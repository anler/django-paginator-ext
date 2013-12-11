import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

py_version = sys.version_info[:2]

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, "README.rst")).read()
    README += open(os.path.join(here, "HISTORY.rst")).read()
except IOError:
    README = "https://github.com/ikame/django-pagination-again"


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name="django-pagination-again",
      version="0.1",
      description="Extensions over Django's default pagination capabilities.",
      long_description=README,
      author="ikame",
      author_email="anler86@gmail.com",
      url="https://github.com/ikame/django-pagination-again",
      license="MIT",
      install_requires=["six"],
      tests_require=["pytest", "mock"],
      cmdclass={"test": PyTest},
      keywords="django pagination paginator",
      classifiers=[
          "Environment :: Plugins",
          "Environment :: Console",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules"])
