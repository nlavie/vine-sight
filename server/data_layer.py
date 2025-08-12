import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
import logging

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.dialects.postgresql import insert

from server.config import POSTGRES_CONNECTION_STRING

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLayer(ABC):
    @abstractmethod
    def query(self, dt: datetime) -> pd.DataFrame:
        pass

    @abstractmethod
    def set(self, df: pd.DataFrame,table_name: str, conflict_columns: list = None):
        pass


class Postgres(DataLayer):
    def __init__(self):
        self.engine = create_engine(POSTGRES_CONNECTION_STRING)
        logger.info("Postgres engine initialized")


    def query(self, query: str):
        logger.info(f"Executing custom query: {query}")
        q = query.strip().lower()
        if q.startswith(("select", "with")):
            return pd.read_sql_query(query, self.engine)
        else:
            with self.engine.begin() as conn:
                conn.execute(text(query))
            return None


    def set(self, df: pd.DataFrame, table_name: str, conflict_columns: list = None):
        logger.info(f"Inserting {len(df)} rows into '{table_name}' with conflict_columns={conflict_columns}")
        if conflict_columns is None:
            raise ValueError("conflict_columns must be provided for upsert behavior.")

        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        if table_name not in metadata.tables:
            logger.error(f"Table '{table_name}' not found in the database.")
            raise ValueError(f"Table '{table_name}' not found in metadata.")

        table = metadata.tables[table_name]

        try:
            with self.engine.begin() as conn:
                for i, (_, row) in enumerate(df.iterrows(), start=1):
                    stmt = insert(table).values(**row.to_dict())
                    stmt = stmt.on_conflict_do_nothing(index_elements=conflict_columns)
                    conn.execute(stmt)
                logger.info(f"Insert/upsert complete for {table_name}")
        except Exception as e:
            logger.exception(f"Failed to insert rows into '{table_name}': {e}")
            raise
