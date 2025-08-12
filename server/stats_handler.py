from abc import abstractmethod
import logging

from config import STATS_TABLE
from data_layer import Postgres
from server.sql import get_agg_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseHandler:

    @abstractmethod
    def handle(self):
        pass

class StatsHandler(BaseHandler):
    def handle(self) -> dict[str]:
        logger.info("StatsHandler: Handling stats")
        data_layer = Postgres()
        df = data_layer.query(get_agg_query(STATS_TABLE))
        logger.info(f"StatsHandler: Stats query result: {df}")

        return df.to_dict(orient='records')