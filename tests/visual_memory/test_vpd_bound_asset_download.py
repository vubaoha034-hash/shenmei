"""Synthetic HTTP transport checks; not visual evidence or real image tests."""
import hashlib
from types import SimpleNamespace

import pytest
from scripts import vpd_download_bound_asset as module


class Response:
    def __init__(self, status, content):
        self.status, self.content = status, content
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def read(self):
        return self.content


def setup(monkeypatch, responses):
    queue = iter(responses)
    calls = []
    def request(req, timeout):
        calls.append(req)
        return next(queue)
    monkeypatch.setattr(module.urllib.request, 'urlopen', request)
    monkeypatch.setattr(module.time, 'sleep', lambda _: None)
    return calls


URL = 'https://www.figma.com/api/mcp/asset/SYNTHETIC_TOKEN.png'
PNG = b'\x89PNG\r\n\x1a\nSYNTHETIC_TRANSPORT_ONLY'
SHA = hashlib.sha256(PNG).hexdigest()


def test_pending_is_not_success_then_exact_pinned_payload_succeeds(monkeypatch):
    calls = setup(monkeypatch, [Response(202, b''), Response(200, PNG)])
    assert module.download(URL, SHA) == (PNG, 2)
    assert len(calls) == 2
    assert calls[0].get_header('User-agent') == 'Mozilla/5.0'


def test_repeated_pending_is_bounded_and_cannot_create_fake_success(monkeypatch):
    calls = setup(monkeypatch, [Response(202, b'') for _ in range(4)])
    with pytest.raises(ValueError, match='ASSET_PENDING_202'):
        module.download(URL, SHA)
    assert len(calls) == 4


@pytest.mark.parametrize('content,error', [(b'<html>pending</html>', 'HTTP_200_ACTUAL_PNG'),
                                          (PNG + b'changed', 'EXACT_PINNED_ASSET_SHA')])
def test_status200_still_needs_png_and_exact_identity(monkeypatch, content, error):
    setup(monkeypatch, [Response(200, content)])
    with pytest.raises(ValueError, match=error):
        module.download(URL, SHA)


def test_unrelated_host_is_rejected_before_network(monkeypatch):
    calls = setup(monkeypatch, [])
    with pytest.raises(ValueError, match='OFFICIAL_FIGMA_ASSET_URL'):
        module.download('https://other.invalid/api/mcp/asset/x', SHA)
    assert not calls
