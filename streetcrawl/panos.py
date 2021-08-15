import logging
import operator
from logging import Logger
from typing import Callable, List

from geopy import Point

from streetcrawl.pano import Pano
from streetcrawl.pano_id import PanoIdOf
from streetcrawl.points_in_square import PointsInSquare


class Panos:
    def __init__(
        self,
        pts: PointsInSquare,
        pano_id: Callable[[Point], PanoIdOf],
        pano: Callable[[str, Point], Pano],
        logger: Logger = logging.getLogger(__name__),
    ):
        self._pts: PointsInSquare = pts
        self._pano_id: Callable[[Point], PanoIdOf] = pano_id
        self._pano: Callable[[str, Point], Pano] = pano
        self._logger: Logger = logger

    def as_list(self) -> List[Pano]:
        ids = dict()
        for p in self._pts.iter():
            self._logger.info(f"Getting pano id for {p.latitude},{p.longitude}...")
            pano_id = self._pano_id(p)
            id_str = pano_id.as_str()
            location = pano_id.location()
            if id_str is not None:
                assert location is not None
                ids[id_str] = location
            else:
                logger.info(f"Got no pano id for {p.latitude},{p.longitude}.")
        return [
            self._pano(id_, location)
            for id_, location in sorted(ids.items(), key=operator.itemgetter(0))
        ]
