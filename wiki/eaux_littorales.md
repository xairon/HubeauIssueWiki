# Surveillance des eaux littorales

## Particularités techniques

- L'API Surveillance des eaux littorales diffusait des données récentes (2021) pour le réseau RNO (code 0000000020) qui est interrompu depuis 2008. (#65)
- L'API Surveillance des eaux littorales ne diffuse plus de données associées au réseau 0000000020 (RNO). (#65)
- L'API Surveillance des eaux littorales inclut dorénavant les données du réseau 0000000178 (ROCCH - Volet Matière vivante) pour les contaminants chimiques. (#65)
- L'utilisation de wildcards `*` dans les paramètres de recherche n'est pas systématiquement implémentée dans les APIs Hub'Eau. (#101)
- Les wildcards sont disponibles dans certains champs de type code (par exemple, les codes entités de l'API Hydrométrie). (#101)
- Les wildcards ne sont pas supportées pour le paramètre `libelle_lieusurv` de l'API Surveillance des eaux littorales. (#101)
- L'API Hub'eau Surveillance des eaux littorales ne fournit pas toutes les données historiques de Quadrige, se limitant principalement aux contaminants chimiques. (#175)
- Les données de surveillance des eaux littorales qui ne sont pas des contaminants chimiques ne sont pas disponibles via l'API Hub'eau. (#175)

## Informations métier

- Le réseau RNO (Réseau National d'Observation de la qualité du milieu marin - Matière vivante, code 0000000020) est interrompu depuis 2008. (#65)
- Le réseau RNO a été remplacé par le réseau ROCCH (Réseau d’Observation de la Contamination Chimique du milieu marin, code 0800000025). (#65)
- Le code SANDRE 0800000025 (ROCCH) est obsolète et doit être remplacé par 0000000105 (volet Sédiments) et 0000000104 (volet Eau). (#65)
- Le réseau 0000000178 correspond au Réseau d'Observation de la Contamination Chimique du milieu marin (ROCCH) - Volet Matière vivante. (#65)
- Les APIs Hub'Eau distinguent les champs de type 'libellé' et 'code' pour les paramètres de recherche. (#101)
- Le paramètre `libelle_lieusurv` permet de rechercher des lieux de surveillance dans l'API Surveillance des eaux littorales. (#101)
- Les données de surveillance des eaux littorales sont issues de la base Quadrige de l'Ifremer. (#175)
- L'API Hub'eau Surveillance des eaux littorales couvre principalement la thématique des Contaminants chimiques. (#175)
- L'outil Surval permet de visualiser les données de surveillance des eaux littorales et d'identifier la catégorie des analyses (ex: absence de catégorie 'Contaminants'). (#175)
- Le lieu de surveillance 60007272 (Surval) contient des données historiques de 1991 à 2011 qui ne sont pas des contaminants chimiques. (#175)

## Tips d'utilisation

- Pour accéder aux données de surveillance des eaux littorales hors du périmètre des contaminants chimiques, il est nécessaire d'utiliser les téléchargements de l'outil Surval. (#175)

---

## Issues sources

- **#65** [API Surveillance du littoral] — L'API Surveillance des eaux littorales a été mise à jour pour corriger la diffusion de données obsolètes du réseau RNO (0000000020) et intègre désormais les données de contaminants chimiques du réseau ROCCH (0000000178), clarifiant les codes SANDRE associés. `[résolu]`
- **#101** Utilisation de Wildcards * dans les recherches (un classic) — Les wildcards `*` ne sont pas systématiquement supportées dans les APIs Hub'Eau, étant limitées à certains champs de type code comme les codes entités de l'API Hydrométrie, mais non disponibles pour les libellés. `[information]`
- **#175** [API Surveillance des eaux littorales] Récupération des données Quadrige - Historique — L'API Hub'eau Surveillance des eaux littorales ne diffuse qu'une partie des données de Quadrige, principalement les contaminants chimiques, et les données hors de ce périmètre doivent être consultées via l'outil Surval. `[résolu]`
