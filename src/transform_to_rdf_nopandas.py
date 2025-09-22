# src/transform_to_rdf_nopandas.py
# -*- coding: utf-8 -*-
"""
CSV -> RDF (Turtle) für MovieLensWorld
Ohne pandas; nur csv + rdflib.
Erzeugt: src/movielens_transformed.ttl

Aufruf (aus dem Repo-Hauptordner):
    py src/transform_to_rdf_nopandas.py --root .

Benötigt:
    pip install rdflib
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, Tuple
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD

# ---------- Namespaces ----------
MOVIE = Namespace("http://example.org/movielens/")
SCHEMA = Namespace("http://schema.org/")
XSD_NS = XSD

# Klassen/Properties (an Ontologie movielens_ontology.ttl angelehnt)
# Falls deine Ontologie andere Prädikate hat, bitte hier anpassen.
CLS_MOVIE   = MOVIE.Movie
CLS_USER    = MOVIE.User
CLS_RATING  = MOVIE.Rating
CLS_TAG     = MOVIE.Tag

P_TITLE     = MOVIE.title
P_GENRES    = MOVIE.genres
P_HASRATING = MOVIE.hasRating        # Movie -> Rating
P_USER      = MOVIE.user             # Rating -> User
P_MOVIE     = MOVIE.movie            # Rating -> Movie
P_VALUE     = MOVIE.value            # Rating -> xsd:decimal
P_TAGVALUE  = MOVIE.tagValue         # Tag -> Literal
P_HAS_TAG   = MOVIE.hasTag           # Movie -> Tag

# ---------- Hilfen ----------
def safe_uri(base: Namespace, kind: str, raw: str) -> URIRef:
    """
    Baut eine 'saubere' URI:
        http://example.org/movielens/<kind>/<raw>
    Entfernt Leerzeichen/ungewollte Zeichen.
    """
    cleaned = "".join(c for c in raw.strip() if c.isalnum() or c in "-_")
    return URIRef(str(base) + f"{kind}/{cleaned}")

def load_movies(g: Graph, movies_csv: Path) -> Dict[str, URIRef]:
    """
    movies.csv: movieId,title,genres
    Legt Movie-Ressourcen an und beschriftet sie.
    """
    id2movie: Dict[str, URIRef] = {}
    with movies_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row.get("movieId") or row.get("movie_id") or row.get("movieID")
            if not mid:
                continue
            m_uri = safe_uri(MOVIE, "movie", mid)
            id2movie[mid] = m_uri

            g.add((m_uri, RDF.type, CLS_MOVIE))

            title = (row.get("title") or "").strip()
            if title:
                g.add((m_uri, P_TITLE, Literal(title)))

            genres = (row.get("genres") or "").strip()
            if genres and genres != "(no genres listed)":
                # Genres als 1 Literal oder – wenn du willst – splitten und mehrere Literale anhängen
                g.add((m_uri, P_GENRES, Literal(genres)))

    return id2movie

def load_ratings(g: Graph, ratings_csv: Path, id2movie: Dict[str, URIRef]) -> Tuple[int, int]:
    """
    ratings.csv: userId,movieId,rating,timestamp
    Legt Rating-Ressourcen an und verlinkt User/Movie.
    """
    user_cache: Dict[str, URIRef] = {}
    added = 0
    skipped = 0

    with ratings_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row.get("userId") or row.get("user_id") or row.get("userID")
            mid = row.get("movieId") or row.get("movie_id") or row.get("movieID")
            val = row.get("rating")

            if not uid or not mid or not val:
                skipped += 1
                continue

            m_uri = id2movie.get(mid)
            if not m_uri:
                skipped += 1
                continue

            # User-Ressource (aus Cache)
            u_uri = user_cache.get(uid)
            if not u_uri:
                u_uri = safe_uri(MOVIE, "user", uid)
                user_cache[uid] = u_uri
                g.add((u_uri, RDF.type, CLS_USER))

            # Rating als eigene Ressource (deterministische ID)
            # Wenn timestamp existiert, macht es die ID eindeutig
            ts = (row.get("timestamp") or "").strip()
            rid_key = f"{uid}-{mid}-{ts or 't0'}"
            r_uri = safe_uri(MOVIE, "rating", rid_key)

            g.add((r_uri, RDF.type, CLS_RATING))
            g.add((r_uri, P_USER, u_uri))
            g.add((r_uri, P_MOVIE, m_uri))

            try:
                g.add((r_uri, P_VALUE, Literal(float(val), datatype=XSD_NS.decimal)))
            except Exception:
                # Fallback: als String
                g.add((r_uri, P_VALUE, Literal(val)))

            # Verknüpfe Movie -> Rating (Convenience-Property)
            g.add((m_uri, P_HASRATING, r_uri))

            added += 1

    return added, skipped

def load_tags(g: Graph, tags_csv: Path, id2movie: Dict[str, URIRef]) -> Tuple[int, int]:
    """
    tags.csv: userId,movieId,tag,timestamp
    Legt Tag-Ressourcen an und verknüpft sie mit dem Film.
    """
    added = 0
    skipped = 0

    if not tags_csv.exists():
        return added, skipped

    with tags_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row.get("movieId")
            tag_text = (row.get("tag") or "").strip()
            if not mid or not tag_text:
                skipped += 1
                continue

            m_uri = id2movie.get(mid)
            if not m_uri:
                skipped += 1
                continue

            # Tag-Ressource; ID aus Film + Text
            t_uri = safe_uri(MOVIE, "tag", f"{mid}-{tag_text[:40]}")
            g.add((t_uri, RDF.type, CLS_TAG))
            g.add((t_uri, P_TAGVALUE, Literal(tag_text)))

            # Verknüpfe Movie -> Tag
            g.add((m_uri, P_HAS_TAG, t_uri))

            added += 1

    return added, skipped

def main() -> None:
    parser = argparse.ArgumentParser(description="CSV -> RDF (Turtle) für MovieLensWorld (ohne pandas)")
    parser.add_argument("--root", type=str, default=".",
                        help="Projektwurzel (darin liegen data/ und src/). Standard: aktuelles Verzeichnis.")
    parser.add_argument("--out", type=str, default="src/movielens_transformed.ttl",
                        help="Ausgabedatei (Turtle). Standard: src/movielens_transformed.ttl")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data_dir = root / "data"
    out_path = (root / args.out).resolve()

    movies_csv  = data_dir / "movies.csv"
    ratings_csv = data_dir / "ratings.csv"
    tags_csv    = data_dir / "tags.csv"           # optional

    if not movies_csv.exists():
        raise FileNotFoundError(f"Nicht gefunden: {movies_csv}")
    if not ratings_csv.exists():
        raise FileNotFoundError(f"Nicht gefunden: {ratings_csv}")

    print(f"📁 Root:     {root}")
    print(f"📄 Movies:   {movies_csv.name}")
    print(f"📄 Ratings:  {ratings_csv.name}")
    if tags_csv.exists():
        print(f"📄 Tags:     {tags_csv.name} (optional)")

    # RDF-Graph
    g = Graph()
    g.bind("movie", MOVIE)
    g.bind("schema", SCHEMA)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD_NS)

    # Daten laden
    id2movie = load_movies(g, movies_csv)
    n_r_ok, n_r_skip = load_ratings(g, ratings_csv, id2movie)
    n_t_ok, n_t_skip = load_tags(g, tags_csv, id2movie)

    # Ausgeben
    out_path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(out_path), format="turtle")

    print("✅ RDF gespeichert:", out_path)
    print("   Filme:", len(id2movie))
    print("   Ratings:  OK =", n_r_ok, "| skipped =", n_r_skip)
    if tags_csv.exists():
        print("   Tags:     OK =", n_t_ok, "| skipped =", n_t_skip)
    print("   Tripel insgesamt:", len(g))

if __name__ == "__main__":
    main()
