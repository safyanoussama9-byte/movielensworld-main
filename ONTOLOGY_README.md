# ONTOLOGY_README

Diese mini Ontologie (Turtle `movielens_ontology.ttl`) modelliert **MovieLens-ähnliche Daten**:
Filme, Nutzer, Bewertungen, Tags/Tagging, Genres sowie Sessions/Interaktionen. Sie lehnt sich an
`schema.org`, `DBpedia Ontology`, `FOAF` und `SKOS` an.

## Mapping (CSV → RDF)
- `movies.csv` → `ml:Movie` + `ml:movieTitle`, `ml:hasGenre`
- `links.csv` → `ml:imdbId`, `ml:tmdbId`
- `ratings.csv` → `ml:Rating` + `ml:hasRating` (User→Rating), `ml:ratedItem` (Rating→Movie), `ml:ratingValue`, `ml:ratingTimestamp`
- `tags.csv` → `ml:Tagging` + `ml:taggingHasTag`, `ml:taggingOfMovie`, `ml:hasTagging`, `ml:taggingTimestamp`
- `genome-tags.csv`/`genome-scores.csv` → `ml:Tag`, `ml:TagRelevance` + `ml:hasTagRelevance`, `ml:relevanceTag`, `ml:relevanceScore`
- `user_profiles.csv` → Eigenschaften an `ml:User` (z. B. `ml:userOccupation`, `ml:signupYear`)
- `sessions.csv` → `ml:Session`, `ml:Interaction` + `ml:interactionUser`, `ml:interactionItem`, `ml:inSession`, Zeit/Typ

## URI‑Design (Beispiel)
- Nutzer: `ex:user/{userId}` – z. B. `ex:user/42`
- Filme: `ex:movie/{movieId}`
- Rating: `ex:rating/{userId}-{movieId}-{timestamp}`
- Tagging: `ex:tagging/{userId}-{movieId}-{tagId}-{timestamp}`
- Tag: `ex:tag/{tagId}`
- Genre: `ex:genre/{name}` (slug)

## Nächste Schritte
1. **Transformationsskript**: CSV → Turtle (`movielens_transformed.ttl`) gemäß Ontologie.
2. **Triple Store (z. B. Fuseki)** laden.
3. **SPARQL‑Queries** gegen **deinen** Graphen ausführen und dokumentieren.
