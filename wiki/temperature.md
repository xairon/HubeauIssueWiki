# Température des cours d'eau

> 10 issues analysées

## Guide

### Comportement actuel  
L'API "Température des cours d'eau" propose des endpoints pour accéder à des données historiques et en temps réel, principalement en format JSON. Les paramètres clés incluent `code_departement`, `size`, et `en_service` pour filtrer les stations. La pagination est limitée à 20 000 résultats maximum (produit de `page` * `size`), avec une taille de page par défaut de 1 000. Les données de stations non en service sont accessibles via le paramètre `en_service`, contrairement à d'autres APIs comme GeoRivière.  

### Pièges à éviter  
La limite de pagination (20 000 résultats) peut bloquer les requêtes volumineuses, nécessitant des appels multiples (#236). Les données récentes sont rares (dernières en 2021) en raison de stations décommissées (#110). L'export Naiades contient des dates incorrectes à la fin des exports, limitant son utilité. Les utilisateurs doivent vérifier la disponibilité des données via des sources alternatives.  

### Bonnes pratiques  
Utilisez le paramètre `en_service` pour filtrer les stations actives. Pour des historiques longs, combinez l'API avec des sources externes comme Naiades, en vérifiant la qualité des dates. Le package R `hubeau` simplifie les requêtes (#137). Testez les requêtes avec des paramètres `size` et `page` optimisés pour éviter les erreurs de pagination.  

### Contexte métier  
Les stations sont identifiées par des codes BSS (Base de Stations de Surveillance) et SANDRE (Système d'Information sur les Réseaux et les Données de l'Environnement). Le paramètre `en_service` indique si une station est opérationnelle, crucial pour l'analyse des données. Les données proviennent principalement de mesures en temps réel et d'archives historiques, souvent liées à des réseaux comme Naiades.  

### Évolutions récentes  
- **2025-06-13 (#236)** : Limite de pagination à 20 000 résultats persiste, avec des erreurs à partir de la page 21.  
- **2022-07-11 (#117)** : Réparation des erreurs serveur interne sur les endpoints `chronique` et `station`.  
- **2022-10-11 (#124)** : Correction de l'erreur 500 sur la route `/temperature/station`, rétablissant l'accès JSON/CSV.  
- **2019-04-27 (#18)** : Mise à jour pour distinguer correctement les horodatages AM/PM.  

### Historique notable  
- **2018-06-15 (#6)** : Correction du bug CSV où seuls les 10 premiers champs étaient renvoyés.  
- **2019-06-07 (#21)** : Réparation des dates futures (2045/2046) liées à la station 03047445.  
- **2021-12-20 (#91)** : Résolution de l'erreur interne serveur pour une requête spécifique.  
- **2022-03-07 (#108)** : Introduction du paramètre `en_service` pour indiquer l'état des stations.

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Les données d'origine (Naiades) contiennent des horodatages correctement distingués entre AM et PM. (#18)
- L'API Température des cours d'eau utilise un paramètre `en_service` pour indiquer l'état d'une station, contrairement à GeoRivière qui utilise une date de fin. (#108)
- La logique actuelle pour déterminer si une station est en service dans GeoRivière repose sur la présence d'une date de fin, ce qui peut être moins explicite qu'un paramètre booléen. (#108)
- La gestion de l'état des stations (en service ou non) est cruciale pour l'analyse des données hydrologiques et la prise de décision. (#108)
- L'API ne fournit pas de données récentes (les dernières données disponibles datent de 2021) (#110)
- Le lien fourni par l'API montre des données obsolètes selon les utilisateurs (#110)
- Plusieurs stations de mesure ont été arrêtées autour de 2013, limitant la disponibilité des données récentes (#110)
- Les utilisateurs demandent des alternatives pour obtenir des données de température récentes (#110)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- L'API impose une limite de 20 000 résultats maximum (produit de `page` * `size`), ce qui peut bloquer les requêtes même avec une taille de page optimale. (#236)
- La taille de page par défaut est de 1 000, ce qui nécessite 20 appels pour atteindre 20 000 résultats. (#236)
- L'erreur se produit à partir de la page 21 avec une taille de 1 000 (21 * 1 000 = 21 000 > 20 000). (#236)
- La limite de 20 000 n'est pas appliquée correctement si le paramètre `size` est omis, permettant des requêtes non limitées. (#236)
- L'export de données depuis Naiades contient des dates incorrectes à la fin de l'export, limitant son utilité pour les utilisateurs. (#236)
- Les utilisateurs ont besoin d'accéder à des historiques de température sur de longues périodes (ex. 2011-2024), mais l'API et l'export actuels posent des problèmes de limites et de qualité des données. (#236)

### Historique des problèmes résolus

- ~~La version CSV de l'API Température des cours d'eau ne retournait pas tous les champs attendus (code_parametre à libelle_qualification) avant la correction du 15 juin 2018 (#6)~~
- ~~La version JSON de l'API fonctionnait correctement en retournant tous les champs attendus (#6)~~
- ~~L'API ne distinguait pas les horodatages AM/PM, entraînant des erreurs de formatage des dates. (#18)~~
- ~~L'API a retourné des dates futures (2045/2046) pour des mesures de température (#21)~~
- ~~La station 03047445 contenait plus de 30 000 entrées avec des dates incorrectes (#21)~~
- ~~L'API renvoie un 'Internal server error' lors de la requête avec les paramètres code_departement=45, size=20, exact_count=true, format=json et pretty. (#91)~~
- ~~L'API Température des cours d'eau a renvoyé des erreurs de serveur interne lors de requêtes vers des endpoints spécifiques (chronique et station). (#117)~~
- ~~La route API /temperature/station a rencontré un erreur 500 serveur pour certains paramètres, y compris l'exemple fourni, et était indisponible en format JSON et CSV. (#124)~~

### Issues sources

- **#6** [Température] Opération chronique.csv ne retourne pas tous les champs (2018-06-15) — L'API Température des cours d'eau présentait un bug dans le format CSV où seuls les 10 premiers champs étaient renvoyés, corrigé par la mise à jour beta-1 du 15 juin 2018.
- **#18** [API TEMPERATURE] - horodatage AM PM erroné (2019-04-27) — L'API de température des cours d'eau présentait un bug de formatage des horodatages (AM/PM), corrigé par une mise à jour en avril 2019.
- **#21** [API température] Données incorrectes (2019-06-07) — L'API de température a corrigé des erreurs de dates futures liées à la station 03047445.
- **#91** [API Températures des cours d'eau] Internal server error (2021-12-20) — L'API de température des cours d'eau a rencontré un erreur serveur interne pour une requête spécifique, signalant un problème technique résolu.
- **#108** [API Qualité de l'eau] Paramètre de station en service (2022-03-07) — L'issue propose d'étendre le paramètre `en_service` utilisé dans l'API Température des cours d'eau à d'autres APIs pour une meilleure cohérence et clarté.
- **#110** [API Temperature] pas de données (2022-07-08) — L'API de température de Hub'Eau présente des limitations de données récentes (dernières données en 2021) et des stations décommissées, nécessitant des alternatives pour les utilisateurs.
- **#117** [API Température des cours d'eau] Internal server error (2022-07-11) — L'API Température des cours d'eau a temporairement rencontré des erreurs de serveur interne, mais le problème a été résolu.
- **#124** Erreur 500 sur la route chronique de l'api de récupération des températures d'eau (2022-10-11) — Une erreur 500 sur l'API de température des cours d'eau a été corrigée, rendant à nouveau disponible l'accès aux données en JSON et CSV.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#236** [API Température des cours d'eau] Problème lié à la pagination de l'API (2025-06-13) — L'API Température des cours d'eau a une limite de pagination (20 000 résultats max) qui empêche les requêtes volumineuses, et l'alternative Naiades présente des erreurs de dates.

</details>
