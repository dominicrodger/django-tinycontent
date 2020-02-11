import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import tinycontent


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="django-tinycontent",
    version=tinycontent.__version__,
    description="A Django app for managing re-usable blocks of tiny content.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="Dominic Rodger",
    author_email="internet@dominicrodger.com",
    url="http://github.com/dominicrodger/django-tinycontent",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=2.0", "django-autoslug>=1.8.0", "markdown"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
    tests_require=(
        "mock==2.0.0",
        "pytest==5.3.5",
        "pytest-cov==2.8.1",
        "pytest-django==3.8.0",
    ),
    cmdclass={"test": PyTest},
)
