from setuptools import setup

setup(
name = 'nse_analyzer',
version = '1.0 dev 1',
author = 'Santosh Elangovan aka Catalyst18',
author_email = 'etsant.18@gmail.com',
packages = ['nse_analyzer'],
python_requires='!=2.7, !=3.0.*, !=3.1.*, !=3.2.*, >=3.3.*, <4',
install_requires = ['psycopg2','pandas','configparser','requests'],
project_urls={
        'Bug Reports': 'https://github.com/Catalyst18/nationalstock_analyzer/issues',
        'Say Thanks!': 'https://www.linkedin.com/in/santosh-elangovan-63721b47/',
        'Source': 'https://github.com/Catalyst18/nationalstock_analyzer',
    }
)