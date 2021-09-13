from apis import UserFetchApi
import pytest
@pytest.mark.parametrize(
    "n_results, expected",
    [
        (10,"https://randomuser.me/api/?results=10&nat=br"),
        (20,"https://randomuser.me/api/?results=20&nat=br"),
        (30,"https://randomuser.me/api/?results=30&nat=br"),
        (40,"https://randomuser.me/api/?results=40&nat=br")
    ]
)
def test_get_endpoint(n_results,expected):
    user_fetch_api = UserFetchApi()

    actual = user_fetch_api._get_endpoint(n_results = n_results)

    assert actual == expected
