import tempfile
from pathlib import Path
from unittest.mock import Mock, seal

from geopy import Point

from streetcrawl.pano import Pano
from streetcrawl.saver import Saver


def test_saver_download_ok():
    api_key = "foo-Bar"
    session = Mock(
        get=Mock(
            side_effect=lambda url: Mock(
                content=f"pic bytes for {url}".encode(),
                ok=True,
            )
        )
    )
    seal(session)
    pano_id = "123451234xcavXsdD"
    with tempfile.TemporaryDirectory() as d:
        assert Saver(120, (900, 600), session, Path(d),).download(
            Pano(pano_id, Point(50.45368983595096, 30.503254762390927), api_key),
        )
        pano_path = Path(d) / pano_id
        assert pano_path.exists()
        assert {p: p.read_bytes() for p in pano_path.iterdir()} == {
            pano_path
            / "120-240.jpg": b"pic bytes for https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=123451234xcavXsdD&heading=240&fov=120&key=foo-Bar&return_error_code=true",
            pano_path
            / "120-120.jpg": b"pic bytes for https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=123451234xcavXsdD&heading=120&fov=120&key=foo-Bar&return_error_code=true",
            pano_path
            / "120-0.jpg": b"pic bytes for https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=123451234xcavXsdD&heading=0&fov=120&key=foo-Bar&return_error_code=true",
        }


def test_saver_download_fail():
    api_key = "foo-Bar"
    session = Mock(
        get=Mock(
            return_value=Mock(
                ok=False,
                status_code=403,
            )
        )
    )
    seal(session)
    pano_id = "123451234xcavXsdD"
    with tempfile.TemporaryDirectory() as d:
        assert (
            Saver(120, (900, 600), session, Path(d),).download(
                Pano(pano_id, Point(50.45368983595096, 30.503254762390927), api_key),
            )
            is False
        )
        pano_path = Path(d) / pano_id
        assert pano_path.exists() is False
