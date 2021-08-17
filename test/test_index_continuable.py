import csv
import tempfile
from pathlib import Path
from unittest.mock import Mock, seal

from geopy import Point

from streetcrawl.catalogue import IndexContinuable
from streetcrawl.pano import Pano


def test_index_continuable_save_new_ok():
    saver = Mock(download=Mock(return_value=True))
    seal(saver)
    api_key = "foobar"
    panos_list = [
        Pano("12345", Point(50.45368983595096, 30.503254762390927), api_key),
        Pano("56789", Point(50.46372686437613, 30.59567480545674), api_key),
        Pano("91011", Point(50.424085510080936, 30.463840332259917), api_key),
    ]
    with tempfile.TemporaryDirectory() as d:
        with IndexContinuable(Path(d), saver) as idx:
            for p in panos_list:
                idx.save(p)

        with (Path(d) / "index.csv").open() as f:
            assert list(csv.reader(f)) == [
                ["12345", "50.45368983595096", "30.503254762390927"],
                ["56789", "50.46372686437613", "30.59567480545674"],
                ["91011", "50.424085510080936", "30.463840332259917"],
            ]


def test_index_continuable_save_continuing_ok():
    saver = Mock(download=Mock(return_value=True))
    seal(saver)
    api_key = "foobar"
    panos_list = [
        Pano("12345", Point(50.45368983595096, 30.503254762390927), api_key),
        Pano("56789", Point(50.46372686437613, 30.59567480545674), api_key),
        Pano("91011", Point(50.424085510080936, 30.463840332259917), api_key),
        Pano("3245", Point(49.85186704684021, 23.95935683388077), api_key),
        Pano("0234", Point(49.90363819419944, 24.210669063464263), api_key),
    ]
    with tempfile.TemporaryDirectory() as d:
        with IndexContinuable(Path(d), saver) as idx:
            for p in panos_list[:3]:
                idx.save(p)

        with IndexContinuable(Path(d), saver) as idx:
            for p in panos_list:
                idx.save(p)

        with (Path(d) / "index.csv").open() as f:
            assert list(csv.reader(f)) == [
                ["12345", "50.45368983595096", "30.503254762390927"],
                ["56789", "50.46372686437613", "30.59567480545674"],
                ["91011", "50.424085510080936", "30.463840332259917"],
                ["3245", "49.85186704684021", "23.95935683388077"],
                ["0234", "49.90363819419944", "24.210669063464263"],
            ]


def test_index_continuable_save_download_fail():
    saver = Mock(download=Mock(return_value=False))
    seal(saver)
    api_key = "foobar"
    panos_list = [
        Pano("12345", Point(50.45368983595096, 30.503254762390927), api_key),
        Pano("56789", Point(50.46372686437613, 30.59567480545674), api_key),
        Pano("91011", Point(50.424085510080936, 30.463840332259917), api_key),
    ]
    with tempfile.TemporaryDirectory() as d:
        with IndexContinuable(Path(d), saver) as idx:
            for p in panos_list:
                idx.save(p)

        with (Path(d) / "index.csv").open() as f:
            assert list(csv.reader(f)) == []
