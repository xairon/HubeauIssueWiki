# Écoulement des cours d'eau

> 8 issues analysées

## Guide

### Comportement actuel  
L'API Écoulement des cours d'eau fournit des données hydrologiques via des endpoints comme `observations` et `stations`, en format JSON. La pagination utilise les paramètres `page` et `size`, mais le paramètre `size` influence l'ordre des résultats, pouvant générer des doublons lors de la pagination (#193). Les filtres de date (`date_observation_min`, `date_observation_max`) appliquent des opérateurs stricts (> et <) au lieu des opérateurs inclusifs indiqués dans la documentation (#192). La description OpenAPI présente des erreurs de nommage et de typage des paramètres (#127).  

### Pièges à éviter  
Les filtres de date stricts empêchent la récupération de données pour des dates spécifiques, contrairement à la documentation. La pagination peut produire des doublons, surtout avec des tailles de page non optimisées. La description OpenAPI incorrecte peut induire en erreur les développeurs lors de la conception de requêtes. Pour contourner ces problèmes, vérifiez les opérateurs de filtre, utilisez des tailles de page petites et testez les requêtes avec des outils comme Postman.  

### Bonnes pratiques  
Utilisez le package R `hubeau` pour accéder à l'API via une syntaxe standardisée, comme `get_Ecoulement_observations` (#137). Documentez les paramètres de pagination et les filtres de date pour éviter les doublons. Pour les requêtes WFS, utilisez les URI fournis par l'API (`uri_cours_eau`) et le code `code_cours_eau` pour identifier les entités hydrographiques (#194).  

### Contexte métier  
Les données proviennent de stations hydrologiques équipées de capteurs, avec des codes BSS (Bassin Sédimentaire) et SANDRE (Système d'Identification des Ressources en Eau) pour identifier les cours d'eau. Les stations sont classées par type (ex: hydrométrique, pluviométrique). Les rapports hydrologiques utilisent ces données pour analyser les débits et les crues.  

### Évolutions récentes  
- **2025-05-21 (#192)** : Les filtres de date restent stricts, malgré les mises à jour de la documentation.  
- **2024-10-18 (#193)** : Les doublons lors de la pagination persistent, avec des impacts sur la reproductibilité.  
- **2024-02-26 (#127)** : Les erreurs de description OpenAPI (noms de paramètres, types) sont toujours en cours de correction.  
- **2024-11-05 (#194)** : La méthode pour retrouver les ressources Sandre via WFS a été résolue.  
- **2023-06-06 (#142)** : La version stable 1.0 de l'API est désormais utilisée (URL `/v1` au lieu de `/vbeta`).  

### Historique notable  
- **2023-06-06 (#142)** : Migration vers la version stable 1.0, avec changement d'URL.  
- **2023-04-12 (#122)** : Mise à jour quotidienne des données depuis avril 2023.  
- **2025-05-14 (#233)** : Problème temporaire sur le endpoint `stations` résolu.  
- **2024-11-05 (#194)** : Correction des paramètres WFS pour accéder à Sandre.

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Le champ 'Numéro de page' dans la description OpenAPI utilise une description au lieu du nom réel du paramètre (#127)
- Le champ 'Liste des champs...' dans la description OpenAPI utilise une description au lieu du nom réel 'fields' (#127)
- Le type du paramètre 'fields' est incorrectement déclaré au lieu de [array(string)] (#127)
- La description du paramètre 'size' est ancrée dans le sous-élément 'schema' au lieu d'être au même niveau que le nom du champ (#127)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- Les paramètres date_observation_min et date_observation_max appliquent des filtres stricts (> et <) au lieu des opérateurs inclusifs (>= et <=) comme indiqué dans la documentation. (#192)
- L'API retourne des doublons lors de la pagination (ex. même feature apparaît sur les pages 1 et 2 avec les mêmes données) (#193)
- Le paramètre 'size' influence l'ordre des résultats, ce qui peut créer des incohérences lors de la pagination (#193)
- La station D0137052 (L'Helpe mineure à Fourmies) a des observations dupliquées pour la date 2024-09-26 (#193)
- Les URI fournis par l'API Hub'Eau (ex: uri_cours_eau) contiennent des informations structurées permettant d'accéder directement aux données Sandre via des services WFS. (#194)

### Historique des problèmes résolus

- ~~Les données de l'API sont mises à jour quotidiennement depuis le 12 avril 2023. (#122)~~
- ~~La version bêta de l'API a été remplacée par la version stable 1.0 le 23 mai 2023. Les URLs doivent utiliser '/v1' au lieu de '/vbeta'. (#142)~~
- ~~Le paramètre TYPENAME dans l'URL WFS est dérivé du nom du jeu de données Sandre (ex: CoursEau_Carthage2017), disponible dans le champ uri_cours_eau de l'API Hub'Eau. (#194)~~
- ~~Le code_cours_eau (ex: M1015000) est utilisé comme filtre dans la requête WFS pour identifier l'entité hydrographique spécifique. (#194)~~
- ~~Le endpoint _stations_ de l'API _Écoulement des cours d'eau_ a connu une interruption de service temporaire, empêchant la récupération des données. (#233)~~

### Issues sources

- **#122** [API Ecoulement des cours d'eau] Fréquence d'actualisation (2023-04-12) — L'API Écoulement des cours d'eau met à jour ses données quotidiennement depuis avril 2023.
- **#127** [API Ecoulement] Erreurs dans la description openapi (2024-02-26) — L'API Écoulement des cours d'eau présente des erreurs dans sa description OpenAPI concernant les noms et types des paramètres de requête.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#142** [API Ecoulement des cours d'eau] Passage en version stable (2023-06-06) — L'API Écoulement des cours d'eau a migré de la version bêta à la version stable 1.0 en mai 2023, nécessitant une mise à jour des paramètres d'URL pour les utilisateurs.
- **#192** [API Ecoulement des cours d'eau] observations - erreur sur les champs date_observation_min & date_observation_max (2025-05-21) — L'API Écoulement des cours d'eau applique des filtres stricts sur les dates contrairement à la documentation, empêchant la récupération de données pour des dates spécifiques.
- **#193** [API Ecoulement des cours d'eau] observations - doublons produits par l'API (2024-10-18) — L'API Écoulement des cours d'eau génère des doublons lors de la pagination, affectant la reproductibilité des résultats.
- **#194** [API Ecoulement des cours d'eau] Comment retrouver les ressources liées ? (2024-11-05) — L'API Écoulement des cours d'eau fournit des URI permettant d'accéder à des jeux de données Sandre via des requêtes WFS, avec des paramètres dépendant de codes hydrographiques et de noms de jeux de données.
- **#233** [API Ecoulement des cours d'eau] pas de données stations (2025-05-14) — Le endpoint _stations_ de l'API Écoulement des cours d'eau a temporairement cessé de fournir des données, mais le problème a été résolu.

</details>
