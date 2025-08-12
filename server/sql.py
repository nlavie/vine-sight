def get_create_table_query(table_name: str) -> str:
    return f'''
                         CREATE TABLE IF NOT EXISTS {table_name} (
                                                                      post_id     TEXT NOT NULL,
                                                                      topic       TEXT,
                                                                      likes       INTEGER NOT NULL DEFAULT -1,
                                                                      shares      INTEGER NOT NULL DEFAULT -1,
                                                                      comments    INTEGER NOT NULL DEFAULT -1,
                                                                      version     INTEGER NOT NULL DEFAULT -1,
                                                                      "timestamp" TIMESTAMPTZ NOT NULL,
                                                                      PRIMARY KEY (post_id, "timestamp")
                             );
    
    '''


def get_agg_query(table_name: str) -> str:
    return f'''
                      WITH latest AS (
                          SELECT pm.*,
                                 ROW_NUMBER() OVER (
               PARTITION BY post_id
               ORDER BY version DESC, "timestamp" DESC
             ) AS rn
                          FROM {table_name} pm
                      )
                      SELECT
                          topic,
                          COUNT(*) AS posts,
                          SUM(CASE WHEN likes    >= 0 THEN likes    ELSE 0 END) AS total_likes,
                          SUM(CASE WHEN shares   >= 0 THEN shares   ELSE 0 END) AS total_shares,
                          SUM(CASE WHEN comments >= 0 THEN comments ELSE 0 END) AS total_comments
                      FROM latest
                      WHERE rn = 1
                      GROUP BY topic
                      ORDER BY topic;
    
    '''