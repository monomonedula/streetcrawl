import csv
import logging
from logging import Logger
from pathlib import Path

from streetcrawl.panos import Panos
from streetcrawl.saver import Saver


class Catalogue:
    def __init__(
        self,
        directory: Path,
        saver: Saver,
        logger: Logger = logging.getLogger(__name__),
    ):
        self._dir: Path = directory
        self._saver: Saver = saver
        self._logger: Logger = logger

    def add(self, panos: Panos):
        if (self._dir / "index.csv").exists():
            raise ValueError(f"index.csv already exists in {self._dir}")
        self._dir.mkdir(exist_ok=True)
        with open(self._dir / "index.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["pano_id", "latitude", "longitude"])
            panos_list = panos.as_list()
            self._logger.info(f"Got {len(panos_list)} panos to explore.")
            for i, pano in enumerate(panos_list, start=1):
                self._logger.info(f"Getting pano {i} of {len(panos_list)}...")
                if self._saver.download(pano):
                    writer.writerow(
                        [
                            pano.id(),
                            pano.location().latitude,
                            pano.location().longitude,
                        ]
                    )
