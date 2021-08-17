from typing import List
from unittest.mock import Mock, seal, call

from geopy import Point

from streetcrawl.catalogue import Catalogue
from streetcrawl.pano import Pano
from streetcrawl.panos import Panos


class PanosDummy(Panos):
    def __init__(self, panos: List[Pano]):
        self._panos = panos

    def as_list(self) -> List[Pano]:
        return self._panos


def test_catalogue_add_ok():
    idx = Mock(save=Mock(return_value=None))
    seal(idx)
    api_key = "fooo-barr"
    panos_list = [
        Pano("12345", Point(50.45368983595096, 30.503254762390927), api_key),
        Pano("56789", Point(50.46372686437613, 30.59567480545674), api_key),
        Pano("91011", Point(50.424085510080936, 30.463840332259917), api_key),
    ]
    Catalogue(idx).add(PanosDummy(panos_list))

    idx.save.assert_has_calls([call(p) for p in panos_list])
    assert idx.save.call_count == len(panos_list)
