#!/usr/bin/env python

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


def test_optional():
    parser = Parser(
        [
            Field("Socket Designation"),
            Field("Bank Connections"),
            Field("Extra Info", optional=True),
            Field("Error Status", specifier="status"),
        ],
        "Handle.*",
    )
    result = parser.parse(DMI_OUTPUT)
    assert {
        "socket_designation": "RAM socket #5",
        "bank_connections": "None",
        "extra_info": "This is extra stuff",
        "status": "OK",
    } in result
    assert {
        "socket_designation": "RAM socket #6",
        "bank_connections": "None",
        "extra_info": None,
        "status": "OK",
    } in result
    assert {
        "socket_designation": "RAM socket #7",
        "bank_connections": "None",
        "extra_info": None,
        "status": "OK",
    } in result
