# Écoulement des cours d'eau

> 8 issues analysées

## Guide

### Comportement actuel

L'API "Écoulement des cours d'eau" est désormais en version stable 1.0, accessible via le chemin `/api/v1/` depuis le 23 mai 2023. Ses données sont mises à jour quotidiennement depuis le 12 avril 2023 (#122, #142). Elle propose des endpoints pour les observations du réseau ONDE, incluant des données pour la Corse, et un endpoint dédié aux informations descriptives des stations hydrométriques (#192, #233). Les observations sont géolocalisées en RGF93 / Lambert 93 et détaillent le cours d'eau, la station, le type d'écoulement et le code de campagne (#193). Il est possible de lier ces données aux entités hydrographiques du Sandre (BD Carthage 2017) via leur service WFS en utilisant les champs `uri_cours_eau` et `code_cours_eau` pour extraire le TYPENAME et le CdEntiteHydrographique (#194).

### Pièges à éviter

La description OpenAPI/Swagger de l'API contient des erreurs qui peuvent gêner l'automatisation. Des champs comme `Numéro de page` et `Liste des champs...` sont incorrectement nommés et le champ `fields` devrait être de type `[array(string)]`. De plus, la description du paramètre `size` est mal structurée (#127). Concernant l'endpoint `observations`, les paramètres `date_observation_min` et `date_observation_max` utilisent des comparaisons strictes (`>` et `<`) au lieu d'inclusives (`>=` et `<=`), ce qui empêche de récupérer les observations d'une journée unique si les dates min et max sont identiques (#192). Enfin, l'API peut produire des doublons d'observations lors de la pagination, et l'ordre des résultats n'est pas garanti si le paramètre `size` est modifié (#193).

### Bonnes pratiques

Pour faciliter l'intégration et l'analyse des données en R, utilisez le package `hubeau` (version 0.4.0 disponible sur le CRAN, code source sur GitHub `inrae/hubeau`). Il permet de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée `get_[API]_[Operation]()` et est bien documenté (#137). Pour contourner le problème des dates inclusives/exclusives, si vous souhaitez récupérer les observations du jour J, définissez `date_observation_min` à J-1 et `date_observation_max` à J (#192). Pour minimiser les doublons lors de la récupération des observations, privilégiez l'utilisation d'un paramètre `_size` plus grand ou un ciblage fonctionnel plus précis afin d'éviter la pagination (#193).

### Contexte métier

L'API "Écoulement des cours d'eau" fournit des observations issues du réseau ONDE (Observatoire National des Étiages), un programme essentiel pour le suivi des étiages. Ces observations décrivent l'état de l'écoulement (par exemple, "écoulement visible") et sont associées à des "codes_campagne" spécifiques (#192, #193). Les entités hydrographiques de référence utilisées par Hub'Eau proviennent de la BD Carthage 2017. Le Sandre, référentiel national, gère les identifiants uniques (CdEntiteHydrographique) de ces entités et propose un service WFS pour accéder à leurs données géographiques détaillées (#194).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Écoulement présente des erreurs dans sa description OpenAPI/Swagger. (#127)
- Le champ `Numéro de page` est incorrectement nommé dans la description OpenAPI de l'API Écoulement, il s'agit d'une description et non d'un nom de champ. (#127)
- Le champ `Liste des champs...` est incorrectement nommé dans la description OpenAPI de l'API Écoulement, il s'agit d'une description et non d'un nom de champ, et devrait être `fields`. (#127)
- Le type du champ `fields` dans la description OpenAPI de l'API Écoulement devrait être `[array(string)]`. (#127)
- La description du champ `size` dans la description OpenAPI de l'API Écoulement est encapsulée incorrectement dans le sous-item "schema". (#127)
- Le paramètre `date_observation_min` de l'API Écoulement des cours d'eau (endpoint `observations`) utilise une comparaison stricte ('>') au lieu de la comparaison inclusive ('>=') documentée. (#192)
- Le paramètre `date_observation_max` de l'API Écoulement des cours d'eau (endpoint `observations`) utilise une comparaison stricte ('<') au lieu de la comparaison inclusive ('<=') documentée. (#192)
- Si `date_observation_min` et `date_observation_max` sont définis sur la même date, l'API Écoulement des cours d'eau (endpoint `observations`) ne renvoie aucune observation. (#192)
- Pour récupérer les observations d'une date spécifique (ex: D), il est nécessaire de définir `date_observation_min` à D-1 et `date_observation_max` à D. (#192)
- L'API Écoulement des cours d'eau fournit des observations du réseau ONDE (Observatoire National des Étiages). (#192)
- Des observations ONDE sont disponibles pour la région Corse via l'API Écoulement des cours d'eau. (#192)
- L'API ecoulement/observations peut produire des doublons d'observations (features) lors de la pagination, où une même observation apparaît sur différentes pages. (#193)
- L'ordre des résultats de l'API ecoulement/observations n'est pas garanti comme étant identique lorsque le paramètre 'size' est modifié. (#193)
- La préconisation pour éviter les doublons est d'utiliser un paramètre '_size' plus grand ou un ciblage fonctionnel plus précis pour éviter la pagination. (#193)
- Le comportement de doublons n'est pas systématiquement reproductible par l'équipe Hub'eau. (#193)
- Les observations d'écoulement incluent des détails sur le cours d'eau (ex: 'l'Helpe Mineure', code 'D0130700'), la station (ex: 'L'Helpe mineure à Fourmies', code 'D0137052'), et le type d'écoulement (ex: '1' pour 'Ecoulement visible'). (#193)
- Les données d'écoulement sont associées à un 'code_campagne'. (#193)
- Les observations sont géolocalisées avec des coordonnées et des informations de projection (RGF93 / Lambert 93). (#193)

### Historique des problèmes résolus

- ~~Depuis le 12 avril 2023, les données de l'API Écoulement des cours d'eau sont mises à jour de façon quotidienne. (#122)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~
- ~~L'API Écoulement des cours d'eau est passée de la version beta à la version stable 1.0 le 23/05/2023. (#142)~~
- ~~La version beta de l'API Écoulement des cours d'eau n'est plus accessible depuis le 26/05/2023. (#142)~~
- ~~Le chemin de l'URL d'interrogation pour l'API Écoulement des cours d'eau a changé de `/api/vbeta/` à `/api/v1/`. (#142)~~
- ~~Le champ uri_cours_eau de l'API Hub'Eau Écoulement des cours d'eau contient le TYPENAME (ex: CoursEau_Carthage2017) nécessaire pour interroger le service WFS du Sandre. (#194)~~
- ~~Le TYPENAME peut être extrait de l'URI http://id.eaufrance.fr/{TYPENAME}/{CODE}. (#194)~~
- ~~Le champ code_cours_eau de l'API Hub'Eau correspond au CdEntiteHydrographique utilisé dans le filtre WFS du Sandre. (#194)~~
- ~~L'URL du service WFS du Sandre pour les données géographiques est https://services.sandre.eaufrance.fr/geo/sandre. (#194)~~
- ~~Le format de sortie GeoJSON pour le WFS du Sandre est OUTPUTFORMAT=application/json; subtype=geojson. (#194)~~
- ~~La BD Carthage 2017 (CoursEau_Carthage2017) est un jeu de données de référence pour les entités hydrographiques utilisé par Hub'eau. (#194)~~
- ~~Le Sandre fournit un service WFS pour accéder aux données géographiques des entités hydrographiques. (#194)~~
- ~~Le CdEntiteHydrographique est l'identifiant unique d'une entité hydrographique dans le référentiel Sandre. (#194)~~
- ~~Le endpoint "stations" de l'API "Écoulement des cours d'eau" a été indisponible et ne retournait pas de données du 10 au 14 mai. (#233)~~
- ~~L'anomalie concernant l'indisponibilité du endpoint "stations" de l'API "Écoulement des cours d'eau" a été traitée et le service rétabli le 14 mai. (#233)~~
- ~~L'API "Écoulement des cours d'eau" propose un endpoint dédié ("stations") pour accéder aux informations descriptives des stations hydrométriques. (#233)~~

### Issues sources

- **#122** [API Ecoulement des cours d'eau] Fréquence d'actualisation — L'API Écoulement des cours d'eau est désormais mise à jour quotidiennement depuis le 12 avril 2023, résolvant les retards de publication. `[résolu]`
- **#127** [API Ecoulement] Erreurs dans la description openapi — L'issue rapporte plusieurs erreurs dans la description OpenAPI de l'API Écoulement, concernant les noms de paramètres, leurs types et la structure des descriptions, ce qui impacte l'automatisation de la gestion des champs. `[en_cours]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#142** [API Ecoulement des cours d'eau] Passage en version stable — L'API Écoulement des cours d'eau est passée de la version beta à la version stable 1.0 le 23/05/2023, nécessitant la modification du chemin de l'URL de `/api/vbeta/` à `/api/v1/`. `[résolu]`
- **#192** [API Ecoulement des cours d'eau] observations - erreur sur les champs date_observation_min & date_observation_max — L'API Écoulement des cours d'eau présente une erreur où les paramètres de date `date_observation_min` et `date_observation_max` utilisent des comparaisons strictes au lieu d'inclusives, ce qui empêche la récupération correcte des données, notamment pour une période d'une seule journée. `[en_cours]`
- **#193** [API Ecoulement des cours d'eau] observations - doublons produits par l'API — L'API Écoulement des cours d'eau peut retourner des doublons d'observations lors de la pagination, et l'ordre des résultats n'est pas stable si le paramètre de taille est modifié. `[en_cours]`
- **#194** [API Ecoulement des cours d'eau] Comment retrouver les ressources liées ? — L'API Écoulement des cours d'eau permet de retrouver les données géographiques des cours d'eau via le service WFS du Sandre en utilisant les champs uri_cours_eau et code_cours_eau. `[résolu]`
- **#233** [API Ecoulement des cours d'eau] pas de données stations — Le endpoint "stations" de l'API "Écoulement des cours d'eau" a connu une indisponibilité temporaire des données entre le 10 et le 14 mai, mais l'anomalie a été résolue. `[résolu]`

</details>
