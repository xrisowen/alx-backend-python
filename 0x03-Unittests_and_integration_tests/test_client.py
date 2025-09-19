#!/usr/bin/env python3
"""Test module for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
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
        expected_url = f"https://api.github.com/orgs/{org_name}"
        client = GithubOrgClient(org_name)
        client.org()
        mocked_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Tests that _public_repos_url returns the correct URL."""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url,
                             "http://example.com/repos")

    @patch('client.get_json')
    def test_public_repos(self, mocked_get_json):
        """Tests that public_repos returns the correct list of repos."""
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mocked_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mocked_public_repos_url:
            mocked_public_repos_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mocked_public_repos_url.assert_called_once()
            mocked_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Tests that has_license returns the correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
