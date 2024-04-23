from spotify_api.spotify_api import func_to_test


def test_answer():
    assert func_to_test(3) == 4
