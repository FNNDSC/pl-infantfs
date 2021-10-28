from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name             = 'infantfs',
    version          = '7.1.1.3',
    description      = 'The infant_recon_all command from Infant FreeSurfer',
    long_description = readme,
    long_description_content_type='text/markdown',
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-infantfs',
    packages         = ['infantfs'],
    install_requires = ['chrisapp'],
    license          = 'FreeSurfer Software License Agreement',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'infantfs = infantfs.__main__:main'
            ]
        }
)
