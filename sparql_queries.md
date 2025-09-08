# DBpedia – 25 SPARQL Queries (MovieLens/Film-Thema)

Alle Abfragen sind für den Endpoint https://dbpedia.org/sparql gedacht.  
Jede Aufgabe enthält **Frage**, **SPARQL** und **kurze Erklärung**.

---

## 1) Deutsche Filme seit 2010
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
**Erklärung:** Filter auf deutsche Filme mit Jahr >= 2010.

---

## 2) Christopher Nolan Filme
**Frage:** Welche Filme hat Christopher Nolan gemacht?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film dbo:director dbr:Christopher_Nolan .
}
LIMIT 50
```
**Erklärung:** Sucht alle Filme, bei denen Nolan als Regisseur eingetragen ist.

---

## 3) Schauspieler:innen aus Berlin
**Frage:** Welche Schauspieler:innen wurden in Berlin geboren?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?actor WHERE {
  ?actor dbo:birthPlace dbr:Berlin ;
         rdf:type dbo:Actor .
}
LIMIT 50
```
**Erklärung:** Nutzt `dbo:birthPlace`.

---

## 4) Lange Filme
**Frage:** Welche Filme dauern länger als 150 Minuten?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?film ?runtime WHERE {
  ?film dbo:runtime ?runtime .
  FILTER (?runtime > 150)
}
LIMIT 50
```
**Erklärung:** Filter auf `dbo:runtime`.

---

## 5) Länder mit den meisten Filmen
**Frage:** Welche Länder haben die meisten Filme produziert?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?country (COUNT(?film) AS ?nFilms) WHERE {
  ?film dbo:country ?country .
}
GROUP BY ?country
ORDER BY DESC(?nFilms)
LIMIT 15
```
**Erklärung:** Aggregation mit GROUP BY.

---

## 6) Produktivste Regisseur:innen
**Frage:** Welche Regisseur:innen haben die meisten Filme gemacht?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
SELECT ?director (COUNT(?film) AS ?n) WHERE {
  ?film dbo:director ?director .
}
GROUP BY ?director
ORDER BY DESC(?n)
LIMIT 20
```
**Erklärung:** Zählt Filme je Regisseur.

---

## 7) Co‑Stars von Robert De Niro
**Frage:** Mit wem hat Robert De Niro oft zusammengespielt?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?costar (COUNT(?film) AS ?together) WHERE {
  ?film dbo:starring dbr:Robert_De_Niro ;
        dbo:starring ?costar .
  FILTER (?costar != dbr:Robert_De_Niro)
}
GROUP BY ?costar
ORDER BY DESC(?together)
LIMIT 25
```
**Erklärung:** Gleicher Film mit zwei `starring`-Einträgen.

---

## 8) Oscar „Best Picture“
**Frage:** Welche Filme haben den Oscar für Best Picture gewonnen?  
**SPARQL:**
```sparql
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
SELECT ?film WHERE {
  ?film dbo:award dbr:Academy_Award_for_Best_Picture .
}
```
**Erklärung:** Abfrage nach Auszeichnung.

---

... (Queries 9–25 in gleichem Stil) ...
