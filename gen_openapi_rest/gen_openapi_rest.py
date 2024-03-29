"""Generates a .http file from a Swagger JSON file.

"""

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


def get_base_url(swagger_json_input):
    """Extracts and returns the base URL from the Swagger JSON input."""
    if swagger_json_input.get("openapi", "").startswith("3."):
        servers = swagger_json_input.get("servers", [])
        return servers[0]["url"] if servers else ""

    # For Swagger 2.0
    host = swagger_json_input.get("host", "localhost")
    base_path = ensure_trailing_slash(swagger_json_input.get("basePath", "/"))
    schemes = swagger_json_input.get("schemes", ["http"])
    return f"{schemes[0]}://{host}{base_path}"


def write_requests_to_file(output_file_input, base_url, paths):
    """Writes the HTTP requests to the output file."""
    with open(output_file_input, "w", encoding="utf-8") as f:
        for path, methods in paths.items():
            for method, details in methods.items():
                request_url = build_request_url(base_url, path)
                parameters = details.get("parameters", [])
                comments, query_params = process_parameters(parameters)
                if query_params:
                    request_url += "?" + "&".join(query_params)
                request = create_request(method.upper(), request_url, details, comments)
                f.write(request + "\n\n")


def generate_http_file(swagger_json_input, output_file_input):
    """Generates an HTTP file from Swagger JSON input."""
    base_url = get_base_url(swagger_json_input)
    write_requests_to_file(output_file_input, base_url, swagger_json_input["paths"])


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
