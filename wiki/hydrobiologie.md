# Hydrobiologie

> 14 issues analysées

## Guide

### Comportement actuel  
L'API Hydrobiologie permet d'accéder aux données de Naïade V1 via les endpoints *indices* et *taxons*, avec un format JSON ou GeoJSON. Les requêtes peuvent inclure des filtres comme *code_support* (10 pour les diatomées), *date_debut_prelevement*, et *code_operation* (ajouté en 2022). La limite de 10 000 résultats par requête est en vigueur, et les erreurs de format de date (JSON vs GeoJSON) persistent (#247). Les stations avec des champs géographiques vides (code_region, etc.) restent difficiles à récupérer (#215).  

### Pièges à éviter  
L'absence d'un endpoint dédié aux opérations de prélèvement biologique limite l'accès complet aux données (#123). Les formats de date incompatibles entre JSON et GeoJSON (ex: Unix timestamp vs ISO 8601) compliquent l'analyse (#247). Les champs *code_region* vides empêchent la récupération de 45 stations (#215). Utilisez *code_support=10* pour les diatomées, et évitez *code_support=13* (résolu en 2022).  

### Bonnes pratiques  
Utilisez *code_indice* avec des codes spécifiques (ex: 5856) pour filtrer les diatomées (#46). Gérez la pagination pour éviter les limites de 10 000 résultats. Privilégiez les endpoints *indices* et *taxons* pour les données hydrobiologiques, et vérifiez les champs *code_operation* pour rattacher les résultats à des opérations.  

### Contexte métier  
Les codes SANDRE (ex: 10 pour diatomées, 13 pour macroinvertébrés) définissent les types d'indices biologiques. Les stations sont gérées par des Agences de l'Eau, et les données proviennent de Naïade V1 (non V0). Les opérations de prélèvement incluent des métadonnées comme *CdPointEauxSurf* et *CdMethode*.  

### Évolutions récentes  
- **2025-10-03** : Incohérence de format de date entre JSON et GeoJSON persiste (#247).  
- **2025-04-08** : Problèmes avec les champs *code_region* vides, impactant 45 stations (#215).  
- **2024-02-26** : Correction de la duplication des observations liée aux conditions environnementales (#129).  
- **2022-07-22** : Mise à jour vers la version v1, corrigeant les bugs liés aux dates et aux paramètres (#81, #107).  
- **2022-07-05** : Ajout des champs *code_operation* dans les endpoints *indices* et *taxons* (#99).  

### Historique notable  
- **2022-02-25** : Erreurs 500/406 résolues via des mises à jour de l'API (#106).  
- **2022-02-09** : Correction de l'exemple d'API utilisant *code_support=13* au lieu de *10* (#97).  
- **2020-09-21** : Support de Naïade V0 non disponible, uniquement V1 (#45).  
- **2020-09-21** : Erreurs de classification des indices biologiques (code SANDRE 13) résolues via *code_indice* (#46).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Hydrobiologie ne prend pas en charge les données de Naïade V0, uniquement celles de Naïade V1. (#45)
- Les données de Naïade V0 sont intégrées progressivement dans Naïade V1 via des transmissions d'Agences de l'Eau. (#45)
- Les données hydrobiologiques hors poisson de Naïade V0 sont disponibles en format brut sur le site dédié, mais non accessibles via l'API Hub'Eau actuelle. (#45)
- La requête avec code_support=13 renvoie des indices invertébrés au lieu des diatomées en raison d'erreurs dans les données sources. (#46)
- Le paramètre code_support=10 doit être utilisé pour les diatomées, mais des erreurs de classification persistent dans ~10% des données. (#46)
- Les données sources transmises à Naïades contiennent des erreurs de classification des indices biologiques selon le code SANDRE. (#46)
- Le code SANDRE 13 (diatomées) est mal attribué à certains indices invertébrés, affectant environ 10% des données. (#46)
- Les informations sur les opérations sont actuellement accessibles via l'endpoint 'taxons', mais un endpoint dédié 'Opérations' est proposé pour une meilleure logique d'exposition des données. (#98)
- Les données environnementales et les informations sur les opérations sont nécessaires pour des calculs comme l'I2M2 à partir des listes faunistiques de l'IBG-DCE. (#98)
- Le champ 'RefOperationPrelBio' permet d'associer de manière unique des résultats biologiques ou des listes taxonomiques à une opération spécifique, même si plusieurs opérations ont lieu sur la même station au même jour. (#99)
- L'API 'Qualité des cours d'eau' ne renvoie pas de données pour des stations configurées pour d'autres types de mesure (ex: hydrobiologie). (#105)
- Les stations listées ne sont pas associées à la qualité des cours d'eau dans le système de données. (#105)
- Les stations du code postal 34 (Hérault) mentionnées sont dédiées à des mesures hydrobiologiques et non à la qualité des cours d'eau. (#105)
- L'API Hydrobiologie renvoie des erreurs 500 (Internal Server Error) et 406 (Not Acceptable) lors de requêtes spécifiques. (#106)
- Les erreurs sont récurrentes mais temporaires, avec une récupération spontanée après quelques minutes/heures. (#106)
- L'API Hydrobiologie ne dispose pas d'un endpoint dédié aux opérations de prélèvement biologique, contrairement à l'API Qualité des cours d'eau. (#123)
- Les utilisateurs ont besoin des champs liés aux opérations de prélèvement (CdPointEauxSurf, CdMethode, etc.) pour rattacher les résultats biologiques à des opérations spécifiques. (#123)
- L'évolution de l'API pour créer un endpoint 'operations' est planifiée dans la feuille de route 2025-2026 mais n'est pas encore réalisée. (#123)
- Les données sur les macrophytes présentaient des quadruplets, mais cette vérification n'était pas approfondie. (#129)
- L'API Hydrobiologie ne permet pas actuellement de filtrer les résultats avec des champs de code_region vides (ou null) via une requête spécifique. (#215)
- Le seuil de 20560 résultats par requête force les utilisateurs à utiliser des boucles géographiques (codes région/département), mais cela manque 46 stations en raison de champs vides. (#215)
- 45 stations ont des champs code_region, code_département, code_commune vides, avec des géolocalisations variables (y compris en dehors de la France). (#215)
- Certaines stations sont situées dans des communes disparues suite à des fusions administratives. (#215)
- L'API Hydrobiologie retourne des dates de prélèvement dans des formats incompatibles selon le format de sortie (json vs geojson). (#247)
- Le format geojson utilise un timestamp Unix en millisecondes pour les dates (ex: 1732060800000) alors que le format json utilise ISO 8601 (ex: 2024-11-20T00:00:00Z). (#247)
- Pour l'endpoint 'indices', le format geojson utilise une date simplifiée (ex: 2024-11-15) sans indication d'heure, contrairement au format json qui inclut l'heure (ex: 2024-11-15T00:00:00Z). (#247)

### Historique des problèmes résolus

- ~~Un contournement consiste à filtrer via code_indice avec des codes spécifiques (ex: 5856, 1022, etc.) pour obtenir uniquement les indices diatomiques valides. (#46)~~
- ~~L'API Hydrobiologie présentait un bug lors de la requête avec des paramètres de dates (date_debut_prelevement ou date_fin_prelevement), entraînant un 'Internal server error'. (#81)~~
- ~~La version v1 de l'API a corrigé ce bug et permet désormais de récupérer des données avec des paramètres de dates sans erreur serveur. (#81)~~
- ~~L'exemple de l'API hydrobio utilisait incorrectement le code support 13 au lieu de 10 pour les diatomées. (#97)~~
- ~~Le code support 10 correspond aux diatomées, tandis que le code support 13 concerne les macroinvertébrés. (#97)~~
- ~~L'API Hydrobiologie ajoutera les champs 'code_banque_reference' et 'code_operation' dans les réponses des endpoints 'indices' et 'taxons' lors de la mise à jour en v1 en juillet 2022. (#99)~~
- ~~Ces nouveaux champs seront requêtables via l'API. (#99)~~
- ~~La version bêta de l'API Hydrobiologie ne supportait pas correctement le paramètre 'date_debut_prelevement', entraînant un 'Internal server error'. (#107)~~
- ~~La mise à jour vers la version v1 de l'API a corrigé ce problème, permettant désormais la filtration des données par date de prélèvement. (#107)~~
- ~~La limite maximale de résultats renvoyés par l'API hydrobiologie est de 10 000 enregistrements, non 20 000 comme indiqué dans la documentation initiale. (#109)~~
- ~~Le champ _code_operation_prelevement_ a été ajouté aux endpoints 'indices' et 'taxons' de l'API Hydrobiologie. (#123)~~
- ~~L'API Hydrobiologie dupliquait les enregistrements lorsqu'il existait des conditions environnementales associées aux prélèvements. (#129)~~
- ~~La duplication entraînait des totaux incorrects (ex. : 13 anguilles affichés comme 26). (#129)~~
- ~~La base de données Aspe contenait des effectifs corrects, mais l'API dupliquait les résultats pour certains prélèvements. (#129)~~

### Issues sources

- **#45** [API HYDROBIOLOGIE]_données Naïades V0 (2020-09-21) — L'API Hydrobiologie de Hub'Eau ne supporte pas encore les données de Naïade V0, qui restent accessibles uniquement via le site web dédié.
- **#46** [API HYDROBIOLOGIE]_requête non fonctionnelle (2020-09-21) — L'API Hydrobiologie retourne des résultats incorrects pour les diatomées (code_support=13) en raison d'erreurs de classification dans les données sources, avec un contournement via le paramètre code_indice.
- **#81** [API Hydrobiologie] Erreur lorsqu'une date de fin ou un de début de prélèvement est indiquée (2022-07-22) — L'API Hydrobiologie a corrigé un bug lié aux paramètres de dates de prélèvement, résolu avec la mise à jour vers la version v1.
- **#97** [hydrobio] coquille dans un des exemples (2022-02-09) — L'issue a corrigé une erreur dans l'exemple de l'API hydrobio concernant le code SANDRE pour les diatomées.
- **#98** [API-Hydrobiologie] Export des conditions environnementales et des informations sur les opérations (2022-02-09) — L'issue souligne la nécessité d'accéder via l'API Hydrobiologie aux données environnementales et aux informations sur les opérations, actuellement partiellement disponibles via l'endpoint 'taxons'.
- **#99** [API-Hydrobiologie] Ajouter la référence de l'opération aux exports (2022-07-05) — L'API Hydrobiologie intègrera un champ de référence d'opération pour permettre une identification précise des prélèvements, même en cas de redondance temporelle et spatiale.
- **#105** Non remontée des données "Qualité des cours d'eau" pour un ensemble de stations dans le 34 (2022-03-09) — Les stations listées dans l'issue ne fournissent pas de données de qualité des cours d'eau car elles sont configurées pour d'autres types de mesures comme l'hydrobiologie.
- **#106** [API Hydrobiologie] Erreurs 500 / 406 dans les réponses de l'API (2022-02-25) — L'API Hydrobiologie de Hub'Eau présente des problèmes récurrents de disponibilité et de compatibilité des formats de réponse (JSON/CSV).
- **#107** [API Hydrobiologie] pb de date dans l'url (2022-07-22) — L'API Hydrobiologie a corrigé un bug empêchant la filtration des données par date de prélèvement, désormais fonctionnelle en version v1.
- **#109** [API hydrobiologie] profondeur d'accès aux résultats (2022-07-05) — L'API hydrobiologie a une limite technique de 10 000 enregistrements par requête, corrigée dans la documentation après identification d'une incohérence.
- **#123** [API Hydrobiologie] ajout de champs présents sous Naïades (2026-02-18) — L'API Hydrobiologie manque de champs et d'un endpoint dédié pour gérer les opérations de prélèvement biologique, bloquant l'utilisation complète des données par les utilisateurs.
- **#129** [API Hydrobiologie] observations dupliquées pour endpoint « taxons » (2024-02-26) — L'API Hydrobiologie dupliquait certaines observations en raison de conditions environnementales associées, mais cette anomalie a été corrigée dans une mise à jour récente.
- **#215** [API Hydrobiologie] champs code_region vides (2025-04-08) — L'API Hydrobiologie présente des lacunes dans la gestion des champs géographiques vides, impactant la récupération complète des stations.
- **#247** [API Hydrobiologie] Inconsistence du format de date_prelevement selon le format json/geojson (2025-10-03) — L'API Hydrobiologie présente une incohérence de format de dates entre les formats json et geojson, impactant la consistance des données hydrobiologiques.

</details>
