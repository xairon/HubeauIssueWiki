# Surveillance des eaux littorales

> 3 issues analysées

## Guide

### Comportement actuel

L'API Hub'Eau "Surveillance des eaux littorales" est principalement conçue pour la diffusion des données de contaminants chimiques. Elle intègre désormais les données du réseau ROCCH (Réseau d'Observation de la Contamination Chimique du milieu marin) - Volet Matière vivante (code 0000000178) (#65). Le paramètre `libelle_lieusurv` est disponible pour effectuer des recherches par nom de lieu de surveillance (#101). L'API a été mise à jour et ne diffuse plus les données obsolètes du réseau RNO (0000000020), interrompu depuis 2008 (#65).

### Pièges à éviter

L'API ne fournit pas l'intégralité des données historiques de la base Quadrige, se concentrant exclusivement sur les contaminants chimiques (#175). Les données de surveillance des eaux littorales qui ne relèvent pas de cette thématique ne sont pas accessibles via l'API et nécessitent l'utilisation de l'outil Surval pour leur consultation ou téléchargement (#175). De plus, les wildcards `*` ne sont pas supportées pour le paramètre `libelle_lieusurv` (#101), ce qui limite les recherches floues par libellé.

### Bonnes pratiques

Pour des recherches efficaces, privilégiez les correspondances exactes pour les paramètres de type 'libellé', comme `libelle_lieusurv`, étant donné l'absence de support des wildcards (#101). Si votre besoin concerne des données de surveillance des eaux littorales autres que les contaminants chimiques, orientez-vous directement vers l'outil Surval de l'Ifremer, qui offre un accès complet à l'historique des données de Quadrige (#175).

### Contexte métier

Les données de surveillance des eaux littorales proviennent de la base Quadrige de l'Ifremer (#175). Il est crucial de comprendre l'évolution des réseaux : le réseau RNO (0000000020) a été interrompu en 2008 et remplacé par le ROCCH (#65). Les codes SANDRE associés au ROCCH ont également évolué, le code 0800000025 étant obsolète au profit des codes 0000000105 (volet Sédiments) et 0000000104 (volet Eau), tandis que le réseau 0000000178 représente spécifiquement le volet Matière vivante du ROCCH (#65). Les APIs Hub'Eau distinguent généralement les champs de recherche par 'libellé' et par 'code' (#101).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'utilisation de wildcards `*` dans les paramètres de recherche n'est pas systématiquement implémentée dans les APIs Hub'Eau. (#101)
- Les wildcards sont disponibles dans certains champs de type code (par exemple, les codes entités de l'API Hydrométrie). (#101)
- Les wildcards ne sont pas supportées pour le paramètre `libelle_lieusurv` de l'API Surveillance des eaux littorales. (#101)
- Les APIs Hub'Eau distinguent les champs de type 'libellé' et 'code' pour les paramètres de recherche. (#101)
- Le paramètre `libelle_lieusurv` permet de rechercher des lieux de surveillance dans l'API Surveillance des eaux littorales. (#101)

### Historique des problèmes résolus

- ~~L'API Surveillance des eaux littorales diffusait des données récentes (2021) pour le réseau RNO (code 0000000020) qui est interrompu depuis 2008. (#65)~~
- ~~L'API Surveillance des eaux littorales ne diffuse plus de données associées au réseau 0000000020 (RNO). (#65)~~
- ~~L'API Surveillance des eaux littorales inclut dorénavant les données du réseau 0000000178 (ROCCH - Volet Matière vivante) pour les contaminants chimiques. (#65)~~
- ~~Le réseau RNO (Réseau National d'Observation de la qualité du milieu marin - Matière vivante, code 0000000020) est interrompu depuis 2008. (#65)~~
- ~~Le réseau RNO a été remplacé par le réseau ROCCH (Réseau d’Observation de la Contamination Chimique du milieu marin, code 0800000025). (#65)~~
- ~~Le code SANDRE 0800000025 (ROCCH) est obsolète et doit être remplacé par 0000000105 (volet Sédiments) et 0000000104 (volet Eau). (#65)~~
- ~~Le réseau 0000000178 correspond au Réseau d'Observation de la Contamination Chimique du milieu marin (ROCCH) - Volet Matière vivante. (#65)~~
- ~~L'API Hub'eau Surveillance des eaux littorales ne fournit pas toutes les données historiques de Quadrige, se limitant principalement aux contaminants chimiques. (#175)~~
- ~~Les données de surveillance des eaux littorales qui ne sont pas des contaminants chimiques ne sont pas disponibles via l'API Hub'eau. (#175)~~
- ~~Pour accéder aux données de surveillance des eaux littorales hors du périmètre des contaminants chimiques, il est nécessaire d'utiliser les téléchargements de l'outil Surval. (#175)~~
- ~~Les données de surveillance des eaux littorales sont issues de la base Quadrige de l'Ifremer. (#175)~~
- ~~L'API Hub'eau Surveillance des eaux littorales couvre principalement la thématique des Contaminants chimiques. (#175)~~
- ~~L'outil Surval permet de visualiser les données de surveillance des eaux littorales et d'identifier la catégorie des analyses (ex: absence de catégorie 'Contaminants'). (#175)~~
- ~~Le lieu de surveillance 60007272 (Surval) contient des données historiques de 1991 à 2011 qui ne sont pas des contaminants chimiques. (#175)~~

### Issues sources

- **#65** [API Surveillance du littoral] — L'API Surveillance des eaux littorales a été mise à jour pour corriger la diffusion de données obsolètes du réseau RNO (0000000020) et intègre désormais les données de contaminants chimiques du réseau ROCCH (0000000178), clarifiant les codes SANDRE associés. `[résolu]`
- **#101** Utilisation de Wildcards * dans les recherches (un classic) — Les wildcards `*` ne sont pas systématiquement supportées dans les APIs Hub'Eau, étant limitées à certains champs de type code comme les codes entités de l'API Hydrométrie, mais non disponibles pour les libellés. `[information]`
- **#175** [API Surveillance des eaux littorales] Récupération des données Quadrige - Historique — L'API Hub'eau Surveillance des eaux littorales ne diffuse qu'une partie des données de Quadrige, principalement les contaminants chimiques, et les données hors de ce périmètre doivent être consultées via l'outil Surval. `[résolu]`

</details>
