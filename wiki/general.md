# Général

> 19 issues analysées

## Guide

### Comportement actuel  
L'API Hub'Eau propose des endpoints principaux comme 'niveaux_nappes' (piézométrie), 'poissons', et 'écoulement'. Les données sont souvent disponibles en format JSON, avec des endpoints comme 'chroniques.csv' pour les données agrégées. La pagination est limitée à 20 000 entités sans automatisation. Le package R 'hubeau' permet d'accéder à 10 APIs via des fonctions standardisées. Les données 'chroniques' sont agrégées journalièrement (valeur maximale NGF) et peuvent être corrigées, contrairement aux données 'temps réel' brutes (#96).  

### Pièges à éviter  
L'endpoint 'chroniques.csv' de 'niveaux_nappes' déclare un format CSV mais utilise un schéma d'objet, causant des conflits (#19). L'API 'poissons' ne permet pas de filtrer par nom d'espèce, uniquement par code OFB, nécessitant une requête préalable via SANDRE (#33). Le paramètre '_format=geojson' n'est pas systématiquement supporté par toutes les APIs, limitant l'intégration avec QGIS (#149).  

### Bonnes pratiques  
Utilisez le package R 'hubeau' pour interroger les APIs, et consultez sa documentation pour des exemples (#137). Vérifiez les dates de maintenance planifiée via le tableau de bord de statut (#258). Pour les poissons, obtenez le code OFB via SANDRE avant d'interroger l'API 'poissons' (#33). Privilégiez les données 'chroniques' pour des analyses à long terme, en sachant qu'elles peuvent être corrigées (#96).  

### Contexte métier  
Les codes OFB (Office Français de la Biodiversité) sont requis pour interroger l'API 'poissons', contrairement aux codes SANDRE (#33). Les données 'temps réel' sont brutes, tandis que les 'chroniques' sont agrégées et peuvent être corrigées (ex. dérive de capteur). Les producteurs de données déterminent la fréquence de mise à jour des 'chroniques' (#96).  

### Évolutions récentes  
- **2025-10-07** : Mise en place d'un tableau de bord de surveillance en temps réel pour tous les endpoints (#258).  
- **2025-06-27** : Maintenance planifiée du 24/06/2025, sans lien avec une anomalie de données antérieure (#237).  
- **2025-03-17** : Maintenance planifiée du 17/03/2025 entre 12h et 15h (#218).  
- **2024-12-26** : Correction rapide d'un incident DNS empêchant l'accès à l'API (#205).  

### Historique notable  
- **2025-10-06** : Hub'Eau ne développe pas d'API pluviométrique, orientant vers Météo-France (#234).  
- **2024-09-04** : Interruption temporaire de toutes les APIs, résolue le même jour (#185).  
- **2023-05-15** : Incident technique de 5 heures affectant l'ensemble du portail (#143).  
- **2020-04-08** : Future API Hydrobiologie (prévue en 2020) pour filtrer les poissons par nom (#33).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Un tutoriel vidéo a été créé après le Hackathon pour utiliser les APIs Hub'Eau avec QGIS (#2)
- Dans l'API 'niveaux_nappes', le endpoint 'chroniques.csv' déclare 'produces' pour un format CSV mais référence un schéma d'objet ('Chronique_pi_zom_trique'), créant un conflit entre le type de données attendu et le schéma de réponse. (#19)
- Certains noms d'objets dans la documentation (ex: 'Résultat d'une rêquete sur les chroniques') sont mal adaptés au code, ce qui peut entraîner des erreurs de génération ou une mauvaise lisibilité. (#19)
- L'API Hub'Eau 'poissons' ne permet pas de filtrer par nom d'espèce, uniquement par code_espece_poisson. (#33)
- Le code à utiliser dans l'API 'poissons' est le code OFB (champ 'code'), pas le code SANDRE ('code_taxon'). (#33)
- Une future API Hydrobiologie (prévue en 2020) permettra de filtrer directement par nom d'espèce. (#33)
- Le référentiel SANDRE contient des correspondances entre noms latins, communs et codes OFB/SANDRE pour 195 espèces de poissons. (#33)
- Le code OFB est nécessaire pour interroger l'API 'poissons' de Hub'Eau, mais il n'est pas directement lié au code SANDRE. (#33)
- Un package R nommé 'hubeau' a été développé pour interroger les APIs Hub'Eau, avec une fonction générique et des fonctions spécifiques par API/opération. (#62)
- Le package est hébergé sur GitHub (https://github.com/inrae/hubeau) et documenté sur https://inrae.github.io/hubeau/ (#62)
- Le package gère actuellement les APIs 'Prélèvements en eau' et 'Indicateurs des services', avec possibilité d'extension. (#62)
- Des bugs dans certaines APIs (référencés comme #72 et #74) ont été signalés, mais le package continue de progresser. (#62)
- Les données 'temps réel' de l'API Piézométrie sont brutes et non corrigées. (#96)
- La profondeur temporelle des données 'temps réel' est actuellement non limitée, mais une limitation à 1 an est envisagée. (#96)
- Le endpoint 'chroniques' agrège les données sur une journée (généralement la valeur maximale du niveau NGF). (#96)
- Les données 'chroniques' peuvent être corrigées (ex. dérive de capteur, nivellement du repère). (#96)
- La fréquence de mise à jour des données 'chroniques' dépend des producteurs, qui ne transmettent pas toujours rapidement leurs données. (#96)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- Le paramètre '_format' permet d'obtenir du GeoJSON via les URLs API, mais cette fonctionnalité n'est pas systématiquement implémentée sur toutes les APIs. (#149)
- Les couches chargées dans QGIS via les APIs sont limitées à 20000 entités sans automatisation des échanges de données. (#149)
- Aucune API existante n'est mentionnée par Hub'eau pour accéder aux données pluviométriques, mais des producteurs comme Météo-France sont suggérés comme alternatives. (#234)
- Une page de statut en temps réel affiche l'état global de tous les endpoints Hub'Eau. (#258)
- Chaque endpoint dispose d'une page détaillée avec des métriques de temps de réponse, historique des incidents et données sur 12 mois. (#258)
- Les incidents détectés déclenchent automatiquement des notifications à l'équipe technique. (#258)

### Historique des problèmes résolus

- ~~Le tutoriel vidéo original est devenu inaccessible et obsolète (#2)~~
- ~~La présence de 'allowEmptyValues: false' dans la documentation Swagger génère des erreurs de génération du client, mais ce problème est résolu à partir de la version 2.9.0 de springfox/springfox. (#19)~~
- ~~Une alternative pour obtenir le code OFB à partir du nom est d'utiliser l'API SANDRE avec un filtre XPath sur 'LbNomCommunAppelTaxon'. (#33)~~
- ~~Incident technique rendant les API et le site Hub'Eau indisponibles le 15/05/2023 (#143)~~
- ~~Interruptions de services sur toutes les API Hub'Eau le 23/07 entre 9h et 17h, avec des arrêts de serveurs temporaires de maximum 1h30 (#176)~~
- ~~Service indisponible temporairement pour toutes les APIs (#185)~~
- ~~Un incident a affecté la résolution DNS du domaine hubeau.eaufrance.fr, empêchant l'accès à l'API. (#205)~~
- ~~Le problème de connexion à l'API a été résolu quelques minutes après la déclaration. (#205)~~
- ~~Interruption planifiée de toutes les API Hub'Eau le 17/03/2025 de 12h à 15h pour maintenance (#218)~~
- ~~Hub'eau ne prévoit pas de créer d'API dédiée à la pluviométrie dans sa feuille de route. (#234)~~
- ~~Maintenance planifiée de l'ensemble des API le 24/06/2025 entre 12h et 15h (#237)~~
- ~~L'interruption de service était indépendante d'une anomalie de données hydrométriques antérieure (#237)~~
- ~~Une anomalie de données hydrométriques temps réel a été corrigée séparément de la maintenance (#237)~~
- ~~Interruption de service planifiée pour maintenance des API (#248)~~
- ~~Interruption de service planifiée du 17 au 18 février 2026 entre 12h et 14h pour des opérations techniques (#273)~~

### Issues sources

- **#2** Tutoriel utilisation des API avec QGIS (2022-10-05) — Un tutoriel vidéo sur l'utilisation des APIs Hub'Eau avec QGIS a été créé mais est désormais inaccessible, avec une proposition de contact alternative pour obtenir des informations.
- **#19** [Toutes APIs] Multiples erreurs lors de la génération d'un client à partir de la documentation Swagger (2019-01-22) — L'issue met en évidence des erreurs techniques dans la documentation Swagger de l'API Piézométrie, notamment des incohérences entre les types de données déclarés et les schémas de réponse, ainsi que des problèmes de nommage des objets.
- **#33** Récupération données poisson depuis son nom (2020-04-08) — L'API Hub'Eau 'poissons' nécessite l'utilisation de codes OFB pour les requêtes, mais des alternatives via SANDRE ou une future API Hydrobiologie permettent de contourner cette limitation.
- **#62** Utilisation de l'API dans R / Package dédié ? (2021-08-18) — Un package R dédié à l'interrogation des APIs Hub'Eau a été développé et est en cours d'amélioration, couvrant actuellement certaines APIs.
- **#80** utilisation logo de hub-eau (2022-01-10) — Le logo Hub'Eau peut être utilisé librement par des projets tiers, avec possibilité de référencement sur la page officielle du portail.
- **#89** Mettre les API sur github (2022-07-05) — Le projet Hub'Eau n'a pas de plans actuels pour partager le code de ses APIs sur GitHub.
- **#96** Profondeur temporelle des données piézométriques (2022-01-28) — L'API Piézométrie fournit des données brutes non corrigées en temps réel, tandis que les données 'chroniques' sont agrégées et peuvent être corrigées, avec une mise à jour dépendante des producteurs.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#143** Site et API indisponibles 15/05/2023 (2023-05-15) — Incident technique affectant la disponibilité globale de Hub'Eau le 15 mai 2023, résolu après 5 heures d'interruption.
- **#149** Tutoriel utilisation des API avec QGIS information #2 by tvilmus was closed on Jul 5, 2022 (2023-12-15) — Les utilisateurs doivent utiliser le paramètre '_format=geojson' dans les URLs API pour obtenir des données GeoJSON compatibles avec QGIS, tout en étant conscients des limitations de format et de volume de données.
- **#176** [Toutes API] Intervention de maintenance le 23/07 en journée (2024-07-23) — Maintenance technique globale sur Hub'Eau le 23 juillet 2024 entraînant des interruptions temporaires de toutes les APIs, résolue à la fin de la journée.
- **#185** [toutes API] Service indisponible (2024-09-04) — Toutes les APIs de Hub'Eau ont été temporairement indisponibles avant d'être rétablies le 4 septembre 2024.
- **#205** [API] Problème de connection depuis hier 14h (2024-12-26) — Un incident technique lié à la résolution DNS a temporairement rendu inaccessible l'API Hubeau, mais a été corrigé rapidement.
- **#218** [toutes API]  interruption de service lun. 17/03/2025 12h-15h (2025-03-17) — Maintenance planifiée et résolue le 17 mars 2025 entraînant une interruption temporaire de toutes les APIs Hub'Eau entre 12h et 15h.
- **#234** API Pluviométrie (2025-10-06) — Hub'eau ne développe pas d'API pluviométrique et oriente vers des sources externes comme Météo-France pour ces données.
- **#237** [toutes API] interruption de service mar. 24/06/2025 12h-15h (2025-06-27) — Une maintenance planifiée a interrompu temporairement toutes les APIs de Hub'Eau le 24/06/2025, sans lien avec une précédente anomalie de données hydrométriques, les deux incidents ayant été résolus.
- **#248** [toutes API] interruption de service mar. 02/09/2025 12h-14h (2025-09-02) — Maintenance planifiée du 02/09/2025 entre 12h et 14h entraînant une interruption temporaire de toutes les API de Hub'Eau, résolue après intervention.
- **#258** [toutes API] tableau de bord (2025-10-07) — La plateforme Hub'Eau a mis en place un tableau de bord de surveillance en temps réel pour tous les endpoints, avec des détails techniques et une gestion automatisée des incidents.
- **#273** [toutes API] interruption de service mar. 17/02/2026 et mer. 18/02/2026 12h-14h (2026-02-18) — Interruption temporaire de toutes les APIs Hub'Eau pour maintenance technique résolue le 18 février 2026.

</details>
