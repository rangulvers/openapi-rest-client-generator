# gen-openapi-rest/__main__.py
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-locals
import sys
from .gen_openapi_rest import fetch_swagger_json, generate_http_file


def main():
    """_summary_"""
    if len(sys.argv) != 3:
        print(
            "Usage: python -m gen_openapi_rest <swagger-json-source> <output-http-file>"
        )
        sys.exit(1)

    swagger_json_source = sys.argv[1]
    output_file = sys.argv[2]

    try:
        swagger_json = fetch_swagger_json(swagger_json_source)
        generate_http_file(swagger_json, output_file)
        print(f"Successfully created {output_file} from {swagger_json_source}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
