from setuptools import setup, find_packages

setup(
    name='openapi-gen',
    version='0.1',
    packages=find_packages(),
    description='Generate .http files from OpenAPI/Swagger JSON. to be used with VS Code REST Client.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='rangulvers',
    author_email='your.email@example.com',
    url='https://github.com/rangulvers/openapi-rest-client-generator',
    license='LICENSE',
    install_requires=[
        'requests',
        'json',
        'sys',
        'urllib'
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
