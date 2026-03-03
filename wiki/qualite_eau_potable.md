# Qualité de l'eau potable

> 17 issues analysées

## Guide

### Comportement actuel  
L'API `/vbeta/qualite_eau_potable/resultats_dis` retourne des données structurées par analyse, non par prélèvement, avec des mises à jour mensuelles le 15 ou 16 du mois (disponibilité à partir du dimanche suivant) (#155, #266). Les paramètres `code_commune` limitent les requêtes à 20 codes Insee simultanément (#128), et le filtrage par `code_departement` n'est pas possible. La pagination utilise le code HTTP 206, incompatible avec certains outils comme DuckDB (#266).  

### Pièges à éviter  
- **Pagination non conforme** : Le code HTTP 206 peut perturber les outils de traitement de flux (ex: DuckDB). Utilisez des bibliothèques compatibles ou traitez les données en lots.  
- **Limitation de `code_commune`** : Les requêtes avec plus de 20 codes Insee échouent. Utilisez des requêtes multiples ou l'API Geo pour contourner cette limite (#128).  
- **Données décalées de deux mois** : Les dernières données disponibles concernent le mois N-2, avec un délai entre prélèvement et traitement (#90).  

### Bonnes pratiques  
- Utilisez `sort=desc` et `size=1` pour obtenir la dernière mesure par paramètre (#84).  
- Privilégiez les codes Sandre (ex: 1302 pour pH) pour des requêtes précises (#141).  
- Traitez les données côté client pour obtenir des prélèvements uniques, car l'API ne les retourne pas par défaut (#211).  
- Consultez la page dédiée de l'API pour vérifier la date de dernière ingestion (#90).  

### Contexte métier  
Les données proviennent de la DGS et du dataset "Resultats du controle sanitaire de l'eau distribuee" sur data.gouv.fr. Les UDI (Unités de Distribution d'Eau) sont associées à des installations amont, mais des erreurs de lien persistent (#276). Les codes SANDRE standardisent les paramètres (ex: pH = 1302), et les UDI sont identifiées par des codes Insee et des réseaux (UGE, distributeurs).  

### Évolutions récentes  
- **2026-02-27** : Correction prévue mi-avril pour les associations incorrectes entre installations amont et UDI aval (#276).  
- **2026-01-27** : Mises à jour mensuelles le 15 ou 16, avec données récentes jusqu'au 30/12/2025 (#266).  
- **2025-12-06** : L'API utilise HTTP 206 pour la pagination, incompatible avec certains outils (#266).  
- **2025-07-16** : Interruption temporaire du service, résolue par l'équipe Hub'eau (#244).  
- **2025-01-29** : Nécessité de traitement client pour agréger des prélèvements uniques (#211).  

### Historique notable  
- **2024-06-25** : Bug corrigé sur les champs de conformité, qui variaient pour les paramètres d'un même prélèvement (#172).  
- **2024-07-17** : Erreur résolue dans le package R `hubeau` pour les champs multivalués comme `code_reseau` (#174).  
- **2022-07-05** : Mise à jour de l'API en version v1, avec ingestion mensuelle tous les 15 du mois (#90).  
- **2021-12-13** : Correction de l'erreur 500 lors de l'absence du paramètre `fields` (#111).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API nécessite l'utilisation des paramètres 'sort=desc' et 'size=1' pour récupérer uniquement la dernière mesure (#84)
- L'API ne permet pas de filtrer simultanément plusieurs paramètres (ex: SO4 et PH) dans une seule requête (#84)
- La fraîcheur des données dépend actuellement du Ministère de la Santé, qui prévoit de mettre en place des webservices dans les années à venir (#84)
- Les données sont ingérées tous les 15 du mois. (#90)
- L'API passera en version v1 en août 2022, avec le même périmètre fonctionnel que la version bêta. (#90)
- Les dernières données disponibles concernent le mois N-2 (deux mois précédents). (#90)
- Le paramètre 'fields' permet de filtrer les colonnes retournées par l'API, mais n'impacte pas leur ordre dans le fichier CSV. (#119)
- L'ordre des colonnes dans les fichiers CSV générés par l'API est stable et déterminé par l'API, indépendamment de l'ordre des paramètres 'fields'. (#119)
- La version bêta de l'API limite le nombre de codes Insee acceptés dans le paramètre `code_commune` à 20 valeurs simultanément. (#128)
- Le paramètre `code_departement` n'est pas disponible pour filtrer les UDI directement via l'API Qualité de l'eau potable. (#128)
- Les données sources (dataset data.gouv.fr) ne contiennent pas les codes départementaux associés aux UDI. (#128)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- L'API actuelle ne permet pas de récupérer une liste de paramètres uniques (sans doublons) pour une commune ou un réseau donné sur une période spécifique. (#139)
- Les champs libelle_parametre... autorisent des recherches permissives (casse, texte partiel, accents). (#141)
- Les prélèvements datant de mois antérieurs au dernier chargement mensuel peuvent être absents de l'API jusqu'à la mise à jour suivante. (#155)
- L'API elle-même ne présente pas d'anomalie ; l'erreur provient du package R `hubeau` qui ne gère pas correctement les cas multivalués. (#174)
- L'API ne fournit pas de description détaillée des réseaux d'eau potable (UGE, distributeurs, MOA, géométrie UDI) via une requête dédiée. Les utilisateurs doivent consulter les données brutes sur data.gouv.fr. (#174)
- L'API ne retourne pas de valeurs uniques par défaut, obligeant les utilisateurs à effectuer un traitement client pour obtenir des prélevements uniques. (#211)
- Les données sont structurées par analyse plutôt que par prélevement, ce qui complique les agrégations statistiques directes. (#211)
- L'API utilise le code HTTP 206 (Partial Content) pour la pagination, ce qui est non conforme aux standards REST et aux RFC. (#261)
- La pagination REST recommande l'utilisation du code HTTP 200 avec des indicateurs de pagination (comme des en-têtes Link ou des champs next). (#261)
- Les données proviennent des fichiers publiés par la DGS (Direction Générale de la Santé). (#266)
- Des associations incorrectes entre installations amont et UDI aval persistent dans les données sources de l'API (#276)
- Aucune donnée complémentaire ne sera déposée avant mi-avril (#276)
- Les prélèvements d'eau amont sont mal associés à des UDI aval dans les données de contrôle sanitaire (#276)
- Les données corrigées ne seront disponibles qu'à partir de mi-avril (#276)

### Historique des problèmes résolus

- ~~La date de dernière ingestion des données est affichée sur la page dédiée de l'API (https://hubeau.eaufrance.fr/page/api-qualite-eau-potable). (#90)~~
- ~~L'API 'resultats_dis' de la qualité de l'eau potable renvoie un 'Internal Server Error' lorsqu'aucun paramètre 'fields' n'est spécifié dans la requête. (#111)~~
- ~~La spécification du paramètre 'fields' permet d'obtenir une réponse valide (même avec 'data': []) sans erreur serveur. (#111)~~
- ~~L'utilisation du paramètre 'sort=asc' dans l'URL de l'API a provoqué un 'Internal Server Error' temporairement. (#113)~~
- ~~Le champ code_parametre_se permet une recherche stricte pour le paramètre 'PH'. (#141)~~
- ~~Le code Sandre pour le paramètre 'pH' est 1302, préférable à code_parametre_se pour l'interopérabilité. (#141)~~
- ~~Les données de l'API sont mises à jour mensuellement le 15 du mois, avec disponibilité à partir du dimanche suivant. (#155)~~
- ~~Les champs de conformité (conformite_references_bact_prelevement, conformite_limites_bact_prelevement, etc.) variaient pour les différents paramètres d'un même prélèvement, ce qui est anormal. (#172)~~
- ~~Le bug a été corrigé lors du traitement d'actualisation des données du 15 mai 2024. (#172)~~
- ~~Les données proviennent du dataset 'Resultats du controle sanitaire de l'eau distribuee commune par commune' sur data.gouv.fr, et les champs de conformité devraient être identiques pour un même prélèvement. (#172)~~
- ~~La fonction R `get_qualite_eau_potable_resultats_dis` génère une erreur lors de la gestion de champs multivalués (comme `code_reseau`) qui produisent des colonnes dupliquées (`reseaux.code` et `reseaux.nom`). (#174)~~
- ~~Le service API /qualite_eau_potable a été temporairement indisponible avant d'être rétabli. (#244)~~
- ~~Les données sont mises à jour le 15 ou 16 de chaque mois, non en début de mois. (#266)~~
- ~~La date du dernier traitement des données est le 23/01/2026. (#266)~~
- ~~Le prélèvement le plus récent dans les données est du 30/12/2025. (#266)~~

### Issues sources

- **#84** /vbeta/qualite_eau_potable/resultats_dis dernière mesure par paramètre (2021-12-13) — L'API de qualité de l'eau potable nécessite des requêtes multiples pour obtenir les dernières mesures par paramètre, avec une amélioration future prévue pour la fraîcheur des données.
- **#90** [API QUALITÉ DE L'EAU POTABLE] - date des données (2022-07-05) — L'API Qualité de l'eau potable affiche désormais la date de dernière ingestion des données, avec une mise à jour mensuelle tous les 15 du mois, et les données disponibles sont décalées de deux mois.
- **#111** [API Qualité de l'eau] Error: Internal Server Error (2022-04-14) — L'API 'resultats_dis' nécessite le paramètre 'fields' pour fonctionner correctement, une exigence technique résolue après relance du service.
- **#113** [API Qualité de l'eau] Error: Internal Server Error (2022-07-05) — Un 'Internal Server Error' sur l'API Qualité de l'eau potable a été résolu après vérification, confirmant que le paramètre 'sort=asc' n'est plus problématique.
- **#119** [API QUALITÉ DE L'EAU POTABLE] (2022-08-07) — L'API Qualité de l'eau potable de Hub'Eau maintient un ordre stable des colonnes dans les fichiers CSV, indépendamment de l'ordre spécifié dans le paramètre 'fields'.
- **#128** API qualité eau potable (2024-02-26) — L'API Qualité de l'eau potable limite les requêtes par commune et ne permet pas de filtrer par département, nécessitant des workarounds avec l'API Geo pour les communes.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#139** [API QUALITÉ DE L'EAU POTABLE] Liste paramètres uniques (sans doublon) (2023-04-28) — L'utilisateur demande une évolution de l'API Qualité de l'eau potable pour permettre la récupération de paramètres uniques (sans doublons) selon des critères géographiques et temporels.
- **#141** [API QUALITÉ DE L'EAU POTABLE] recherche contenu parametre "PH". Anomalie ? (2023-05-30) — L'API Qualité de l'eau potable permet des recherches partielles sur les libellés de paramètres, mais recommande d'utiliser des codes standards (Sandre ou CAS) pour des requêtes précises.
- **#155** [API QUALITÉ DE L'EAU POTABLE] numéro de prélèvement non trouvé (2023-10-16) — L'API Qualité de l'eau potable met à jour ses données mensuellement le 15, avec un délai de disponibilité jusqu'au dimanche suivant, expliquant la disparition temporaire de certains prélèvements.
- **#172** [API Qualité de l'eau] bug sur les conformités (2024-06-25) — Un bug dans l'API Qualité de l'eau potable a été corrigé, empêchant les champs de conformité de varier pour les différents paramètres d'un même prélèvement.
- **#174** [API : QUALITE EAU POTABLE] Erreur sur interrogation par réseau (2024-07-17) — L'issue révèle une incompatibilité entre le package R `hubeau` et les champs multivalués de l'API Qualité de l'eau potable, ainsi qu'une absence de fonctionnalité pour obtenir des métadonnées détaillées sur les réseaux.
- **#211** [API : QUALITE EAU POTABLE] Besoin de calculer le nombre de prelevement sans parcourir response.data (2025-01-29) — L'API Qualité de l'eau potable ne permet pas de récupérer directement le nombre de prélevements uniques, nécessitant un traitement supplémentaire côté client.
- **#244** [API : QUALITE EAU POTABLE] service HS (2025-07-16) — L'API Qualité de l'eau potable a connu une interruption temporaire de service, résolue par l'équipe Hub'eau.
- **#261** HTTP 206 renvoyé pour des données paginées : flux non lisible dasn DuckDB par exemple (2025-12-06) — L'API Qualité de l'eau potable utilise incorrectement le code HTTP 206 pour la pagination, ce qui peut poser des problèmes de compatibilité avec certains outils comme DuckDB.
- **#266** [API qualite_eau_potable] Données non mises à jour (2026-01-27) — L'API Qualité de l'eau potable met à jour ses données le 15 ou 16 de chaque mois, avec un délai entre la date de prélèvement et le traitement des données.
- **#276** [API Qualité de l'eau potable] anomalie dans les données sources (2026-02-27) — Une anomalie dans les associations entre installations amont et UDI aval affecte les données de l'API Qualité de l'eau potable, avec des corrections prévues mi-avril.

</details>
