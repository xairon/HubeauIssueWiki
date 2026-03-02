# Piézométrie

> 33 issues analysées

## Guide

### Comportement actuel

L'API Piézométrie offre trois endpoints principaux : `/niveaux_nappes/stations` pour les informations sur les points de mesure, `/niveaux_nappes/chroniques` pour les données historiques agrégées, et `/niveaux_nappes/chroniques_tr` pour les mesures brutes en temps réel. Le endpoint `stations` accepte les identifiants `bss_id` (nouveau code BSS) et `code_bss` (ancien), tandis que `chroniques_tr` utilise le `bss_id` et `chroniques` l'ancien `code_bss` (#49, #59, #207). Les niveaux de nappe (`niveau_nappe_eau`) sont exprimés en mètres NGF, et la profondeur (`profondeur_nappe`) en mètres par rapport à un repère de mesure, avec la relation `niveau_nappe_eau = altitude_repere - profondeur_nappe` (#34). Le paramètre `size` par défaut est de 5000 résultats, et il est possible de requêter jusqu'à 200 `code_bss` simultanément (#180).

### Pièges à éviter

L'endpoint `/niveaux_nappes/chroniques` ne supporte pas le `bss_id` (nouveau code BSS), nécessitant l'utilisation de l'ancien `code_bss` (#49, #59, #207). Le paramètre `date_fin_mesure` filtre sur le `timestamp_mesure` (date et heure), excluant les données après 00h00 du jour spécifié, ce qui peut entraîner la perte des mesures les plus récentes (#259). Il n'existe pas de filtre par date de mise à jour des données, obligeant à recharger des jeux de données complets pour la synchronisation (#131). Les informations de "période d'activité" des stations ne sont pas mises à jour en temps réel, pouvant fausser les requêtes récentes sur `/stations` (#50, #93). Le filtrage par `code_reseau` n'est pas disponible, et cette information est absente des résultats des stations (#63, #230). Enfin, le tri global par `date_mesure` n'est pas direct pour plusieurs piézomètres, le tri s'appliquant d'abord par `code_bss` (#163).

### Bonnes pratiques

Pour contourner l'absence de filtre par date de mise à jour, il est recommandé de requêter périodiquement (ex: mensuellement) les données sur une période donnée (ex: la dernière année) pour identifier les changements, même si cette approche est sous-optimale (#131). Lors de l'extraction de chroniques pour plusieurs piézomètres, si vous souhaitez la dernière mesure de chacun, il est plus fiable d'effectuer des requêtes individuelles ou de post-traiter le jeu de résultats global (#163). Utilisez le paramètre `fields` pour limiter les champs retournés et optimiser le volume de données (#260). Pour les développeurs R, le package `hubeau` d'INRAE (disponible sur GitHub) simplifie l'interrogation des APIs Hub'Eau, y compris la Piézométrie (#62, #137).

### Contexte métier

Les points d'eau souterraine sont identifiés par un `code_bss` (ancien) ou un `bss_id` (nouveau, officiel depuis 2016) (#49, #59, #207). Les anciens codes BSS incluent un indice de 10 caractères pour l'identification unique et une désignation, tandis que les nouveaux `bss_id` sont des identifiants uniques sans désignation (#230). Les données piézométriques proviennent de la base ADES (Accès aux Données sur les Eaux Souterraines) et sont disponibles sous forme de chroniques historiques (agrégées et corrigées) ou temps réel (brutes, issues des capteurs) (#96). Les nomenclatures SANDRE définissent les codes de statut et de qualification des données, essentiels pour leur interprétation (#260). L'altitude du repère de mesure (`altitude_repere`) peut varier dans le temps pour un même piézomètre, impactant le calcul du niveau de nappe (#34).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API `/niveaux_nappes/chroniques` ne supporte pas le paramètre `bss_id` (nouveau code BSS) et retourne une erreur "code BSS ne peut pas être null". (#49)
- L'API `/niveaux_nappes/chroniques` fonctionne avec le paramètre `code_bss` (ancien code BSS). (#49)
- L'API `/niveaux_nappes/chroniques_tr` supporte le paramètre `bss_id`. (#49)
- Il existe un "nouveau code BSS" (identifié comme `bss_id`) et un "ancien code BSS" (identifié comme `code_bss`) pour les données piézométriques. (#49)
- La récupération des historiques de chroniques piézométriques est impactée par l'utilisation de ces codes. (#49)
- L'API niveaux_nappes/stations accepte le paramètre 'bss_id' pour les nouveaux codes BSS et le paramètre 'code_bss' pour les anciens codes BSS. (#59)
- L'API niveaux_nappes/chroniques (chroniques historiques/temps différé) n'accepte que le paramètre 'code_bss' (anciens codes BSS). (#59)
- L'API niveaux_nappes/chroniques_tr (chroniques temps réel) accepte le paramètre 'bss_id' (nouveaux codes BSS). (#59)
- Il existe un bug où la 'date_fin_mesure' retournée par l'API niveaux_nappes/stations peut être obsolète par rapport aux données réelles des chroniques. (#59)
- Le support des nouveaux codes BSS ('bss_id') pour les chroniques historiques (niveaux_nappes/chroniques) est prévu dans la feuille de route 2023. (#59)
- Les stations de piézométrie possèdent deux types de codes identifiants : un 'ancien code BSS' (ex: 05202X0099/P) et un 'nouveau code BSS' (ex: BSS001KJRF). (#59)
- Les données de piézométrie sont disponibles sous forme de 'chroniques temps différé' (historiques) et 'chroniques temps réel'. (#59)
- L'API Piézométrie ne permettait pas de filtrer les stations ou les chroniques par code_reseau. (#63)
- L'API Qualité des nappes ne permettait pas de filtrer les stations par code_reseau (mais le permettait pour les analyses). (#63)
- L'API Qualité des nappes permettait de filtrer les stations par nom_reseau. (#63)
- Les informations sur les réseaux de mesure (code, mnémo, nom) sont présentes dans l'index sous-jacent de Hub'Eau. (#63)
- L'ajout de filtres par code_reseau et l'inclusion des détails du réseau dans les réponses API étaient envisagés mais non prioritaires. (#63)
- La base ADES permet de consulter et d'extraire les données par code_reseau. (#63)
- Les réseaux de mesure ont des fiches consultables publiquement sur ades.eaufrance.fr (ex: 0400000020 pour le réseau Bretagne). (#63)
- Le filtrage par code_reseau est jugé plus pratique que par nom_reseau. (#63)
- Les utilisateurs peuvent utiliser des listes de codes BSS comme solution de contournement en l'absence de filtrage par réseau. (#63)
- L'API Piézométrie (endpoint `niveaux_nappes/stations`) ne met pas à jour les données de stations immédiatement. (#93)
- L'utilisation du paramètre `date_recherche` sur l'API `niveaux_nappes/stations` peut renvoyer un nombre variable de stations, y compris zéro, pour des dates récentes, même si des données existent pour des dates antérieures proches. (#93)
- La disponibilité des stations piézométriques via l'API pour une `date_recherche` donnée peut être inconsistante pour les dates récentes, reflétant un délai dans la publication des données. (#93)
- Les APIs Hub'Eau (notamment Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) ne disposent pas de paramètre de filtre par date de mise à jour des données. (#131)
- L'absence de filtre par date de mise à jour oblige les utilisateurs à charger l'intégralité des données pour rester à jour. (#131)
- L'API Hydrométrie inclut une 'date de production' dans ses résultats, mais ce paramètre n'est pas utilisable comme filtre de requête. (#131)
- L'ajout d'un filtre par date de mise à jour n'est pas prévu à court terme pour l'API Piézométrie. (#131)
- L'ajout d'un filtre par date de mise à jour est une évolution identifiée pour l'API Hydrométrie. (#131)
- Le service web ADES (Accès aux Données sur les Eaux Souterraines) offre une fonctionnalité de synchronisation des points d'eau et mesures basée sur une date de mise à jour. (#131)
- La synchronisation par date de mise à jour est essentielle pour récupérer uniquement les différences et les corrections apportées aux données sans télécharger l'intégralité du jeu de données. (#131)
- Les données environnementales peuvent être corrigées après leur première publication ('date de production'), nécessitant un mécanisme de mise à jour efficace. (#131)
- Une pratique courante pour contourner l'absence de filtre est de requêter toutes les données d'une période (ex: dernière année) mensuellement, ce qui est sous-optimal. (#131)
- Il est proposé d'implémenter le format GeoJSON pour les chroniques en temps réel de l'API Piézométrie. (#140)
- Les chroniques en temps réel sont des séries de mesures piézométriques continues dans le temps. (#140)
- Le paramètre `sort` (asc/desc) de l'API Piézométrie (`niveaux_nappes/chroniques`) trie les mesures au sein de chaque station (bss_id), et non globalement par date sur l'ensemble des résultats. (#163)
- Le premier critère de tri global de l'API Piézométrie est le `code_bss`. (#163)
- Lorsqu'une requête inclut plusieurs `bss_id` et un paramètre `size`, le `size` s'applique à la page de résultats globale après le tri par `code_bss`, ce qui peut renvoyer plusieurs mesures pour le premier `bss_id` au lieu d'une mesure par `bss_id`. (#163)
- Pour obtenir la dernière mesure de plusieurs piézomètres, il est nécessaire de faire autant de requêtes que de piézomètres ou de traiter le jeu de résultats en rupture sur le code du piézomètre. (#163)
- Le comportement de l'API concernant le tri pourra être ajusté lors d'une prochaine évolution. (#163)
- Les données de piézométrie incluent des informations comme le `code_bss` (identifiant du piézomètre), la `date_mesure` et la `profondeur_nappe`. (#163)
- Un cas d'usage courant est de vouloir récupérer la dernière mesure pour une liste de piézomètres. (#163)
- La valeur par défaut pour le paramètre `code_bss` (ex: "07548X0009/F") mentionnée dans la documentation s'applique uniquement à la console de test (formulaire) de l'API et non à l'API Hub'Eau elle-même. (#180)
- L'API Hub'Eau pour `niveaux_nappes/chroniques_tr` ne fixe pas de valeur par défaut pour les paramètres `code_bss` ou `bss_id` lors d'un appel direct. (#180)
- Lors de l'utilisation du formulaire de test, si des paramètres comme `code_bss` (par défaut) et `bss_id` sont présents simultanément dans l'URL générée, l'utilisateur doit en retirer un manuellement pour éviter les conflits. (#180)
- La valeur par défaut du paramètre `size` est de 5000 pour l'API Hub'Eau, tandis qu'elle est de 20 dans la console de test. (#180)
- `code_bss` est un code national de station (ancien code BSS) pour les piézomètres. (#180)
- `bss_id` est un autre identifiant pour les piézomètres. (#180)
- Il est possible d'interroger jusqu'à 200 `code_bss` en les séparant par une virgule dans la requête. (#180)
- L'API Piézométrie permet de télécharger les données de stations en utilisant le paramètre bss_id. (#207)
- Le téléchargement des chroniques (séries temporelles) via l'API Piézométrie ne peut être réalisé qu'en passant l'ancien code BSS en paramètre. (#207)
- Le bss_id (identifiant BSS en vigueur depuis 2016) n'est pas utilisable comme paramètre pour le téléchargement des chroniques de piézométrie. (#207)
- Le bss_id est l'identifiant BSS officiel des points d'eau en vigueur depuis 2016. (#207)
- Il existe un ancien code BSS qui n'est plus le code officiel des points d'eau pour les points de piézométrie. (#207)
- L'API piézométrie ne permet pas de requêter par code(s) de réseau. (#230)
- L'information du code de réseau est manquante dans les résultats du endpoint `/v1/niveaux_nappes/stations`. (#230)
- Il est suggéré que l'API piézométrie accepte des requêtes basées uniquement sur les 10 premiers caractères des codes BSS (anciens et nouveaux) pour l'identification d'un point. (#230)
- L'utilisation d'une désignation ('/X') avec les nouveaux codes BSS peut créer une confusion car elle n'est pas nécessaire et imite l'ancien format. (#230)
- Les anciens codes BSS (ex: 00471X0095/PZ2013) sont composés d'un indice (les 10 premiers caractères) et d'une désignation. (#230)
- Seul l'indice (les 10 premiers caractères) des codes BSS est utile pour l'identification unique d'un point piézométrique. (#230)
- La désignation des codes BSS n'est pas toujours stockée dans les bases de données et n'est pas pertinente pour l'identification unique. (#230)
- Les nouveaux codes BSS (ex: BSS000EBLL) sont des codes uniques et n'incluent pas de désignation. (#230)
- Les codes de réseau (ex: 0102400001) sont des identifiants pertinents pour la piézométrie. (#230)
- Le paramètre `date_fin_mesure` de l'API Piézométrie (`niveaux_nappes/chroniques`) filtre les données en fonction du `timestamp_mesure` (date et heure), et non de la `date_mesure` (date seule). (#259)
- Ce comportement fait que les mesures enregistrées après 00h00 le jour de `date_fin_mesure` sont exclues par défaut. (#259)
- Pour inclure toutes les données d'une journée `Dfin`, il est nécessaire de spécifier `date_fin_mesure = Dfin + 1 jour`. (#259)
- L'utilisation de `Dfin + 1 jour` peut occasionnellement inclure une donnée indésirable si une mesure existe à 00h00 le jour `Dfin + 1`. (#259)
- Le comportement d'inclusion/exclusion de `date_fin_mesure` est inconsistent entre différentes stations piézométriques. (#259)
- Le paramètre `date_debut_mesure` de l'API Piézométrie filtre également sur le `timestamp_mesure` (date et heure). (#259)
- L'API Hydrométrie (`hydrometrie/chroniques`) semble traiter correctement les paramètres de date pour les observations élaborées (historiques) en se basant sur la date seule. (#259)
- Les utilisateurs de l'API Piézométrie de Hub'Eau risquent de rater des données, souvent les plus récentes, s'ils ne compensent pas le comportement du paramètre `date_fin_mesure`. (#259)
- Les mesures piézométriques peuvent être enregistrées à différentes heures de la journée, pas seulement à 00h00. (#259)
- Il est proposé de modifier le filtrage temporel pour qu'il s'appuie sur la colonne `date_mesure` (date sans heure) et soit inclusif aux bornes. (#259)
- L'API Piézométrie fournit actuellement des libellés textuels longs pour certains champs (ex: statut, qualification) sans les codes numériques ou mnémoniques correspondants. (#260)
- L'ajout de codes courts pour ces champs permettrait de réduire le volume de données exportées et d'accélérer les extractions. (#260)
- Il est possible de limiter les champs exportés via le paramètre 'fields'. (#260)
- Les données de chronique piézométrique incluent des champs comme 'mode_obtention', 'statut', 'qualification', 'code_continuite', 'nom_continuite', 'code_producteur', 'nom_producteur', 'code_nature_mesure', 'nom_nature_mesure'. (#260)
- Les codes de qualification (0, 1, 2, 3, 4) et de statut (1 à 4 ou mnémoniques comme Brute, NV1) sont définis par les nomenclatures du SANDRE. (#260)
- Les nomenclatures SANDRE pour le statut (urn:sandre:donnees:416) et la qualification (urn:sandre:donnees:414) des données sont des références clés pour les données sur l'eau en France. (#260)

### Historique des problèmes résolus

- ~~L'opération `qualite_nappes/stations` de l'API Qualité des nappes permet de récupérer des informations détaillées sur un point d'eau à partir de son code BSS. (#10)~~
- ~~L'API Qualité des nappes fournit des informations complètes sur les points d'eau de type qualitomètre, incluant des données géographiques, administratives et hydrogéologiques (ex: masses d'eau, entités BDLISA). (#10)~~
- ~~L'API Piézométrie fournissait, au moment de l'issue, moins d'informations sur les points d'eau (notamment les masses d'eau) que l'API Qualité des nappes. (#10)~~
- ~~Un code BSS (BSS_ID) identifie un point d'eau souterraine et peut être utilisé pour interroger ses caractéristiques. (#10)~~
- ~~Les points d'eau souterraine sont associés à des masses d'eau (codes_masse_eau_rap, codes_masse_eau_edl) et des entités hydrogéologiques BDLISA. (#10)~~
- ~~Les données de qualité des eaux souterraines proviennent de la base ADES. (#10)~~
- ~~La spécification Swagger des APIs Hub'Eau contenait des propriétés "allowEmptyValues: false" non conformes à la spécification Swagger, empêchant la génération de clients API. (#19)~~
- ~~L'API Piézométrie (niveaux_nappes) avait un endpoint `chroniques.csv` dont le `produces` indiquait un format binaire/stream (CSV) mais référençait un schéma d'objet (`Chronique_pi_zom_trique`), causant une erreur de génération de client. (#19)~~
- ~~Les noms d'objets dans la spécification Swagger (ex: "Résultat d'une rêquete sur les chroniques") n'étaient pas optimaux pour la génération de code, rendant le code client potentiellement "douteux". (#19)~~
- ~~L'API Piézométrie (niveaux_nappes) fournit des données de chroniques (séries temporelles) pour les niveaux de nappe. (#19)~~
- ~~Avant le 23 avril 2019, l'API Piézométrie pouvait présenter des retards ou des manques de données par rapport à la base ADES. (#22)~~
- ~~Depuis le 23 avril 2019, l'API Piézométrie est synchronisée avec ADES, fournissant l'intégralité des données piézométriques avec la même fréquence de mise à jour. (#22)~~
- ~~L'API Piézométrie utilise le paramètre `code_bss` pour identifier les points d'eau (e.g., 00271X0002/P2). (#22)~~
- ~~ADES (Accès aux Données sur les Eaux Souterraines) est la source de référence pour les données piézométriques en France. (#22)~~
- ~~Les données piézométriques concernent les niveaux de nappe. (#22)~~
- ~~L'opération 'stations' de l'API Piézométrie a été enrichie pour inclure des informations sur les masses d'eau. (#29)~~
- ~~L'API Piézométrie fournit désormais le code, le nom et l'URI de la masse d'eau captée pour chaque piézomètre. (#29)~~
- ~~Les informations sur les masses d'eau fournies par l'API Piézométrie sont basées sur la version 'état des lieux'. (#29)~~
- ~~Les piézomètres peuvent être liés à des 'masses d'eau'. (#29)~~
- ~~L'API 'qualité des nappes' intégrait déjà la liaison aux masses d'eau. (#29)~~
- ~~La liaison entre les entités BD LISA et les masses d'eau était historiquement prévue à partir de l'état des lieux 2019. (#29)~~
- ~~Des données de liaison entre les masses d'eau de 'rapportage' et les piézomètres sont disponibles dans la base de données Waterbase Quantity de l'EEA (données remontées par la France pour la Directive Cadre sur l'Eau). (#29)~~
- ~~Dans la base Waterbase Quantity, 'waterBodyIdentifier' représente un code de masse d'eau et 'monitoringSiteIdentifier' un code de piézomètre. (#29)~~
- ~~L'API Piézométrie chroniques ne fournissait pas d'information sur la continuité des courbes, ce qui pouvait fausser l'interprétation des chroniques piézométriques. (#31)~~
- ~~L'API Piézométrie chroniques a été mise à jour pour inclure l'information sur la continuité des courbes. (#31)~~
- ~~L'API Piézométrie chroniques a été enrichie avec des informations sur le producteur, la nature de la mesure et la profondeur de l'eau par rapport au repère de mesure. (#31)~~
- ~~La documentation du site Hub'Eau (exemples et liste des changements) a été mise à jour pour refléter l'ajout de ces nouveaux champs dans l'API chroniques. (#31)~~
- ~~Les données piézométriques peuvent présenter des ruptures de suivi et des points initiaux multiples, reflétant des suivis irréguliers sur certains sites. (#31)~~
- ~~La valorisation des chroniques piézométriques nécessite de connaître la continuité des courbes pour une interprétation correcte des données. (#31)~~
- ~~Des métadonnées importantes pour les chroniques piézométriques incluent le producteur, la nature de la mesure et la profondeur de l'eau par rapport au repère de mesure. (#31)~~
- ~~L'endpoint `chroniques` de l'API Piézométrie supporte les paramètres `sort` (asc/desc), `size` et `fields` pour filtrer et ordonner les résultats. (#34)~~
- ~~L'endpoint `chroniques_tr` (données temps réel) de l'API Piézométrie fournit directement la `cote_ngf_repere` (altitude NGF du repère de mesure), mais toutes les stations ne disposent pas de données en temps réel. (#34)~~
- ~~L'endpoint `stations` de l'API Piézométrie fournit l'`altitude_station` (altitude du sol au niveau du piézomètre). (#34)~~
- ~~Des informations détaillées sur les piézomètres, y compris l'historique des altitudes des repères de mesure, sont accessibles via le lien `urn_bss` fourni par Hub'Eau, qui mène au portail ADES, puis à la 'Fiche BSSEAU'. (#34)~~
- ~~`niveau_nappe_eau` dans l'API Piézométrie est exprimé en mètres NGF (Nivellement Général de la France), représentant l'altitude de la nappe par rapport au niveau de la mer. (#34)~~
- ~~`profondeur_nappe` dans l'API Piézométrie est exprimée en mètres par rapport à un repère de mesure spécifique (ex: sol, haut du tube piézométrique, margelle du puits). (#34)~~
- ~~La relation entre les champs est `niveau_nappe_eau = altitude_repere - profondeur_nappe`, où `altitude_repere` est l'altitude NGF du repère de mesure. (#34)~~
- ~~L'`altitude_repere` peut varier dans le temps pour un même piézomètre (ex: suite à des travaux ou changements de pratiques de mesure). (#34)~~
- ~~La précision des mesures de `profondeur_nappe` est de l'ordre du centimètre, tandis que la précision des altitudes (NGF) est de l'ordre du mètre. (#34)~~
- ~~Pour connaître l'`altitude_repere` exacte d'une mesure, il faut consulter la 'Fiche BSSEAU' via ADES ou la calculer avec `altitude_repere = niveau_nappe_eau + profondeur_nappe`. (#34)~~
- ~~L'API Piézométrie de Hub'Eau fournit les informations de continuité des chroniques via les champs `code_continuite` et `nom_continuite`. (#43)~~
- ~~Pour récupérer les informations de continuité, il est nécessaire de spécifier les champs `code_continuite` et `nom_continuite` dans la requête API. (#43)~~
- ~~Le démonstrateur Hub'Eau (visualiseur en ligne) ne gère pas et n'affiche pas les informations de continuité des chroniques piézométriques. (#43)~~
- ~~Les chroniques piézométriques peuvent présenter des ruptures de continuité, qui sont des informations importantes pour l'analyse des données. (#43)~~
- ~~Le site ADES (ades.eaufrance.fr) est une source de référence pour les chroniques piézométriques et affiche les informations de continuité. (#43)~~
- ~~L'API niveaux_nappes/stations utilise une information de "période d'activité" pour filtrer les stations par date_recherche. (#50)~~
- ~~L'information de "période d'activité" des stations n'est pas rafraîchie très fréquemment dans l'API Hub'Eau. (#50)~~
- ~~Un délai de rafraîchissement de 1 à 2 mois pour l'information de "période d'activité" des stations a été constaté. (#50)~~
- ~~Des requêtes avec date_recherche trop proche de la date actuelle peuvent retourner moins de résultats que prévu à cause du délai de rafraîchissement de la "période d'activité". (#50)~~
- ~~La "période d'activité" est un critère important pour la recherche de stations piézométriques actives à une date donnée. (#50)~~
- ~~Il existe un décalage temporel entre l'activité réelle d'une station piézométrique et la mise à jour de sa "période d'activité" dans les données de l'API. (#50)~~
- ~~Le démonstrateur Hub'Eau pour la piézométrie présente des graphiques d'évolution des données et des liens vers les détails des points de mesure. (#54)~~
- ~~L'affichage des données piézométriques sur des écrans de faible résolution (ex: 1366x768) peut nécessiter des adaptations (ex: suppression de graphiques) pour garantir l'accessibilité des informations essentielles comme les liens de détail. (#54)~~
- ~~L'API Hub'Eau Piézométrie supporte les requêtes Cross-Origin (CORS). (#61)~~
- ~~L'en-tête `access-control-allow-origin: *` est inclus dans les réponses de l'API Hub'Eau, permettant l'accès depuis n'importe quelle origine. (#61)~~
- ~~Les requêtes vers l'API Hub'Eau sont servies via Cloudflare. (#61)~~
- ~~Un blocage de requête Cross-Origin avec l'API Hub'Eau est plus probablement dû à une implémentation client (ex: exécution asynchrone) qu'à un manque de support CORS côté serveur. (#61)~~
- ~~L'API Piézométrie fournit des données sur la chronique du niveau des nappes. (#61)~~
- ~~L'endpoint `/api/v1/niveaux_nappes/stations` permet de récupérer des informations sur les stations de mesure des niveaux de nappes. (#61)~~
- ~~Le BRGM fournit un exemple d'appel de l'API Hub'Eau avec R pour les données piézométriques, disponible sur GitHub à l'adresse https://github.com/BRGM/hubeau/blob/master/code_examples/Trac%C3%A9%20d'une%20chronique%20pi%C3%A9zom%C3%A9trique%20avec%20R.ipynb. (#62)~~
- ~~Le BRGM prévoit de publier d'autres exemples de code R pour l'API Hub'Eau sur son dépôt GitHub à l'adresse https://github.com/BRGM/hubeau/tree/master/code_examples. (#62)~~
- ~~Un package R nommé `hubeau` est développé par INRAE pour interroger les APIs Hub'Eau. (#62)~~
- ~~Le package R `hubeau` inclut une fonction générique d'interrogation et des fonctions spécifiques par API/opération, retournant les résultats sous forme de data.frame. (#62)~~
- ~~Le package R `hubeau` prend en charge initialement les APIs 'Prélèvements en eau' et 'Indicateurs des services'. (#62)~~
- ~~Le package R `hubeau` est disponible sur GitHub à l'adresse https://github.com/inrae/hubeau et sa documentation à https://inrae.github.io/hubeau/. (#62)~~
- ~~L'API Hub'Eau présente des bugs connus, mentionnés dans les issues #72 et #74. (#62)~~
- ~~Les données "temps réel" de l'API Piézométrie sont brutes, non corrigées et proviennent directement des capteurs. (#96)~~
- ~~La profondeur temporelle des données "temps réel" de l'API Piézométrie n'est actuellement pas limitée, mais une limitation à 1 an est envisagée. (#96)~~
- ~~Les données du endpoint `/chroniques` de l'API Piézométrie sont agrégées et peuvent être corrigées. (#96)~~
- ~~Hub'Eau se synchronise une fois par jour avec la banque ADES pour alimenter le endpoint `/chroniques` de l'API Piézométrie. (#96)~~
- ~~La fréquence de remontée des données par les producteurs vers ADES peut varier, entraînant des délais dans la disponibilité des données récentes pour le endpoint `/chroniques`. (#96)~~
- ~~Les données "temps réel" de l'API Piézométrie sont des données brutes issues des capteurs et ne subissent pas de corrections. (#96)~~
- ~~Les données du endpoint `/chroniques` de l'API Piézométrie sont des données agrégées et peuvent être corrigées (ex: dérive de capteur, nouveau nivellement du repère de mesure). (#96)~~
- ~~La banque ADES est la source des données alimentant le endpoint `/chroniques` de l'API Piézométrie. (#96)~~
- ~~Les données du endpoint `/chroniques` sont agrégées sur une journée, retenant généralement la valeur maximale du niveau NGF (valeur minimale de la profondeur), mais cela peut varier selon les points d'eau. (#96)~~
- ~~Les corrections et l'agrégation des données piézométriques sont réalisées par les producteurs de données avant transmission à la banque ADES. (#96)~~
- ~~L'API Piézométrie (endpoint `niveaux_nappes/chroniques`) peut ne pas renvoyer immédiatement les dernières mesures disponibles en raison de délais de transmission des données. (#116)~~
- ~~Les chroniques de niveaux de nappe (piézométrie) ne sont pas toujours disponibles en temps réel et peuvent apparaître dans l'API avec un certain décalage après la date de mesure. (#116)~~
- ~~Le paramètre `code_bss` est utilisé pour identifier les stations de piézométrie et récupérer leurs chroniques. (#116)~~
- ~~L'endpoint `niveaux_nappes/chroniques` de l'API Piézométrie retournait une réponse vide sans erreur lors de requêtes multiples sur le paramètre `code_bss`. (#130)~~
- ~~L'endpoint `niveaux_nappes/chroniques` fonctionnait correctement pour une requête sur un seul `code_bss`. (#130)~~
- ~~L'endpoint `niveaux_nappes/chronique_tr` de l'API Piézométrie fonctionnait correctement pour une liste de `code_bss`. (#130)~~
- ~~Le problème de l'endpoint `niveaux_nappes/chroniques` avec les requêtes multiples `code_bss` a été résolu. (#130)~~
- ~~Le paramètre `code_bss` identifie un ouvrage (piézomètre) dans les données de piézométrie. (#130)~~
- ~~Les données de piézométrie peuvent être filtrées par une plage de dates via les paramètres `date_debut_mesure` et `date_fin_mesure`. (#130)~~
- ~~Le champ `niveau_nappe_eau` représente le niveau de la nappe d'eau. (#130)~~
- ~~L'API Hub'Eau ne traitait pas correctement les paramètres de requête avec plusieurs valeurs séparées par des virgules (ex: code_bss=val1,val2) pour l'endpoint niveaux_nappes/chroniques de l'API Piézométrie. (#132)~~
- ~~Ce dysfonctionnement était une régression suite à une migration technique réalisée en décembre 2022. (#132)~~
- ~~La même anomalie affectait l'endpoint _analyses_ de l'API Qualité des nappes d'eau souterraines et les endpoints 'stations' de diverses APIs. (#132)~~
- ~~Une solution de contournement temporaire était d'effectuer des appels API séparés pour chaque valeur unitaire. (#132)~~
- ~~L'anomalie a été corrigée en mars 2023, et la recherche avec plusieurs valeurs séparées par des virgules est de nouveau fonctionnelle. (#132)~~
- ~~Le paramètre code_bss est utilisé pour filtrer les chroniques piézométriques. (#132)~~
- ~~Les endpoints 'stations' permettent de lister les points de mesure selon des critères comme la masse d'eau ou le département. (#132)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~
- ~~Le paramètre `bbox` de l'API Piézométrie (endpoint `/niveaux_nappes/stations`) doit être fourni comme une seule chaîne de caractères avec les quatre coordonnées (min_lon,min_lat,max_lon,max_lat) séparées par des virgules. (#144)~~
- ~~L'utilisation de paramètres séparés comme `bbox1`, `bbox2`, `bbox3`, `bbox4` pour définir une boîte englobante n'est pas supportée par l'API Piézométrie et peut entraîner le retour de toutes les données nationales. (#144)~~
- ~~Les données piézométriques peuvent être filtrées géographiquement pour des bassins spécifiques, comme le bassin de la Vilaine, en utilisant le paramètre `bbox`. (#144)~~
- ~~Avant le correctif, l'utilisation du paramètre "fields" sur l'endpoint "niveaux_nappes/chroniques" avec "timestamp_mesure" seul pouvait retourner des valeurs nulles pour "timestamp_mesure". (#178)~~
- ~~Le problème était contourné en incluant "date_mesure" dans le paramètre "fields" en plus de "timestamp_mesure". (#178)~~
- ~~Un correctif a été déployé : le champ "timestamp_mesure" est désormais correctement valorisé indépendamment de la présence du champ "date_mesure" lors de l'utilisation du paramètre "fields" sur l'endpoint "niveaux_nappes/chroniques". (#178)~~
- ~~L'endpoint concerné est `/api/v1/niveaux_nappes/chroniques`. (#178)~~
- ~~Le paramètre `fields` permet de sélectionner les champs à retourner dans la réponse de l'API. (#178)~~
- ~~Les données de piézométrie incluent des champs comme `timestamp_mesure` (horodatage de la mesure), `niveau_nappe_eau` (niveau de la nappe d'eau) et `date_mesure` (date de la mesure). (#178)~~
- ~~Les stations de mesure des niveaux de nappe sont identifiées par un `code_bss` (ex: `07548X0009/F`). (#178)~~
- ~~Les API Hydrométrie et Piézométrie ont retourné une erreur 500 et étaient indisponibles. (#184)~~
- ~~Un dysfonctionnement a affecté l'ensemble des API Hub'Eau, les rendant momentanément indisponibles. (#184)~~
- ~~Les API Hub'Eau ont été rétablies et sont de nouveau disponibles. (#184)~~
- ~~Le projet SUBLIM utilise les données des API Hub'Eau Hydrométrie et Piézométrie pour simuler le débit des cours d'eau et les niveaux piézométriques via des réseaux de neurones artificiels. (#203)~~
- ~~SUBLIM est un service de prévision hydrologique automatisé à l'échelle du territoire métropolitain. (#203)~~
- ~~Les données Hub'Eau sont combinées avec des données météorologiques historiques (ERA5) et prévisionnelles (CEP/ECMWF 0.25°) pour la modélisation hydrologique. (#203)~~
- ~~Le service SUBLIM visualise les données historiques (2 ans maximum) et les prévisions au pas de temps journalier pour la majorité des stations hydrologiques et piézométriques en temps réel. (#203)~~
- ~~Le site SUBLIM permet d'accéder à la qualité de prévision des modèles (entraînement et utilisation) et à des indicateurs comme la tendance des prévisions à 10 jours. (#203)~~

### Issues sources

- **#10** caractéristiques hydrogéologiques  — L'API Qualité des nappes permet de récupérer des informations hydrogéologiques détaillées pour un code BSS, incluant les masses d'eau, contrairement à l'API Piézométrie qui était plus limitée à l'époque de l'issue. `[résolu]`
- **#19** [Toutes APIs] Multiples erreurs lors de la génération d'un client à partir de la documentation Swagger — Des erreurs dans la spécification Swagger des APIs Hub'Eau, notamment des propriétés non conformes et des noms d'objets inadaptés, empêchaient la génération correcte de clients API, particulièrement pour l'API Piézométrie. `[résolu]`
- **#22** [API Hydro] données manquantes par rapport à ADES — Un problème de données piézométriques manquantes ou en retard dans Hub'Eau par rapport à ADES a été résolu, assurant désormais une synchronisation complète et à jour des données de niveaux de nappe. `[résolu]`
- **#29** [API Piézométrie] - ajout des codes masses d'eau (requête et résultat) — L'API Piézométrie de Hub'Eau a été mise à jour pour inclure les codes, noms et URIs des masses d'eau associées aux piézomètres, améliorant ainsi les capacités de liaison des données. `[résolu]`
- **#31** API Piézométrie: Chroniques et chroniqes_tr — L'API Piézométrie chroniques a été enrichie pour inclure l'information sur la continuité des courbes et des métadonnées essentielles (producteur, nature de la mesure, profondeur de l'eau) afin de mieux valoriser les données piézométriques présentant des ruptures de suivi. `[résolu]`
- **#34** [Niveaux nappes] - Quelles unités ? — Cette issue clarifie les unités et l'interprétation des champs `niveau_nappe_eau` (mètres NGF) et `profondeur_nappe` (mètres par rapport à un repère) de l'API Piézométrie, et explique comment déterminer l'altitude du repère de mesure. `[résolu]`
- **#43** Gestion des continuités pour l'API Piézométrie — L'API Piézométrie de Hub'Eau fournit les informations de continuité des chroniques via des champs dédiés (`code_continuite`, `nom_continuite`), bien que le démonstrateur en ligne ne les affiche pas. `[résolu]`
- **#49** Bug sur l'API piézo pour chroniques — L'API Hub'Eau de piézométrie pour les chroniques (`/niveaux_nappes/chroniques`) ne permet pas d'utiliser le nouveau code BSS (`bss_id`), contrairement à l'API de chroniques transformées (`/niveaux_nappes/chroniques_tr`), et nécessite l'ancien code BSS (`code_bss`). `[en_cours]`
- **#50** Liste des stations piézométriques — L'API Piézométrie peut retourner des résultats incomplets pour les stations actives à une date récente en raison d'un délai de rafraîchissement de l'information sur la période d'activité des stations. `[résolu]`
- **#54** [Démonstrateur piézo] problème d'affichage — Le démonstrateur piézométrique a été adapté pour afficher correctement les détails des points de mesure sur les écrans de faible résolution en supprimant le graphique d'évolution. `[résolu]`
- **#59** API  Piézométrie   - bug codes bss et api station — L'API Piézométrie de Hub'Eau utilise différents paramètres (bss_id ou code_bss) pour les anciens et nouveaux codes BSS selon les endpoints (stations, chroniques historiques, chroniques temps réel), et un bug affecte la date de dernière mesure. `[en_cours]`
- **#61** [API Piezométrie] Blocage d’une requête multiorigines (Cross-Origin Request) — L'API Hub'Eau Piézométrie supporte les requêtes Cross-Origin (CORS) via l'en-tête `access-control-allow-origin: *`, et les problèmes de blocage sont probablement liés à l'implémentation client. `[résolu]`
- **#62** Utilisation de l'API dans R / Package dédié ? — Cette issue a mené au développement et à la publication du package R `hubeau` par INRAE pour interroger les APIs Hub'Eau, complété par des exemples de code R du BRGM et la mention de bugs existants dans l'API. `[résolu]`
- **#63** [API Piezométrie] Ajout d'un filtre par code réseau de mesure — L'API Piézométrie et l'API Qualité des nappes ne permettaient pas de filtrer par code réseau de mesure pour les stations, bien que l'information soit présente dans l'index sous-jacent et que la Qualité des nappes permette de filtrer par nom de réseau. `[information]`
- **#64** [API Piezometrie] Une réutilisation à référencer — Une réutilisation de l'API Piézométrie a été signalée et il a été confirmé qu'elle était déjà référencée sur la page GitHub des réutilisations de Hub'Eau, distincte de la page du site web. `[résolu]`
- **#93** API Piézométrie - aucune station depuis le 23 décembre — L'API Piézométrie présente un décalage dans la mise à jour des données de stations, ce qui peut entraîner des résultats incohérents ou nuls pour des requêtes sur des dates récentes. `[information]`
- **#96** Profondeur temporelle des données piézométriques — Cette issue clarifie la nature (brute vs. corrigée, agrégée), la profondeur temporelle et la fréquence de mise à jour des données piézométriques disponibles via les différents endpoints de l'API Hub'Eau. `[résolu]`
- **#116** [API Piézométrie] Absence de chronique depuis début juin — L'API Piézométrie peut présenter un délai dans la disponibilité des chroniques de niveaux de nappe, les données n'étant pas toujours immédiatement accessibles après la mesure. `[résolu]`
- **#130** [API Piézométrie] fonction chronique — L'API Piézométrie, endpoint `chroniques`, renvoyait une réponse vide lors de requêtes sur plusieurs `code_bss`, tandis que `chronique_tr` fonctionnait, et le problème a été résolu. `[résolu]`
- **#131** [API Piézométrie] Synchronisation des données — Les APIs Hub'Eau (Piézométrie, Hydrobiologie, Qualité des cours d'eau, Hydrométrie) manquent d'un filtre par date de mise à jour pour une synchronisation efficace des données, une fonctionnalité prévue pour l'API Hydrométrie mais pas à court terme pour la Piézométrie. `[information]`
- **#132** API Hub'Eau - Piézométrie — Une régression technique a temporairement empêché l'utilisation de multiples valeurs séparées par des virgules pour certains paramètres (ex: code_bss) sur plusieurs APIs Hub'Eau (Piézométrie, Qualité des nappes, endpoints 'stations'), mais l'anomalie a été corrigée. `[résolu]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#140**  [API Piézométrie] Proposer le format GeoJSON pour les chroniques en temps réel — L'issue demande l'ajout du support du format GeoJSON pour les chroniques en temps réel de l'API Piézométrie. `[en_cours]`
- **#144** [API Piézométrie] bug avec paramètre bbox ? — L'issue clarifie la syntaxe correcte du paramètre `bbox` pour filtrer les stations piézométriques, qui doit être une chaîne unique de coordonnées séparées par des virgules. `[résolu]`
- **#163** [API Piézométrie] Ordre de tri — L'API Piézométrie trie d'abord par `code_bss` puis applique le paramètre `sort` aux mesures de chaque station, ce qui empêche de récupérer directement la dernière mesure de plusieurs piézomètres en une seule requête. `[en_cours]`
- **#178** [API Piézométrie] Erreur dans le critère field  — Un bug a été corrigé sur l'API Piézométrie où le champ `timestamp_mesure` était nul lors de l'utilisation du paramètre `fields` sans `date_mesure`, et est maintenant correctement valorisé. `[résolu]`
- **#180** Imprécision dans la documentation API Piézo / chroniques_tr — La documentation de l'API Piézo concernant le paramètre `code_bss` indique une valeur par défaut qui s'applique uniquement à la console de test et non à l'API elle-même, où aucun `code_bss` ou `bss_id` n'est par défaut, mais le paramètre `size` a une valeur par défaut de 5000. `[information]`
- **#184** [API Hydrométrie] [API piézométrie] Erreur de connexion a hub'eau — Les API Hydrométrie et Piézométrie de Hub'Eau ont connu une indisponibilité générale avec des erreurs 500, qui a été résolue par les équipes techniques. `[résolu]`
- **#203** [Site Web] Demande de référencement sur la page "Cas d'usage". — Le projet SUBLIM utilise les APIs Hub'Eau Hydrométrie et Piézométrie, combinées à des données météorologiques, pour développer un démonstrateur de prévision hydrologique automatisée par réseaux de neurones artificiels. `[résolu]`
- **#207** [Piézométrie] Ajout du paramètre bss_id — L'API Piézométrie permet de télécharger les données de stations avec le bss_id actuel, mais le téléchargement des chroniques nécessite l'ancien code BSS, ce qui est une limitation identifiée pour évolution. `[en_cours]`
- **#230** [API piezométrie] Requête par réseaux et indices — L'issue demande l'ajout de la possibilité de requêter l'API piézométrie par code de réseau et de gérer les codes BSS en se basant uniquement sur les 10 premiers caractères pour une identification unique, tout en signalant des lacunes et confusions actuelles. `[information]`
- **#259** [API piezométrie] param date_fin_mesure au comportement pas comme attendu — Le paramètre `date_fin_mesure` de l'API Piézométrie de Hub'Eau présente un comportement incohérent et souvent exclusif basé sur le timestamp, entraînant la perte de données pour les utilisateurs et nécessitant une modification pour filtrer sur la date seule de manière inclusive. `[en_cours]`
- **#260** [API piezométrie] Ajout des CODES en plus des libellés des champs qualifiant les données — L'API Piézométrie ne fournit que les libellés longs pour certains champs de données (ex: statut, qualification), et une demande a été faite pour ajouter les codes correspondants (selon les nomenclatures SANDRE) afin de réduire le volume des exports et d'améliorer la performance. `[en_cours]`

</details>
