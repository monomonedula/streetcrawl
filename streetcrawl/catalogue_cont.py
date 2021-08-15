import csv
import logging
from logging import Logger
from pathlib import Path

from streetcrawl.panos import Panos
from streetcrawl.saver import Saver


class CatalogueContinuing:
    def __init__(
        self,
        directory: Path,
        saver: Saver,
        logger: Logger = logging.getLogger(__name__),
    ):
        self._dir: Path = directory
        self._saver: Saver = saver
        self._logger: Logger = logger

    def index_path(self) -> Path:
        return self._dir / "index.csv"

    def add(self, panos: Panos):
        existing_panos = set()
        self._logger.info(f"Continuing {self.index_path()}...")
        with self.index_path().open() as f:
            for row in csv.reader(f):
                pano_id, lat, lng = row
                existing_panos.add(pano_id.strip())
        with self.index_path().open("a") as csvfile:
            writer = csv.writer(csvfile)
            panos_list = panos.as_list()
            self._logger.info(f"Got {len(panos_list)} panos to explore.")
            for i, pano in enumerate(panos_list, start=1):
                self._logger.info(f"Getting pano {i} of {len(panos_list)}...")
                if pano.id() in existing_panos:
                    self._logger.info(f"Skipping pano {i} (already present).")
                else:
                    if self._saver.download(pano):
                        writer.writerow(
                            [
                                pano.id(),
                                pano.location().latitude,
                                pano.location().longitude,
                            ]
                        )
