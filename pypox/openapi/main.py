from abc import ABC, abstractclassmethod
from pprint import pprint
from typing import Any, Optional
from starlette.routing import Route

try:
    from pydantic import BaseModel
except ImportError as e:
    raise e


class OpenAPI(BaseModel):
    """Represents an OpenAPI specification.

    Args:
        BaseModel (type): The base model class.

    Attributes:
        openapi (str): The OpenAPI version.
        info (Info): Information about the API.
        jsondialect (str): The JSON dialect used.
        servers (dict): The servers hosting the API.
        paths (dict): The API paths and operations.
        webhooks (dict): The API webhooks.
        components (dict): The API components.
        security (dict): The API security definitions.
        tag (dict): The API tags.
        externalDocs (dict): External documentation for the API.
    """

    openapi: str
    info: Optional["Info"] = None
    jsondialect: Optional[str] = None
    servers: Optional[list["Server"]] = None
    paths: Optional[dict[str, "PathItem"]] = None
    webhooks: Optional[dict[str, "PathItem | Reference"]] = None
    components: Optional["Components"] = None
    security: Optional["SecurityRequirement"] = None
    tag: Optional[list["Tag"]] = None
    externalDocs: Optional["ExternalDocumentation"] = None


class Info(BaseModel):
    """
    Represents information about the API.

    Args:
        BaseModel: The base model class.

    Attributes:
        title (str): The title of the API.
        description (str): The description of the API.
        termsOfService (str): The terms of service for the API.
        contact (Contact): The contact information for the API.
        license (License): The license information for the API.
        version (str): The version of the API.
    """

    title: Optional[str] = ""
    description: Optional[str] = ""
    termsOfService: Optional[str] = ""
    contact: Optional["Contact"] = None
    license: Optional["License"] = None
    version: Optional[str] = ""


class Contact(BaseModel):
    """
    Represents a contact.

    Args:
        name (str): The name of the contact.
        url (str): The URL of the contact.
        email (str): The email address of the contact.
    """

    name: Optional[str] = ""
    url: Optional[str] = ""
    email: Optional[str] = ""


class License(BaseModel):
    """Represents a license.

    Args:
        name (str): The name of the license.
        url (str): The URL of the license.
    """

    name: Optional[str] = ""
    url: Optional[str] = ""


class Server(BaseModel):
    """Represents a server.

    Args:
        BaseModel (type): The base model class.

    Attributes:
        url (str): The URL of the server.
        description (str): The description of the server.
        variables (dict): The server variables.
    """

    url: Optional[str] = None
    description: Optional[str] = None
    variables: Optional["ServerVariable"] = None


class ServerVariable(BaseModel):
    enum: Optional[list[str]] = None
    default: Optional[str] = None
    description: Optional[str] = None


class Components(BaseModel):
    schemas: Optional[dict[str, dict]] = None
    responses: Optional[dict[str, "Response | Reference"]] = None
    parameters: Optional[dict[str, "Parameter | Reference"]] = None
    examples: Optional[dict[str, dict]] = None
    requestBodies: Optional[dict[str, "RequestBody | Reference"]] = None
    securitySchemas: Optional[dict[str, dict]] = None
    links: Optional[dict[str, dict]] = None
    callbacks: Optional[dict[str, dict]] = None
    pathItems: Optional[dict[str, dict]] = None


class Response(BaseModel):
    description: Optional[str] = ""
    headers: Optional[dict[str, "Header | Reference"]] = None
    content: Optional[dict[str, "MediaType"]] = None
    links: Optional[dict[str, "Links | Reference"]] = None


class Parameter(BaseModel):
    name: Optional[str] = ""
    in_: Optional[str] = ""
    description: Optional[str] = ""
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None


class Header(Parameter):
    pass


class MediaType(BaseModel):
    schema_: Optional[dict] = None
    example: Optional[Any] = None
    examples: Optional[dict[str, "Example | Reference"]] = None
    encoding: Optional[dict[str, "Encoding"]] = None


class Encoding(BaseModel):
    contentType: Optional[str] = None
    headers: Optional[dict[str, "Header | Reference"]] = None
    style: Optional[str] = None
    explode: Optional[bool] = False
    allowReserved: Optional[bool] = False


class Example(BaseModel):
    summary: Optional[str] = ""
    description: Optional[str] = ""
    value: Optional[Any] = None
    externalValue: Optional[str] = ""


class RequestBody(BaseModel):
    description: Optional[str] = ""
    content: Optional[dict[str, "MediaType"]] = None
    required: Optional[bool] = False


class SecurityScheme(BaseModel):
    type: Optional[str] = ""
    description: Optional[str] = ""
    name: Optional[str] = ""
    in_: Optional[str] = ""
    _scheme: Optional[str] = ""
    bearerFormat: Optional[str] = ""
    flows: Optional[dict] = None
    openIdConnectUrl: Optional[str] = ""


class Links(BaseModel):
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[dict[str, Any]] = None
    requestBody: Optional["RequestBody"] = None
    description: Optional[str] = None
    server: Optional["Server"] = None


class Callbacks(BaseModel):
    pass


class PathItem(BaseModel):
    _ref: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional["Operation"] = None
    post: Optional["Operation"] = None
    put: Optional["Operation"] = None
    delete: Optional["Operation"] = None
    options: Optional["Operation"] = None
    head: Optional["Operation"] = None
    patch: Optional["Operation"] = None
    trace: Optional["Operation"] = None
    servers: Optional[list["Server"]] = None
    parameters: Optional[list["Parameter"]] = None


class Operation(BaseModel):
    tag: Optional[list[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional["ExternalDocumentation"] = None
    operationId: Optional[str] = None
    parameters: Optional[list["Parameter | Reference"]] = None
    requestBody: Optional["RequestBody | Reference"] = None
    responses: Optional[dict[str, Response]] = None
    callbacks: Optional[dict[str, "Callbacks | Reference"]] = None
    deprecated: bool = False
    security: Optional[list["SecurityRequirement"]] = None
    servers: Optional[list[Server]] = None


class ExternalDocumentation(BaseModel):
    description: Optional[str] = None
    url: Optional[str] = None


class SecurityRequirement(BaseModel):
    pass


class Reference(BaseModel):
    _ref: Optional[str] = ""
    summary: Optional[str] = ""
    description: Optional[str] = ""


class Tag(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    externalDocs: Optional["ExternalDocumentation"] = None
