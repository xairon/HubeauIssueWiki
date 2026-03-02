# Qualité des cours d'eau

> 31 issues analysées

## Guide

### Comportement actuel

L'API Hub'Eau "Qualité des cours d'eau" diffuse des données de physico-chimie (résultats PC) provenant de la banque nationale Naïades, avec un léger décalage de mise à jour (#32, #146, #154, #169, #199). Les endpoints `/v2/qualite_rivieres/analyse_pc` et `/v2/qualite_rivieres/operation_pc` donnent accès aux analyses et opérations de prélèvement, filtrables par `code_station`, `date_debut_prelevement`, `date_fin_prelevement` (#44, #103, #134, #268). L'endpoint `/v2/qualite_rivieres/condition_environnementale_pc` fournit des conditions environnementales associées aux prélèvements, avec des résultats cohérents en v2 (#24, #199). La v2 inclut les champs `code_prelevement` (numérique ou alphanumérique) et `profondeur` (`operation_pc`) essentiels pour l'identification et la jointure des données, notamment pour les plans d'eau (#56, #250, #254). Les filtres `date_debut_maj` et `date_fin_maj` s'appliquent sur `date_maj_analyse` (#135). La pagination est gérée par `page` et `size`, l'attribut `count` indiquant le total des résultats, et ce comportement est identique pour les formats CSV et JSON (#104, #152). Les noms de champs sont en `snake_case` en JSON, et le paramètre `fields` fonctionne avec cette casse (#246). Le champ `libelle_station` est disponible pour le nom des stations (#166). Un nouveau endpoint `_parametres` est prévu pour optimiser la recherche de métadonnées sur les APIs de qualité, en commençant par celle des cours d'eau (#204). Le statut "hors service" d'une station est déduit de la présence d'une date de fin renseignée (#108).

### Pièges à éviter

L'API impose une limite stricte de 20 000 enregistrements cumulés par requête (`page * size`), déclenchant une erreur 'ValidatePageDepth' pour les volumes plus importants (#23, #152, #200). Par défaut, Naïades limite les recherches aux 3 dernières années, ce qui peut masquer des données plus anciennes (#32). Il n'existe pas de filtre par date de mise à jour des données, obligeant à recharger des jeux de données entiers pour rester à jour (#131). Des stations peuvent exister dans le référentiel mais ne pas avoir de données de qualité des cours d'eau dans cette API spécifique (#105). L'API ne permet pas de sélection directe par critère générique (ex: 'PFAS') et ne fournit pas d'agrégations complexes ou journalières à l'échelle départementale (#217, #220). Des incidents techniques sur les systèmes sources (Naïades) peuvent entraîner des baisses temporaires de volume de données (#158). L'API peut être fortement sollicitée, impactant ses temps de réponse (#198). L'endpoint `operation_pc` peut retourner une erreur "Internal server error" sans `field_errors` spécifiques (#268). Le filtrage par `code_prelevement=RAS` sur `operation_pc` peut être incomplet en raison de la réutilisation de codes dans les données sources, sans correction possible par Hub'Eau (#252). Enfin, des inconsistances de nommage (`snake_case` vs `camelCase`) et des problèmes avec le paramètre `fields` existent entre les formats JSON et GeoJSON, et pour l'export CSV, les espaces après les virgules dans le paramètre `fields` doivent être supprimés pour que l'URL fonctionne (#246, #199).

### Bonnes pratiques

Pour gérer les volumes importants, segmentez vos requêtes en utilisant des filtres temporels (`date_debut_prelevement`, `date_fin_prelevement`) ou géographiques pour rester sous la limite des 20 000 enregistrements (#23, #152, #200). Utilisez un petit `size` (ex: `size=1`) et l'attribut `count` pour estimer le volume total de données avant de les télécharger (#104). Pour accéder à des données historiques au-delà des 3 dernières années par défaut, spécifiez une `date_debut_prelevement` antérieure (ex: `01-01-1970`) (#32). Pour connaître les dates de prélèvement disponibles pour une station, interrogez l'API avec `fields=date_prelevement` et extrayez les valeurs distinctes (#152). En cas d'erreur "Internal server error" sur l'endpoint `operation_pc`, essayez d'ajouter explicitement le paramètre `fields` à votre requête (#268). Pour l'initialisation de bases locales avec un historique important, les exports massifs du site Naïades (https://naiades.eaufrance.fr/france-entiere#/) sont plus adaptés que l'API (#200). Consultez les schémas de données détaillés dans la section `Models` de chaque page d'accueil d'API Hub'Eau pour comprendre les variables (#156). Pour des questions méthodologiques ou des informations détaillées sur les paramètres analytiques (ex: PFAS), contactez directement les équipes expertes de Naïades, Sandre ou Aquaref (#32, #217, #220).

### Contexte métier

L'API Hub'Eau "Qualité des cours d'eau" s'appuie sur la plateforme nationale Naïades, qui agrège les données de qualité des eaux superficielles (cours d'eau et plans d'eau) collectées par les Agences de l'eau, et le Sandre est le référentiel des stations (#24, #32, #56, #154, #158, #169). L'API fournit des données brutes ou semi-brutes d'analyses physico-chimiques, d'opérations de prélèvement et de conditions environnementales (#24, #44, #56, #156, #199, #220). Pour les plans d'eau, le champ `profondeur` est crucial car plusieurs prélèvements peuvent avoir lieu à différentes profondeurs le même jour (#56, #254). Les champs `code_banque_reference` et `code_prelevement` sont essentiels pour l'identification unique et la jointure des opérations et analyses (#56). La `date_maj_analyse` indique la date d'importation dans Naïades, mais sa fréquence de mise à jour varie par station et agence, et ne reflète pas toujours une modification individuelle de l'analyse (#135, #152). Le référentiel analytique (paramètres, groupes de paramètres) est géré par le Sandre et Aquaref (#217).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Température des cours d'eau inclut un paramètre 'en_service' pour les stations. (#108)
- Il est proposé d'ajouter un paramètre 'en_service' aux stations des autres APIs Hub'Eau. (#108)
- Actuellement, le statut 'hors service' d'une station est déduit de la présence d'une date de fin renseignée. (#108)
- Le concept de station 'en service' est une information clé pour l'utilisation des données hydrologiques. (#108)
- Les APIs Hub'Eau (notamment Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) ne disposent pas de paramètre de filtre par date de mise à jour des données. (#131)
- L'absence de filtre par date de mise à jour oblige les utilisateurs à charger l'intégralité des données pour rester à jour. (#131)
- L'API Hydrométrie inclut une 'date de production' dans ses résultats, mais ce paramètre n'est pas utilisable comme filtre de requête. (#131)
- L'ajout d'un filtre par date de mise à jour n'est pas prévu à court terme pour l'API Piézométrie. (#131)
- L'ajout d'un filtre par date de mise à jour est une évolution identifiée pour l'API Hydrométrie. (#131)
- Le service web ADES (Accès aux Données sur les Eaux Souterraines) offre une fonctionnalité de synchronisation des points d'eau et mesures basée sur une date de mise à jour. (#131)
- La synchronisation par date de mise à jour est essentielle pour récupérer uniquement les différences et les corrections apportées aux données sans télécharger l'intégralité du jeu de données. (#131)
- Les données environnementales peuvent être corrigées après leur première publication ('date de production'), nécessitant un mécanisme de mise à jour efficace. (#131)
- Une pratique courante pour contourner l'absence de filtre est de requêter toutes les données d'une période (ex: dernière année) mensuellement, ce qui est sous-optimal. (#131)
- La limite de 20 000 enregistrements s'applique à la taille totale du résultat retourné par une interrogation, toutes pages cumulées, et non à la taille d'une page individuelle. (#200)
- Pour récupérer de grands volumes de données (au-delà de 20 000 enregistrements), il est nécessaire de segmenter les interrogations en utilisant des critères géographiques, temporels ou autres. (#200)
- Pour l'initialisation d'une base locale avec un historique important, le site Naïades (https://naiades.eaufrance.fr/france-entiere#/) propose des exports de données plus adaptés. (#200)
- Les APIs Hub'Eau sont conçues pour collecter les données postérieures à un import initial depuis Naïades. (#200)
- L'API Qualité des nappes peut nécessiter de nombreuses requêtes pour obtenir des métadonnées (années, producteurs, paramètres) par station, pouvant entraîner des résultats vides. (#204)
- Il existe une limitation à 20 000 résultats par requête sur l'API Qualité des nappes, nécessitant le fractionnement des requêtes. (#204)
- Un nouveau endpoint "_parametres" est prévu pour les APIs de qualité (rivières, nappes, eau potable) afin d'optimiser les interrogations. (#204)
- Le endpoint "_parametres" sera d'abord ajouté à l'API Qualité des cours d'eau. (#204)
- Les remarques de l'utilisateur concernant les métadonnées (années, producteurs, paramètres) seront prises en compte pour l'implémentation du endpoint "_parametres" sur l'API Qualité des nappes. (#204)
- Les utilisateurs de l'API Qualité des nappes ont besoin de connaître les années de données disponibles, les producteurs d'analyses et les paramètres analysés pour chaque station de mesure afin d'optimiser leurs requêtes. (#204)
- Pour l'API Qualité des cours d'eau, les noms de champs sont en snake_case (ex: code_operation) en format JSON. (#246)
- Pour l'API Qualité des cours d'eau, les noms de champs sont en camelCase (ex: codeOperation) en format GeoJSON, créant une inconsistance avec le format JSON. (#246)
- L'argument 'fields' ne fonctionne pas correctement avec le format GeoJSON: utiliser 'fields=code_operation' (snake_case) ne retourne aucune propriété. (#246)
- L'argument 'fields' ne fonctionne pas correctement avec le format GeoJSON: utiliser 'fields=codeOperation' (camelCase) ne filtre pas les champs et retourne toutes les propriétés. (#246)
- L'argument 'fields' fonctionne comme attendu avec le format JSON en utilisant le snake_case (ex: fields=code_operation). (#246)
- L'argument 'fields' ne filtre pas les champs avec le format JSON si le camelCase est utilisé (ex: fields=codeOperation). (#246)
- L'endpoint `/v2/qualite_riviere/operation_pc` peut retourner un nombre incomplet d'enregistrements lors d'une recherche filtrée uniquement par `code_prelevement=RAS`. (#252)
- Une recherche combinant `code_prelevement=RAS` et `code_station` peut révéler des enregistrements supplémentaires non trouvés avec le seul filtre `code_prelevement=RAS`. (#252)
- Le problème est lié au processus de regroupement des campagnes à partir des données unitaires lors de l'exposition via l'API. (#252)
- Hub'Eau ne peut pas intervenir pour corriger ce comportement, car il est lié à la réutilisation de codes identiques dans les données sources. (#252)
- Le champ `code_prelevement` du dataset `operation_pc` peut contenir la valeur 'RAS'. (#252)
- La valeur 'RAS' pour `code_prelevement` est également présente dans les données Naïades (CdPrelevement). (#252)
- La cause du problème est la réutilisation de codes identiques dans les données sources, ce qui affecte le regroupement des campagnes. (#252)
- L'OFB a été informé de ce problème et a communiqué avec les producteurs de données concernés. (#252)
- L'endpoint `operation_pc` de l'API `qualite_rivieres` peut retourner une erreur "Internal server error" sans `field_errors` spécifiques. (#268)
- Un contournement pour l'erreur de l'endpoint `operation_pc` consiste à ajouter le paramètre `fields` à la requête. (#268)
- L'endpoint `operation_pc` est utilisé pour récupérer des données de prélèvements. (#268)
- L'endpoint `operation_pc` de l'API `Qualité des cours d'eau` fournit des données sur les prélèvements (échantillons) effectués dans les cours d'eau. (#268)
- Les données de prélèvements peuvent être filtrées par `code_station`, `date_debut_prelevement`, `date_fin_prelevement`. (#268)
- Des champs comme `code_station`, `libelle_station`, `code_support`, `code_methode`, `date_prelevement`, `code_prelevement` sont disponibles pour les prélèvements. (#268)

### Historique des problèmes résolus

- ~~L'attribut 'next' de la pagination est généré avec une URL même lorsque la page de données est vide, contrairement à la documentation qui indique 'null'. (#15)~~
- ~~Ce comportement est lié à des inconsistances dans le 'count' total des résultats renvoyés par l'API. (#15)~~
- ~~Lorsque le 'count' change sur la dernière page, l'API peut générer un 'next' infini et un 'last' nul. (#15)~~
- ~~Contournement possible : vérifier que `page * size` ne dépasse pas le 'count' obtenu lors du premier appel. (#15)~~
- ~~Contournement possible : utiliser de grandes valeurs pour 'size' (5000-20000) pour réduire le nombre de pages et l'impact des inconsistances de 'count'. (#15)~~
- ~~L'utilisation de très grandes valeurs pour 'size' peut potentiellement entraîner des timeouts. (#15)~~
- ~~L'API Qualité des cours d'eau impose une limite de 20000 résultats maximum par requête (produit de `page` * `size`). (#23)~~
- ~~Pour récupérer un nombre total de résultats supérieur à 20000 pour une même station, il est nécessaire de scinder la requête en utilisant des filtres temporels, tels que `date_debut_prelevement` et `date_fin_prelevement`. (#23)~~
- ~~Certaines stations de mesure de la qualité des cours d'eau peuvent comporter un très grand nombre d'analyses (plusieurs dizaines de milliers). (#23)~~
- ~~L'API v1 `qualite_rivieres/condition_environnementale_pc` pouvait retourner des résultats multiples et identiques pour un même paramètre (ex: code_parametre "1418" répété plus de 1000 fois). (#24)~~
- ~~L'API v1 `qualite_rivieres/condition_environnementale_pc` présentait une incohérence entre le `count` annoncé (1274) et le nombre d'items dans `data` (26999) pour une même requête. (#24)~~
- ~~Le problème a été résolu avec la mise en place de l'API v2 (disponible depuis juillet 2022). (#24)~~
- ~~L'API v2 `qualite_rivieres/condition_environnementale_pc` renvoie un nombre de résultats cohérent (ex: 27 résultats pour la requête problématique de la v1). (#24)~~
- ~~La résolution du problème a impliqué une refonte des procédures d'alimentation et d'indexation des données physico-chimiques et températures de Naiades. (#24)~~
- ~~L'endpoint `condition_environnementale_pc` concerne les conditions environnementales. (#24)~~
- ~~Le nombre de paramètres mesurés pour les conditions environnementales est rarement supérieur à 30. (#24)~~
- ~~Les données physico-chimiques et de températures de l'API Hub'Eau proviennent de Naiades. (#24)~~
- ~~L'API Hub'Eau Qualité des cours d'eau diffuse les données présentes dans Naïades, avec un léger décalage de mise à jour. (#32)~~
- ~~Par défaut, Naïades (source des données pour Hub'Eau) fixe les recherches de données sur les 3 dernières années de prélèvement ou mesure. (#32)~~
- ~~Il est possible de rechercher des données plus anciennes dans Naïades en spécifiant une date de début antérieure (ex: 01-01-1970). (#32)~~
- ~~Certaines stations référencées dans le Sandre peuvent ne pas avoir de données de physicochimie diffusées par Naïades. (#32)~~
- ~~Des stations peuvent avoir des données anciennes dans Naïades (ex: 1994-1996) qui ne sont pas visibles avec la recherche par défaut des 3 dernières années. (#32)~~
- ~~Le Sandre est le référentiel des stations, tandis que Naïades est la plateforme de diffusion des données de mesure de physicochimie. (#32)~~
- ~~Pour des informations complémentaires sur les données disponibles pour une station, il est possible de contacter l'agence de l'eau concernée. (#32)~~
- ~~Le formulaire de contact de Naïades est disponible pour poser des questions spécifiques à cette plateforme. (#32)~~
- ~~L'API Qualité des cours d'eau a connu une indisponibilité temporaire de sa page de description et de test. (#44)~~
- ~~L'API Qualité des cours d'eau ne renvoyait pas de données pour des requêtes sur une station spécifique (ex: 04204300) en limitant à un paramètre ou pour l'historique. (#44)~~
- ~~Le problème technique a été résolu. (#44)~~
- ~~L'API Qualité des cours d'eau fournit des 'résultats PC' (Paramètres de Caractérisation, probablement physico-chimiques) pour les cours d'eau. (#44)~~
- ~~Les données de l'API Qualité des cours d'eau sont structurées par station (ex: 04204300) et permettent des requêtes historiques ou par paramètre. (#44)~~
- ~~L'API Qualité des cours d'eau endpoint operation_pc renvoyait des données incomplètes pour les plans d'eau, agrégeant abusivement les opérations par station et date de prélèvement. (#56)~~
- ~~Avant la version 2, les champs heure_debut (dans operation_pc), code_support, code_zone_verticale_prospectee et profondeur (dans analyse_pc) étaient manquants, rendant difficile l'association correcte des analyses aux opérations. (#56)~~
- ~~Il existait un décalage de synchronisation (environ une semaine) entre les données de NAIADES et l'API Hub'Eau, pouvant entraîner des écarts. Un index commun était prévu pour 2021 pour résoudre cela. (#56)~~
- ~~La version 2 de l'API Qualité des cours d'eau introduit les champs code_banque_reference et code_prelevement qui permettent de faire la jointure entre opérations, analyses et conditions environnementales. (#56)~~
- ~~La version 2 de l'API Qualité des cours d'eau endpoint operation_pc inclut désormais le champ profondeur. (#56)~~
- ~~Les données de qualité physico-chimique pour les plans d'eau sont disponibles dans NAIADES et sont intégrées à Hub'Eau. (#56)~~
- ~~Pour les plans d'eau (lacs), plusieurs opérations de prélèvement peuvent avoir lieu le même jour sur une même station, à différentes profondeurs et/ou niveaux d'intégration. (#56)~~
- ~~Les champs code_banque_reference et code_prelevement sont essentiels pour l'identification unique et la jointure des opérations de prélèvement et des analyses, notamment pour les plans d'eau. (#56)~~
- ~~La profondeur de prélèvement est une information clé pour l'exploitation des données de qualité sur les plans d'eau. (#56)~~
- ~~L'interface Swagger de l'API Qualité des cours d'eau ajoute des caractères "%22" (guillemets encodés) autour du paramètre "code_station" dans l'URL générée. (#103)~~
- ~~Ces caractères "%22" doivent être supprimés manuellement de l'URL pour que la requête renvoie des données. (#103)~~
- ~~Dans l'interface Swagger, le paramètre "code_station" doit être mis entre guillemets pour activer le bouton "Execute". (#103)~~
- ~~Ce comportement est un bug de l'interface Swagger, prévu pour être corrigé. (#103)~~
- ~~Le paramètre "code_station" est utilisé pour filtrer les données de qualité physico-chimique des cours d'eau par station (ex: "04102400"). (#103)~~
- ~~L'endpoint `/qualite_rivieres/operation_pc` permet d'accéder aux données d'opérations physico-chimiques. (#103)~~
- ~~L'attribut `count` de la réponse de l'API indique le nombre total de données disponibles pour une requête. (#104)~~
- ~~Il est possible d'obtenir le nombre total de données sans les télécharger en utilisant un paramètre `size` (ex: `size=1` ou `size=20`) et en lisant l'attribut `count` de la réponse. (#104)~~
- ~~L'API Qualité des cours d'eau (`qualite_rivieres/analyse_pc`) contenait plus de 141 millions d'analyses physico-chimiques disponibles au 1er mars 2022. (#104)~~
- ~~L'API 'Qualité des cours d'eau' peut retourner un résultat vide pour des stations qui n'ont pas de données de qualité des cours d'eau, même si ces stations existent et ont des données pour d'autres types de mesures. (#105)~~
- ~~Les stations avec les codes 06188870, 06188880, 06188890, 06188895, 06188900, 06188910, 06188930, 06187450, 06188860, 06188920, 06188925, 06188850 ne remontent pas de données via l'API 'Qualité des cours d'eau'. (#105)~~
- ~~Une station de mesure peut exister et avoir des données pour certains types de mesures (ex: hydrobiologie) mais pas pour d'autres (ex: qualité des cours d'eau). (#105)~~
- ~~Les stations mentionnées dans l'issue, situées autour du bassin de Thau (34), sont des exemples de stations ayant des données hydrobiologiques mais pas de données de qualité des cours d'eau. (#105)~~
- ~~L'endpoint `/v2/qualite_rivieres/analyse_pc` de l'API Qualité des cours d'eau peut retourner une erreur HTTP 500 (Internal Server Error). (#134)~~
- ~~Le corps de réponse d'une erreur 500 de cette API est `{"code": "Internal server error", "field_errors": null, "message": ""}`. (#134)~~
- ~~L'endpoint `/v2/qualite_rivieres/analyse_pc` accepte le paramètre `code_station`. (#134)~~
- ~~Des anomalies de fonctionnement temporaires peuvent affecter l'API Qualité des cours d'eau, entraînant des erreurs 500. (#134)~~
- ~~L'endpoint `/v2/qualite_rivieres/analyse_pc` permet d'accéder aux données d'analyses physicochimiques des cours d'eau. (#134)~~
- ~~Les données d'analyses physicochimiques peuvent être filtrées par `code_station` (ex: `06188930`). (#134)~~
- ~~Les filtres `date_debut_maj` et `date_fin_maj` de l'API Qualité des cours d'eau s'appliquent sur le champ `date_maj_analyse`. (#135)~~
- ~~Le filtre `date_debut_maj` permet de récupérer les analyses dont la `date_maj_analyse` est égale ou postérieure à la date spécifiée. (#135)~~
- ~~Le filtre `date_fin_maj` permet de récupérer les analyses dont la `date_maj_analyse` est égale ou antérieure à la date spécifiée. (#135)~~
- ~~Le champ `date_maj_analyse` correspond à la date d'importation de l'analyse dans la base de données Naïades. (#135)~~
- ~~La base Naïades est alimentée par des opérations d'annulation et de remplacement de tout ou partie des données collectées par les Agences de l'eau ou Offices de l'eau. (#135)~~
- ~~Pour la majorité des agences, la `date_maj_analyse` est la même pour toutes les analyses importées car elles remplacent l'intégralité de leurs données à chaque alimentation. (#135)~~
- ~~L'agence Rhône-Méditerranée-Corse (et bientôt Seine-Normandie et Loire-Bretagne) alimente Naïades avec des données modifiées tous les 15 jours, ce qui entraîne des `date_maj_analyse` différentes pour les analyses qu'elle collecte. (#135)~~
- ~~L'API Hub'Eau Qualité des cours d'eau diffuse des données provenant de la banque nationale Naïades. (#146)~~
- ~~Les analyses de physicochimie collectées par l’agence de l’eau Loire-Bretagne étaient temporairement absentes de la banque Naïades. (#146)~~
- ~~L'indisponibilité des données de physicochimie du bassin Loire-Bretagne a duré environ deux semaines. (#146)~~
- ~~La banque nationale Naïades est désormais connectée à la banque de référence de l’Agence de l’eau Loire-Bretagne. (#146)~~
- ~~Les analyses physico-chimiques du bassin Loire-Bretagne, diffusées par l’API Hub'Eau Qualité des cours d'eau, sont mises à jour toutes les deux semaines. (#146)~~
- ~~L'API `/v2/qualite_rivieres/analyse_pc` impose une limite de profondeur de pagination, déclenchant une erreur 'ValidatePageDepth' lorsque le produit `size * page` dépasse environ 20000 enregistrements. (#152)~~
- ~~Pour les requêtes générant plus de 20000 enregistrements, il est nécessaire d'affiner la recherche avec des paramètres supplémentaires (ex: date, paramètre) pour éviter la limite de profondeur de pagination. (#152)~~
- ~~Le comportement de pagination et la limite de profondeur sont identiques pour les formats CSV et JSON. (#152)~~
- ~~Pour obtenir les dates de prélèvement disponibles pour une station, il faut interroger l'API en spécifiant `fields=date_prelevement` et extraire les valeurs distinctes du résultat. (#152)~~
- ~~Le problème de duplication de données lors de la pagination, initialement signalé, n'a pas été reproduit par l'équipe Hub'Eau. (#152)~~
- ~~La fréquence de mise à jour des données de qualité physico-chimique des cours d'eau n'est pas quotidienne et varie d'une station à l'autre. (#152)~~
- ~~L'API ne fournit pas directement une liste des dates pour lesquelles des analyses existent pour une station donnée. (#152)~~
- ~~L'API Hub'Eau qualite_rivieres/analyse_pc.csv reflète directement la disponibilité des données dans sa base source, Naïades. (#154)~~
- ~~L'API Hub'Eau pour la qualité physico-chimique des cours d'eau (analyse_pc) utilise la base de données Naïades comme source. (#154)~~
- ~~Une absence de données dans l'API Hub'Eau peut être due à une absence temporaire ou permanente dans la base source Naïades. (#154)~~
- ~~Un retard d'alimentation de la base Naïades a entraîné une absence de données de physico-chimie à partir du 2023-08-05, qui a été résolue ultérieurement. (#154)~~
- ~~Les schémas des données (descriptifs des variables) pour les APIs Hub'Eau sont disponibles dans la section `Models` en bas de chaque page d'accueil d'une API. (#156)~~
- ~~Dans l'API Qualité des cours d'eau, pour l'endpoint `condition_environnementale_pc`, l'attribut `resultat` correspond au 'Résultat de la mesure du paramètre environnemental (résultat direct si le paramètre est quantitatif ou code si le paramètre est qualitatif)'. (#156)~~
- ~~L'API Qualité des cours d'eau peut présenter des baisses de volume de données dues à des incidents techniques sur les systèmes sources (ex: remontée des données de l'Agence de l'eau Loire-Bretagne vers Naïades). (#158)~~
- ~~Les données de certaines stations peuvent ne pas être récupérées en cas d'incident sur la chaîne de transmission des données sources. (#158)~~
- ~~L'incident technique sur les données sources de l'Agence de l'eau Loire-Bretagne (AELB) a été résolu. (#158)~~
- ~~Les données de prélèvements de qualité des cours d'eau pour la région Pays de la Loire (code_region=52) ont montré une chute spectaculaire pour les millésimes 2020 et 2021. (#158)~~
- ~~La plateforme Naïades est la source des données de qualité des cours d'eau pour Hub'Eau. (#158)~~
- ~~L'Agence de l'eau Loire-Bretagne (AELB) est un fournisseur de données pour Naïades. (#158)~~
- ~~L'API qualite_rivieres/station_pc a présenté un problème d'encodage pour le champ `libelle_station`, affichant des caractères ISO8859-1 (ex: "Ã") au lieu de UTF-8. (#166)~~
- ~~L'anomalie d'encodage a été corrigée dans l'API Hub'Eau et le système source Naïades. (#166)~~
- ~~Le champ `libelle_station` de l'API Qualité des cours d'eau contient le nom de la station de mesure. (#166)~~
- ~~L'anomalie d'encodage provenait du système source Naïades, dont Hub'Eau est dépendant. (#166)~~
- ~~Plusieurs bassins (Rhône, Garonne, Loire, Seine, Réunion) et des milliers de stations ont été affectés par ce problème d'encodage. (#166)~~
- ~~Le package R `hubeau` peut être utilisé pour explorer et analyser les données des APIs Hub'Eau. (#166)~~
- ~~L'API Hub'Eau "Qualité des cours d'eau" dépend de la plateforme Naïades pour l'agrégation des données. (#169)~~
- ~~Naïades utilise un mécanisme de moissonnage différentiel basé sur des tables de logs pour aspirer les données des services web des agences de l'eau (ex: Sandre SOAP de l'AELB). (#169)~~
- ~~Une mauvaise initialisation des tables de logs chez l'Agence de l'Eau Loire-Bretagne (AELB) a empêché la diffusion de données historiques vers Naïades et donc Hub'Eau. (#169)~~
- ~~La correction a impliqué l'insertion manuelle de lignes manquantes dans la table des logs pour forcer le moissonnage différentiel des données historiques par Naïades. (#169)~~
- ~~Le service web Sandre SOAP de l'AELB a été corrigé pour assurer la diffusion des données. (#169)~~
- ~~Des données de qualité des cours d'eau du bassin Loire-Bretagne (ex: station 04670020, producteur 20003408000065) étaient absentes de Naïades et Hub'Eau. (#169)~~
- ~~Le problème a affecté environ 56 000 prélèvements et 7 millions d'analyses. (#169)~~
- ~~La période des prélèvements impactés s'étendait du 10/07/2006 au 15/06/2022. (#169)~~
- ~~Les données sources étaient disponibles via le service web Sandre de l'AELB (services-sandre.eau-loire-bretagne.fr/Monitoring_2_1.svc?wsdl). (#169)~~
- ~~L'API Qualité des cours d'eau peut retourner une erreur '502 Proxy Error'. (#198)~~
- ~~L'API Qualité des cours d'eau peut être fortement sollicitée, ce qui impacte ses temps de réponse. (#198)~~
- ~~L'export CSV de l'endpoint /v2/qualite_rivieres/condition_environnementale_pc a été corrigé et fonctionne désormais. (#199)~~
- ~~Pour l'export CSV, les espaces après les virgules dans le paramètre 'fields' doivent être supprimés pour que l'URL fonctionne correctement. (#199)~~
- ~~L'API Hub'Eau expose les données telles qu'elles figurent dans Naïades. (#199)~~
- ~~L'endpoint /v2/qualite_rivieres/condition_environnementale_pc retourne des données relatives aux conditions environnementales associées aux prélèvements, et non des analyses directes de paramètres. (#199)~~
- ~~Le paramètre 1553 correspond aux 'Hauteurs des précipitations'. (#199)~~
- ~~Le paramètre 1553 (Hauteur des précipitations) ne fait pas l'objet d'analyses directes dans Naïades pour cet endpoint, mais est valorisé uniquement dans certains cas comme condition environnementale. (#199)~~
- ~~L'API Hub'Eau ne permet pas une sélection directe des données selon un critère générique comme 'PFAS'. (#217)~~
- ~~La sélection des paramètres est possible par groupe de paramètres. (#217)~~
- ~~Si un groupe de paramètres est incomplet pour une substance spécifique, une requête complémentaire par paramètre individuel peut être nécessaire. (#217)~~
- ~~Le support Hub'Eau ne fournit pas d'informations de référence sur les paramètres PFAS spécifiques présents dans l'API ou les requêtes associées. (#217)~~
- ~~Les PFAS (substances per- et polyfluoroalkylées) sont des composés chimiques d'intérêt pour la surveillance de la qualité de l'eau. (#217)~~
- ~~La gestion du référentiel analytique (paramètres, groupes de paramètres) en France est assurée par le Sandre en collaboration avec le consortium de laboratoires Aquaref. (#217)~~
- ~~Pour obtenir des informations détaillées sur les paramètres PFAS et leurs références, il convient de contacter directement le Sandre ou Aquaref. (#217)~~
- ~~Les APIs Hub'Eau ne fournissent pas de concentrations journalières agrégées à l'échelle départementale pour des paramètres spécifiques comme le métolachlore ESA. (#220)~~
- ~~Le rôle de Hub'Eau est de donner accès aux données brutes ou semi-brutes, et non de fournir des analyses hydrologiques complexes ou des agrégations de données à l'échelle départementale. (#220)~~
- ~~L'estimation d'une concentration journalière globale pour un paramètre (ex: métolachlore ESA) sur un département entier à partir de mesures de stations multiples nécessite une méthodologie spécifique. (#220)~~
- ~~La simple moyenne des concentrations mesurées par toutes les stations un jour donné n'est pas nécessairement la méthode la plus pertinente pour estimer une concentration départementale globale. (#220)~~
- ~~Pour les questions méthodologiques concernant l'interprétation et l'agrégation des données de qualité de l'eau (eaux souterraines ou superficielles), il convient de contacter directement les équipes expertes d'Ades (eaux souterraines) ou de Naïades (eaux superficielles). (#220)~~
- ~~La route `/v2/qualite_rivieres/analyse_pc` de l'API Qualité des cours d'eau a rencontré une erreur 500 lorsque le paramètre `code_prelevement` était utilisé. (#250)~~
- ~~Le filtre par `code_prelevement` sur la route `/v2/qualite_rivieres/analyse_pc` a été rétabli et fonctionne correctement. (#250)~~
- ~~Le `code_prelevement` est un identifiant unique pour un prélèvement d'eau, utilisé pour filtrer les analyses de qualité des rivières. (#250)~~
- ~~Les `code_prelevement` peuvent être numériques (ex: `585524`) ou alphanumériques avec des tirets (ex: `20191114191340-PC-434581`). (#250)~~
- ~~Le champ `profondeur` est disponible sur le endpoint `_operation_pc` de l'API Qualité des cours d'eau pour les données de profondeur de prélèvement. (#254)~~
- ~~Le champ `code_prelevement` permet de lier les profondeurs de prélèvement (endpoint `operation_pc`) aux résultats de mesures (endpoint `analyse_pc`) dans l'API Qualité des cours d'eau. (#254)~~
- ~~L'API Qualité des cours d'eau contient également des données sur la qualité des plans d'eau. (#254)~~
- ~~La profondeur du prélèvement est une information indispensable pour l'interprétation des données de qualité des eaux, notamment pour les plans d'eau. (#254)~~
- ~~Le champ `ProfondeurPrel` dans Naïades correspond au champ `profondeur` dans l'API Hub'Eau Qualité des cours d'eau. (#254)~~

### Issues sources

- **#15** L'attribut 'next' est toujours généré même sans page suivante — L'API Hub'Eau génère un attribut 'next' non nul même sans page suivante, un comportement lié à des inconsistances de comptage, avec des contournements possibles. `[résolu]`
- **#23** [API Qualité des cours d'eau ] - Erreur lors de la récupération des analyses  — L'API Qualité des cours d'eau limite le nombre de résultats par requête à 20000, mais cette limite peut être contournée en utilisant des filtres temporels pour scinder les requêtes. `[résolu]`
- **#24** [API Qualité des cours d'eau] - [condition_environnementale_pc] multiples résultats identiques  — L'API v1 `qualite_rivieres/condition_environnementale_pc` retournait des résultats dupliqués et des incohérences de comptage, un problème résolu par la refonte des procédures d'alimentation de Naiades et la mise en œuvre de l'API v2. `[résolu]`
- **#32** Station qualité non trouvé sur l'API Qualité — L'API Hub'Eau Qualité des cours d'eau s'appuie sur Naïades, qui peut ne pas diffuser toutes les données du Sandre ou limiter les résultats aux 3 dernières années par défaut, nécessitant parfois de contacter l'agence de l'eau pour des précisions. `[résolu]`
- **#44** Plantage de l'API cours d'eau — L'API Qualité des cours d'eau a rencontré une indisponibilité temporaire empêchant la récupération de données pour des stations spécifiques et des requêtes historiques ou par paramètre, problème qui a été résolu. `[résolu]`
- **#56** [API Qualité des cours d'eau] - données operation_pc incomplètes — L'API Qualité des cours d'eau avait un bug où les opérations de prélèvement pour les plans d'eau étaient incomplètes et mal agrégées, résolu en version 2 par l'ajout de champs clés comme code_prelevement et profondeur. `[résolu]`
- **#103** [Qualité physico-chimique des cours d'eau] bug — Un bug dans l'interface Swagger de l'API Qualité des cours d'eau entraînait l'ajout de guillemets encodés (`%22`) autour du `code_station` dans l'URL, nécessitant une suppression manuelle pour obtenir des données. `[résolu]`
- **#104** [Qualité physico-chimique des cours d'eau] interrogation de la base — L'API Hub'Eau fournit le nombre total de données disponibles pour une requête via l'attribut `count` de la réponse, permettant d'anticiper la taille des téléchargements. `[résolu]`
- **#105** Non remontée des données "Qualité des cours d'eau" pour un ensemble de stations dans le 34 — Cette issue clarifie que des stations peuvent exister dans Hub'Eau mais ne pas avoir de données pour une API spécifique (ex: Qualité des cours d'eau), tout en ayant des données pour d'autres types de mesures (ex: hydrobiologie). `[résolu]`
- **#108** [API Qualité de l'eau] Paramètre de station en service — L'issue propose d'ajouter un paramètre 'en_service' aux stations des APIs Hub'Eau, à l'instar de l'API Température, pour simplifier la détermination du statut opérationnel des stations. `[en_cours]`
- **#131** [API Piézométrie] Synchronisation des données — Les APIs Hub'Eau (Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) manquent d'un filtre par date de mise à jour pour une synchronisation efficace des données, une fonctionnalité prévue pour l'API Hydrométrie mais pas à court terme pour la Piézométrie. `[information]`
- **#134** [API Qualité des cours d'eau] Erreur 500 sur `/v2/qualite_rivieres/analyse_pc` — L'API Qualité des cours d'eau a rencontré une anomalie temporaire provoquant des erreurs 500 sur l'endpoint `/v2/qualite_rivieres/analyse_pc` pour les analyses physicochimiques, mais le problème a été résolu par un redémarrage du service. `[résolu]`
- **#135** API Qualité des cours d'eau - signification des champs date_debut_maj date_fin_maj — Cette issue clarifie la signification et le fonctionnement des filtres `date_debut_maj` et `date_fin_maj` qui s'appliquent sur le champ `date_maj_analyse` dans l'API Qualité des cours d'eau, ainsi que les mécanismes d'alimentation de la base Naïades. `[résolu]`
- **#146** [Qualité des cours d’eau] Indisponibilité des données physicochimie Loire-Bretagne — L'API Hub'Eau Qualité des cours d'eau a connu une indisponibilité temporaire des données de physicochimie du bassin Loire-Bretagne, désormais résolue avec une mise à jour bimensuelle des données via une connexion directe entre Naïades et la banque de l'Agence de l'eau Loire-Bretagne. `[résolu]`
- **#152** API Hub'Eau - Qualité physico-chimique des cours d'eau — L'API Hub'Eau pour la qualité des cours d'eau a une limite de profondeur de pagination d'environ 20000 enregistrements, nécessitant d'affiner les requêtes pour les grands volumes, et la fréquence de mise à jour des données varie par station, avec une méthode spécifique pour découvrir les dates de prélèvement disponibles. `[résolu]`
- **#154** Pas de données renvoyées à partir du 2023-08-05 par l'API https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc.csv — L'absence temporaire de données dans l'API Hub'Eau Qualité des cours d'eau était due à un retard d'alimentation de la base source Naïades, problème qui a été résolu par la suite. `[résolu]`
- **#156** Qualité des cours d'eau ,nomenclature des variables utilisées — Cette issue explique où trouver les descriptions des variables pour les APIs Hub'Eau (section Models) et fournit la définition de l'attribut `resultat` pour l'API Qualité des cours d'eau. `[résolu]`
- **#158** Qualité des cours d'eau — Une baisse anormale des données de qualité des cours d'eau pour la région Pays de la Loire en 2020 et 2021 était due à un incident technique de remontée des données de l'Agence de l'eau Loire-Bretagne vers Naïades, désormais résolu. `[résolu]`
- **#166** [API Qualité des cours d'eau] encoding issue with the field `libelle_station` — L'API Qualité des cours d'eau a rencontré un problème d'encodage (ISO8859-1 au lieu de UTF-8) sur le champ `libelle_station` provenant du système source NAIADES, affectant de nombreuses stations et bassins, mais l'anomalie a été corrigée. `[résolu]`
- **#169** [API Qualité des cours d'eau] - absence de données — Cette issue détaille comment une mauvaise initialisation des tables de logs pour le moissonnage différentiel des données Sandre par Naïades a causé l'absence de millions d'analyses de qualité des cours d'eau du bassin Loire-Bretagne sur Hub'Eau entre 2006 et 2022, et la résolution de ce problème. `[résolu]`
- **#198** [API Qualité des cours d'eau] — L'API Qualité des cours d'eau a rencontré une erreur '502 Proxy Error' due à une forte sollicitation, mais le problème a été résolu et l'API est de nouveau disponible. `[résolu]`
- **#199** [API Qualité des cours d'eau] /v2/qualite_rivieres/condition_environnementale_pc — Cette issue clarifie que l'endpoint /v2/qualite_rivieres/condition_environnementale_pc fournit des conditions environnementales liées aux prélèvements et non des analyses directes de paramètres comme les précipitations (code 1553), et signale la correction d'un bug d'export CSV. `[résolu]`
- **#200** [API Qualité des cours d'eau] Recuperation de donnees au delà de 20.000 rows, objectif 1000000 rows. — Les APIs Hub'Eau imposent une limite de 20 000 enregistrements par requête totale, nécessitant une segmentation des interrogations pour les grands volumes et recommandant le site Naïades pour les exports historiques massifs. `[information]`
- **#204** [API Qualité des nappes d'eau souterraines] Ajout d'élément à la liste des stations de mesure — L'issue met en évidence le besoin de métadonnées (années, producteurs, paramètres) pour les stations de qualité des nappes afin d'optimiser les requêtes et contourner la limite de 20 000 résultats, et Hub'Eau prévoit un nouveau endpoint "_parametres" pour les APIs de qualité, d'abord sur les cours d'eau. `[en_cours]`
- **#217** Absence de data PFAS de la platforme https://pdh.cnrs.fr/fr/datasets/ france_naiades sur hub'eau — L'API Hub'Eau ne permet pas la sélection directe des données PFAS, nécessitant une requête par groupe ou paramètre individuel, et renvoie vers Sandre/Aquaref pour le référentiel analytique. `[résolu]`
- **#220** Question sur le calcul de la concentration journalière du métolachlore ESA du departement de Finistère de toutes les stations present. — Hub'Eau ne fournit pas de concentrations journalières agrégées à l'échelle départementale et redirige vers Ades ou Naïades pour les questions méthodologiques d'interprétation des données de qualité de l'eau. `[résolu]`
- **#246** [API Qualité des cours d'eau] Inconsistence des champs retournés en cas de modification du format json/geojson — L'API Qualité des cours d'eau présente des inconsistances dans le nommage des champs (snake_case vs. camelCase) entre les formats JSON et GeoJSON, et le paramètre 'fields' ne fonctionne pas correctement ou de manière cohérente selon le format et la casse utilisée. `[en_cours]`
- **#250** [API Qualité des cours d'eau] Erreur 500 avec code_prelevement depuis /v2/qualite_riviere/analyse_pc — L'API Qualité des cours d'eau renvoyait une erreur 500 lors de l'utilisation du paramètre `code_prelevement` sur la route `/v2/qualite_rivieres/analyse_pc`, mais ce comportement a été corrigé. `[résolu]`
- **#252** [API Qualité des cours d'eau] Erreur sur code_prelevement depuis /v2/qualite_riviere/operation_pc — L'API Hub'Eau Qualité des cours d'eau peut retourner des résultats incomplets pour le filtre `code_prelevement=RAS` sur l'endpoint `operation_pc` en raison d'une réutilisation de codes dans les données sources et de la logique de regroupement de l'API, sans intervention possible de Hub'Eau. `[information]`
- **#254** [API Qualité des cours d'eau] profondeur du prélèvement issue de Naïades — L'API Qualité des cours d'eau fournit la profondeur de prélèvement via le champ `profondeur` du endpoint `_operation_pc`, et cette information peut être liée aux résultats de mesures via le `code_prelevement`. `[résolu]`
- **#268** [API Qualité des cours d'eau] Bug de l'API operation_pc — L'API `operation_pc` de `Qualité des cours d'eau` rencontre un bug "Internal server error" qui peut être contourné en spécifiant explicitement le paramètre `fields` dans la requête. `[en_cours]`

</details>
