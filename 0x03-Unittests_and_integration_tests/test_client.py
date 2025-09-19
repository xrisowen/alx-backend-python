#!/usr/bin/env python3
"""Test module for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mocked_get_json):
        """Tests that org method returns the correct value."""
        # Define the expected URL based on the parameterized input
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Create an instance of the client with the provided org_name
        client = GithubOrgClient(org_name)
        client.org()

        # Assert that get_json was called exactly once with the expected URL
        mocked_get_json.assert_called_once_with(expected_url)
