"""
Make fixtures discoverable by pytest.

https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68
"""
pytest_plugins = [
   "tests.fixtures.app",
   "tests.fixtures.twitter.account_activity",
   "tests.fixtures.twitter.mock_api",
]
