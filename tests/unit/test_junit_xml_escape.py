# SPDX-License-Identifier: MIT
"""Test that generate_junit escapes XML-special characters in platform names."""

import os
import tempfile
import xml.etree.ElementTree as ET

from eosim.artifacts.manager import generate_junit


def test_junit_escapes_ampersand_in_name():
    """A platform name with '&' must produce valid, parseable XML."""
    results = [
        {"platform": "board&<v2>", "success": True, "duration_s": 1.5},
        {"platform": 'name"quoted"', "success": False, "duration_s": 0.0},
    ]
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "junit.xml")
        generate_junit(results, output=out)
        tree = ET.parse(out)
        root = tree.getroot()
        names = [tc.get("name") for tc in root.findall("testcase")]
        assert names == ["board&<v2>", 'name"quoted"']
