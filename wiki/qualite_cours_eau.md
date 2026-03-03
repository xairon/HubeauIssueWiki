# Qualité des cours d'eau

> 28 issues analysées

## Guide

### Comportement actuel  
L'API Hub'Eau "Qualité des cours d'eau" propose des endpoints comme `/v2/qualite_rivieres/analyse_pc` et `/operation_pc`, avec des formats JSON et GeoJSON. La pagination est limitée à 20 000 résultats par requête, avec un paramètre `size` et des pages (`page`). Le champ `profondeur` est disponible dans `operation_pc` mais absent des exports Hub'Eau. Les filtres comme `date_debut_maj` et `date_fin_maj` s'appliquent à la date d'import (`date_maj_analyse`) et non à la date de prélèvement.  

### Pièges à éviter  
La limite de 20 000 résultats par requête oblige à segmenter les requêtes via des filtres temporels ou géographiques. Le paramètre `fields` doit être spécifié même avec des valeurs redondantes (ex: `fields=code_station`) pour éviter les erreurs sur `/operation_pc`. Les données de `date_maj_analyse` ne reflètent pas la date de prélèvement, ce qui peut induire en erreur. Les duplications de données sont possibles avec `size=10 000`.  

### Bonnes pratiques  
Utilisez `count` pour connaître le nombre total de résultats avant de filtrer. Pour les grandes quantités de données, privilégiez Naïades pour les exports. Associez `code_prelevement` et `profondeur` (via `operation_pc`) pour interpréter correctement les analyses. Évitez les requêtes sans `fields` sur `/operation_pc`.  

### Contexte métier  
Les stations sont liées à Naïades, source principale des données. Les codes BSS (Bassin Sédimentaire) et SANDRE (Système d'Analyse et de Référentiel pour l'Environnement) structurent les données. Les stations peuvent manquer de données si elles ne sont pas dans Naïades ou si les agences ne les mettent pas à jour. Les paramètres comme `resultat` (valeur numérique ou code) dépendent du type de mesure.  

### Évolutions récentes  
- **2026-01-28 (#268)** : Bug dans `/operation_pc` corrigé en forçant l'usage de `fields`.  
- **2025-10-03 (#254)** : `profondeur` accessible via `operation_pc`, mais non dans les exports.  
- **2025-09-30 (#250)** : Erreur 500 sur `/analyse_pc` avec `code_prelevement` résolue.  
- **2025-07-24 (#246)** : Incohérences de noms de champs (ex: `code_operation` vs `codeOperation`) en GeoJSON.  
- **2024-12-06 (#199)** : Problème d'export CSV résolu en supprimant les espaces dans les paramètres.  
- **2024-11-21 (#200)** : Limite de 20 000 résultats par requête confirmée, avec recommandation de segmenter.  

### Historique notable  
- **2023-02-13 (#134)** : Erreur 500 sur `/analyse_pc` corrigée.  
- **2022-07-21 (#24)** : Mise à jour vers API v2 pour résoudre les doublons et les erreurs de comptage.  
- **2022-03-01 (#103)** : Bug dans Swagger corrigé (guillemets HTML autour de `code_station`).  
- **2020-04-10 (#32)** : Absence de données pour certaines stations liée à Naïades et à des filtres temporels.  
- **2019-07-18 (#23)** : Limite de 20 000 résultats par requête introduite.  
- **2018-12-18 (#15)** : Génération incorrecte de l'attribut `next` résolue.

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'attribut 'next' est généré dans l'URL de réponse même lorsque la page suivante n'existe pas (par exemple, lorsque 'data' est vide). (#15)
- Pour contourner la limite, il est recommandé de filtrer les données par intervalles de dates (date_debut_prelevement/date_fin_prelevement) et de diviser la requête en plusieurs appels. (#23)
- La station 04180100 a 28865 analyses associées, nécessitant une pagination complexe pour l'obtention complète des données. (#23)
- Le nombre de paramètres mesurés pour les conditions environnementales est rarement supérieur à 30 (#24)
- L'API Qualité des cours d'eau de Hubeau dépend des données de Naïades, qui applique par défaut un filtre temporel de 3 dernières années. (#32)
- La station 06750945 n'est pas présente dans Naïades, ce qui explique son absence sur Hubeau malgré sa présence sur Sandre. (#32)
- La station 06750945 est référencée sur Sandre mais aucune donnée de physicochimie n'est diffusée par Naïades. (#32)
- Les utilisateurs doivent contacter l'agence de l'eau Rhône-Méditerranée-Corse pour obtenir des informations complémentaires sur la station 06750945. (#32)
- Sur les plans d'eau, plusieurs prélèvements peuvent avoir lieu le même jour à différentes profondeurs ou zones verticales, nécessitant une granularité plus fine que celle offerte par l'agrégation par date et station. (#56)
- L'API 'Qualité des cours d'eau' ne renvoie pas de données pour des stations configurées pour d'autres types de mesure (ex: hydrobiologie). (#105)
- Les stations listées ne sont pas associées à la qualité des cours d'eau dans le système de données. (#105)
- Les stations du code postal 34 (Hérault) mentionnées sont dédiées à des mesures hydrobiologiques et non à la qualité des cours d'eau. (#105)
- L'API Température des cours d'eau utilise un paramètre `en_service` pour indiquer l'état d'une station, contrairement à GeoRivière qui utilise une date de fin. (#108)
- La logique actuelle pour déterminer si une station est en service dans GeoRivière repose sur la présence d'une date de fin, ce qui peut être moins explicite qu'un paramètre booléen. (#108)
- La gestion de l'état des stations (en service ou non) est cruciale pour l'analyse des données hydrologiques et la prise de décision. (#108)
- Le champ date_maj_analyse correspond à la date d'intégration des données dans la base Naïades, non à la date de collecte des prélèvements. (#135)
- Lorsque le nombre total d'enregistrements dépasse 20 000, il est nécessaire de filtrer les données via des paramètres comme la date ou le paramètre analysé pour éviter les limites de pagination. (#152)
- La fréquence de mise à jour des données varie selon les stations et n'est pas quotidienne. (#152)
- L'API ne permet pas de lister directement les dates disponibles pour une station, mais on peut interroger le champ 'date_prelevement' pour identifier les périodes couvertes. (#152)
- L'API Qualité des cours d'eau ne renvoie pas de données à partir du 2023-08-05 en raison d'une absence de données dans la base Naïades, source principale de l'API. (#154)
- La base de données Naïades ne contient pas de données physico-chimiques des cours d'eau à partir du 2023-08-05, ce qui affecte l'ensemble des requêtes sur cette période. (#154)
- Les schémas de données sont documentés dans la section `Models` de chaque page d'accueil d'API, mais cette information n'est pas immédiatement visible sans exploration proactive. (#156)
- Les écarts observés dans le nombre de prélèvements (ex. 3390 en 2022 vs 4649 en 2019) sont liés à une interruption temporaire de la collecte de données par l'agence de l'eau Loire-Bretagne. (#158)
- La limite de résultats retournés par l'API (size=20000) n'a pas été respectée pour le paramètre 1553, mais cela est lié à l'absence de données historiques plutôt qu'à une limite technique. (#199)
- Le paramètre 1553 ne correspond pas aux hauteur des précipitations, mais à une autre mesure, et n'est pas analysé dans le système Naïades. (#199)
- Les données de précipitations ne sont pas systématiquement disponibles dans l'API /v2/qualite_rivieres/condition_environnementale_pc, mais uniquement dans certains cas spécifiques. (#199)
- La limite de 20 000 enregistrements s'applique à la taille totale du résultat d'une requête API, pas par page. (#200)
- Pour dépasser cette limite, il faut segmenter les requêtes selon des critères géographiques, temporels ou autres. (#200)
- La pagination n'est pas adaptée pour récupérer plus de 20 000 enregistrements, il faut utiliser des filtres pour restreindre les résultats. (#200)
- Pour des besoins de collecte de données historiques à grande échelle, le site Naïades propose des exports adaptés. (#200)
- L'API Hub'eau ne permet pas de filtrer directement les données par critère PFAS, uniquement par groupe de paramètres. (#217)
- Les paramètres PFAS sont gérés par le référentiel analytique Sandre et l'organisme Aquaref, et non directement disponibles via l'API Hub'eau. (#217)
- L'API Hub'Eau ne fournit pas de méthode de calcul automatisée pour agréger les concentrations de polluants mesurées par plusieurs stations sur une journée donnée. (#220)
- La concentration journalière globale d'un paramètre comme le métolachlore ESA nécessite une approche métier spécifique, non standardisée par l'API, et dépend des besoins opérationnels (ex: moyenne, interpolation spatiale). (#220)
- Les données de qualité de l'eau (paramètres chimiques) sont collectées par des stations hétérogènes en termes de localisation et de fréquence de mesure, ce qui complique l'agrégation temporelle/spatiale. (#220)
- Le format JSON et GeoJSON retournent des noms de champs incohérents (code_operation vs codeOperation) pour les mêmes données. (#246)
- L'argument `fields` ne fonctionne pas correctement en format GeoJSON : utiliser `code_operation` ne retourne aucun champ, tandis que `codeOperation` ne filtre pas les propriétés. (#246)
- La requête API avec `code_prelevement=RAS` retourne uniquement un enregistrement, alors que des données supplémentaires existent et sont accessibles en spécifiant un `code_station` particulier. (#252)
- Le comportement de regroupement des données lors de l'exposition des campagnes à partir des données unitaires est lié à la réutilisation de codes identiques (comme 'RAS') dans les sources de données. (#252)
- Le code 'RAS' pour `code_prelevement` est présent dans la base de données Naïades, mais son utilisation entraîne un regroupement des données lors de l'agrégation. (#252)
- Le champ `profondeur` est disponible dans le endpoint `operation_pc` de l'API Qualité des cours d'eau, mais n'est pas mentionné dans les exports Hub'Eau. (#254)
- La station J736520, située sur un plan d'eau, nécessite la connaissance de la profondeur de prélèvement pour interpréter correctement les données de qualité de l'eau. (#254)
- L'endpoint /operation_pc de l'API Qualité des cours d'eau renvoie un 'Internal server error' lors de requêtes sans paramètre 'fields', même avec des filtres simples (code_station, dates). (#268)
- Un contournement temporaire consiste à ajouter un paramètre 'fields' explicitement, même avec des valeurs redondantes (ex: 'fields=code_station,libelle_station...') pour forcer le traitement. (#268)

### Historique des problèmes résolus

- ~~L'API impose une limite de 20000 résultats maximum par requête (page * size), déclenchant une erreur 'InvalidRequest' si dépassée. (#23)~~
- ~~L'API v1 de 'condition_environnementale_pc' renvoyait des doublons et un comptage incorrect (1274 vs 26999 résultats) (#24)~~
- ~~La mise à jour vers l'API v2 a corrigé le problème de doublons et de comptage (#24)~~
- ~~La station 04146850 est présente sur Hubeau mais pas sur Naïades, avec des données historiques disponibles jusqu'en 1996. (#32)~~
- ~~L'endpoint operation_pc agrégait les opérations par code_station et date de prélèvement, empêchant la distinction de prélèvements à différentes profondeurs ou zones verticales sur les plans d'eau. (#56)~~
- ~~La version 2 de l'API a introduit les champs code_prelevement et profondeur pour permettre la jointure entre opérations, analyses et conditions environnementales. (#56)~~
- ~~L'interface Swagger de l'API génère des URLs avec des guillemets HTML (%22) autour du paramètre code_station, ce qui rend les requêtes non fonctionnelles. (#103)~~
- ~~L'API retourne un attribut `count` dans la réponse pour indiquer le nombre total de résultats disponibles avant même de filtrer les données. (#104)~~
- ~~L'API /v2/qualite_rivieres/analyse_pc a retourné un code 500 Internal Server Error pour des requêtes spécifiques, liées à des erreurs de traitement interne. (#134)~~
- ~~Les paramètres date_debut_maj et date_fin_maj filtrent les données en fonction du champ date_maj_analyse (date d'import dans Naïades), non la date de prélèvement. (#135)~~
- ~~Les agences comme Rhône-Méditerranée-Corse mettent à jour Naïades toutes les 15 jours, ce qui génère des dates_maj_analyse variées pour les mêmes stations. (#135)~~
- ~~L'intégration des données physicochimiques de l'agence Loire-Bretagne dans Naïades a entraîné une indisponibilité temporaire de ces données sur l'API Qualité des cours d'eau. (#146)~~
- ~~Les données physicochimiques sont désormais mises à jour toutes les deux semaines dans Naïades. (#146)~~
- ~~Les travaux d'intégration avec l'agence Loire-Bretagne ont permis une alimentation plus régulière des données physicochimiques dans Naïades. (#146)~~
- ~~L'API a une limite de profondeur (size) de 20 000 enregistrements, empêchant la récupération complète des données au-delà de ce seuil sans pagination. (#152)~~
- ~~La pagination avec size=10000 entraîne une duplication de données entre les pages 1 et 2 pour certaines stations. (#152)~~
- ~~La variable `resultat` dans l'API Qualité des cours d'eau correspond au résultat de la mesure d'un paramètre environnemental (valeur numérique pour les paramètres quantitatifs, code pour les paramètres qualitatifs). (#156)~~
- ~~Un incident technique a affecté la remontée des données de l'agence de l'eau Loire-Bretagne vers Naïades, entraînant une sous-représentation des prélèvements. (#158)~~
- ~~L'API retourne le champ `libelle_station` avec une encodage ISO8859-1 au lieu de UTF-8 pour certains enregistrements. (#166)~~
- ~~Le problème d'encodage a été résolu dans Hub'eau et dans le système Naïades. (#166)~~
- ~~Les bassins hydrographiques affectés incluent la Seine, le Rhône, la Garonne, la Loire et la Réunion. (#166)~~
- ~~Plus de 3000 stations dans les bassins de la Garonne, Loire et Seine présentaient des libellés mal encodés. (#166)~~
- ~~Le service web Sandre SOAP de l'AELB n'a pas diffusé les données en raison d'une table de log mal initialisée dans Naïades. (#169)~~
- ~~Les logs des prélèvements ont été initialisés avec une date incorrecte (2022 au lieu de la date réelle), entraînant un manque de données historiques. (#169)~~
- ~~56 000 prélèvements (2006-2022) étaient affectés par l'absence de données en raison de l'erreur de log. (#169)~~
- ~~La station 04670020 (bassin Loire-Bretagne) avait des données manquantes pour l'année 2021 avant la correction. (#169)~~
- ~~L'API Qualité des cours d'eau a rencontré un problème de surcharge entraînant des erreurs 502 Proxy Error. (#198)~~
- ~~La surcharge a impacté les temps de réponse de l'API, mais le service est de nouveau disponible. (#198)~~
- ~~L'export CSV de l'API /v2/qualite_rivieres/condition_environnementale_pc ne fonctionnait pas correctement en raison de caractères non valides (espaces après les virgules) dans le paramètre 'fields'. (#199)~~
- ~~L'API /v2/qualite_rivieres/analyse_pc renvoyait une erreur 500 lors de la requête avec le paramètre code_prelevement. (#250)~~
- ~~Le champ `code_prelevement` permet de relier les données de profondeur du endpoint `operation_pc` aux résultats de mesures du endpoint `analyse_pc`. (#254)~~

### Issues sources

- **#15** L'attribut 'next' est toujours généré même sans page suivante (2018-12-18) — L'API Hub'Eau génère incorrectement l'attribut 'next' lorsqu'il n'y a pas de page suivante, affectant la navigation paginée des résultats.
- **#23** [API Qualité des cours d'eau ] - Erreur lors de la récupération des analyses  (2019-07-18) — L'API Qualité des cours d'eau limite les requêtes à 20000 résultats, nécessitant un découpage temporel pour accéder à l'intégralité des données d'une station.
- **#24** [API Qualité des cours d'eau] - [condition_environnementale_pc] multiples résultats identiques  (2022-07-21) — L'API v1 de 'condition_environnementale_pc' souffrait de doublons et d'un comptage incorrect, résolu par la mise en œuvre de l'API v2.
- **#32** Station qualité non trouvé sur l'API Qualité (2020-04-10) — La disponibilité des stations sur l'API Qualité des cours d'eau dépend de leur présence dans Naïades, avec des limitations temporelles et des absences de données pour certaines stations.
- **#56** [API Qualité des cours d'eau] - données operation_pc incomplètes (2022-07-21) — L'API Qualité des cours d'eau avait un bug d'agrégation des opérations de prélèvement, résolu en version 2 avec l'ajout de champs permettant une meilleure distinction des prélèvements.
- **#103** [Qualité physico-chimique des cours d'eau] bug (2022-03-01) — L'API Qualité des cours d'eau présente un bug dans l'interface Swagger où les guillemets autour du code_station empêchent la récupération des données, mais ce problème sera corrigé dans la prochaine version.
- **#104** [Qualité physico-chimique des cours d'eau] interrogation de la base (2022-03-01) — L'API Hub'Eau permet d'obtenir le nombre total de données disponibles via l'attribut `count` avant d'appliquer des filtres, évitant ainsi les téléchargements excessifs.
- **#105** Non remontée des données "Qualité des cours d'eau" pour un ensemble de stations dans le 34 (2022-03-09) — Les stations listées dans l'issue ne fournissent pas de données de qualité des cours d'eau car elles sont configurées pour d'autres types de mesures comme l'hydrobiologie.
- **#108** [API Qualité de l'eau] Paramètre de station en service (2022-03-07) — L'issue propose d'étendre le paramètre `en_service` utilisé dans l'API Température des cours d'eau à d'autres APIs pour une meilleure cohérence et clarté.
- **#134** [API Qualité des cours d'eau] Erreur 500 sur `/v2/qualite_rivieres/analyse_pc` (2023-02-13) — Une erreur serveur (500) sur l'API de qualité des cours d'eau a été corrigée, affectant temporairement l'accès aux données physicochimiques.
- **#135** API Qualité des cours d'eau - signification des champs date_debut_maj date_fin_maj (2023-02-22) — Les paramètres date_debut_maj et date_fin_maj filtrent les données en fonction de la date d'import dans Naïades, non de la date de prélèvement, ce qui explique leur comportement inattendu.
- **#146** [Qualité des cours d’eau] Indisponibilité des données physicochimie Loire-Bretagne (2023-09-04) — L'API Qualité des cours d'eau a connu une indisponibilité temporaire des données physicochimiques de l'agence Loire-Bretagne, résolue par une mise à jour régulière toutes les deux semaines.
- **#152** API Hub'Eau - Qualité physico-chimique des cours d'eau (2023-10-30) — L'API Qualité des cours d'eau présente des limites de pagination (20 000 enregistrements max) et des duplications possibles, nécessitant des filtres supplémentaires pour récupérer des données complètes et précises.
- **#154** Pas de données renvoyées à partir du 2023-08-05 par l'API https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc.csv (2023-10-30) — L'absence de données physico-chimiques des cours d'eau à partir du 2023-08-05 dans l'API Qualité des cours d'eau est due à un manque de données dans la base Naïades.
- **#156** Qualité des cours d'eau ,nomenclature des variables utilisées (2023-11-02) — L'issue met en évidence l'absence de documentation centralisée des variables de l'API Qualité des cours d'eau, mais fournit une explication précise de la signification de la variable `resultat`.
- **#158** Qualité des cours d'eau (2024-02-26) — Un incident technique affectant l'agence de l'eau Loire-Bretagne a causé des lacunes dans les données de prélèvements sur la qualité des cours d'eau, résolu en février 2024.
- **#166** [API Qualité des cours d'eau] encoding issue with the field `libelle_station` (2024-03-20) — L'API Qualité des cours d'eau présentait un problème d'encodage UTF-8 pour le champ `libelle_station`, affectant plusieurs bassins hydrographiques, mais ce problème a été résolu.
- **#169** [API Qualité des cours d'eau] - absence de données (2024-07-03) — L'absence de données pour la qualité des cours d'eau était due à une erreur de configuration des logs dans Naïades, corrigée par l'AELB et l'insertion des données manquantes.
- **#198** [API Qualité des cours d'eau] (2024-11-20) — L'API Qualité des cours d'eau a temporairement été indisponible en raison d'une surcharge, entraînant des erreurs 502, mais le problème a été résolu.
- **#199** [API Qualité des cours d'eau] /v2/qualite_rivieres/condition_environnementale_pc (2024-12-06) — L'issue révèle des limites de disponibilité des données historiques pour le paramètre 1553 et un problème technique d'export CSV résolu par la suppression des espaces dans les paramètres d'URL.
- **#200** [API Qualité des cours d'eau] Recuperation de donnees au delà de 20.000 rows, objectif 1000000 rows. (2024-11-21) — L'API Qualité des cours d'eau a une limite de 20 000 enregistrements par requête, avec une recommandation d'utilisation de Naïades pour les grands volumes.
- **#217** Absence de data PFAS de la platforme https://pdh.cnrs.fr/fr/datasets/ france_naiades sur hub'eau (2025-05-14) — L'API Hub'eau ne permet pas de sélectionner directement les données PFAS, nécessitant des requêtes supplémentaires par groupe de paramètres et une consultation externe pour les détails des paramètres.
- **#220** Question sur le calcul de la concentration journalière du métolachlore ESA du departement de Finistère de toutes les stations present. (2025-05-14) — L'issue met en évidence l'absence de méthode standardisée dans l'API Hub'Eau pour calculer des concentrations journalières agrégées de polluants, nécessitant une consultation directe des organismes gestionnaires (Ades/Naïades).
- **#246** [API Qualité des cours d'eau] Inconsistence des champs retournés en cas de modification du format json/geojson (2025-07-24) — L'API Qualité des cours d'eau présente des incohérences de noms de champs entre les formats JSON et GeoJSON, ainsi qu'un comportement anormal du paramètre `fields` en GeoJSON.
- **#250** [API Qualité des cours d'eau] Erreur 500 avec code_prelevement depuis /v2/qualite_riviere/analyse_pc (2025-09-30) — L'API Qualité des cours d'eau a corrigé un bug provoquant une erreur 500 lors de la recherche par code_prelevement.
- **#252** [API Qualité des cours d'eau] Erreur sur code_prelevement depuis /v2/qualite_riviere/operation_pc (2025-09-30) — L'API Qualité des cours d'eau retourne des résultats incomplets pour `code_prelevement=RAS` en raison d'un regroupement des données lié à la réutilisation de codes identiques, nécessitant l'ajout d'un `code_station` pour accéder à toutes les entrées.
- **#254** [API Qualité des cours d'eau] profondeur du prélèvement issue de Naïades (2025-10-03) — La profondeur de prélèvement est accessible via le endpoint `operation_pc` de l'API Qualité des cours d'eau, et doit être associée aux résultats via le `code_prelevement`.
- **#268** [API Qualité des cours d'eau] Bug de l'API operation_pc (2026-01-28) — L'API Qualité des cours d'eau présente un bug dans l'endpoint operation_pc, nécessitant l'ajout d'un paramètre 'fields' pour fonctionner, ce qui indique une vulnérabilité dans la gestion des requêtes sans spécification de champs.

</details>
