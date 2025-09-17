# MovieLens World – Mini Recommender (im Stil des F1-Beispiels)

Dieses Projekt folgt **dem gleichen Stil** wie das bereitgestellte Beispielrepo (Ordner `data/`, `imgs/`, `src/`, README mit Übersicht) – aber mit dem Thema **MovieLens‑ähnliche Empfehlungen**.

## Daten (`/data`)
- `users.csv` – Nutzermerkmale
- `movies.csv` – Filminformationen
- `ratings.csv` – Bewertungen (implizit/explicit)
- `tags.csv` – Schlagwörter

## Bilder (`/imgs`)
- `pipeline.svg` – Daten → Preprocessing → Modell
- `movielens.svg` – Mini‑KG‑Skizze

## Code & Ontologie (`/src`)
- `explore_data.ipynb` – Einstieg in EDA
- `movielens.ttl`, `movielens_transformed.ttl` – Ontologie‑Skizzen

## Wie ausführen
- Notebook in `src/` öffnen (Jupyter / VS Code)
- CSVs liegen klein bei – für echte Experimente ersetze die Daten durch **MovieLens** (siehe RUCAIBox/RecSysDatasets).

## Quelle für Datensätze
- Sammlung: RUCAIBox **RecSysDatasets** (MovieLens, Yelp, Amazon, …)
<<<<<<< HEAD
=======
## SPARQL-Queries ausführen

**Option A (GUI, empfohlen): Apache Jena Fuseki**
1. Fuseki starten → http://localhost:3030
2. Neues Dataset anlegen (z. B. `movielens`)
3. Datei `src/movielens_transformed.ttl` hochladen
4. Im Tab **Query** ausführen – Prefix:
PREFIX movie: http://example.org/movielens/

PREFIX xsd: http://www.w3.org/2001/XMLSchema#

5. Fragen aus `sparql_queries.md` verwenden
>>>>>>> 647dfb9 (Initial commit - add project)
