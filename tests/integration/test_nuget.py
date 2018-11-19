#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `nuget` module.
Tests functionality of the NuGet Runner integration
"""
import unittest
import os
import shutil
from unittest.mock import MagicMock, patch

from ugetcli.utils import create_empty_file, temp_dir
from nuget import NuGetRunner


class TestUGetCliNuGetRunner(unittest.TestCase):
    """Tests for `ugetcli` package - `nuget` module"""

    @patch('nuget.call')
    def test_nuget_runner_locate_nuget(self, mock_call):
        """Test NuGetRunner.locate_nuget """
        mock_call.return_value = 0
        assert NuGetRunner.locate_nuget() == "nuget"

    @patch('nuget.escape_exe_path')
    @patch('nuget.open')
    @patch('nuget.call')
    def test_nuget_runner_valid_nuget_executable(self, mock_call, mock_open, mock_escape_exe_path):
        """Test NuGetRunner.valid_nuget_executable """
        mock_call.return_value = 0
        with open(os.devnull, "w") as devnull:
            mock_open_handler = MagicMock()
            mock_open.return_value = mock_open_handler
            mock_open_handler.__enter__.return_value = devnull
            mock_escape_exe_path.return_value = "nuget.exe"
            assert NuGetRunner.valid_nuget_executable("nuget.exe")
            mock_call.assert_called_with("nuget.exe help", shell=True, stderr=devnull, stdout=devnull)

    @patch('nuget.Popen')
    def test_nuget_runner_pack(self, mock_popen):
        """Test NuGetRunner.pack """
        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        expected_command_str = "nuget.exe pack TestProject.csproj -OutputDirectory Output " \
                               "-Properties unityPackagePath=TestProject.1.0.0.unitypackage;Configuration=Debug " \
                               "-Verbosity normal"

        nuget_runner = NuGetRunner("nuget.exe")
        assert nuget_runner.pack("TestProject.csproj", "Output", "Debug", "TestProject.1.0.0.unitypackage") == 0
        mock_popen.assert_called_with(expected_command_str, shell=True)

    @patch('nuget.Popen')
    def test_nuget_runner_push(self, mock_popen):
        """Test NuGetRunner.push"""
        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        expected_command_str = "nuget.exe push Test.nupkg -Verbosity normal " \
                               "-Source http://test.com/nuget " \
                               "-ApiKey myapikey7"

        nuget_runner = NuGetRunner("nuget.exe")
        assert nuget_runner.push("Test.nupkg", "http://test.com/nuget", "myapikey7") == 0
        mock_popen.assert_called_with(expected_command_str, shell=True)

