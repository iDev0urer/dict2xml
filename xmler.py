#!/usr/bin/env python
# coding: utf-8

"""
Converts a Python dictionary to a valid XML string
"""

from __future__ import unicode_literals

import sys
from decimal import Decimal
from xml.dom import minidom
from xml.etree.ElementTree import Element, tostring

__version__ = "0.2.1"
version = __version__


def to_text(value):
    return unicode(value) if sys.version_info.major < 3 else str(value)


def to_bytes(value):
    return str(value) if sys.version_info.major < 3 else bytes(value)


def is_text(value):
    return (
        isinstance(value, unicode)
        if sys.version_info.major < 3
        else isinstance(value, str)
    )


def iteritems(dict_obj):
    return dict_obj.iteritems() if sys.version_info.major < 3 else dict_obj.items()


def dict2xml(dict_obj, encoding="utf-8", pretty=False):
    """Converts a python dictionary into a valid XML string

    Args:
        - `dict_obj` is the dict-like object to convert. It can contain
          other dictionaries, with string keys and values convertable to
          strings, as well as list, sets, and tuples of such dictionaries.
        - `encoding` specifies the encoding to be included in the encoding
          segment. If set to False no encoding segment will be displayed.
        - `pretty` (False by default) can be True if you want to get a
          "prettified" result as a string, which also ensures the result
          is well-formed XML.

    Returns:
        A XML formatted string representing the dictionary.

    Examples:
        ```
        dic = {
            "Envelope": {
                "@ns": "soapenv",
                "@attrs": {
                    "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
                    "xmlns:urn": "urn:partner.soap.sforce.com"
                },
                "Header": {
                    "@ns": "soapenv",
                    "SessionHeader": {
                        "@ns": "urn",
                        "sessionId": {
                            "@ns": "urn",
                            "@value": "00D36000000b28L!ARsAQMtHo4XD71VYRxoz"
                        }
                    }
                },
                "Body": {
                    "@ns": "soapenv",
                    "query": {
                        "@ns": "urn",
                        "queryString": {
                            "@ns": "urn",
                            "@value": "SELECT Id, Name FROM Account LIMIT 2"
                        }
                    }
                }
            }
        }

        xml = dict2xml(dic, pretty=True)
        print(xml)
        ```

        output:
        ```
        <?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
          xmlns:urn="urn:partner.soap.sforce.com">
          <soapenv:Header>
            <urn:SessionHeader>
              <urn:sessionId>00D36000000b28L!ARsAQMtHo4XD71VYRxoz</urn:sessionId>
            </urn:SessionHeader>
          </soapenv:Header>
          <soapenv:Body>
            <urn:query>
              <urn:queryString>SELECT Id, Name FROM Account LIMIT 2</urn:queryString>
            </urn:query>
          </soapenv:Body>
        </soapenv:Envelope>
        ```
    """

    xml_string = to_bytes(tostring(parse(dict_obj, pretty=pretty), encoding=encoding))

    if pretty:
        xml_pretty_string = minidom.parseString(xml_string.decode(encoding))
        return xml_pretty_string.toprettyxml(encoding=encoding, indent="  ").decode(
            encoding
        )
    else:
        return to_text(xml_string.decode(encoding))


def parse(dict_obj, parent={}, pretty=False):

    for key, value in iteritems(dict_obj):

        if isinstance(value, (int, float, Decimal, bool)):
            value = to_text(value)

        if "@ns" in value:
            parent["namespace"] = value["@ns"]
            value.pop("@ns")

        if "@attrs" in value:
            parent["attributes"] = value["@attrs"]
            value.pop("@attrs")

        if "@name" in value:
            parent["name"] = value["@name"]
            value.pop("@name")
        else:
            parent["name"] = key

        if "@value" in value:
            parent["value"] = value = value["@value"]
        else:
            parent["value"] = value

    if "namespace" in parent:
        parent["name"] = "%s:%s" % (parent["namespace"], parent["name"])

    if "attributes" in parent:
        element = Element(parent["name"], parent["attributes"])
    else:
        element = Element(parent["name"])

    if isinstance(parent["value"], dict):
        for child_key, child_value in iteritems(parent["value"]):
            element.append(parse({child_key: child_value}, parent={}))

    elif isinstance(parent["value"], (list, set, tuple)):
        for child in parent["value"]:
            element.append(parse(child, parent={}))

    else:
        element.text = to_text(parent["value"])

    return element
