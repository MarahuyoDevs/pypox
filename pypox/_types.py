"""
This module defines custom types used in the pypox library.

Types:
- QueryStr: A new type representing a string used in query parameters.
- QueryInt: A new type representing an integer used in query parameters.
- QueryFloat: A new type representing a float used in query parameters.
- QueryBool: A new type representing a boolean used in query parameters.
- PathStr: A new type representing a string used in path parameters.
- PathInt: A new type representing an integer used in path parameters.
- PathFloat: A new type representing a float used in path parameters.
- PathBool: A new type representing a boolean used in path parameters.
- HeaderStr: A new type representing a string used in headers.
- HeaderInt: A new type representing an integer used in headers.
- HeaderFloat: A new type representing a float used in headers.
- HeaderBool: A new type representing a boolean used in headers.
- CookieStr: A new type representing a string used in cookies.
- CookieInt: A new type representing an integer used in cookies.
- CookieFloat: A new type representing a float used in cookies.
- CookieBool: A new type representing a boolean used in cookies.
- BodyDict: A new type representing a dictionary used in request bodies.
- BodyForm: A new type representing a form data used in request bodies.

"""

from typing import NewType


QueryStr = NewType("QueryStr", str)
QueryInt = NewType("QueryInt", int)
QueryFloat = NewType("QueryFloat", float)
QueryBool = NewType("QueryBool", bool)
PathStr = NewType("PathStr", str)
PathInt = NewType("PathInt", int)
PathFloat = NewType("PathFloat", float)
PathBool = NewType("PathBool", bool)
HeaderStr = NewType("HeaderStr", str)
HeaderInt = NewType("HeaderInt", int)
HeaderFloat = NewType("HeaderFloat", float)
HeaderBool = NewType("HeaderBool", bool)
CookieStr = NewType("CookieStr", str)
CookieInt = NewType("CookieInt", int)
CookieFloat = NewType("CookieFloat", float)
CookieBool = NewType("CookieBool", bool)
BodyDict = NewType("BodyDict", dict)
BodyForm = NewType("BodyForm", dict)
