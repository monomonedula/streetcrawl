import pytest
from geopy import Point

from streetcrawl.pano import Pano, ImgRequest


@pytest.fixture()
def pano():
    return Pano(
        "132XdfSx", Point(50.34230961203757, 27.894199383237012), "foo-bar-1234"
    )


@pytest.mark.parametrize(
    "fov, resolution, requests",
    [
        (
            90,
            (400, 500),
            [
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=400x500&pano=132XdfSx&heading=0&fov=90&key=foo-bar-1234&return_error_code=true",
                    fov=90,
                    heading=0,
                ),
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=400x500&pano=132XdfSx&heading=90&fov=90&key=foo-bar-1234&return_error_code=true",
                    fov=90,
                    heading=90,
                ),
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=400x500&pano=132XdfSx&heading=180&fov=90&key=foo-bar-1234&return_error_code=true",
                    fov=90,
                    heading=180,
                ),
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=400x500&pano=132XdfSx&heading=270&fov=90&key=foo-bar-1234&return_error_code=true",
                    fov=90,
                    heading=270,
                ),
            ],
        ),
        (
            120,
            (900, 600),
            [
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=132XdfSx&heading=0&fov=120&key=foo-bar-1234&return_error_code=true",
                    fov=120,
                    heading=0,
                ),
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=132XdfSx&heading=120&fov=120&key=foo-bar-1234&return_error_code=true",
                    fov=120,
                    heading=120,
                ),
                ImgRequest(
                    url="https://maps.googleapis.com/maps/api/streetview?size=900x600&pano=132XdfSx&heading=240&fov=120&key=foo-bar-1234&return_error_code=true",
                    fov=120,
                    heading=240,
                ),
            ],
        ),
    ],
)
def test_pano_img_requests(pano, fov, resolution, requests):
    assert pano.image_requests(fov, *resolution) == requests
