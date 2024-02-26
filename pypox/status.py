from typing import Literal


class HTTP_100_CONTINUE:
    code = 100


class HTTP_101_SWITCHING_PROTOCOLS:
    code = 101


class HTTP_102_PROCESSING:
    code = 102


class HTTP_103_EARLY_HINTS:
    code = 103


class HTTP_200_OK:
    code = 200


class HTTP_201_CREATED:
    code = 201


class HTTP_202_ACCEPTED:
    code = 202


class HTTP_203_NON_AUTHORITATIVE_INFORMATION:
    code = 203


class HTTP_204_NO_CONTENT:
    code = 204


class HTTP_205_RESET_CONTENT:
    code = 205


class HTTP_206_PARTIAL_CONTENT:
    code = 206


class HTTP_207_MULTI_STATUS:
    code = 207


class HTTP_208_ALREADY_REPORTED:
    code = 208


class HTTP_226_IM_USED:
    code = 226


class HTTP_300_MULTIPLE_CHOICES:
    code = 300


class HTTP_301_MOVED_PERMANENTLY:
    code = 301


class HTTP_302_FOUND:
    code = 302


class HTTP_303_SEE_OTHER:
    code = 303


class HTTP_304_NOT_MODIFIED:
    code = 304


class HTTP_305_USE_PROXY:
    code = 305


class HTTP_306_RESERVED:
    code = 306


class HTTP_307_TEMPORARY_REDIRECT:
    code = 307


class HTTP_308_PERMANENT_REDIRECT:
    code = 308


class HTTP_400_BAD_REQUEST:
    code = 400


class HTTP_401_UNAUTHORIZED:
    code = 401


class HTTP_402_PAYMENT_REQUIRED:
    code = 402


class HTTP_403_FORBIDDEN:
    code = 403


class HTTP_404_NOT_FOUND:
    code = 404


class HTTP_405_METHOD_NOT_ALLOWED:
    code = 405


class HTTP_406_NOT_ACCEPTABLE:
    code = 406


class HTTP_407_PROXY_AUTHENTICATION_REQUIRED:
    code = 407


class HTTP_408_REQUEST_TIMEOUT:
    code = 408


class HTTP_409_CONFLICT:
    code = 409


class HTTP_410_GONE:
    code = 410


class HTTP_411_LENGTH_REQUIRED:
    code = 411


class HTTP_412_PRECONDITION_FAILED:
    code = 412


class HTTP_413_REQUEST_ENTITY_TOO_LARGE:
    code = 413


class HTTP_414_REQUEST_URI_TOO_LONG:
    code = 414


class HTTP_415_UNSUPPORTED_MEDIA_TYPE:
    code = 415


class HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE:
    code = 416


class HTTP_417_EXPECTATION_FAILED:
    code = 417


class HTTP_418_IM_A_TEAPOT:
    code = 418


class HTTP_421_MISDIRECTED_REQUEST:
    code = 421


class HTTP_422_UNPROCESSABLE_ENTITY:
    code = 422


class HTTP_423_LOCKED:
    code = 423


class HTTP_424_FAILED_DEPENDENCY:
    code = 424


class HTTP_425_TOO_EARLY:
    code = 425


class HTTP_426_UPGRADE_REQUIRED:
    code = 426


class HTTP_428_PRECONDITION_REQUIRED:
    code = 428


class HTTP_429_TOO_MANY_REQUESTS:
    code = 429


class HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE:
    code = 431


class HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS:
    code = 451


class HTTP_500_INTERNAL_SERVER_ERROR:
    code = 500


class HTTP_501_NOT_IMPLEMENTED:
    code = 501


class HTTP_502_BAD_GATEWAY:
    code = 502


class HTTP_503_SERVICE_UNAVAILABLE:
    code = 503


class HTTP_504_GATEWAY_TIMEOUT:
    code = 504


class HTTP_505_HTTP_VERSION_NOT_SUPPORTED:
    code = 505


class HTTP_506_VARIANT_ALSO_NEGOTIATES:
    code = 506


class HTTP_507_INSUFFICIENT_STORAGE:
    code = 507


class HTTP_508_LOOP_DETECTED:
    code = 508


class HTTP_510_NOT_EXTENDED:
    code = 510


class HTTP_511_NETWORK_AUTHENTICATION_REQUIRED:
    code = 511


class WS_1000_NORMAL_CLOSURE:
    code = 1000


class WS_1001_GOING_AWAY:
    code = 1001


class WS_1002_PROTOCOL_ERROR:
    code = 1002


class WS_1003_UNSUPPORTED_DATA:
    code = 1003


class WS_1005_NO_STATUS_RCVD:
    code = 1005


class WS_1006_ABNORMAL_CLOSURE:
    code = 1006


class WS_1007_INVALID_FRAME_PAYLOAD_DATA:
    code = 1007


class WS_1008_POLICY_VIOLATION:
    code = 1008


class WS_1009_MESSAGE_TOO_BIG:
    code = 1009


class WS_1010_MANDATORY_EXT:
    code = 1010


class WS_1011_INTERNAL_ERROR:
    code = 1011


class WS_1012_SERVICE_RESTART:
    code = 1012


class WS_1013_TRY_AGAIN_LATER:
    code = 1013


class WS_1014_BAD_GATEWAY:
    code = 1014


class WS_1015_TLS_HANDSHAKE:
    code = 1015
