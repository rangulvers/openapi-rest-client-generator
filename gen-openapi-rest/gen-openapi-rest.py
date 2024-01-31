"""Generates a .http file from a Swagger JSON file.

"""

# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-locals
import json
from urllib.parse import urlparse

import requests


def fetch_swagger_json(source):
    """
    Fetches the Swagger JSON from a URL or a local file.
    """
    parsed_url = urlparse(source)
    if parsed_url.scheme in ("http", "https"):
        response = requests.get(source, timeout=60)
        response.raise_for_status()
        return response.json()
    with open(source, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_http_file(swagger_json_input, output_file_input):
    """_summary_

    Args:
        swagger_json_input (_type_): _description_
        output_file (_type_): _description_
    """
    # Check for OpenAPI version and handle 'servers' or 'host' + 'basePath'
    if swagger_json_input.get("openapi", "").startswith("3."):
        # OpenAPI 3.x.x
        servers = swagger_json_input.get("servers", [])
        base_url = servers[0]["url"] if servers else ""
    else:
        # Swagger 2.0
        host = swagger_json_input.get("host", "localhost")
        base_path = ensure_trailing_slash(swagger_json_input.get("basePath", "/"))
        schemes = swagger_json_input.get("schemes", ["http"])
        base_url = f"{schemes[0]}://{host}{base_path}"
    with open(output_file_input, "w", encoding="utf-8") as f:
        for path, methods in swagger_json_input["paths"].items():
            for method, details in methods.items():
                request_url = build_request_url(base_url, path)
                parameters = details.get("parameters", [])
                comments, query_params = process_parameters(parameters)
                if query_params:
                    request_url += "?" + "&".join(query_params)
                request = create_request(method.upper(), request_url, details, comments)
                f.write(request + "\n\n")


def ensure_trailing_slash(path):
    """
    Ensures that the path ends with a slash.
    """
    return path if path.endswith("/") else path + "/"


def build_request_url(base_url, path):
    """
    Builds the request URL from its components.
    """
    return f"{ensure_trailing_slash(base_url)}{path.lstrip('/')}"


def process_parameters(parameters):
    """
    Processes parameters to extract comments and query parameters.
    """
    comments = []
    query_params = []
    for param in parameters:
        if param["in"] == "query":
            param_value = f"{{{param['name']}}}"
            if param.get("type") == "array" and "enum" in param["items"]:
                options = ", ".join(param["items"]["enum"])
                comments.append(f"# {param['name']} options: {options}")
                example_option = param["items"]["enum"][0]
                param_value = example_option
            query_params.append(f"{param['name']}={param_value}")
    return comments, query_params


def create_request(method, request_url, details, comments):
    """
    Creates the HTTP request text.
    """
    headers = create_headers(details.get("parameters", []))
    body = create_body(details.get("parameters", []))
    comments_section = "\n".join(comments) + "\n" if comments else ""
    request_line = (
        f"###\n# {details.get('summary', 'No summary')}\n"
        f"{comments_section}{method} {request_url} HTTP/1.1\n"
    )
    return request_line + headers + "\n" + body


def create_headers(parameters):
    """
    Creates the headers section of the HTTP request.
    """
    headers = ""
    for parameter in parameters:
        if parameter["in"] == "header":
            headers += (
                f"{parameter['name']}:"
                f"{parameter.get('default', '{'+parameter['name']+'}')}\n"
            )
    return headers


def create_body(parameters):
    """
    Creates the body of the HTTP request.
    """
    body = ""
    for parameter in parameters:
        if parameter["in"] == "body":
            # Assuming the body is JSON. You might need to handle other types as well.
            body = json.dumps(parameter["schema"], indent=2)
    return body


# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python script.py <swagger-json-source> <output-http-file>")
#         sys.exit(1)
#     swagger_json_source = sys.argv[1]
#     output_file = sys.argv[2]
#     try:
#         swagger_json = fetch_swagger_json(swagger_json_source)
#         generate_http_file(swagger_json, output_file)
#         print(f"Successfully created {output_file} from {swagger_json_source}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
