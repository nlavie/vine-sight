# tests/test_topic_stats.py
import os
import pandas as pd
import pandas.testing as pdt
import pytest

from server.config import STATS_TABLE, DATA_DIR, MOCK_DATA_FILENAME
from server.data_layer import Postgres
from server.sql import get_create_table_query, get_agg_query


@pytest.mark.integration
def test_topic_stats_aggregation_matches_python():
    pg = Postgres()

    table = f"{STATS_TABLE}_test"
    create_sql = get_create_table_query(table)

    try:
        pg.query(create_sql)

        csv_path = os.path.join(os.path.dirname(os.getcwd()), DATA_DIR, MOCK_DATA_FILENAME)
        df = pd.read_csv(csv_path)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

        pg.set(df, table, ["post_id", "timestamp"])

        sql = get_agg_query(table)
        got = pd.read_sql_query(sql, pg.engine)

        df_latest = (
            df.sort_values(["post_id", "version", "timestamp"], ascending=[True, False, False])
            .drop_duplicates(subset=["post_id"], keep="first")
        )

        for col in ["likes", "shares", "comments"]:
            if col in df_latest.columns:
                df_latest[col] = df_latest[col].where(df_latest[col] >= 0, 0)

        expected = (
            df_latest.groupby("topic", dropna=False)
            .agg(posts=("post_id", "count"),
                 total_likes=("likes", "sum"),
                 total_shares=("shares", "sum"),
                 total_comments=("comments", "sum"))
            .reset_index()
            .sort_values("topic", kind="mergesort")
            .reset_index(drop=True)
        )

        expected["topic"] = expected["topic"].astype(object).where(expected["topic"].notna(), None)

        got = got[["topic", "posts", "total_likes", "total_shares", "total_comments"]] \
            .sort_values("topic", kind="mergesort").reset_index(drop=True)

        pdt.assert_frame_equal(
            got.reset_index(drop=True),
            expected.reset_index(drop=True),
            check_dtype=False,
            check_like=True,
        )

    finally:
        try:
            pg.query(f"DROP TABLE IF EXISTS {table};")
        except Exception:
            pass
