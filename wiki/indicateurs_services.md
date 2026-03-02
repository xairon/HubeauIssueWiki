# Indicateurs des services

> 10 issues analysées

## Guide

### Comportement actuel

L'API Hub'Eau "Indicateurs des services" fournit principalement des données pour les services d'eau potable (#75, #195). Elle permet de filtrer les résultats par code indicateur (par exemple, 'D102.0') et par année (#72). L'endpoint `/communes` retourne les données à la granularité du service, même si une commune est desservie par plusieurs entités, avec un enregistrement par service incluant les `codes_service` et `noms_service` (#74). Pour la pagination, l'API renvoie un statut HTTP 200 OK si tous les éléments tiennent sur une page, ou 206 Partial Content sur la dernière page si le nombre d'éléments est inférieur à la taille demandée (#72).

### Pièges à éviter

*   **Absence de données d'assainissement:** L'API ne retourne pas de résultats pour les services d'assainissement collectif (AC) et non-collectif (ANC) (#75), et des indicateurs clés comme D201.0 et D301.0 sont absents (#195). Ce problème persiste car la refonte de l'API, prévue pour y remédier, a été reportée indéfiniment (#195). Les utilisateurs doivent donc se tourner vers d'autres sources pour ces données.
*   **Granularité des données communales inattendue:** L'endpoint `/communes` fournit des données par service et non agrégées par commune, même si plusieurs services desservent une commune. Contrairement à la documentation, aucune agrégation (min, max, moyenne) n'est calculée (#74). Les développeurs doivent agréger les données manuellement si une vue communale est requise.
*   **Fraîcheur des données limitée:** L'API ne propose des données que jusqu'à 2019 via l'endpoint `/indicateurs`, alors que des informations plus récentes (jusqu'à 2023) sont disponibles sur `services.eaufrance.fr` (#225). Pour les données les plus à jour, il est nécessaire de consulter directement la plateforme source.
*   **Format GeoJSON inopérant:** Le format GeoJSON n'est pas supporté par l'API "Indicateurs des services" car les données sous-jacentes ne contiennent pas de coordonnées géographiques. Bien que le swagger l'indique pour l'endpoint `communes`, les géométries sont vides ou la réponse est en JSON par défaut (#219). Il est donc inutile de demander ce format.
*   **Interprétation de la pagination:** Le code de statut HTTP (200 ou 206) ne suffit pas à déterminer la fin de la pagination. Pour une gestion fiable, fiez-vous uniquement à la présence de la balise 'next' dans la réponse de l'API pour savoir si d'autres pages sont disponibles (#72).
*   **Filtrage par code SANDRE d'ouvrage pour l'assainissement:** L'API ne permet pas d'interroger les données d'Assainissement Collectif via le code SANDRE de l'ouvrage (#78). Cette fonctionnalité est manquante, limitant la recherche par identifiant standard pour ce type de service.

### Bonnes pratiques

*   Pour une intégration facilitée dans des environnements R, privilégiez l'utilisation du package `hubeau` (disponible sur le CRAN). Il simplifie les requêtes avec une syntaxe dédiée (`get_[API]_[Operation]`) et structure les résultats en data.frame, couvrant l'API "Indicateurs des services" parmi d'autres (#137).
*   Lors de l'implémentation de la pagination, basez votre logique sur la présence de la balise 'next' dans la réponse de l'API. C'est le seul indicateur fiable pour détecter la dernière page, indépendamment du code de statut HTTP (200 ou 206) (#72).
*   Consultez la documentation officielle du package `hubeau` sur GitHub ou CRAN pour des exemples d'utilisation avancés et des vignettes illustrant l'intégration des données dans des analyses ou des visualisations (#137).

### Contexte métier

Les services publics d'eau et d'assainissement peuvent varier en granularité, une même commune pouvant être desservie par plusieurs services (#74). Les données de l'API incluent des indicateurs de performance spécifiques (ex: D102.0, P101.1, VP.178) pour ces services (#74). Le code SANDRE de l'ouvrage est un identifiant standard essentiel pour les infrastructures d'eau en France, notamment pour l'Assainissement Collectif (#78). Les indicateurs D201.0 et D301.0 représentent respectivement le nombre d'habitants desservis en Assainissement Collectif (AC) et Non Collectif (ANC) (#195).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Hub'Eau renvoie un code de statut HTTP 206 Partial Content sur la dernière page d'une requête paginée si le nombre d'éléments retournés est inférieur à la taille de page demandée (paramètre 'size'). (#72)
- L'API Hub'Eau renvoie un code de statut HTTP 200 OK si la taille de page demandée (paramètre 'size') est suffisante pour récupérer tous les éléments disponibles en une seule requête. (#72)
- La balise 'next' dans la réponse de l'API Hub'Eau est l'indicateur fiable pour déterminer si une page est la dernière d'une séquence paginée, indépendamment du code de statut HTTP (200 ou 206). (#72)
- Le code indicateur 'D102.0' est utilisé dans l'API indicateurs_services pour filtrer les données. (#72)
- Les données de l'API indicateurs_services peuvent être filtrées par année, par exemple '2012'. (#72)
- L'API `/indicateurs_services/communes` retourne un enregistrement par service pour une commune et une année données, même si la commune est desservie par plusieurs services. (#74)
- Contrairement à la documentation, l'API ne calcule pas et ne retourne pas de valeurs agrégées (minimum, maximum, moyenne) pour les indicateurs lorsqu'une commune est desservie par plusieurs services. (#74)
- Chaque enregistrement pour une commune et une année données contient un tableau `codes_service` et `noms_service` qui, dans l'exemple fourni, ne contient qu'un seul service, confirmant la granularité par service. (#74)
- Une même commune peut être desservie par plusieurs services publics d'eau et d'assainissement. (#74)
- Les données incluent des indicateurs de performance pour ces services (ex: D102.0, P101.1, VP.178). (#74)
- L'API Indicateurs des services ne retourne pas de résultats pour les services d'assainissement collectif (type_service=AC). (#75)
- L'API Indicateurs des services ne retourne pas de résultats pour les services d'assainissement non-collectif (type_service=ANC). (#75)
- L'API Indicateurs des services est prévue pour être refondue en 2023. (#75)
- Une nouvelle version de l'API Indicateurs des services, intégrant les corrections, devrait entrer en production après l'été 2023. (#75)
- Les données des services d'assainissement collectif (AC) et non-collectif (ANC) sont absentes de l'API Indicateurs des services. (#75)
- L'API Indicateurs des services fournit uniquement les résultats pour les services d'eau potable. (#75)
- Au 07/09/2021, l'API Indicateurs des services ne permettait pas d'interroger les données d'Assainissement Collectif via le code SANDRE de l'ouvrage. (#78)
- Le code SANDRE de l'ouvrage est un identifiant standard pour les infrastructures d'eau en France, pertinent pour les données d'Assainissement Collectif. (#78)
- L'API Indicateurs des services ne permet pas d'accéder aux indicateurs D201.0 et D301.0. (#195)
- Les indicateurs D201.0 et D301.0 ne sont pas implémentés dans l'API Indicateurs des services. (#195)
- Le point d'accès `indicateurs_services/indicateurs` semble ne renvoyer que des entrées pour l'eau potable pour certains indicateurs. (#195)
- Le chantier de refonte de l'API Indicateurs des services, qui devait résoudre ce problème, a été reporté sans replanification. (#195)
- Les évolutions de l'API Indicateurs des services évoquées dans l'issue #75 et attendues pour l'été 2023 n'ont pas été réalisées. (#195)
- Les indicateurs D201.0 et D301.0 représentent le nombre d'habitants desservis en Assainissement Collectif (AC) et Assainissement Non Collectif (ANC) respectivement. (#195)
- Les données d'assainissement (AC/ANC) par commune ne sont pas disponibles via l'API Indicateurs des services pour les indicateurs D201.0 et D301.0. (#195)
- Le format GeoJSON n'est pas implémenté sur l'API Hub'Eau "Indicateurs des services". (#219)
- Les données de la version 0 de l'API "Indicateurs des services" ne contiennent pas de coordonnées géographiques. (#219)
- Le format GeoJSON est désactivé sur tous les endpoints de l'API "Indicateurs des services", à l'exception de l'endpoint `communes`. (#219)
- Lorsqu'on demande le format GeoJSON sur l'endpoint `communes` de l'API "Indicateurs des services", les géométries retournées sont vides. (#219)
- Le comportement attendu pour l'endpoint `communes` de l'API "Indicateurs des services" (version 0) est de retourner une réponse au format JSON même si le format GeoJSON est demandé. (#219)
- Le swagger de l'API "Indicateurs des services" liste l'option GeoJSON pour l'endpoint `communes` alors qu'elle n'est pas fonctionnelle. (#219)
- Les utilisateurs de l'endpoint `communes` de l'API "Indicateurs des services" pourraient s'attendre à obtenir les géométries communales pour des usages cartographiques. (#219)
- La représentation géographique des "services" (au sens de l'API) est complexe. (#219)
- L'API 'Indicateurs des services' de Hub'Eau ne fournit des données que jusqu'à 2019 via l'endpoint `/indicateurs` (ex: `https://hubeau.eaufrance.fr/api/v0/indicateurs_services/indicateurs?code_indicateur=D102.0&size=5000`). (#225)
- Les indicateurs de service sont disponibles jusqu'à 2023 sur le site `services.eaufrance.fr`, ce qui indique un décalage de fraîcheur des données par rapport à l'API Hub'Eau. (#225)
- L'indicateur `D102.0` est un exemple d'indicateur de service affecté par le problème de fraîcheur des données. (#225)

### Historique des problèmes résolus

- ~~L'API Indicateurs des services a rencontré un bug où elle retournait des résultats vides pour certaines requêtes (ex: indicateurs?code_indicateur=P101.1, services?code_commune=17300). (#12)~~
- ~~Les données de l'API Indicateurs des services proviennent de la plateforme http://www.services.eaufrance.fr/donnees/telechargement. (#12)~~
- ~~La source des données pour l'API Indicateurs des services (www.services.eaufrance.fr/donnees/telechargement) est mise à jour hebdomadairement. (#12)~~
- ~~Le BRGM fournit un exemple d'appel de l'API Hub'Eau avec R pour les données piézométriques, disponible sur GitHub à l'adresse https://github.com/BRGM/hubeau/blob/master/code_examples/Trac%C3%A9%20d'une%20chronique%20pi%C3%A9zom%C3%A9trique%20avec%20R.ipynb. (#62)~~
- ~~Le BRGM prévoit de publier d'autres exemples de code R pour l'API Hub'Eau sur son dépôt GitHub à l'adresse https://github.com/BRGM/hubeau/tree/master/code_examples. (#62)~~
- ~~Un package R nommé `hubeau` est développé par INRAE pour interroger les APIs Hub'Eau. (#62)~~
- ~~Le package R `hubeau` inclut une fonction générique d'interrogation et des fonctions spécifiques par API/opération, retournant les résultats sous forme de data.frame. (#62)~~
- ~~Le package R `hubeau` prend en charge initialement les APIs 'Prélèvements en eau' et 'Indicateurs des services'. (#62)~~
- ~~Le package R `hubeau` est disponible sur GitHub à l'adresse https://github.com/inrae/hubeau et sa documentation à https://inrae.github.io/hubeau/. (#62)~~
- ~~L'API Hub'Eau présente des bugs connus, mentionnés dans les issues #72 et #74. (#62)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~

### Issues sources

- **#12** [API Indicateur de services] : pas de résultat  — L'API Indicateurs des services a connu un bug de résultats vides, désormais résolu, et ses données proviennent de services.eaufrance.fr avec une mise à jour hebdomadaire. `[résolu]`
- **#62** Utilisation de l'API dans R / Package dédié ? — Cette issue a mené au développement et à la publication du package R `hubeau` par INRAE pour interroger les APIs Hub'Eau, complété par des exemples de code R du BRGM et la mention de bugs existants dans l'API. `[résolu]`
- **#72** [API indicateurs_services] operation "indicateurs" statut 206 sur la dernière page — L'API Hub'Eau `indicateurs_services` renvoie un statut 206 Partial Content sur la dernière page si le nombre d'éléments retournés est inférieur à la taille de page demandée, et c'est la balise 'next' qui indique la fin de la pagination. `[information]`
- **#74** [API indicateurs services] duplication des communes si plusieurs services — L'API `/indicateurs_services/communes` de Hub'Eau retourne des données par service plutôt qu'agrégées par commune comme indiqué dans la documentation, lorsqu'une commune est desservie par plusieurs services. `[en_cours]`
- **#75** [API indicateurs services] Absence des services d'assainissement  — L'API Indicateurs des services présente un bug où elle ne retourne pas les données pour les services d'assainissement collectif et non-collectif, et une refonte de l'API est prévue en 2023 pour corriger cette anomalie. `[en_cours]`
- **#78** Interroger API services AC à partir du Code SANDRE ouvrage — Cette issue demande et enregistre la possibilité d'interroger l'API Indicateurs des services pour l'Assainissement Collectif en utilisant le code SANDRE de l'ouvrage. `[en_cours]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#195** [API indicateurs services] accès aux données assainissement D201.0 et D301.0 — L'API Indicateurs des services ne fournit pas les données pour les indicateurs d'assainissement D201.0 et D301.0 car leur implémentation et la refonte de l'API ont été reportées indéfiniment. `[en_cours]`
- **#219** [API indicateurs des services] format geojson inopérant sur l'endpoint communes — L'API Hub'Eau "Indicateurs des services" ne supporte pas le format GeoJSON car les données sous-jacentes n'incluent pas de coordonnées, et l'endpoint `communes` retourne des géométries vides ou du JSON par défaut malgré l'affichage de l'option GeoJSON dans le swagger. `[information]`
- **#225** Indicateurs de service - Fraicheur des données — L'API Hub'Eau des indicateurs de service présente un retard de fraîcheur des données, ne proposant des informations que jusqu'à 2019 alors que des données plus récentes (jusqu'à 2023) sont disponibles sur services.eaufrance.fr. `[en_cours]`

</details>
