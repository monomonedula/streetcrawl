import tempfile
from pathlib import Path
import pytest

from streetcrawl.pano import ImgRequest
from streetcrawl.pano_folder_glued import PanoFolderGlued


@pytest.mark.parametrize(
    "duplicate_on_seams, img_name, expected_img",
    [
        (True, "120-0--120-0--120-120--120-0.jpg", "1.jpg"),
        (False, "120-0--120-120--120-0.jpg", "2.jpg"),
    ],
)
def test_pano_folder_glued(duplicate_on_seams, img_name, expected_img):
    pano_id = "x1234xadfaSz"
    with tempfile.TemporaryDirectory() as d:
        PanoFolderGlued(Path(d), pano_id, duplicate_on_seams=duplicate_on_seams).save(
            [
                (
                    Path("resources/pano/120-0.jpg").read_bytes(),
                    ImgRequest("whatever", 120, 0),
                ),
                (
                    Path("resources/pano/120-120.jpg").read_bytes(),
                    ImgRequest(
                        "whatever",
                        120,
                        120,
                    ),
                ),
                (
                    Path("resources/pano/120-240.jpg").read_bytes(),
                    ImgRequest("whatever", 120, 0),
                ),
            ]
        )
        assert list((Path(d) / pano_id).iterdir()) == [Path(d) / pano_id / img_name]
        assert (Path(d) / pano_id / img_name).read_bytes() == (
            Path("resources/glued") / expected_img
        ).read_bytes()
