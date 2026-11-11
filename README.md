# Filtered Vector Search Inside Relational Engines

CMP461 DBMS araştırma projesi (P8). PostgreSQL + pgvector ve DuckDB + VSS üzerinde filtreli vektör aramasını (selectivity ve filtre–vektör korelasyonuna göre) ölçüyor; selectivity tabanlı bir access-path seçici öneriyor.

## Kurulum

Gereken: Docker Desktop (WSL2 backend), Python 3.10+

```bash
# 1) PostgreSQL 17 + pgvector
docker compose up -d

# 2) Python ortamı
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/WSL: source .venv/bin/activate)
pip install -r requirements.txt

# 3) Doğrulama
python scripts/check_env.py
```

`check_env.py` iki sistemde de küçük bir HNSW index kurup sorgu atar ve versiyonları `results/env_versions.txt` dosyasına yazar.

## Klasör yapısı

```
db/init/        PostgreSQL ilk kurulum SQL'leri
scripts/        Veri üretimi, yükleme, deney script'leri
results/        Ölçüm çıktıları
paper/          ACM sigconf rapor kaynakları
```
