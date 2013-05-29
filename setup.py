from setuptools import setup, find_packages

import tinycontent

setup(
    name='django-tinycontent',
    version=tinycontent.__version__,
    description="A Django app for managing re-usable blocks of tiny content.",
    long_description=open('README.rst').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/django-tinycontent',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=1.4.5",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
    ],
    tests_require=(
        'django-setuptest==0.1.3',
    ),
    test_suite='setuptest.setuptest.SetupTestSuite',
)
