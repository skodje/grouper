#!/usr/bin/env python

import pytest

from grouper import Parser, Field


DMI_OUTPUT = """
Handle 0x008A, DMI type 6, 12 bytes
Memory Module Information
    Socket Designation: RAM socket #5
    Bank Connections: None
    Extra Info: This is extra stuff
    Current Speed: Unknown
    Type: DIMM
    Installed Size: Not Installed
    Enabled Size: Not Installed
    Error Status: OK

Handle 0x008B, DMI type 6, 12 bytes
Memory Module Information
    Socket Designation: RAM socket #6
    Bank Connections: None
    Current Speed: Unknown
    Type: DIMM
    Installed Size: Not Installed
    Enabled Size: Not Installed
    Error Status: OK

Handle 0x008C, DMI type 6, 12 bytes
Memory Module Information
    Socket Designation: RAM socket #7
    Bank Connections: None
    Current Speed: Unknown
    Type: DIMM
    Installed Size: Not Installed
    Enabled Size: Not Installed
    Error Status: OK
"""


@pytest.mark.parametrize(
    "fields, separator, expected",
    [
        pytest.param(
            [
                Field("Socket Designation"),
            ],
            "Handle.*",
            [
                {
                    "socket_designation": "RAM socket #5",
                },
                {
                    "socket_designation": "RAM socket #6",
                },
                {
                    "socket_designation": "RAM socket #7",
                },
            ],
            id="Single field",
        ),
        pytest.param(
            [
                Field("Socket Designation"),
                Field("Bank Connections"),
            ],
            r"^\s*$",
            [
                {
                    "socket_designation": "RAM socket #5",
                    "bank_connections": "None",
                },
                {
                    "socket_designation": "RAM socket #6",
                    "bank_connections": "None",
                },
                {
                    "socket_designation": "RAM socket #7",
                    "bank_connections": "None",
                },
            ],
            id="Empty separator",
        ),
        pytest.param(
            [
                Field("Socket Designation"),
                Field("Bank Connections"),
                Field("Extra Info", optional=True),
                Field("Error Status", specifier="status"),
            ],
            "Handle.*",
            [
                {
                    "socket_designation": "RAM socket #5",
                    "bank_connections": "None",
                    "extra_info": "This is extra stuff",
                    "status": "OK",
                },
                {
                    "socket_designation": "RAM socket #6",
                    "bank_connections": "None",
                    "extra_info": None,
                    "status": "OK",
                },
                {
                    "socket_designation": "RAM socket #7",
                    "bank_connections": "None",
                    "extra_info": None,
                    "status": "OK",
                },
            ],
            id="Including optional parameter",
        ),
        pytest.param(
            [
                Field("Socket Designation"),
                Field("Bank Connections"),
                Field("Extra Info", optional=True),
                Field("Error Status", specifier="status"),
            ],
            "Handle.*",
            [
                {
                    "socket_designation": "RAM socket #5",
                    "bank_connections": "None",
                    "extra_info": "This is extra stuff",
                    "status": "OK",
                },
                {
                    "socket_designation": "RAM socket #6",
                    "bank_connections": "None",
                    "extra_info": None,
                    "status": "OK",
                },
                {
                    "socket_designation": "RAM socket #7",
                    "bank_connections": "None",
                    "extra_info": None,
                    "status": "OK",
                },
            ],
            id="Including optional parameter",
        ),
    ],
)
def test_parser(fields, separator, expected):
    """Test the string parser"""
    parser = Parser(fields, separator)
    assert parser.parse(DMI_OUTPUT) == expected
