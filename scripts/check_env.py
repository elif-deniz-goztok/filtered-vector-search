"""Ortam dogrulama: PostgreSQL+pgvector ve DuckDB+VSS calisiyor mu?

Kullanim:  python scripts/check_env.py
Cikti:     results/env_versions.txt  (rapordaki "System setup" bolumu icin)
"""
import os
import platform
import sys
from pathlib import Path

import numpy as np

DIM = 8
N = 1000
K = 5
PG_DSN = os.environ.get(
    "PG_DSN", "host=localhost port=5432 dbname=vectordb user=dbms password=dbms"
)

rng = np.random.default_rng(42)
data = rng.random((N, DIM), dtype=np.float32)
query = rng.random(DIM, dtype=np.float32)
truth = np.argsort(np.linalg.norm(data - query, axis=1))[:K].tolist()

lines = [
    f"OS: {platform.platform()}",
    f"Python: {sys.version.split()[0]}",
    f"NumPy: {np.__version__}",
]
ok = True


def vec_literal(v):
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


# ---------- PostgreSQL + pgvector ----------
try:
    import psycopg

    with psycopg.connect(PG_DSN, autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute("SHOW server_version")
        pg_ver = cur.fetchone()[0]
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute("SELECT extversion FROM pg_extension WHERE extname='vector'")
        pgv_ver = cur.fetchone()[0]

        cur.execute("DROP TABLE IF EXISTS env_check")
        cur.execute(f"CREATE TABLE env_check (id int PRIMARY KEY, v vector({DIM}))")
        with cur.copy("COPY env_check (id, v) FROM STDIN") as cp:
            for i, row in enumerate(data):
                cp.write_row((i, vec_literal(row)))
        cur.execute("CREATE INDEX ON env_check USING hnsw (v vector_l2_ops)")
        cur.execute("SET enable_seqscan = off")
        cur.execute(
            "SELECT id FROM env_check ORDER BY v <-> %s::vector LIMIT %s",
            (vec_literal(query), K),
        )
        got = [r[0] for r in cur.fetchall()]
        cur.execute("DROP TABLE env_check")

    recall = len(set(got) & set(truth)) / K
    lines += [f"PostgreSQL: {pg_ver}", f"pgvector: {pgv_ver}"]
    print(f"[OK] PostgreSQL {pg_ver} + pgvector {pgv_ver}  (HNSW recall@{K}={recall:.2f})")
except Exception as e:
    ok = False
    print(f"[HATA] PostgreSQL/pgvector: {e}")
    print("       -> 'docker compose up -d' calisti mi?")

# ---------- DuckDB + VSS ----------
try:
    import duckdb

    con = duckdb.connect()
    con.execute("INSTALL vss; LOAD vss;")
    vss_ver = con.execute(
        "SELECT extension_version FROM duckdb_extensions() WHERE extension_name='vss'"
    ).fetchone()[0]
    con.execute(f"CREATE TABLE t (id INTEGER, v FLOAT[{DIM}])")
    con.executemany("INSERT INTO t VALUES (?, ?)", [(i, r.tolist()) for i, r in enumerate(data)])
    con.execute("CREATE INDEX idx ON t USING HNSW (v)")
    got = [
        r[0]
        for r in con.execute(
            f"SELECT id FROM t ORDER BY array_distance(v, ?::FLOAT[{DIM}]) LIMIT {K}",
            [query.tolist()],
        ).fetchall()
    ]
    recall = len(set(got) & set(truth)) / K
    lines += [f"DuckDB: {duckdb.__version__}", f"DuckDB vss: {vss_ver}"]
    print(f"[OK] DuckDB {duckdb.__version__} + vss {vss_ver}  (HNSW recall@{K}={recall:.2f})")
except Exception as e:
    ok = False
    print(f"[HATA] DuckDB/VSS: {e}")

out = Path(__file__).resolve().parent.parent / "results" / "env_versions.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\nVersiyonlar yazildi: {out}")
sys.exit(0 if ok else 1)
