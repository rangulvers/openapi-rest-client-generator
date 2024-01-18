from setuptools import setup, find_packages

setup(
    name='gen-openapi-rest',
    version='0.0.1',
    packages=find_packages(),
    description='Generate .http files from OpenAPI/Swagger JSON. to be used with VS Code REST Client.',
    long_description='Generate .http files from OpenAPI/Swagger JSON. to be used with VS Code REST Client',
    long_description_content_type='text/markdown',
    author='rangulvers',
    url='https://github.com/rangulvers/openapi-rest-client-generator',
    license='LICENSE',
    install_requires=[
        'requests'
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
