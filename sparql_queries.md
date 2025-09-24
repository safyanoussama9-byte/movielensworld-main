
# SPARQL Queries – MovieLens (lokal in Fuseki getestet)

## 1) Anzahl Filme, Ratings und User
**Frage:** Wie viele verschiedene Filme, Bewertungen und Benutzer gibt es?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT 
  (COUNT(DISTINCT ?m) AS ?movies)
  (COUNT(DISTINCT ?r) AS ?ratings)
  (COUNT(DISTINCT ?u) AS ?users)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?m ;
     movie:user ?u .
}
```
**Erklärung:** Zählt eindeutige Filme, Ratings und User.

---

## 2) Alle Filme mit Rating > 4.0
**Frage:** Welche Filme haben ein Rating größer als 4.0?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie ?rating
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie ;
     movie:value ?rating .
  FILTER(xsd:decimal(?rating) > 4.0)
}
LIMIT 10
```
**Erklärung:** Listet die Filme mit Bewertung größer 4.0.

---

## 3) Filme mit durchschnittlichem Rating > 4.5
**Frage:** Welche Filme haben eine durchschnittliche Bewertung über 4.5?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (AVG(xsd:decimal(?rating)) AS ?avgRating)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie ;
     movie:value ?rating .
}
GROUP BY ?movie
HAVING (AVG(xsd:decimal(?rating)) > 4.5)
```
**Erklärung:** Berechnet Durchschnittsbewertungen je Film und filtert > 4.5.

---

## 4) Top 5 Filme mit den meisten Ratings
**Frage:** Welche 5 Filme haben die meisten Bewertungen?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (COUNT(?r) AS ?ratingCount)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie .
}
GROUP BY ?movie
ORDER BY DESC(?ratingCount)
LIMIT 5
```
**Erklärung:** Aggregiert die Anzahl Ratings pro Film.

---

## 5) User mit den meisten Ratings
**Frage:** Welcher Benutzer hat die meisten Bewertungen abgegeben?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?user (COUNT(?r) AS ?ratingCount)
WHERE {
  ?r a movie:Rating ;
     movie:user ?user .
}
GROUP BY ?user
ORDER BY DESC(?ratingCount)
LIMIT 1
```
**Erklärung:** Zählt die Ratings pro Benutzer.

---

## 6) Durchschnittliche Bewertung pro Benutzer
**Frage:** Welcher User gibt im Schnitt die höchsten Bewertungen?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?user (AVG(xsd:decimal(?rating)) AS ?avgRating)
WHERE {
  ?r a movie:Rating ;
     movie:user ?user ;
     movie:value ?rating .
}
GROUP BY ?user
ORDER BY DESC(?avgRating)
LIMIT 5
```
**Erklärung:** Berechnet den Durchschnitt pro User.

---

## 7) Alle Filme bewertet von einem bestimmten User
**Frage:** Welche Filme hat User1 bewertet?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie ?rating
WHERE {
  ?r a movie:Rating ;
     movie:user <http://example.org/movielens/user/1> ;
     movie:movie ?movie ;
     movie:value ?rating .
}
LIMIT 10
```
**Erklärung:** Gibt die Ratings von User1 zurück.

---

## 8) Anzahl Bewertungen pro Film (aufsteigend)
**Frage:** Wie viele Bewertungen hat jeder Film (aufsteigend sortiert)?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (COUNT(?r) AS ?ratingCount)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie .
}
GROUP BY ?movie
ORDER BY ASC(?ratingCount)
LIMIT 10
```
**Erklärung:** Listet Filme mit ihren Bewertungsanzahlen.

---

## 9) Filme mit exakt Rating 5.0
**Frage:** Welche Filme haben ein Rating von 5.0?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie ?rating
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie ;
     movie:value ?rating .
  FILTER(xsd:decimal(?rating) = 5.0)
}
LIMIT 10
```
**Erklärung:** Filtert auf Bewertungen mit Wert 5.0.

---

## 10) User, die denselben Film bewertet haben
**Frage:** Welche Benutzer haben denselben Film bewertet?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie ?user1 ?user2
WHERE {
  ?r1 a movie:Rating ;
      movie:movie ?movie ;
      movie:user ?user1 .
  ?r2 a movie:Rating ;
      movie:movie ?movie ;
      movie:user ?user2 .
  FILTER(?user1 != ?user2)
}
LIMIT 10
```
**Erklärung:** Findet Paare von Usern, die denselben Film bewertet haben.

---

## 11) Top 5 User mit den meisten 5-Sterne-Bewertungen
**Frage:** Wer vergibt die meisten 5.0-Ratings?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?user (COUNT(?r) AS ?fiveStarCount)
WHERE {
  ?r a movie:Rating ;
     movie:user ?user ;
     movie:value ?rating .
  FILTER(xsd:decimal(?rating) = 5.0)
}
GROUP BY ?user
ORDER BY DESC(?fiveStarCount)
LIMIT 5
```
**Erklärung:** Zählt die 5-Sterne-Bewertungen pro User.

---

## 12) Filme mit mehr als 20 Bewertungen
**Frage:** Welche Filme haben über 20 Ratings?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (COUNT(?r) AS ?ratingCount)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie .
}
GROUP BY ?movie
HAVING (COUNT(?r) > 20)
ORDER BY DESC(?ratingCount)
```
**Erklärung:** Filtert Filme mit mehr als 20 Bewertungen.

---

## 13) User mit durchschnittlichem Rating < 2.0
**Frage:** Welche Benutzer vergeben im Schnitt weniger als 2 Sterne?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?user (AVG(xsd:decimal(?rating)) AS ?avgRating)
WHERE {
  ?r a movie:Rating ;
     movie:user ?user ;
     movie:value ?rating .
}
GROUP BY ?user
HAVING (AVG(xsd:decimal(?rating)) < 2.0)
```
**Erklärung:** Findet besonders kritische User.

---

## 14) Filme bewertet von mindestens 10 verschiedenen Usern
**Frage:** Welche Filme wurden von mehr als 10 unterschiedlichen Usern bewertet?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (COUNT(DISTINCT ?user) AS ?userCount)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie ;
     movie:user ?user .
}
GROUP BY ?movie
HAVING (COUNT(DISTINCT ?user) > 10)
```
**Erklärung:** Misst die Popularität anhand verschiedener User.

---

## 15) Filme mit durchschnittlichem Rating zwischen 3.0 und 4.0
**Frage:** Welche Filme haben ein durchschnittliches Rating zwischen 3.0 und 4.0?  
**SPARQL:**
```sparql
PREFIX movie: <http://example.org/movielens/>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?movie (AVG(xsd:decimal(?rating)) AS ?avgRating)
WHERE {
  ?r a movie:Rating ;
     movie:movie ?movie ;
     movie:value ?rating .
}
GROUP BY ?movie
HAVING (AVG(xsd:decimal(?rating)) >= 3.0 && AVG(xsd:decimal(?rating)) <= 4.0)
LIMIT 10
```
**Erklärung:** Filtert Filme mit mittleren Bewertungen.
