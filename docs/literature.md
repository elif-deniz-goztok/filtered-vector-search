# Literatür taraması: okuma listesi

Son güncelleme: 16 Kasım 2026. 19 makale; hepsinin künyesi Crossref veya yayıncı sayfasından doğrulandı ve `paper/refs.bib` içinde hazır. Parantez içindeki anahtar, `\cite{...}` ile kullanılacak isim.

**Uyarı:** Aşağıdaki özetler makalelerin abstract'larına ve genel bilgiye dayanıyor, makalelerin tamamı okunarak yazılmadı. Related Work'e bir iddia yazmadan önce ilgili makaleyi okuyup doğrulayın.

Durum sütunu: `[ ]` okunmadı, `[x]` okundu.

## Önce bunları okuyun (projeye en yakın 5 makale)

Bu beşi projenin doğrudan komşuları. Araştırma boşluğunu (gap) bunlara göre tanımlamak gerekiyor.

| | Makale | Ne yapıyor | Projeyle ilgisi |
|---|---|---|---|
| [ ] | **Amanbayev et al., 2026** (`amanbayev2026filtered`), arXiv ön-baskı | FAISS, Milvus ve pgvector'de filtreleme stratejilerini ölçüyor. 768 boyutlu MoReVec veri setini ve filtre–sorgu ilişkisini ölçen GLS metriğini öneriyor. ANN-Benchmarks'ı filtreli aramaya genişletiyor. | **En yakın çalışma.** Abstract'a göre "pgvector'ün sorgu optimizer'ı bazen kötü plan seçiyor" ve "düşük selectivity'de IVFFlat HNSW'yi geçiyor" diyor. İlki chooser fikrinin motivasyonu, ikincisi reproduce edilebilecek bir sonuç. |
| [ ] | **Lu et al., SIGMOD 2026** (`lu2026filteragnostic`) | Üretim seviyesinde, PostgreSQL uyumlu bir veritabanında post-filtering ve inline-filtering'i; graf tabanlı NaviX/ACORN ile kümeleme tabanlı ScaNN'i selectivity ve korelasyona göre karşılaştırıyor. | Sorunun aynısını başka bir sistemde soruyor. Ana bulgusu: tek bir kazanan yok, seçim iş yüküne ve sistemin veri erişim maliyetine bağlı. Chooser fikrini destekliyor. |
| [ ] | **Sanca & Ailamaki, DaMoN 2024** (`sanca2024accesspaths`) | Vektör + ilişkisel aramada tarama (scan) ile index probe arasındaki seçimi selectivity'ye göre inceliyor; geçiş noktasının boyuta ve eşzamanlı sorgu sayısına bağlı olduğunu gösteriyor. | Hedef venue'de (DaMoN) yayınlanmış, "access path seçimi" çerçevesini kuran makale. Yazım ve kapsam için de örnek. |
| [ ] | **Wei et al., VLDB 2020** (`wei2020analyticdbv`) | Alibaba'nın AnalyticDB-V sistemi: yapılandırılmış ve vektör verisini tek SQL sorgusunda birleştiriyor. | Hibrit sorgular için birden fazla yürütme stratejisi arasından maliyet tabanlı seçim yapan ilk sistemlerden. Chooser'ın en yakın atası; farkı (kapalı sistem, kendi index'i) netleştirilmeli. |
| [ ] | **Patel et al., SIGMOD 2024** (`patel2024acorn`) | HNSW'yi predicate'ten bağımsız filtreli aramaya uyarlıyor (predicate subgraph traversal). | Proje dokümanındaki başlangıç referansı. Pre-/post-filtering'in neden bozulduğunu ve korelasyon kavramını en açık anlatan makale. "Yeni index" yaklaşımının temsilcisi; biz yeni index kurmadan çözmeye çalışıyoruz. |

## 1. ANN index'leri ve benchmark

| | Makale | Ne yapıyor | Projeyle ilgisi |
|---|---|---|---|
| [ ] | Malkov & Yashunin, TPAMI 2020 (`malkov2020hnsw`) | HNSW: çok katmanlı graf index'i. | pgvector ve DuckDB VSS'in kullandığı index. `m`, `ef_construction`, `ef_search` parametrelerinin anlamı burada. |
| [ ] | Jégou et al., TPAMI 2011 (`jegou2011pq`) | Product quantization ve ters dosya (IVF) yapısı. | pgvector'deki IVFFlat'in dayandığı IVF fikri için standart atıf. |
| [ ] | Jayaram Subramanya et al., NeurIPS 2019 (`subramanya2019diskann`) | DiskANN: diskte çalışan Vamana graf index'i. | Filtered-DiskANN'in temeli; arka plan atfı. |
| [ ] | Aumüller et al., Information Systems 2020 (`aumuller2020annbenchmarks`) | ANN-Benchmarks: recall–throughput ölçüm çerçevesi ve standart veri setleri. | Ölçüm metodolojisi (recall@k tanımı, tekrarlı koşular) için atıf. Week 4'te reproduce edilecek sonuç için aday kaynak. |

## 2. Filtreli ANN algoritmaları

| | Makale | Ne yapıyor | Projeyle ilgisi |
|---|---|---|---|
| [ ] | Gollapudi et al., WWW 2023 (`gollapudi2023filtereddiskann`) | Etiket filtrelerini graf kurulumuna katan FilteredVamana ve StitchedVamana. | Başlangıç referansı. Filtreye özel index kuran yaklaşımın temsilcisi. |
| [ ] | Zuo et al., SIGMOD 2024 (`zuo2024serf`) | SeRF: sayısal aralık filtreleri için sıkıştırılmış graf. | Bizim sayısal (ör. fiyat) filtrelerimizin özel index'li karşılığı. |
| [ ] | Sehgal & Salihoğlu, VLDB 2025 (`sehgal2025navix`) | NaviX: bir graf DBMS'in içine gömülü, predicate'ten bağımsız HNSW araması. | "DBMS'in içinde filtreli arama" örneği; Lu et al.'ın karşılaştırdığı algoritmalardan biri. |

## 3. Vektör veritabanları ve DBMS içi vektör arama

| | Makale | Ne yapıyor | Projeyle ilgisi |
|---|---|---|---|
| [ ] | Wang et al., SIGMOD 2021 (`wang2021milvus`) | Milvus: amaca özel vektör veritabanı. | Başlangıç referansı. Attribute filtreleme stratejilerini ve bölümleme (partition) tabanlı yaklaşımı anlatıyor; partitioned index stratejimizin dayanağı. |
| [ ] | Yang et al., SIGMOD 2020 (`yang2020pase`) | PASE: PostgreSQL için ANN eklentisi. | pgvector'den önceki PostgreSQL içi vektör index'i; "ilişkisel motorun içinde ANN" çizgisinin başlangıcı. |
| [ ] | Zhang et al., OSDI 2023 (`zhang2023vbase`) | VBASE: PostgreSQL üzerinde vektör aramasını ve ilişkisel operatörleri "relaxed monotonicity" ile birleştiriyor. | Post-filtering'in az sonuç döndürme sorununa yürütme motoru seviyesinde çözüm. pgvector'ün iterative scan'i ile aynı sorunu hedefliyor. |
| [ ] | Zhang et al., ICDE 2024 (`zhang2024limitations`) | PostgreSQL içindeki vektör aramasının (PASE) özel bir kütüphaneye (Faiss) göre neden yavaş olduğunu inceliyor. | "İlişkisel motorun içinde ölçmek neden farklı" sorusunun cevabı; sistem ek yüklerini açıklarken atıf. |
| [ ] | Pan et al., VLDB Journal 2024 (`pan2024survey`) | Vektör veritabanı yönetim sistemleri üzerine survey. | Pre-/post-/single-stage filtering sınıflandırması ve hibrit sorgu optimizasyonu için terminoloji kaynağı. İlk okunacak genel bakış. |

## 4. Access path seçimi ve filtreli arama benchmark'ları

| | Makale | Ne yapıyor | Projeyle ilgisi |
|---|---|---|---|
| [ ] | Selinger et al., SIGMOD 1979 (`selinger1979access`) | System R: selectivity tahminiyle maliyet tabanlı access path seçimi. | Chooser'ın kavramsal temeli. "Optimizer tarzı seçici" derken atıf yapılacak klasik makale. |
| [ ] | Lim et al., 2026 (`lim2026hardness`), arXiv ön-baskı | Filtreli ANN benchmark'larının zorluğunu ölçen α-Hardness metriği ve HCBGen iş yükü üreteci. | Selectivity ve korelasyonun sorgu zorluğunu tek başına açıklamadığını savunuyor. Filtre üretecimizin tasarımı ve "threats to validity" için önemli. |

## Araştırma boşluğu (gap) için ilk gözlemler

Bunlar abstract'lardan çıkan ilk izlenimler; makaleleri okuduktan sonra kesinleştirin.

1. **Konu kalabalık, boşluk dar.** 2026'da iki çalışma (Amanbayev et al., Lu et al.) filtreli aramayı selectivity ve korelasyona göre zaten ölçüyor. "pgvector'de filtreli aramayı ölçtük" tek başına katkı sayılmaz.
2. **Ölçüm tarafında kalan boşluk adayları:** DuckDB VSS'in filtreli arama davranışı (abstract'larda geçmiyor), pgvector 0.8'in iterative scan'i ve partitioned index stratejisi, "dönen sonuç sayısı vs. k" metriği.
3. **Asıl katkı adayı chooser.** Amanbayev et al. pgvector optimizer'ının kötü plan seçtiğini söylüyor; Lu et al. tek bir kazanan olmadığını söylüyor. İkisi de sorunu gösteriyor. Yeni index kurmadan, PostgreSQL'in kendi selectivity tahminlerini kullanarak stratejiyi seçen ve bir oracle'a ne kadar yaklaştığı ölçülen bir chooser, bu iki çalışmanın bıraktığı yerden devam eder.
4. **Kontrol edilmesi gereken:** Amanbayev et al. ve Lu et al. kendi içlerinde bir seçici/öneri mekanizması sunuyor mu? Sunuyorsa chooser'ın farkı (ör. açık kaynak pgvector üzerinde, eklenti olarak, oracle karşılaştırmalı) buna göre yazılmalı.

## Week 4 için: reproduce edilecek sonuç adayları

- **Amanbayev et al.:** pgvector üzerinde ölçüm yapıyor ve ANN-Benchmarks uzantısı kullanıyor; aynı sistem olduğu için en doğal aday. Veri seti 768 boyutlu; bellek sınırımıza sığıp sığmadığına ve kodunun açık olup olmadığına bakılmalı.
- **ANN-Benchmarks (Aumüller et al.):** pgvector HNSW'nin SIFT1M (128 boyut) gibi standart bir veri setindeki recall–QPS noktası. Küçük boyutlu olduğu için donanımımıza rahat sığar; güvenli yedek.
