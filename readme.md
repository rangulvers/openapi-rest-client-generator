[![Upload Python Package](https://github.com/rangulvers/openapi-rest-client-generator/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rangulvers/openapi-rest-client-generator/actions/workflows/python-publish.yml)

# OpenAPI to VSCode REST Client Generator

This tool automatically generates `.http` files for the VSCode REST Client from an OpenAPI (Swagger) specification. It supports both local and remote (URL) OpenAPI JSON files.

## Features

- Fetch OpenAPI JSON from a URL or a local file.
- Generate `.http` files compatible with the VSCode REST Client.
- Handle path and query parameters, including enum options.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- `requests` library for Python (Install using `pip install requests`)

## Usage

To use the OpenAPI to VSCode REST Client Generator, follow these steps:

1. Clone or download this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the script using the following command:

```bash
python gen_openapi_rest.py <swagger-json-source> <output-http-file>
