# Poisson

> 17 issues analysées

## Guide

### Comportement actuel

L'API Poisson de Hub'Eau propose trois nouveaux endpoints pour les indicateurs IPR/IRP+, les opérations et les stations de mesure (Issue #159). Les données incluent des protocoles de pêche (méthode, moyen, nombre de passages) depuis la version v1 (Issue #4). Le format JSON est recommandé pour les requêtes complexes, avec des limites de 5000 lignes pour les exports CSV (Issue #226). Les coordonnées des points de prélèvement sont actuellement diffusées avec une seule décimale (Issue #251).

### Pièges à éviter

Impossible de filtrer simultanément par espèce et par station (Issue #1), limitant les analyses croisées. Les exports CSV tronquent les données pour les départements comme le 38 (Issue #226), et les listes de faciès sont incomplètes (Issue #275). Le filtre par nom d'espèce n'est pas directement supporté, nécessitant l'utilisation de l'API SANDRE (Issue #33). Les données ASPE peuvent être retardées ou restreintes selon les règles des agences de l'eau (Issue #181).

### Bonnes pratiques

Utilisez l'API SANDRE pour obtenir les codes OFB à partir des noms d'espèces (Issue #33), et privilégiez le format JSON pour les requêtes volumineuses (Issue #226). Le package R 'hubeau' simplifie l'accès aux données (Issue #137). Vérifiez les règles de validation des données pour les agences comme l'AELB (Issue #181), et consultez les indicateurs IPR/IRP+ via les nouveaux endpoints (Issue #159).

### Contexte métier

Les codes OFB (Office français de la biodiversité) et SANDRE (Système d'information sur les données de l'eau) sont essentiels pour identifier les espèces. Les indicateurs IPR/IRP+ mesurent la pression sur les ressources halieutiques. Les données proviennent de la base ASPE, avec des restrictions pour certaines opérations en cours de saisie. Les codes WAMA, anciens, sont remplacés par ASPE depuis 2018 (Issue #256).

### Évolutions récentes

- **2026-02-17** : Incohérences dans les descriptions des faciès (Issue #275).  
- **2025-10-16** : Correction du libellé tronqué dans le swagger et valorisation des champs WAMA (Issues #255, #256).  
- **2025-07-17** : Mise à jour quotidienne des données ASPE, avec restrictions pour certaines opérations (Issue #181).  
- **2023-11-21** : Ajout de trois nouveaux endpoints pour les indicateurs, opérations et stations (Issue #159).  
- **2023-07-13** : Synchronisation des données ASPE et amélioration de la chaîne d'alimentation (Issue #148).

### Historique notable

- **2023-07-13** : Correction du retard des données ASPE dans l'API (Issue #148).  
- **2022-07-05** : Intégration des protocoles de pêche électrique (Issue #4).  
- **2020-04-08** : Correction des noms communs pour les codes BLN, LPX, ATH, COR (Issue #30).  
- **2018-05-17** : Mise à jour du format de date dans les GEOJSON (Issue #3).  
- **2018-05-17** : Limites techniques initiales sur les filtres et les données opérationnelles (Issue #1).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Poisson ne permet pas de filtrer simultanément les données par espèce et par station, limitant la flexibilité des requêtes. (#1)
- Le connecteur JSON de Tableau ne gère pas nativement les requêtes complexes nécessitant des joints ou des filtres multiples (ex: date de pêche, cours d'eau). (#1)
- Les données de l'API ne contiennent pas de champ explicite pour les dates d'opération (pêche), les effectifs ou les poids par espèce. (#1)
- Certaines stations de suivi de l'anguille européenne (codes 4411022 à 4411033) sont mal géoréférencées, impactant la précision des visualisations cartographiques. (#1)
- Les données sur les poissons sont structurées sans détails opérationnels (protocole, date, cours d'eau) nécessaires à une analyse temporelle ou spatiale fine. (#1)
- Le démonstrateur de l'API Poisson est incompatibile avec la version v1 de l'API, nécessitant une mise à jour pour fonctionner correctement. (#20)
- Les codes PHX, GOX, BBX et CAX conservent une valeur vide pour 'nom_commun' car ils représentent des genres et non des espèces. (#30)
- Les codes PHX, GOX, BBX et CAX correspondent à des genres et ne disposent pas de nom commun standardisé, justifiant leur valeur vide. (#30)
- L'API Hub'Eau 'poissons' ne permet pas de filtrer par nom d'espèce, uniquement par code_espece_poisson. (#33)
- Le code à utiliser dans l'API 'poissons' est le code OFB (champ 'code'), pas le code SANDRE ('code_taxon'). (#33)
- Une future API Hydrobiologie (prévue en 2020) permettra de filtrer directement par nom d'espèce. (#33)
- Le référentiel SANDRE contient des correspondances entre noms latins, communs et codes OFB/SANDRE pour 195 espèces de poissons. (#33)
- Le code OFB est nécessaire pour interroger l'API 'poissons' de Hub'Eau, mais il n'est pas directement lié au code SANDRE. (#33)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- Une évolution de l'API (ajout de trois endpoints) est en cours pour améliorer la chaîne d'alimentation (#148)
- L'API Poisson a ajouté trois nouveaux endpoints pour diffuser des indicateurs IPR/IRP+, des données des opérations et des informations descriptives des stations (#159)
- Les indicateurs IPR (Indice de Pression sur les Ressources) et IPR+ sont désormais accessibles via l'API (#159)
- Les données environnementales et contextuelles des opérations sont désormais disponibles (#159)
- Les stations de mesure disposent maintenant de données descriptives enrichies (#159)
- Les opérations sous maîtrise d'ouvrage de certaines agences de l'eau nécessitent une validation supplémentaire avant leur diffusion. (#181)
- Les opérations sous maîtrise d'ouvrage de l’agence de l’eau Loire-Bretagne (AELB) ne sont diffusées que si elles sont validées niveau 2 ou datées de plus d'un an. (#181)
- L'API Poisson ne retourne pas toutes les opérations de pêche électrique en Isère (code département 38) lors de l'export via RStudio, contrairement à l'export ASPE. (#223)
- Le script R utilise une URL spécifique pour l'API, mais ne gère pas correctement les champs JSON imbriqués (ex: 'operateur_libelle_aspe') qui peuvent contenir des listes. (#223)
- Les données diffusées via l'API Poisson peuvent présenter des lacunes par rapport aux exports ASPE, indiquant une possible restriction ou une différence de couverture des données. (#223)
- L'export CSV de l'API Poisson limite les résultats à 5000 lignes, ce qui peut exclure des données filtrées (ex. département 38). (#226)
- L'API Poisson en format JSON permet des requêtes filtrées (ex. code_departement=38) et retourne 615 résultats pour le département 38, contrairement à l'export CSV. (#226)
- La base ASPE contient des opérations non présentes dans l'API Poisson, notamment en raison de règles de gestion (données en cours de saisie, bassins spécifiques). (#226)
- Certains producteurs de données (ex. AQUASCOP, CNRS) ne figurent pas dans ASPE ou Hubeau, limitant l'exhaustivité des données accessibles via l'API. (#226)
- Les comptes rendus de pêche (CR) transmis aux DDT/OFB ne sont pas systématiquement intégrés dans ASPE ou Hubeau, malgré leur potentiel d'enrichissement des bases nationales. (#226)
- L'API Poisson diffuse les coordonnées des points de prélèvement avec une seule décimale au lieu de deux en raison d'une anomalie Aspe. (#251)
- L'application WAMA (gestion des observations piscicoles) a été remplacée par Aspe en 2018, expliquant l'absence de codes WAMA pour les données récentes. (#256)
- L'API Poisson retourne des listes de faciès incomplètes (ex. 'facies_libelle_type' et 'facies_profondeur_moyenne') avec des disparités entre les champs, manquant des entrées présentes dans les exports. (#275)
- Les données des faciès (ex. 'Plat') sont inconsistantes entre les exports et l'API, ce qui peut fausser l'analyse des opérations de surveillance piscicole. (#275)

### Historique des problèmes résolus

- ~~Le format de date dans les fichiers GEOJSON était converti en timestamp (nombre entier représentant le nombre de millisecondes depuis l'époque Unix) au lieu de rester au format 'YYYY-MM-DD'. (#3)~~
- ~~L'API Poissons a été mise à jour en version v1 pour intégrer de nouvelles données, notamment les protocoles de pêche (méthode, moyen, nombre de passages). (#4)~~
- ~~Les données sur les protocoles de pêche électrique (Méthode de prospection, Moyen de Prospection, Nombre de passages) sont désormais accessibles via l'API Poissons à partir de la version v1. (#4)~~
- ~~L'API 'code_espece_poisson' et 'poissons' retourne une valeur vide pour 'nom_commun' pour certains codes (comme BLN) avant la correction. (#30)~~
- ~~Les codes BLN (Blageon), LPX (Lamproie), ATH (Athérine) et COR (Corégone) ont maintenant un 'nom_commun' correctement renseigné dans l'API. (#30)~~
- ~~Une alternative pour obtenir le code OFB à partir du nom est d'utiliser l'API SANDRE avec un filtre XPath sur 'LbNomCommunAppelTaxon'. (#33)~~
- ~~L'API Poisson utilisait une copie décalée de la base ASPE avant la mise à jour du 13 juillet 2023 (#148)~~
- ~~Les données ASPE étaient initialement retardées de plusieurs mois dans l'API par rapport à la source originale (#148)~~
- ~~La mise à jour du 13 juillet 2023 a corrigé ce retard pour les données de 2023 (#148)~~
- ~~La mise à jour des données depuis la base ASPE est programmée quotidiennement, mais des blocages temporaires peuvent survenir. (#181)~~
- ~~Le libellé du champ 'objectifs_operations' dans le swagger de l'API Poisson était tronqué par une ellipse, ce qui pouvait induire en erreur les utilisateurs. (#255)~~
- ~~Les champs WAMA de l'API Poisson étaient initialement vides pour les données récentes, mais sont désormais valorisés pour les cas applicables après mise à jour du traitement. (#256)~~
- ~~L'endpoint 'indicateurs' de l'API Poisson utilise des libellés textuels ('Très bon', 'Bon', etc.) pour le champ 'iprplus_libelle_classe', contrairement à la documentation initiale qui indiquait des codes numériques (1, 2, etc.). (#257)~~

### Issues sources

- **#1** API Poissons et Tableau Software (2018-05-17) — L'API Poisson de Hub'Eau présente des limites techniques et des lacunes de données (géoréférencement, détails opérationnels) qui restreignent son utilisation pour des analyses avancées de la répartition des espèces.
- **#3** Format de date GEOJSON (2018-05-17) — L'API 'Poisson' a corrigé un problème de format de date dans les fichiers GEOJSON, passant d'un timestamp à 'YYYY-MM-DD' pour faciliter l'analyse temporelle avec des outils comme QGIS.
- **#4** Protocole de pêche manquant pour l'API Poissons (2022-07-05) — L'API Poissons a été mise à jour pour inclure des informations sur les protocoles de pêche, rendant disponibles des données clés pour l'analyse des résultats de pêche électrique.
- **#20** [API Poissons] (2022-07-05) — L'API Poisson a été mise à jour vers la version v1, rendant le démonstrateur existant obsolète et nécessitant des adaptations techniques.
- **#30** [API Poisson] Code poisson BLN - nom_poisson (2020-03-06) — L'API 'Poisson' a été corrigée pour certains codes (BLN, LPX, ATH, COR) afin de fournir un 'nom_commun', tandis que d'autres codes (PHX, GOX, BBX, CAX) conservent une valeur vide car ils représentent des genres.
- **#33** Récupération données poisson depuis son nom (2020-04-08) — L'API Hub'Eau 'poissons' nécessite l'utilisation de codes OFB pour les requêtes, mais des alternatives via SANDRE ou une future API Hydrobiologie permettent de contourner cette limitation.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#148** [API Poisson] Date de maj de données ASPE ? (2023-07-13) — L'API Poisson a été mise à jour pour synchroniser les données ASPE, avec des améliorations de la chaîne d'alimentation en cours.
- **#159** L'API poisson s'enrichit de trois nouveaux endpoints (2023-11-21) — L'API Poisson a été mise à jour avec trois nouveaux endpoints pour les indicateurs IPR/IRP+, les opérations et les stations de mesure.
- **#181** [API Poissons] Fréquence de moissonage de la base ASPE (2024-09-04) — L'API Poisson met à jour quotidiennement les données ASPE, mais certaines opérations sont restreintes en raison de validations supplémentaires imposées par les agences de l'eau.
- **#223** [ API Poisson ] Export de données via l'API URL et Rstudio : manque t'il des données ? (2025-07-17) — L'API Poisson manque certaines données de pêche électrique en Isère par rapport à l'export ASPE, probablement en raison de limitations de l'API ou de différences de traitement des données.
- **#226** [ API Poisson ] liaison API avec Naîades et APSE (2025-07-17) — L'API Poisson présente des limites d'export (CSV) et des écarts de données par rapport à ASPE et aux compilations locales, liés à des règles de gestion et à l'absence de centralisation de certains producteurs.
- **#251** [API Poisson] précision des coordonnées des points de prélèvements (2025-08-29) — L'API Poisson présente une réduction de la précision des coordonnées des points de prélèvement en raison d'une anomalie temporaire.
- **#255** [API Poisson] - Imprécision du swagger pour les valeurs du champ objectifs_operations (2025-10-16) — Le libellé tronqué dans le swagger de l'API Poisson a été corrigé, améliorant la clarté des informations disponibles pour les utilisateurs.
- **#256** [API Poisson] - champs WAMA inutiles (2025-10-16) — L'API Poisson a corrigé l'absence de champs WAMA pour les données récentes, tout en clarifiant que ces codes proviennent de l'ancienne application WAMA remplacée par Aspe en 2018.
- **#257** [API Poisson] - errreur de la documentation sur les valeurs attendues (2025-10-16) — L'API Poisson a corrigé une erreur de documentation sur les valeurs attendues pour le champ 'iprplus_libelle_classe', qui utilisent des libellés textuels au lieu de codes numériques.
- **#275** [API Poisson] problème sur description des faciès (2026-02-17) — L'API Poisson présente des incohérences dans la description des faciès entre les exports et les requêtes API, affectant la fiabilité des données.

</details>
