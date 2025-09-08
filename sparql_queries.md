# DBpedia – 25 SPARQL Queries (MovieLens/Film-Thema)

Endpoint: https://dbpedia.org/sparql  
Jede Aufgabe enthält **Frage**, **SPARQL** und **kurze Erklärung**. Prefixe stehen pro Query dabei.

---

## 1) Deutsche Filme seit 2010 (Titel + Jahr)
**Frage:** Welche deutschen Filme wurden seit 2010 veröffentlicht?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?film ?label ?year WHERE {
  ?film rdf:type dbo:Film ;
        dbo:country dbr:Germany ;
        dbo:releaseDate ?date ;
        rdfs:label ?label .
  BIND(year(xsd:date(?date)) AS ?year)
  FILTER (?year >= 2010)
  FILTER (lang(?label) IN ("de","en"))
}
ORDER BY DESC(?year)
LIMIT 50
```
**Erklärung:** Filtert Filme mit `dbo:country Germany` und Jahr ≥ 2010; Labels nur DE/EN.

---

## 2) Filmografie Christopher Nolan (mit Jahr)
**Frage:** Welche Filme hat Christopher Nolan gedreht und in welchem Jahr?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?film ?title ?year WHERE {
  ?film rdf:type dbo:Film ;
        dbo:director dbr:Christopher_Nolan ;
        rdfs:label ?title .
  OPTIONAL { ?film dbo:releaseDate ?d . BIND(year(xsd:date(?d)) AS ?year) }
  FILTER (lang(?title) IN ("de","en"))
}
ORDER BY ?year
```
**Erklärung:** Auswahl über `dbo:director`; Jahr optional, da nicht immer vorhanden.

---

## 3) Schauspieler:innen aus Berlin (mit Beispiel-Film)
**Frage:** Welche Schauspieler:innen sind in Berlin geboren (mit Beispiel-Film)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT DISTINCT ?actor ?name ?sampleFilm WHERE {
  ?actor rdf:type dbo:Actor ;
         dbo:birthPlace dbr:Berlin ;
         rdfs:label ?name .
  OPTIONAL { ?film rdf:type dbo:Film ; dbo:starring ?actor . BIND(?film AS ?sampleFilm) }
  FILTER (lang(?name) IN ("de","en"))
}
LIMIT 50
```
**Erklärung:** `dbo:birthPlace` auf Berlin; OPTIONAL zeigt einen Beispiel-Film.

---

## 4) Lange Filme (>150 Minuten)
**Frage:** Welche Filme dauern länger als 150 Minuten?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?film ?runtime WHERE {
  ?film rdf:type dbo:Film ;
        dbo:runtime ?runtime .
  FILTER (?runtime > 150)
}
ORDER BY DESC(?runtime)
LIMIT 50
```
**Erklärung:** Numerischer Filter auf `dbo:runtime`.

---

## 5) Anzahl Filme je Produktionsland (Top 15)
**Frage:** Welche Länder produzieren die meisten Filme (Top 15)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?country (COUNT(*) AS ?nFilms) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:country ?country .
}
GROUP BY ?country
ORDER BY DESC(?nFilms)
LIMIT 15
```
**Erklärung:** Aggregation über `dbo:country`.

---

## 6) Produktivste Regisseur:innen (Top 20)
**Frage:** Welche Regisseur:innen haben die meisten Filme in DBpedia (Top 20)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?director (COUNT(?f) AS ?n) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:director ?director .
}
GROUP BY ?director
ORDER BY DESC(?n)
LIMIT 20
```
**Erklärung:** Gruppierung nach `dbo:director` und Zählen.

---

## 7) Häufige Co‑Stars von Robert De Niro
**Frage:** Mit wem stand Robert De Niro am häufigsten gemeinsam vor der Kamera?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?costar (COUNT(*) AS ?together) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:starring dbr:Robert_De_Niro ;
     dbo:starring ?costar .
  FILTER (?costar != dbr:Robert_De_Niro)
}
GROUP BY ?costar
ORDER BY DESC(?together)
LIMIT 25
```
**Erklärung:** Zwei `dbo:starring`-Links auf demselben Film, einer davon De Niro.

---

## 8) Oscar „Best Picture“ – Gewinnerliste
**Frage:** Welche Filme gewannen den Academy Award for Best Picture?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film rdf:type dbo:Film ;
        dbo:award dbr:Academy_Award_for_Best_Picture .
}
LIMIT 200
```
**Erklärung:** Filter auf `dbo:award`.

---

## 9) Filme, die auf Romanen basieren
**Frage:** Welche Filme basieren auf Romanen/Büchern?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?film ?source WHERE {
  ?film rdf:type dbo:Film ;
        dbo:basedOn ?source .
}
LIMIT 100
```
**Erklärung:** Nutzung von `dbo:basedOn`.

---

## 10) Animationsfilme der 1990er
**Frage:** Welche Animationsfilme erschienen in den 1990ern?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?film ?year WHERE {
  ?film rdf:type dbo:Film ;
        dbo:genre dbr:Animated_film ;
        dbo:releaseDate ?d .
  BIND(year(xsd:date(?d)) AS ?year)
  FILTER (?year >= 1990 && ?year < 2000)
}
ORDER BY ?year
```
**Erklärung:** Genre-Filter `Animated_film` + Jahresbereich.

---

## 11) In Berlin gedrehte Filme
**Frage:** Welche Filme wurden in Berlin gedreht?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film rdf:type dbo:Film ;
        dbo:filmingLocation dbr:Berlin .
}
LIMIT 100
```
**Erklärung:** `dbo:filmingLocation` auf `dbr:Berlin`.

---

## 12) Science‑Fiction‑Filme (Titel + Regie)
**Frage:** Welche Sci‑Fi‑Filme gibt es (mit Titel/Regie)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film ?title ?director WHERE {
  ?film rdf:type dbo:Film ;
        dbo:genre dbr:Science_fiction_film ;
        rdfs:label ?title .
  OPTIONAL { ?film dbo:director ?director }
  FILTER (lang(?title) IN ("de","en"))
}
LIMIT 100
```
**Erklärung:** Genre-Filter + OPTIONAL Regisseur.

---

## 13) Mehrsprachige Filme (≥ 2 Sprachen)
**Frage:** Welche Filme sind mehrsprachig (mind. 2 Sprachen)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?film (COUNT(DISTINCT ?lang) AS ?nLang) WHERE {
  ?film rdf:type dbo:Film ;
        dbo:language ?lang .
}
GROUP BY ?film
HAVING (COUNT(DISTINCT ?lang) >= 2)
ORDER BY DESC(?nLang)
LIMIT 50
```
**Erklärung:** Gruppierung + HAVING-Bedingung.

---

## 14) Produzent:innen mit den meisten Filmen
**Frage:** Wer hat die meisten Filme produziert (Top 25)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?producer (COUNT(?f) AS ?n) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:producer ?producer .
}
GROUP BY ?producer
ORDER BY DESC(?n)
LIMIT 25
```
**Erklärung:** Aggregation über `dbo:producer`.

---

## 15) Besetzung von „Inception“
**Frage:** Wer spielt in „Inception“ mit?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?actor WHERE {
  dbr:Inception dbo:starring ?actor .
}
```
**Erklärung:** Direkte Abfrage der `dbo:starring`-Kanten.

---

## 16) Abstract (DE/EN) zu „Inception“
**Frage:** Gib die Kurzbeschreibung zu „Inception“ auf Deutsch/Englisch aus.  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?lang ?abstract WHERE {
  dbr:Inception dbo:abstract ?abstract .
  BIND (lang(?abstract) AS ?lang)
  FILTER (?lang IN ("de","en"))
}
```
**Erklärung:** Nutzung von Abstracts in mehreren Sprachen.

---

## 17) Schauspieler:innen mit den meisten Auftritten
**Frage:** Welche Schauspieler:innen haben die meisten `dbo:starring`-Auftritte (Top 25)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?actor (COUNT(?f) AS ?nFilms) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:starring ?actor .
}
GROUP BY ?actor
ORDER BY DESC(?nFilms)
LIMIT 25
```
**Erklärung:** Zählt Filme je Person mit `starring`.

---

## 18) Personen, die Regie führten **und** schauspielerten
**Frage:** Wer hat mindestens einen Film gedreht und in einem (anderen) gespielt?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT DISTINCT ?person WHERE {
  ?f1 rdf:type dbo:Film ; dbo:director ?person .
  ?f2 rdf:type dbo:Film ; dbo:starring ?person .
}
LIMIT 100
```
**Erklärung:** Schnittmenge von Regie- und Schauspielmengen.

---

## 19) Durchschnittliche Laufzeit je Genre
**Frage:** Wie lang sind Filme im Schnitt je Genre (Top 25)?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?genre (AVG(?rt) AS ?avgRuntime) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:genre ?genre ;
     dbo:runtime ?rt .
}
GROUP BY ?genre
ORDER BY DESC(?avgRuntime)
LIMIT 25
```
**Erklärung:** Mittelwert über `dbo:runtime` pro Genre.

---

## 20) Früheste Veröffentlichungen von Studio Ghibli
**Frage:** Was sind die frühesten Veröffentlichungen von Studio Ghibli?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?film (MIN(year(xsd:date(?d))) AS ?firstYear) WHERE {
  ?film rdf:type dbo:Film ;
        dbo:productionCompany dbr:Studio_Ghibli ;
        dbo:releaseDate ?d .
}
GROUP BY ?film
ORDER BY ?firstYear
LIMIT 10
```
**Erklärung:** Filter auf `dbo:productionCompany` + Aggregation.

---

## 21) Filme mit Musik von Hans Zimmer
**Frage:** Zu welchen Filmen hat Hans Zimmer die Musik komponiert?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film rdf:type dbo:Film ;
        dbo:musicComposer dbr:Hans_Zimmer .
}
LIMIT 200
```
**Erklärung:** Filter auf `dbo:musicComposer`.

---

## 22) Gemeinsame Filme: De Niro & Al Pacino
**Frage:** In welchen Filmen spielen Robert De Niro **und** Al Pacino zusammen?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film rdf:type dbo:Film ;
        dbo:starring dbr:Robert_De_Niro , dbr:Al_Pacino .
}
```
**Erklärung:** Zwei `starring`-Bindings auf dasselbe Film-Subjekt.

---

## 23) Anzahl Filme je Jahrzehnt
**Frage:** Wie viele Filme gibt es je Jahrzehnt?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?decade (COUNT(*) AS ?n) WHERE {
  ?f rdf:type dbo:Film ;
     dbo:releaseDate ?d .
  BIND (SUBSTR(STR(year(xsd:date(?d))),1,3) AS ?dec)
  BIND (CONCAT(?dec, "0s") AS ?decade)
}
GROUP BY ?decade
ORDER BY ?decade
```
**Erklärung:** Formt das Jahr zu Dekaden um und zählt.

---

## 24) Drehlocations in Deutschland (mit Koordinaten)
**Frage:** Welche Filme (Land: Germany) haben Drehlocations in Deutschland – mit Koordinaten?  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film ?place ?lat ?long WHERE {
  ?film rdf:type dbo:Film ;
        dbo:country dbr:Germany ;
        dbo:filmingLocation ?place .
  OPTIONAL { ?place dbo:latitude ?lat ; dbo:longitude ?long }
}
LIMIT 100
```
**Erklärung:** Produktionsland + Drehlocation + optionale Geokoordinaten.

---

## 25) Filme + (aggregierte) Besetzung nach Jahr
**Frage:** Liste Filme mit Jahr und aggregierter Besetzung (falls vorhanden).  
**SPARQL:**
```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
SELECT ?film ?title ?year (GROUP_CONCAT(DISTINCT STR(?actor); separator=", ") AS ?cast) WHERE {
  ?film rdf:type dbo:Film ;
        rdfs:label ?title ;
        dbo:releaseDate ?d .
  OPTIONAL { ?film dbo:starring ?actor }
  BIND(year(xsd:date(?d)) AS ?year)
  FILTER (lang(?title) IN ("de","en"))
}
GROUP BY ?film ?title ?year
ORDER BY DESC(?year)
LIMIT 100
```
**Erklärung:** Aggregiert `starring`-Werte je Film und sortiert nach Jahr.
