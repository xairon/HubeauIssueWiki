# Hydrobiologie

## Particularités techniques

- L'API Hub'Eau "Poisson" (endpoint `/poissons`) ne permet pas de récupérer les données d'un poisson par son nom, seulement par son `code_espece_poisson`. (#33)
- L'endpoint `/code_espece_poisson` de l'API "Poisson" permet d'obtenir la liste des correspondances entre codes OFB, codes SANDRE, noms latins et français des espèces. (#33)
- La future API Hub'Eau "Hydrobiologie" permettra d'interroger les données par le nom de l'espèce. (#33)
- L'API Référentiel du SANDRE (`api.sandre.eaufrance.fr/referentiels/v1/apt.json`) peut être utilisée pour faire la correspondance nom-code. (#33)
- Avec l'API SANDRE, on peut filtrer par nom latin (`NomLatinAppelTaxon`) pour obtenir le code OFB (sous `CodeAlternatifAp` où `OrgCdAlternatif="ASPE"`). (#33)
- Avec l'API SANDRE, on peut filtrer par nom commun (`//LbNomCommunAppelTaxon`) en utilisant une expression XPath dans le paramètre `filter`. (#33)
- L'API Hub'Eau Hydrobiologie n'intègre que les données de la version actuelle de Naïades (V1). (#45)
- Les données de Naïades V0 ne sont pas directement accessibles via l'API Hub'Eau Hydrobiologie. (#45)
- Les données manquantes dans Naïades V1 seront automatiquement visibles dans Hub'Eau une fois intégrées à Naïades V1. (#45)
- La requête initiale avec `code_support=13` pour les diatomées est incorrecte et renvoie des indices invertébrés. (#46)
- Le paramètre `code_support=10` doit être utilisé pour interroger les indices de diatomées. (#46)
- L'endpoint `/api/v1/hydrobio/indices` permet désormais de filtrer correctement par `date_debut_prelevement` et `date_fin_prelevement`. (#81)
- L'exemple de l'API Hub'Eau Hydrobiologie pour la recherche d'indices biologiques avec le paramètre `code_support=13` associait incorrectement ce code aux diatomées. (#97)
- Les données environnementales et les informations sur les opérations sont disponibles dans la requête 'taxons' de l'API Hydrobiologie. (#98)
- Il est suggéré de créer une requête dédiée 'Opérations' pour exposer ces informations de manière plus logique. (#98)
- L'API Hydrobiologie a été mise à jour en v1 en juillet 2022. (#99)
- Les champs `code_banque_reference` et `code_operation` ont été ajoutés à la réponse de l'API pour les endpoints `indices` et `taxons`. (#99)
- Les champs `code_banque_reference` et `code_operation` sont également requêtables sur l'API Hydrobiologie. (#99)
- Avant cette mise à jour, il était difficile de rattacher une liste taxonomique à l'opération correspondante sans le champ `RefOperationPrelBio`. (#99)
- L'API Hub'Eau Hydrobiologie a migré de la version `vbeta` à la version `v1`. (#107)
- Le paramètre `date_debut_prelevement` est fonctionnel dans l'API Hub'Eau Hydrobiologie `v1` pour filtrer les données par date de prélèvement. (#107)
- La limite de profondeur d'accès aux résultats pour l'API Hydrobiologie est de 10 000 enregistrements maximum. (#109)
- Cette limite a été réduite de 20 000 à 10 000 enregistrements pour éviter les timeouts de l'API. (#109)
- La documentation de l'API Hydrobiologie sera mise à jour pour refléter cette nouvelle limite. (#109)
- L'API peut renvoyer un code 206 (Partial Content) si le nombre total d'enregistrements disponibles dépasse la limite interne de 10 000. (#109)
- L'API Hydrobiologie ne dispose pas d'un endpoint dédié aux opérations de prélèvement, contrairement à l'API Qualité des cours d'eau. (#123)
- Un champ "_code_operation_prelevement_" a été ajouté aux endpoints "indices" et "taxons" de l'API Hydrobiologie. (#123)
- La création d'un endpoint "operations" spécifique ou l'ajout de champs supplémentaires pour les opérations de prélèvement est une évolution envisagée pour la feuille de route 2025-2026 mais non planifiée à ce stade. (#123)
- Les champs initialement demandés pour les exports d'opérations sont : CdPointEauxSurf, CdMethode, CdProducteur, CdPreleveur, CdDeterminateur, CodeSandreRdd, CdStatutResBioOperationPrelBio, CdQualResBioOperationPrelBio, ObjOperationPrelBio. (#123)
- Avant correction, l'endpoint `/hydrobio/taxons` de l'API Hydrobiologie pouvait retourner des observations de taxons et des indices dupliqués. (#129)
- La duplication des taxons et des indices était causée par la présence de conditions environnementales associées à l'opération de prélèvement. (#129)
- Une nouvelle version de l'API Hydrobiologie a été déployée pour corriger cette anomalie de duplication. (#129)
- La correction des doublons a entraîné une diminution du volume de données diffusées par l'API (2 millions d'observations de taxons en moins, 100 000 indices en moins). (#129)
- Les APIs Hub'Eau (notamment Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) ne disposent pas de paramètre de filtre par date de mise à jour des données. (#131)
- L'absence de filtre par date de mise à jour oblige les utilisateurs à charger l'intégralité des données pour rester à jour. (#131)
- L'API Hydrométrie inclut une 'date de production' dans ses résultats, mais ce paramètre n'est pas utilisable comme filtre de requête. (#131)
- L'ajout d'un filtre par date de mise à jour n'est pas prévu à court terme pour l'API Piézométrie. (#131)
- L'ajout d'un filtre par date de mise à jour est une évolution identifiée pour l'API Hydrométrie. (#131)
- L'API Hydrobiologie ne permet pas de filtrer les stations dont les champs géographiques (ex: code_region) sont vides ou non renseignés via une requête code_region = "" (chaîne vide). (#215)
- Une requête sur un champ avec une chaîne de texte vide se comporte comme une absence de renseignement de l'argument, ne filtrant pas les valeurs vides. (#215)
- Il n'est pas possible dans l'état actuel de modifier le comportement de la recherche pour autoriser une valeur chaîne vide ou null comme critère de filtrage. (#215)
- L'équipe Hub'Eau étudie la possibilité de retourner une valeur générique pour les champs non renseignés afin de permettre leur filtrage ultérieur. (#215)
- Le nombre total de stations dans l'API Hydrobiologie est d'environ 20560, dépassant le seuil de résultats pour une requête sans critère. (#215)
- Le champ 'date_prelevement' de l'API Hydrobiologie a un format de date inconsistent selon le format de sortie demandé (JSON ou GeoJSON). (#247)
- Pour l'endpoint '/hydrobio/taxons', 'date_prelevement' est au format ISO 8601 ('YYYY-MM-DDTHH:MM:SSZ') en JSON et en timestamp Unix millisecondes en GeoJSON. (#247)
- Pour l'endpoint '/hydrobio/indices', 'date_prelevement' est au format ISO 8601 ('YYYY-MM-DDTHH:MM:SSZ') en JSON et au format 'YYYY-MM-DD' en GeoJSON. (#247)

## Informations métier

- L'endpoint `/code_espece_poisson` répertorie 195 espèces de poissons. (#33)
- Les codes OFB sont utilisés par l'API Hub'Eau "Poisson" pour identifier les espèces. (#33)
- La future API Hub'Eau "Hydrobiologie" diffusera des données sur les poissons, les macroinvertébrés, les diatomées et les macrophytes. (#33)
- Naïades V0 contient des données hydrobiologiques (hors poisson) qui ne sont pas encore toutes présentes dans Naïades V1. (#45)
- L'intégration des données manquantes dans Naïades V1 dépend de la transmission par les Agences de l'Eau LB et RM. (#45)
- Des données brutes au format CSV et XLS existent dans Naïades V0. (#45)
- Le code SANDRE correct pour le support des diatomées est 10. (#46)
- Le code SANDRE 13 ne correspond pas aux diatomées pour les indices biologiques. (#46)
- L'indice biologique 'IBG Normalisé' (code indice : 1000) est un indice d'invertébrés. (#46)
- Il existe des problèmes de qualité des données dans Naïades où des indices sont affectés à un mauvais code support (ex: indices invertébrés affectés au support diatomées). (#46)
- Les codes d'indices 5856, 1022, 1080, 8059, 8060, 1692, 6335 sont des indices spécifiques aux diatomées. (#46)
- L'API Hydrobiologie fournit des données sur les indices hydrobiologiques. (#81)
- Les données d'indices hydrobiologiques incluent des informations sur les dates de prélèvement. (#81)
- Le code SANDRE support `13` pour les indices biologiques correspond aux macroinvertébrés. (#97)
- Le code SANDRE support `10` pour les indices biologiques correspond aux diatomées. (#97)
- Les exports Naïades hydrobiologie contiennent des données environnementales et des informations sur les opérations. (#98)
- Ces informations sont indispensables pour les scripts du SEEE, notamment pour le calcul de l'indice I2M2 à partir des listes faunistiques de l'IBG-DCE. (#98)
- Le champ `RefOperationPrelBio` (désormais `code_operation`) est crucial pour différencier les résultats si plusieurs opérations de prélèvement biologique ont été effectuées le même jour sur la même station. (#99)
- Le champ `RefOperationPrelBio` est la référence de l’opération de prélèvement dans la banque de référence Naïades. (#99)
- Ce champ permet d’effectuer une jointure avec les fichiers `Operations ResultatsBiologiques` et `ListesFauneFlore` des exports Naïades. (#99)
- L'API Hydrobiologie permet d'extraire des indices hydrobiologiques en filtrant par département (`code_departement`) et par type d'indice (`code_indice`). (#107)
- Les données disponibles via l'API Hydrobiologie incluent des champs comme `code_indice`, `code_station_hydrobio`, `date_prelevement`, `resultat_indice`, `unite_indice`, `code_departement`, `code_support`, `libelle_support`, `code_qualification`. (#107)
- L'API `hydrobio/taxons` permet d'accéder aux données de taxons hydrobiologiques. (#109)
- Les données hydrobiologiques peuvent être filtrées par `code_station_hydrobio`. (#109)
- Les champs manquants sont nécessaires et obligatoires pour créer une opération de prélèvement biologique à laquelle des résultats biologiques doivent être rattachés. (#123)
- Les informations clés pour créer une opération de prélèvement biologique ne sont pas toutes disponibles via les APIs "indices" et "taxons" de l'API Hydrobiologie, même avec l'ajout du champ "_code_operation_prelevement_". (#123)
- Les données d'opérations de prélèvement sont disponibles via des exports CSV depuis Naïades. (#123)
- Certaines données d'hydrobiologie diffusées par l'API proviennent de la base d'origine "Aspe". (#129)
- La duplication des données dans l'API pouvait entraîner des totaux d'effectifs incorrects pour les taxons (ex: 13 anguilles affichées comme 26). (#129)
- Le `code_appel_taxon` 2038 correspond aux anguilles. (#129)
- Le service web ADES (Accès aux Données sur les Eaux Souterraines) offre une fonctionnalité de synchronisation des points d'eau et mesures basée sur une date de mise à jour. (#131)
- La synchronisation par date de mise à jour est essentielle pour récupérer uniquement les différences et les corrections apportées aux données sans télécharger l'intégralité du jeu de données. (#131)
- Les données environnementales peuvent être corrigées après leur première publication ('date de production'), nécessitant un mécanisme de mise à jour efficace. (#131)
- Une pratique courante pour contourner l'absence de filtre est de requêter toutes les données d'une période (ex: dernière année) mensuellement, ce qui est sous-optimal. (#131)
- Environ 45 stations sur 20560 dans l'API Hydrobiologie ont des champs géographiques (code_region, code_departement, code_commune, code_cours_eau, code_masse_eau) non renseignés. (#215)
- Parmi les stations avec des champs géographiques non renseignés, certaines sont géolocalisées en France et d'autres à l'étranger (Suisse, Espagne). (#215)
- Certaines stations avec des champs géographiques non renseignés sont positionnées sur des communes ayant disparu suite à une fusion. (#215)
- Boucler sur les codes région ne permet pas de récupérer toutes les stations, car celles avec des codes région vides sont omises (environ 45 stations manquantes). (#215)

## Problèmes connus

- Même avec `code_support=10`, environ 10% des résultats peuvent être des indices d'invertébrés en raison d'erreurs dans les données sources. (#46)
- Les erreurs de données proviennent des sources (Naïades) et ne peuvent pas être corrigées directement par Hub'Eau. (#46)
- L'API Hydrobiologie en version vbeta renvoyait une erreur 'Internal server error' lors de l'utilisation des paramètres `date_debut_prelevement` ou `date_fin_prelevement` sur l'endpoint `/indices`. (#81)
- Les dates de prélèvement retournées par l'API Hydrobiologie (vbeta) sans filtre de date étaient au format date/heure au lieu de date seule, ce qui était potentiellement lié au bug de filtrage. (#81)
- Le bug a été corrigé lors du passage de l'API Hydrobiologie de la version `vbeta` à la version `v1`. (#81)
- L'API Hydrobiologie peut retourner des erreurs 500 (erreur interne du serveur). (#106)
- L'API Hydrobiologie peut retourner des erreurs 406 (Not Acceptable), notamment lors de requêtes pour des formats spécifiques comme CSV. (#106)
- Des problèmes d'inaccessibilité du serveur de l'API Hydrobiologie sont récurrents, mais la situation se rétablit généralement après quelques minutes ou heures. (#106)
- L'API Hub'Eau Hydrobiologie en version `vbeta` rencontrait un bug (erreur 500) lors de l'utilisation du paramètre `date_debut_prelevement`. (#107)
- Le bug lié au paramètre `date_debut_prelevement` a été corrigé dans la version `v1` de l'API Hydrobiologie. (#107)

## Tips d'utilisation

- Le code à utiliser dans l'endpoint `/poissons` est le code OFB (champ "code") et non le code SANDRE (champ "code_taxon"). (#33)
- Pour obtenir uniquement les indices de diatomées, il est recommandé de filtrer par les codes d'indices spécifiques (ex: `code_indice=5856,1022,1080,8059,8060,1692,6335`). (#46)

---

## Issues sources

- **#33** Récupération données poisson depuis son nom — L'API Hub'Eau "Poisson" ne permet pas de rechercher par nom d'espèce mais uniquement par code OFB, nécessitant l'utilisation de l'endpoint `/code_espece_poisson` ou de l'API SANDRE pour la correspondance nom-code, en attendant la future API Hydrobiologie. `[résolu]`
- **#45** [API HYDROBIOLOGIE]_données Naïades V0 — L'API Hub'Eau Hydrobiologie n'intègre que les données de Naïades V1, expliquant l'absence de certaines données de Naïades V0 qui seront progressivement intégrées à Naïades V1 puis à Hub'Eau. `[information]`
- **#46** [API HYDROBIOLOGIE]_requête non fonctionnelle — L'API Hydrobiologie présente des erreurs de données pour les indices de diatomées (code support 10), mélangeant des indices d'invertébrés, nécessitant un filtrage par codes d'indices spécifiques pour obtenir des résultats corrects. `[résolu]`
- **#81** [API Hydrobiologie] Erreur lorsqu'une date de fin ou un de début de prélèvement est indiquée — L'API Hydrobiologie en version vbeta rencontrait un bug 'Internal server error' lors de l'utilisation des filtres de date de prélèvement, corrigé avec le passage à la version v1 de l'API. `[résolu]`
- **#97** [hydrobio] coquille dans un des exemples — Cette issue corrige une erreur dans la documentation de l'API Hydrobiologie de Hub'Eau, précisant que le code SANDRE support 13 est pour les macroinvertébrés et le code 10 pour les diatomées. `[résolu]`
- **#98** [API-Hydrobiologie] Export des conditions environnementales et des informations sur les opérations — L'API Hydrobiologie de Hub'Eau contient les données environnementales et les informations sur les opérations (nécessaires au calcul de l'I2M2) au sein de la requête 'taxons', bien qu'une requête dédiée 'Opérations' serait plus logique. `[information]`
- **#99** [API-Hydrobiologie] Ajouter la référence de l'opération aux exports — L'API Hydrobiologie a été mise à jour pour inclure les champs `code_banque_reference` et `code_operation` dans les endpoints `indices` et `taxons`, améliorant la différenciation des opérations et la capacité de jointure des données. `[résolu]`
- **#106** [API Hydrobiologie] Erreurs 500 / 406 dans les réponses de l'API — L'API Hydrobiologie a rencontré des erreurs 500 et 406 récurrentes, signalant des problèmes d'inaccessibilité temporaires du serveur. `[résolu]`
- **#107** [API Hydrobiologie] pb de date dans l'url — L'API Hub'Eau Hydrobiologie `vbeta` présentait un bug empêchant le filtrage par date de prélèvement, corrigé lors de la migration vers la version `v1`. `[résolu]`
- **#109** [API hydrobiologie] profondeur d'accès aux résultats — La limite de profondeur d'accès aux résultats de l'API Hydrobiologie a été réduite de 20 000 à 10 000 enregistrements maximum pour éviter les timeouts, et la documentation sera mise à jour. `[résolu]`
- **#123** [API Hydrobiologie] ajout de champs présents sous Naïades — L'API Hydrobiologie a ajouté le champ "_code_operation_prelevement_" aux endpoints "indices" et "taxons", mais un endpoint dédié aux opérations de prélèvement ou l'ajout de champs supplémentaires est nécessaire pour permettre la création complète d'opérations de prélèvement biologique, une évolution envisagée mais non planifiée pour 2025-2026. `[en_cours]`
- **#129** [API Hydrobiologie] observations dupliquées pour endpoint « taxons » — L'API Hydrobiologie a corrigé un bug de duplication des observations de taxons et des indices, causé par les conditions environnementales associées aux prélèvements, ce qui a réduit le volume total de données diffusées. `[résolu]`
- **#131** [API Piézométrie] Synchronisation des données — Les APIs Hub'Eau (Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) manquent d'un filtre par date de mise à jour pour une synchronisation efficace des données, une fonctionnalité prévue pour l'API Hydrométrie mais pas à court terme pour la Piézométrie. `[information]`
- **#215** [API Hydrobiologie] champs code_region vides — L'API Hydrobiologie ne permet pas de filtrer les stations avec des champs géographiques vides, ce qui entraîne une perte de données lors des requêtes par région et nécessite une évolution de l'API pour gérer ces cas. `[en_cours]`
- **#247** [API Hydrobiologie] Inconsistence du format de date_prelevement selon le format json/geojson — L'API Hydrobiologie de Hub'Eau présente des formats de date_prelevement inconsistants entre les formats de sortie JSON et GeoJSON pour les endpoints taxons et indices. `[en_cours]`
