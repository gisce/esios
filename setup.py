from setuptools import setup, find_packages

PACKAGES_DATA = {'esios': ['data/*.xsd']}

setup(
    name='esios',
    version='0.16.1',
    packages=find_packages(),
    url='https://github.com/gisce/esios',
    license='MIT',
    install_requires=['libsaas'],
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Interact with e.sios API',
    package_data=PACKAGES_DATA,
)
