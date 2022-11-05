#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

test_requirements = ['pytest>=3', ]

setup(
    author="Luis C. Berrocal",
    author_email='luis.berrocal.1942@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Django tools for quick scaffolding.",
    entry_points={
        'console_scripts': [
            'django_scaffolding_tools=django_scaffolding_tools.cli:main',
            'django_gen=django_scaffolding_tools.django.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='django_scaffolding_tools',
    name='django_scaffolding_tools',
    packages=find_packages(include=['django_scaffolding_tools', 'django_scaffolding_tools.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luiscberrocal/django_scaffolding_tools',
    version='0.9.1',
    zip_safe=False,
    package_data={'': ['templates/*.j2']},
)
