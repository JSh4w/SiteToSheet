from setuptools import setup, find_packages

setup(
    name='SiteToSheet',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.3',
        'googlemaps==4.10.0',
        'gspread==6.1.2',
        'numpy==2.0.1',
        'pandas==2.2.2',
        'protobuf==5.27.3',
        'python-dotenv==1.0.1',
        'ratelimit==2.2.1',
        'requests==2.32.3',
        'setuptools==69.2.0',
        'spacy==3.7.5'
    ],
    entry_points={
        'console_scripts': [
            'sitetosheet=SiteToSheet.run:main',
        ],
    },
)