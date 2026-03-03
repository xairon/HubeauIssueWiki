# Surveillance des eaux littorales

> 3 issues analysées

## Guide

### Comportement actuel  
L'API Surveillance des eaux littorales fournit des données via des endpoints structurés, principalement en format JSON. La pagination est appliquée pour les requêtes volumineuses. Les paramètres clés incluent les codes SANDRE (ex. 0000000104, 0000000105) et les thèmes de données (ex. contaminants chimiques). Les données du réseau ROCCH (code 0000000178) sont désormais accessibles, remplacant l'ancien réseau RNO (#65).  

### Pièges à éviter  
Les wildcards * ne sont pas supportés dans les champs de type libellé (ex. libelle_lieusurv), limitant les recherches flexibles (#101). L'API ne propose pas l'accès à l'ensemble des données historiques de Quadrige, uniquement celles liées aux contaminants chimiques (#175). Ces limitations peuvent entraîner des résultats incomplets si les utilisateurs ne s'alignent pas sur les codes SANDRE ou les thèmes de données.  

### Bonnes pratiques  
Utilisez des codes SANDRE exacts pour les requêtes, et filtrez par thème (ex. contaminants) pour maximiser la pertinence des résultats. Pour les recherches par libellé, privilégiez les termes complets ou les codes associés. Vérifiez régulièrement les mises à jour des codes SANDRE, car certains anciens (ex. 0800000025) sont obsolètes (#65).  

### Contexte métier  
Les codes SANDRE identifient les réseaux et stations de surveillance. Le réseau RNO (Matière vivante) a été remplacé par ROCCH (code 0000000178) en 2008. Les données de contaminants chimiques sont structurées via des codes spécifiques (ex. 0000000104 pour l'eau). Comprendre ces codes permet d'interpréter correctement les résultats de l'API.  

### Évolutions récentes  
- **2024-06-07** : L'API limite l'accès aux données historiques de Quadrige aux seuls contaminants chimiques (#175).  
- **2022-07-05** : Les wildcards * restent partiellement supportés pour les codes hydrométriques, mais pas pour les libellés (#101).  
- **2021-12-14** : Mise à jour des codes SANDRE pour intégrer ROCCH et corriger les données associées à RNO (#65).  

### Historique notable  
- **2021-12-14** : Correction de l'erreur de diffusion des données liées au réseau RNO, remplacé par ROCCH (code 0000000178) (#65).  
- **2021-12-14** : Intégration des données du réseau ROCCH via les codes SANDRE 0000000104 et 0000000105, conformément aux recommandations de l'IFREMER (#65).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Le réseau RNO (Matière vivante) a été interrompu en 2008 et remplacé par ROCCH, dont les données sont désormais associées au code SANDRE 0000000178. (#65)
- Les codes SANDRE 0000000104 (Eau) et 0000000105 (Sédiments) remplacent le code obsolète 0800000025 pour le ROCCH. (#65)
- Les wildcards * ne sont pas systématiquement implémentés dans les champs de recherche de l'API Surveillance des eaux littorales, notamment pour le paramètre libelle_lieusurv. (#101)
- Les wildcards * sont disponibles dans certains champs de type code de l'API Hydrométrie (ex. codes entités). (#101)
- L'API Surveillance des eaux littorales ne diffuse que les données de Quadrige liées aux 'Contaminants chimiques', et non toutes les données historiques disponibles. (#175)
- Les données historiques pour certains lieux de surveillance (ex. 60007272) ne sont pas accessibles via l'API Hub'eau car elles ne relèvent pas de la thématique 'Contaminants chimiques'. (#175)

### Historique des problèmes résolus

- ~~L'API Surveillance du Littoral a corrigé la diffusion de données associées au réseau obsolète 0000000020 (RNO) après mise à jour des données. (#65)~~
- ~~Les données de contaminants chimiques incluent désormais le réseau 0000000178 (ROCCH - Volet Matière vivante) conformément aux recommandations de l'IFREMER. (#65)~~

### Issues sources

- **#65** [API Surveillance du littoral] (2021-12-14) — L'API Surveillance du Littoral a corrigé une erreur de diffusion de données associées à un réseau obsolète et intègre désormais les données du réseau ROCCH via un nouveau code SANDRE.
- **#101** Utilisation de Wildcards * dans les recherches (un classic) (2022-07-05) — Les wildcards * sont partiellement supportés dans certaines APIs de Hub'Eau, notamment pour les codes hydrométriques mais pas pour les libellés de lieux de surveillance littorale.
- **#175** [API Surveillance des eaux littorales] Récupération des données Quadrige - Historique (2024-06-07) — L'API Surveillance des eaux littorales ne propose pas l'accès à l'ensemble des données historiques de Quadrige, uniquement celles liées aux contaminants chimiques.

</details>
