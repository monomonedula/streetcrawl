from unittest.mock import Mock, seal

from geopy import Point

from streetcrawl.pano_id import PanoIdClosestTo


def test_pano_id_ok():
    apikey = "foo-bar1234Xcs"
    pano_id = "65637SxSxxxz"
    lat = 50.45368983595086
    lng = 30.50325476239093
    session = Mock(
        get=Mock(
            return_value=Mock(
                json=Mock(
                    return_value={
                        "status": "OK",
                        "pano_id": pano_id,
                        "location": {"lat": lat, "lng": lng},
                    }
                )
            )
        )
    )
    seal(session)
    pid = PanoIdClosestTo(Point(50.45368983595096, 30.503254762390927), apikey, session)
    assert pid.as_str() == pano_id
    assert pid.pano_location() == Point(lat, lng)
    session.get.assert_called_once_with(
        "https://maps.googleapis.com/maps/api/streetview/metadata?location=50.45368983595096%2C30.503254762390927&key=foo-bar1234Xcs"
    )


def test_pano_id_fail():
    apikey = "foo-bar1234Xcs"
    session = Mock(
        get=Mock(
            return_value=Mock(
                json=Mock(
                    return_value={
                        "status": "ZERO_RESULTS",
                    }
                )
            )
        )
    )
    seal(session)
    pid = PanoIdClosestTo(Point(50.45368983595096, 30.503254762390927), apikey, session)
    assert pid.as_str() is None
    assert pid.pano_location() is None
    session.get.assert_called_once_with(
        "https://maps.googleapis.com/maps/api/streetview/metadata?location=50.45368983595096%2C30.503254762390927&key=foo-bar1234Xcs"
    )
