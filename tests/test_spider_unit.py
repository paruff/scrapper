"""Unit tests for VrmSpider behavior without network.

Covers: state loading, start_requests settings, parse item extraction,
pagination follow behavior, and page cap handling.
"""

from types import SimpleNamespace
from typing import Any

import pytest
from scrapy.http import Request, TextResponse

from vrm_crawl.spiders.vrm import VrmSpider, extract_inline_model


def _build_response(url: str, body: str, meta: dict[str, Any] | None = None) -> TextResponse:
    request = Request(url=url, meta=meta or {})
    return TextResponse(url=url, request=request, body=body.encode("utf-8"), encoding="utf-8")


class DummySettings:
    def __init__(self, values: dict[str, int] | None = None):
        self._values = values or {}

    def getint(self, key: str, default: int) -> int:
        return int(self._values.get(key, default))


def test_load_states_from_yaml_success():
    spider = VrmSpider()
    states = spider._load_states_from_yaml()
    assert isinstance(states, list)
    # repo's states.yml includes these examples
    assert "VA" in states and "TX" in states


def test_load_states_from_yaml_missing_defaults(monkeypatch):
    spider = VrmSpider()

    import builtins

    real_open = builtins.open

    def fake_open(path, *args, **kwargs):  # type: ignore[no-redef]
        if str(path).endswith("states.yml"):
            raise FileNotFoundError
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)

    states = spider._load_states_from_yaml()
    assert states == ["VA"]


def test_start_requests_uses_settings_and_builds_urls():
    spider = VrmSpider(states="VA,TX")
    spider.crawler = SimpleNamespace(settings=DummySettings({"VRM_MAX_PAGES": 123}))
    reqs = list(spider.start_requests())
    urls = [r.url for r in reqs]
    assert "https://www.vacationrentalmanagers.com/va" in urls
    assert "https://www.vacationrentalmanagers.com/tx" in urls
    assert spider.max_pages == 123
    # meta contains normalized uppercase state
    for r in reqs:
        assert r.meta["state"] in {"VA", "TX"}


def test_parse_yields_items_and_next_request():
    spider = VrmSpider(states="VA")
    spider.crawler = SimpleNamespace(settings=DummySettings({"VRM_MAX_PAGES": 10}))
    list(spider.start_requests())  # initialize max_pages and page_count

    html = (
        "<html><head><script>window.__INITIAL_STATE__ = {\n"
        '  "properties": [{"name":"A","city":"City","address":"Addr","price":"$1","bedrooms":"1","bathrooms":"1","url":"/a"}]\n'
        "};</script></head>"
        '<body><a class="next-page" href="/va?page=2">Next</a></body></html>'
    )
    resp = _build_response(
        "https://www.vacationrentalmanagers.com/va", html, meta={"state": "VA"}
    )

    out = list(spider.parse(resp))
    # One item and one follow request
    items = [o for o in out if isinstance(o, dict)]
    follows = [o for o in out if isinstance(o, Request)]

    assert len(items) == 1
    item = items[0]
    assert item["state"] == "VA"
    assert item["name"] == "A"
    assert item["url"] == "/a"
    # slug is generated when name and city are present
    assert item["slug"].endswith("va")

    assert len(follows) == 1
    assert follows[0].url.endswith("/va?page=2")
    assert follows[0].meta["state"] == "VA"


def test_parse_respects_max_pages_no_follow():
    spider = VrmSpider(states="VA")
    spider.crawler = SimpleNamespace(settings=DummySettings({"VRM_MAX_PAGES": 1}))
    list(spider.start_requests())

    html = (
        "<html><head><script>window.__INITIAL_STATE__ = {\n"
        '  "properties": [{"name":"Only","city":"C","address":"A","price":"$","bedrooms":"1","bathrooms":"1","url":"/only"}]\n'
        "};</script></head>"
        '<body><a class="next-page" href="/va?page=2">Next</a></body></html>'
    )
    resp = _build_response(
        "https://www.vacationrentalmanagers.com/va", html, meta={"state": "VA"}
    )

    out = list(spider.parse(resp))
    follows = [o for o in out if isinstance(o, Request)]
    assert follows == []


def test_extract_inline_model_whitespace_and_multiple_scripts():
    html = (
        "<script>console.log('pre');</script>\n"
        "<script>window.__INITIAL_STATE__    =   {\n  \"properties\": []\n};</script>\n"
        "<script>console.log('post');</script>"
    )
    model = extract_inline_model(html)
    assert model is not None
    assert "properties" in model
