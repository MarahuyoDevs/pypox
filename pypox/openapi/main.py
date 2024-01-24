"""

"""
from abc import ABC, abstractmethod
from typing import Any, Union


class OpenAPI(ABC):
    def __init__(self) -> None:
        self._openapi = "3.0.0"

    @abstractmethod
    def json(self) -> str:
        return ""

    @abstractmethod
    def yaml(self) -> str:
        return ""


class Specification(OpenAPI):
    def __init__(self) -> None:
        super().__init__()


class ServerVariable(OpenAPI):
    def __init__(self, enum: list[str], default: str, description: str) -> None:
        super().__init__()
        self._enum = enum
        self._default = default
        self._description = description

    @property
    def enum(self) -> list[str]:
        return self._enum

    @property
    def default(self) -> str:
        return self._default

    @property
    def description(self) -> str:
        return self._description


class Server(OpenAPI):
    def __init__(
        self, url: str, description: str, variable: dict[str, ServerVariable]
    ) -> None:
        super().__init__()
        self._url = url
        self._description = description
        self._variable = variable

    @property
    def url(self) -> str:
        return self._url

    @property
    def description(self) -> str:
        return self._description

    @property
    def variable(self) -> dict[str, ServerVariable]:
        return self._variable


class Contact(OpenAPI):
    def __init__(self, name: str, url: str, email: str) -> None:
        self._name = name
        self._url = url
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def email(self) -> str:
        return self._email


class License(OpenAPI):
    def __init__(self, name: str, identifier: str, url: str) -> None:
        self._name = name
        self._identifier = identifier
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def url(self) -> str:
        return self._url


class Info(OpenAPI):
    def __init__(
        self,
        title: str,
        summary: str,
        description: str,
        termsOfService: str,
        contact: Contact,
        license: License,
        version: str,
    ) -> None:
        super().__init__()
        self._title = title
        self._summary = summary
        self._description = description
        self._termsOfService = termsOfService
        self._contact = contact
        self._license = license
        self._version = version

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def termsOfService(self) -> str:
        return self._termsOfService

    @property
    def contact(self) -> Contact:
        return self._contact

    @property
    def license(self) -> License:
        return self._license

    @property
    def version(self) -> str:
        return self._version


class Parameter(OpenAPI):
    def __init__(
        self,
        name: str,
        in_: str,
        description: str,
        required: bool = False,
        deprecated: bool = False,
        allowEmptyValue: bool = False,
        style: str = "form",
        explode: bool = False,
        allowReserved: bool = False,
        schema: "Schema" | "Reference" | None = None,
        example: Any = None,
        examples: dict[str, "Example" | "Reference"] | None = None,
        content: dict[str, "MediaType"] | None = None,
    ) -> None:
        super().__init__()
        self._name = name
        self._in = in_
        self._description = description
        self._required = required
        self._deprecated = deprecated
        self._allowEmptyValue = allowEmptyValue
        self._style = style
        self._explode = explode
        self._allowReserved = allowReserved
        self._schema = schema
        self._example = example
        self._examples = examples
        self._content = content

    @property
    def name(self) -> str:
        return self._name

    @property
    def in_(self) -> str:
        return self._in

    @property
    def description(self) -> str:
        return self._description

    @property
    def required(self) -> bool:
        return self._required

    @property
    def deprecated(self) -> bool:
        return self._deprecated

    @property
    def allowEmptyValue(self) -> bool:
        return self._allowEmptyValue

    @property
    def style(self) -> str:
        return self._style

    @property
    def explode(self) -> bool:
        return self._explode

    @property
    def allowReserved(self) -> bool:
        return self._allowReserved

    @property
    def schema(self) -> "Schema" | "Reference" | None:
        return self._schema

    @property
    def example(self) -> Any:
        return self._example

    @property
    def examples(self) -> dict[str, "Example" | "Reference"] | None:
        return self._examples

    @property
    def content(self) -> dict[str, "MediaType"] | None:
        return self._content


class RequestBody(OpenAPI):
    def __init__(
        self,
        description: str,
        required: bool = False,
        content: dict[str, "MediaType"] | None = None,
    ) -> None:
        super().__init__()
        self._description = description
        self._required = required
        self._content = content


class Response(OpenAPI):
    def __init__(
        self,
        description: str,
        headers:dict[str,Union["Header","Reference"]],
        content: dict[str, "MediaType"],
        links: dict[str, "Link" | "Reference"],
    ) -> None:
        super().__init__()
        self._description = description
        self._content = content
        self._headers = headers
        self._links = links
        
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def content(self) -> dict[str, "MediaType"]:
        return self._content
    
    @property
    def headers(self) -> dict[str,Union["Header","Reference"]]:
        return self._headers
    
    @property
    def links(self) -> dict[str, "Link" | "Reference"]:
        return self._links


class Reference(OpenAPI):
    def __init__(
        self,
        ref: str,
        summary: str | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__()
        self._ref = ref
        self._summary = summary
        self._description = description

    @property
    def ref(self) -> str:
        return self._ref

    @property
    def summary(self) -> str | None:
        return self._summary

    @property
    def description(self) -> str | None:
        return self._description


class ExternalDocumentation(OpenAPI):
    def __init__(self, description: str, url: str) -> None:
        self._description = description
        self._url = url
        super().__init__()

    @property
    def description(self) -> str:
        return self._description

    @property
    def url(self) -> str:
        return self._url


class SecurityRequirement(OpenAPI):
    def __init__(self, name: str, scopes: list[str]) -> None:
        super().__init__()
        self._name = name
        self._scopes = scopes


class Operation(OpenAPI):
    def __init__(
        self,
        tags: list[str],
        summary: str,
        description: str,
        operationId: str,
        externalDocs: ExternalDocumentation,
        parameters: list[Parameter | Reference],
        requestBody: RequestBody | Reference,
        responses: dict[str, Response],
        callabacks: dict[str, "Callback" | Reference] | None = None,
        deprecated: bool = False,
        security: list[dict[str, list[str]]] | None = None,
        servers: list[Server] | None = None,
    ) -> None:
        super().__init__()
        self._tags = tags
        self._summary = summary
        self._description = description
        self._operationId = operationId
        self._parameters = parameters
        self._requestBody = requestBody
        self._responses = responses
        self._deprecated = deprecated
        self._security = security
        self._servers = servers

    @property
    def tags(self) -> list[str]:
        return self._tags

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def description(self) -> str:
        return self._description

    @property
    def operationId(self) -> str:
        return self._operationId

    @property
    def parameters(self) -> list[Parameter]:
        return self._parameters

    @property
    def requestBody(self) -> RequestBody:
        return self._requestBody

    @property
    def responses(self) -> dict[str, Response]:
        return self._responses

    @property
    def deprecated(self) -> bool:
        return self._deprecated

    @property
    def security(self) -> list[dict[str, list[str]]]:
        return self._security

    @property
    def servers(self) -> list[Server]:
        return self._servers


class PathItem(OpenAPI):
    def __init__(
        self,
        summary: str,
        description: str,
        get: Operation | None = None,
        put: Operation | None = None,
        post: Operation | None = None,
        delete: Operation | None = None,
        options: Operation | None = None,
        head: Operation | None = None,
        patch: Operation | None = None,
        trace: Operation | None = None,
        servers: list[Server] | None = None,
        parameters: list[Parameter] | None = None,
    ) -> None:
        self._summary = summary
        self._description = description
        self._get = get
        self._put = put
        self._post = post
        self._delete = delete
        self._options = options
        self._head = head
        self._patch = patch
        self._trace = trace
        self._servers = servers
        self._parameters = parameters
        super().__init__()

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def description(self) -> str:
        return self._description

    @property
    def get(self) -> Operation | None:
        return self._get

    @property
    def put(self) -> Operation | None:
        return self._put

    @property
    def post(self) -> Operation | None:
        return self._post

    @property
    def delete(self) -> Operation | None:
        return self._delete

    @property
    def options(self) -> Operation | None:
        return self._options

    @property
    def head(self) -> Operation | None:
        return self._head

    @property
    def patch(self) -> Operation | None:
        return self._patch

    @property
    def trace(self) -> Operation | None:
        return self._trace

    @property
    def servers(self) -> list[Server] | None:
        return self._servers

    @property
    def parameters(self) -> list[Parameter] | None:
        return self._parameters


class Encoding(OpenAPI):
    def __init__(
        self,
        contentType: str,
        headers: dict[str, Union["Header", "Reference"]],
        style: str,
        explode: str,
        allowReserved: bool,
    ) -> None:
        self._contentType = contentType
        self._headers = headers
        self._style = style
        self._explode = explode
        self._allowReserved = allowReserved

        super().__init__()

    @property
    def contentType(self) -> str:
        return self._contentType

    @property
    def headers(self) -> dict[str, Union["Header", "Reference"]]:
        return self._headers

    @property
    def style(self) -> str:
        return self._style

    @property
    def explode(self) -> str:
        return self._explode

    @property
    def allowReserved(self) -> bool:
        return self._allowReserved


class Example(OpenAPI):
    def __init__(
        self, summary: str, description: str, value: Any, externalValue: str
    ) -> None:
        self._summary = summary
        self._description = description
        self._value = value
        self._externalValue = externalValue
        super().__init__()

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def description(self) -> str:
        return self._description

    @property
    def value(self) -> Any:
        return self._value

    @property
    def externalValue(self) -> str:
        return self._externalValue


class MediaType(OpenAPI):
    def __init__(
        self,
        schema: "Schema",
        example: Any,
        examples: dict[str, "Example" | "Reference"],
        encoding: dict[str, "Encoding"],
    ) -> None:
        super().__init__()


class Responses(OpenAPI):
    def __init__(
        self,
        default: Union["Response", "Reference"],
        http_fields: dict[str, Union["Response", "Reference"]],
    ) -> None:
        self._default = default
        self._http_fields = http_fields
        super().__init__()
    
    @property
    def default(self) -> Union["Response", "Reference"]:
        return self._default
    
    @property
    def http_fields(self) -> dict[str, Union["Response", "Reference"]]:
        return self._http_fields
    
    
    


class Paths(OpenAPI):
    def __init__(self, path: str) -> None:
        self._paths = path
        super().__init__()

    @property
    def paths(self) -> dict[str, PathItem]:
        return self._paths


class Components(OpenAPI):
    def __init__(self, schemas: dict[str, "Schema"]) -> None:
        super().__init__()

    @property
    def schemas(self) -> dict[str, "Schema"]:
        return self._schemas

    @property
    def responses(self) -> dict[str, Response]:
        return self._responses

    @property
    def parameters(self) -> dict[str, Parameter]:
        return self._parameters

    @property
    def examples(self) -> dict[str, "Example"]:
        return self._examples

    @property
    def requestBodies(self) -> dict[str, RequestBody]:
        return self._requestBodies

    @property
    def headers(self) -> dict[str, "Header"]:
        return self._headers

    @property
    def securitySchemes(self) -> dict[str, "SecurityScheme"]:
        return self._securitySchemes

    @property
    def links(self) -> dict[str, "Link"]:
        return self._links

    @property
    def callbacks(self) -> dict[str, "Callback"]:
        return self._callbacks

    @property
    def pathItems(self) -> dict[str, PathItem]:
        return self._pathItems
