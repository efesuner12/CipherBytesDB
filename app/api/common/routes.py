from app.api.requests.handle_requests import Request_Handler
from app.api.requests.authentication import Authentication

## Initialises the URLs
#
def initialise_routes(api):
    api.add_resource(Authentication, '/api/v1/auth')
    api.add_resource(Request_Handler, '/api/v1/requests/<sql_request>')
