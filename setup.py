from setuptools import find_packages, setup

setup(
    name='css2video',
    version='1.0.0',
    author='Sagar Chakravarthy',
    author_email='bp.sagar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyparsing>=2.1.9',
        'nose>=1.3.7'
    ],
    zip_safe=False
)
