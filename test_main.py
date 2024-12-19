import pytest
import json
from unittest.mock import mock_open, patch
from main import ConfigCompiler

def test_parse_json():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        compiler = ConfigCompiler("input.json", "output.txt")
        data = compiler.parse_json()
        assert data == {"key": "value"}


def test_write_output():
    mock_output = "Test output"
    with patch("builtins.open", mock_open()) as mock_file:
        compiler = ConfigCompiler("input.json", "output.txt")
        compiler.write_output(mock_output)
        mock_file.assert_called_once_with("output.txt", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(mock_output)


def test_compile():
    data = {
        "name": "TestApp",
        "version": "1.0.0",
        "features": ["login", "logout"]
    }
    compiler = ConfigCompiler("input.json", "output.txt")
    result = compiler.compile(data)
    expected_output = """{
(define name q(TestApp));
(define version q(1.0.0));
(define features [q(login), q(logout)]);
}"""
    assert result == expected_output


def test_process_comments():
    content = """
    || This is a comment
    (define name q(TestApp));
    || Another comment
    """
    compiler = ConfigCompiler("input.json", "output.txt")
    result = compiler.process_comments(content)

    expected_output = """
(define name q(TestApp));
"""
    assert result == expected_output


def test_handle_syntax():
    content = "!(define CONST 10); !{CONST}"
    compiler = ConfigCompiler("input.json", "output.txt")
    result = compiler.handle_syntax(content)
    expected_output = "!(define CONST 10); !{CONST}"
    assert result == expected_output
