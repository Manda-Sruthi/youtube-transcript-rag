
import pytest
from rag_pipeline import get_video_id


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=abcdefghijk",
        "https://youtu.be/abcdefghijk",
        "https://www.youtube.com/shorts/abcdefghijk",
        "https://www.youtube.com/embed/abcdefghijk",
    ],
)
def test_get_video_id(url):
    assert get_video_id(url) == "abcdefghijk"


@pytest.mark.parametrize(
    "url",
    [
        "",
        "not-a-url",
        "https://example.com/watch?v=abcdefghijk",
        "https://www.youtube.com/watch?v=bad",
    ],
)
def test_invalid_video_url(url):
    with pytest.raises(ValueError):
        get_video_id(url)
