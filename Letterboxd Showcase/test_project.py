#Run with:  pytest test_project.py

from project import parse_movies_from_html


# ======================================================================
# Sample HTML snippets that mimic the cinema site’s markup
# ======================================================================

SINGLE_MOVIE_HTML = """
<div class="swiper-slide">
    <div class="description">The Matrix</div>
    <div class="tagline">Sci-Fi</div>
    <div class="hd">PG-13</div>
    <a class="play-btn" href="https://example.com/matrix"></a>
</div>
"""

MISSING_RATING_HTML = """
<div class="swiper-slide">
    <div class="description">Dune</div>
    <div class="tagline">Adventure</div>
    <a class="play-btn" href="https://example.com/dune"></a>
</div>
"""

MISSING_LINK_HTML = """
<div class="swiper-slide">
    <div class="description">Interstellar</div>
    <div class="tagline">Sci-Fi</div>
    <div class="hd">PG</div>
</div>
"""


# ======================================================================
# Tests
# ======================================================================

def test_parse_single_movie():
    movies = parse_movies_from_html(SINGLE_MOVIE_HTML)
    assert len(movies) == 1
    m = movies[0]
    assert m["Title"] == "The Matrix"
    assert m["Genre"] == "Sci-Fi"
    assert m["Rating"] == "PG-13"
    assert m["Purchase Link"] == "https://example.com/matrix"


def test_parse_missing_rating_defaults_to_NA():
    movies = parse_movies_from_html(MISSING_RATING_HTML)
    assert movies[0]["Rating"] == "N/A"


def test_parse_missing_play_button_gives_blank_link():
    movies = parse_movies_from_html(MISSING_LINK_HTML)
    assert movies[0]["Purchase Link"] == ""
