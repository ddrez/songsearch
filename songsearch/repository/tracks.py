from collections import defaultdict
import sqlite3
from typing import Tuple, List

DB_NAME = "songsearch.sqlite3"

def _init_schema(conn) -> None:
    conn.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS tracks USING 
                 fts5(
                    hashsum,
                    title,
                    lyrics,
                    phonemics,
                    language,
                    tokenize = 'trigram')
                 """)

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    _init_schema(conn)
    return conn

def insert_one(**kwargs):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO tracks 
                            (
                             hashsum, 
                             title, 
                             lyrics, 
                             phonemics,
                             language
                            ) 
                            VALUES
                            (
                             :hashsum, 
                             :title, 
                             :lyrics, 
                             :phonemics,
                             :language
                            ) 
            """, kwargs)

def record_exists(hashsum: str) -> bool:
    res = []
    with get_conn() as conn:
        res = conn.execute(
            """select 1
                 from tracks t 
                where hashsum == ?
            """,
            (hashsum,)
        ).fetchall()

    return len(res) > 0

def _triplets_condition(query: str) -> str:
    if len(query) > 2:
        return ' OR '.join([query[i:i+3] for i in range(0,len(query)-2)])
    else:
        return query

def search_similar(
    lyrics: str,
    phonemics: str
) -> List[Tuple]:

    res0 = []
    res1 = []

    triplets = _triplets_condition(phonemics)

    with get_conn() as conn:
        res0 = conn.execute(
            """select 
                      t.hashsum as id,
                      t.*
                 from tracks t 
                where phonemics MATCH ? 
                ORDER BY 
                      rank 
                LIMIT 10
            """,
            (triplets,)
        ).fetchall()
        res1 = conn.execute(
            """select 
                      t.hashsum as id,
                      t.*
                 from tracks t 
                where lyrics MATCH ? 
                ORDER BY 
                      rank 
                LIMIT 10
            """,
            (lyrics,)
        ).fetchall()

    items = {r[0]: r for r in set(res0 + res1)}
    
    scores = defaultdict(float)
    for result in [res0, res1]:
        for rank, rec in enumerate(result, start=1):
            reciprocal_rank = 1 / (60 + rank)
            scores[rec[0]] += reciprocal_rank
    
    fused_ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    res = [items[k][1:] for k,_ in fused_ranking]

    return res
