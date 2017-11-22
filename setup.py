from setuptools import setup, find_packages

import sixquant

setup(
        name='sixquant',
        version=sixquant.__version__,
        packages=find_packages(),
        description='A quick and stable data source for finance data.',
        author='caviler',
        author_email='caviler@gmail.com',
        license='BSD',
        url='https://github.com/sixquant/sixquant',
        keywords='finance data',
        install_requires=['numpy', 'pandas'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'License :: OSI Approved :: BSD License'],
)
