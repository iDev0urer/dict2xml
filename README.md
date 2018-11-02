# What am I

xmler is a python package for converting python dictionaries into valid XML. Most XML conversion utilities out there don't seem to provide any namespace support, which was my main reason for creating this package. Inspiration was drawn from the current most popular dictionary to  XML conversion utility [dicttoxml](https://github.com/quandyfactory/dicttoxml).

# Details

xmler has a very specific api that it abides by and, for now, doesn't have very good error handling. Getting namespace support with python dictionaries is not easy so there may be some quirks.

To be used with this package your dictionary must be formatted in the following way:

```python
import dict2xml from xmler

myDict = {
	"RootTag": {						# The root tag. Will not necessarily be root. (see #customRoot)
		"@ns": "soapenv",			# The namespace for the RootTag. The RootTag will appear as <soapenv:RootTag ...>
		"@attrs": {						# @attrs takes a dictionary. each key-value pair will become an attribute
			{ "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/" }
		},
		"childTag": {
			"@attrs": {
				"someAttribute": "colors are nice"
			},
			"grandchild": "This is a text tag"
		}
	}
}

print(dict2xml(myDict, pretty=True))
```

Which will return the following XML:

```xml
<soapenv:RootTag xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
	<childTag someAttribute="colors are nice">
		<grandchild>This is a text tag</grandchild>
	</childTag>
</soapenv:RootTag>
```

As you can see if a key is given a string rather than a dictionary it becomes a text tag.

# API

### Options

#### @ns

The namespace option. Adds the supplied namespace to the element.

**Example:**

Python input:
```python
myDict = {
	"RootTag": {
		"@ns": "soapenv"
	}
}
```

Pretty XML Output:
```xml
<soapenv:RootTag />
```

#### @attrs

The attributes option takes a dictionary of attributes. The key for each becomes the attribute itself, while the value becomes the attribute's value.

**Example:**

Python input:
```python
myDict = {
	"RootTag": {
		"@ns": "soapenv",
		"@attrs": {
			"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"
		}
	}
}
```

Pretty XML Output:
```xml
<soapenv:RootTag xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" />
```

#### @name

Changes the name of the tag.

*Example:*

Python input:
```python
myDict = {
	"RootTag": {
		"@ns": "soapenv",
		"@attrs": {
			"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"
		},
		"@name": "SomethingElse"
	}
}
```

Pretty XML Output:
```xml
<soapenv:SomethingElse xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" />
```

#### @value

Allows you to give the tag a string value rather than having nested tags.

**Example:**

Python input:
```python
myDict = {
	"RootTag": {
		"@ns": "soapenv",
		"@attrs": {
			"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/"
		},
		"@value": "Namespace test",
		"@name": "SomethingElse"
	}
}
```

Pretty XML Output:
```xml
<soapenv:SomethingElse xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">Namespace test</soapenv:SomethingElse>
```

### Tags

Tags are defined by using a key value for the dictionary that does not start with a `@`. For now no syntax checking is being done on tag names, so use this wisely.

The value of the dictionary key can be either a dictionary or a string. If a dictionary is used you can define a namespace, attributes, name, and value for the tag. If a string is supplied you can only have a basic tag with text content.

**Example:**

```python
# The following two tags are exactly the same,
# but defined in a different way

myDict = {
	"SomeTag": {
		"@value": "Some value"
	},
	"SomeTag": "Some value"
}
```

#### Sequences within a dictionary

This fork (https://github.com/dimitern/xmler/) additionally supports having
sequences of type `list`, `set`, or `tuple` (as well as `dict`) as values.
Non-string values (`int`, `float`, `decimal.Decimal`, and `bool`) are
converted to strings automatically.

**Example:**

Python input:
```python
myDict = {
	"root": {
		"child": [
			{
				"id": 12,
			},
			{
				"price": Decimal("5.6782")
			},
			{
				"meta": ({"on_stock": True}, {"rating": 3.14})
			}
		]
	}
}
```

Pretty XML Output:
```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <child>
    <id>12</id>
    <price>5.6782</price>
    <meta>
      <on_stock>True</on_stock>
      <rating>3.14</rating>
    </meta>
  </child>
</root>
```


# Installation

xmler is [published to PyPi](https://pypi.python.org/pypi/xmler), so installing it is as easy as:

```shell
pip install xmler
```

OR

```shell
easy_install xmler
```

You can also download the installer as a tar archive and install it using python with:

```shell
python setup.py install
```

# Original Author

+ Author: Chris Watson
+ Email: chris@watzon.me
+ Repository: http://github.com/watzon/xmler

# Fork Author
+ Author: Dimiter Naydenov
+ Email: dimiter@naydenov.net
+ Repository: http://github.com/dimitern/xmler

# Original Version

+ Version: 0.2.0
+ Release date: 2016-09-16
+ Direct link: https://github.com/watzon/xmler/releases/tag/0.2.0

# Forked Version

+ Version: 0.2.1
+ Release date: 2019-11-02
+ Changes:
	- Made Python 2 and Python 3 compatible.
	- Allow sequences as children, updated README.

# Copyright and License

Copyright 2016 by Christopher Watson

Released under the GNU General Public Licence, Version 2:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
