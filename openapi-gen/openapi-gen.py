import json
import sys
import requests
from urllib.parse import urljoin, urlparse

def fetch_swagger_json(source):
    """
    Fetches the Swagger JSON from a URL or a local file.
    """
    parsed_url = urlparse(source)
    if parsed_url.scheme in ('http', 'https'):
        response = requests.get(source)
        response.raise_for_status()
        return response.json()
    else:
        with open(source, 'r') as f:
            return json.load(f)

def generate_http_file(swagger_json, output_file):
    """
    Generates a .http file from Swagger JSON.
    """
    host = swagger_json['host']
    base_path = ensure_trailing_slash(swagger_json.get('basePath', '/'))
    schemes = swagger_json['schemes']
    
    with open(output_file, "w") as f:
        for path, methods in swagger_json['paths'].items():
            for method, details in methods.items():
                request_url = build_request_url(schemes[0], host, base_path, path)
                comments, query_params = process_parameters(details.get('parameters', []))
                if query_params:
                    request_url += '?' + '&'.join(query_params)
                request = create_request(method.upper(), request_url, details, comments)
                f.write(request + '\n\n')

def ensure_trailing_slash(path):
    """
    Ensures that the path ends with a slash.
    """
    return path if path.endswith('/') else path + '/'

def build_request_url(scheme, host, base_path, path):
    """
    Builds the request URL from its components.
    """
    return f"{scheme}://{host}{ensure_trailing_slash(base_path)}{path.lstrip('/')}"


def process_parameters(parameters):
    """
    Processes parameters to extract comments and query parameters.
    """
    comments = []
    query_params = []
    for param in parameters:
        if param['in'] == 'query':
            param_value = f"{{{param['name']}}}"
            if param.get('type') == 'array' and 'enum' in param['items']:
                options = ', '.join(param['items']['enum'])
                comments.append(f"# {param['name']} options: {options}")
                example_option = param['items']['enum'][0]
                param_value = example_option
            query_params.append(f"{param['name']}={param_value}")
    return comments, query_params

def create_request(method, request_url, details, comments):
    """
    Creates the HTTP request text.
    """
    headers = create_headers(details.get('parameters', []))
    body = create_body(details.get('parameters', []))
    comments_section = '\n'.join(comments) + '\n' if comments else ''
    request_line = f"###\n# {details.get('summary', 'No summary')}\n{comments_section}{method} {request_url} HTTP/1.1\n"
    return request_line + headers + '\n' + body

def create_headers(parameters):
    """
    Creates the headers section of the HTTP request.
    """
    headers = ''
    for parameter in parameters:
        if parameter['in'] == 'header':
            headers += f"{parameter['name']}: {parameter.get('default', '{' + parameter['name'] + '}')}\n"
    return headers

def create_body(parameters):
    """
    Creates the body of the HTTP request.
    """
    body = ''
    for parameter in parameters:
        if parameter['in'] == 'body':
            # Assuming the body is JSON. You might need to handle other types as well.
            body = json.dumps(parameter['schema'], indent=2)
    return body

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <swagger-json-source> <output-http-file>")
        sys.exit(1)
    
    swagger_json_source = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        swagger_json = fetch_swagger_json(swagger_json_source)
        generate_http_file(swagger_json, output_file)
        print(f'Successfully created {output_file} from {swagger_json_source}')
    except Exception as e:
        print(f"An error occurred: {e}")