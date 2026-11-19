from setuptools import setup, find_packages

PACKAGES_DATA = {'esios': ['data/*.xsd']}

setup(
    name='esios',
    version='0.27.1',
    packages=find_packages(),
    url='https://github.com/gisce/esios',
    license='MIT',
    install_requires=[
        'libsaas',
        'lxml',
        'python-dateutil',
        'requests==2.27.1; python_version < "3.0"',
        'requests; python_version >= "3.0"',
        'pytz'
    ],
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Interact with e.sios API',
    package_data=PACKAGES_DATA,
)
