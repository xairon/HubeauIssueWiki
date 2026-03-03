# Indicateurs des services

> 9 issues analysées

## Guide

### Comportement actuel  
L'API "Indicateurs des services" fournit des données via des endpoints comme `indicateurs` et `communes`, en format JSON par défaut. La pagination utilise le code de statut 206 (Partial Content) même sur la dernière page, sans garantir la présence de la balise `next` (#72). Les données proviennent de sources téléchargeables sur [services.eaufrance.fr](http://www.services.eaufrance.fr/donnees/telechargement) (#12).  

### Pièges à éviter  
- **Données incomplètes** : Les indicateurs d'assainissement (D201.0, D301.0) et les services d'assainissement collectif/non-collectif sont absents (#75, #195).  
- **Duplication des communes** : Les résultats ne sont pas agrégés par commune/année, mais listés par service public (#74).  
- **Absence de filtrage SANDRE** : Impossible de filtrer par code SANDRE (identifiant des ouvrages d'assainissement) (#78).  
- **Format GeoJSON non supporté** : L'endpoint `communes` ne retourne pas de géométries en GeoJSON, malgré sa présence dans le swagger (#219).  
- **Données obsolètes** : Les données ne sont mises à jour qu'après 2019, alors que le site web affiche jusqu'en 2023 (#225).  

### Bonnes pratiques  
Utilisez le package R `hubeau` pour interroger l'API avec une syntaxe standardisée, notamment pour l'écoulement des cours d'eau (#137). Vérifiez la fraîcheur des données avant de les utiliser. Pour la pagination, traitez les réponses avec le code 206 comme des pages valides, même si `next` est absent.  

### Contexte métier  
Les codes SANDRE (Système d'Analyse et de Numérisation des Réseaux d'Égouts) identifient les ouvrages d'assainissement collectif. Les indicateurs comme D201.0 et D301.0 mesurent le nombre d'habitants desservis en assainissement. Les données proviennent de sources officielles, mais leur mise à jour est asynchrone avec le site web.  

### Évolutions récentes  
- **2025-05-05** : Incohérence entre les données du site web (jusqu'en 2023) et l'API (seulement après 2019) (#225).  
- **2025-03-21** : Format GeoJSON non implémenté sur l'endpoint `communes` (#219).  
- **2024-11-12** : Absence des indicateurs D201.0 et D301.0 liés à l'assainissement (#195).  
- **2023-05-30** : Publication du package R `hubeau` pour accéder à 10 APIs Hub'Eau (#137).  

### Historique notable  
- **2019-03-29** : Un bug rendait l'API inutilisable pour certains paramètres (ex: P101.1), résolu ultérieurement (#12).  
- **2023-03-14** : Refonte de l'API planifiée pour corriger l'absence de données d'assainissement (#75).  
- **2023-05-30** : Le package R `hubeau` est publié, facilitant l'accès aux APIs (#137).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Les données de l'API proviennent des sources téléchargeables sur http://www.services.eaufrance.fr/donnees/telechargement (#12)
- L'API renvoie un code de statut 206 (Partial Content) sur la dernière page d'une pagination, même si la balise 'next' est vide. (#72)
- Le code 206 est utilisé lorsque le nombre d'éléments renvoyés est inférieur au nombre total disponible, indépendamment de la présence de la balise 'next'. (#72)
- L'API retourne un enregistrement par service public au lieu d'agréger les indicateurs (min, max, moyenne) pour une même commune et année comme indiqué dans la documentation (#74)
- La documentation mentionne un calcul d'agrégats (min, max, moyenne) pour les indicateurs de performance des services publics sur une commune, mais les données réelles ne reflètent pas cette logique d'agrégation (#74)
- L'API 'Indicateurs des services' ne retourne aucun résultat pour les services d'assainissement collectif (AC) et non-collectif (ANC). (#75)
- L'API 'Indicateurs des services' est en cours de refonte en 2023 pour corriger cette absence de données. (#75)
- Les indicateurs relatifs aux services d'assainissement collectif et non-collectif ne sont pas disponibles via l'API actuelle. (#75)
- L'API 'Indicateurs des services' ne permet pas actuellement de filtrer les données par le code SANDRE de l'ouvrage. (#78)
- Le code SANDRE est un identifiant unique utilisé pour référencer les ouvrages dans le domaine de l'assainissement collectif. (#78)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- L'API 'indicateurs_services/indicateurs' ne retourne pas les données pour les indicateurs D201.0 et D301.0 (assainissement), uniquement des données sur l'eau potable. (#195)
- Le chantier de refonte de l'API Indicateurs des services a été reporté, empêchant l'implémentation de certains indicateurs. (#195)
- Les indicateurs D201.0 et D301.0, liés au nombre d'habitants desservis en assainissement collectif (AC) et non collectif (ANC), ne sont pas accessibles via l'API actuelle. (#195)
- Le format GeoJSON n'est pas implémenté sur l'endpoint 'communes' de l'API 'Indicateurs des services', malgré sa présence dans le swagger. (#219)
- L'endpoint 'communes' retourne des géométries vides lorsqu'on demande le format GeoJSON, car les données sous-jacentes ne contiennent pas de coordonnées. (#219)
- La version 0 de l'API retourne un format JSON même lorsqu'on demande GeoJSON sur l'endpoint 'communes'. (#219)
- Les données utilisées par l'API 'Indicateurs des services' ne contiennent pas de coordonnées, empêchant l'implémentation du format GeoJSON. (#219)
- L'API 'Indicateurs des services' ne propose pas de données après 2019, alors que le site web services.eaufrance.fr affiche des données jusqu'en 2023. (#225)
- Une incohérence existe entre la disponibilité des données sur le site web et l'API pour les indicateurs de service. (#225)

### Historique des problèmes résolus

- ~~L'API 'Indicateurs de services' renvoyait des résultats vides pour certains paramètres (ex: code_indicateur=P101.1) en raison d'un dysfonctionnement (#12)~~

### Issues sources

- **#12** [API Indicateur de services] : pas de résultat  (2019-03-29) — L'API 'Indicateurs des services' a connu un bug rendant les résultats vides, résolu ultérieurement, avec une confirmation de la provenance des données depuis des sources téléchargeables.
- **#72** [API indicateurs_services] operation "indicateurs" statut 206 sur la dernière page (2022-07-21) — L'API 'Indicateurs des services' utilise le code de statut 206 sur la dernière page de pagination, conformément à la logique définie par l'équipe de développement.
- **#74** [API indicateurs services] duplication des communes si plusieurs services (2021-08-06) — L'API Indicateurs des services retourne des enregistrements dupliqués par service public au lieu d'agréger les indicateurs par commune et année comme indiqué dans la documentation.
- **#75** [API indicateurs services] Absence des services d'assainissement  (2023-03-14) — L'API 'Indicateurs des services' de Hub'Eau manque de données sur l'assainissement collectif et non-collectif, avec une refonte planifiée pour 2023.
- **#78** Interroger API services AC à partir du Code SANDRE ouvrage (2021-10-01) — Une demande a été formulée pour permettre de consulter l'API 'Indicateurs des services' via le code SANDRE des ouvrages, ce qui faciliterait l'accès aux données spécifiques à un ouvrage donné.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#195** [API indicateurs services] accès aux données assainissement D201.0 et D301.0 (2024-11-12) — L'API Indicateurs des services ne permet pas encore l'accès aux données d'assainissement (D201.0 et D301.0) en raison d'un retard dans la refonte de l'API.
- **#219** [API indicateurs des services] format geojson inopérant sur l'endpoint communes (2025-03-21) — L'endpoint 'communes' de l'API 'Indicateurs des services' ne supporte pas le format GeoJSON en raison d'une absence de coordonnées dans les données, malgré sa présence dans le swagger.
- **#225** Indicateurs de service - Fraicheur des données (2025-05-05) — L'API 'Indicateurs des services' présente un retard de mise à jour des données par rapport au site web services.eaufrance.fr, avec une analyse en cours pour résoudre ce problème.

</details>
