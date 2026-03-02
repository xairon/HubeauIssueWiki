# Qualité des nappes

> 22 issues analysées

## Guide

### Comportement actuel

L'API Qualité des nappes d'eau souterraines propose des endpoints pour les analyses et les stations de mesure (#186). Le endpoint `/stations` supporte le format GeoJSON, facilitant son intégration dans les SIG. Les coordonnées des captages d'eau potable sont floutées et remplacées par celles du chef-lieu de la commune pour des raisons réglementaires ; le champ `precision_coordonnees` (valeurs '0' pour réelles, '18' pour floutées, selon Sandre 916) indique cette précision (#270). Le filtrage des stations par `nom_reseau` est actuellement disponible (#63, #210).

### Pièges à éviter

L'API ne fournit pas les attributs 'laboratoire', 'préleveur' ni le 'support de l'analyse' (#51). Le endpoint `/analyses` ne supporte pas le format GeoJSON ; toute requête avec `format=geojson` retournera du JSON standard (#186). Une limitation de 20 000 résultats par requête (`page * size`) impose de fractionner les requêtes volumineuses (#204). Le filtrage des stations par `code_reseau` n'est pas encore implémenté, seule la recherche par `nom_reseau` est possible (#63, #210). Le champ "heure de prélèvement" est manquant, ce qui peut compliquer la comparaison avec d'autres sources et la différenciation de prélèvements multiples le même jour sur un même site (#235). L'accès aux métadonnées (années, producteurs, paramètres) par station est actuellement inefficace et un endpoint dédié est en cours de développement pour d'autres APIs avant d'être étendu aux nappes (#204).

### Bonnes pratiques

Pour pallier l'absence du 'support de l'analyse', sachez que le 'code support' est généralement '3' (eau), et peut être reconstitué à partir du 'code fraction' (ex: 3, 22, 23) (#51). En l'absence de filtrage par `code_reseau` pour les stations, utilisez des listes de codes BSS comme solution de contournement (#63). Il est recommandé de privilégier l'API Hub'Eau Qualité des nappes plutôt que le WS getData d'ADES, ce dernier étant connu pour sa lenteur et ses timeouts (#51).

### Contexte métier

Les données de qualité des eaux souterraines sont issues de la base ADES (#51, #235). Les réseaux de surveillance sont identifiables par un 'code réseau' et un 'nom de réseau', et leurs fiches sont consultables sur ades.eaufrance.fr (#63, #210). Le 'code support 3' correspond à l'eau, et les codes fraction 3, 22, 23 y sont associés (#51). Le champ `precision_coordonnees` utilise la nomenclature Sandre 916 pour indiquer la précision des coordonnées, notamment le floutage des captages AEP pour des raisons réglementaires (#270). Les utilisateurs ont besoin de métadonnées telles que les années de données, les producteurs et les paramètres analysés par station pour optimiser leurs requêtes (#204).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Qualité des nappes ne renvoie pas les attributs 'laboratoire' et 'préleveur'. (#51)
- L'API Qualité des nappes ne renvoie pas le 'support de l'analyse'. (#51)
- Le 'code support' peut être reconstitué à partir du 'code fraction' (ex: code fraction 3, 22, 23 -> code support 3). (#51)
- Le 'code support' est a priori toujours égal à 3 (eau) dans l'API Qualité des nappes. (#51)
- Le code support 3 correspond à l'eau. (#51)
- Les codes fraction 3, 22, 23 sont associés au code support 3 (eau). (#51)
- Le WS getData d'ADES est connu pour être lent et sujet aux timeouts, incitant à l'utilisation de l'API Hub'Eau Qualité des nappes. (#51)
- L'API Piézométrie ne permettait pas de filtrer les stations ou les chroniques par code_reseau. (#63)
- L'API Qualité des nappes ne permettait pas de filtrer les stations par code_reseau (mais le permettait pour les analyses). (#63)
- L'API Qualité des nappes permettait de filtrer les stations par nom_reseau. (#63)
- Les informations sur les réseaux de mesure (code, mnémo, nom) sont présentes dans l'index sous-jacent de Hub'Eau. (#63)
- L'ajout de filtres par code_reseau et l'inclusion des détails du réseau dans les réponses API étaient envisagés mais non prioritaires. (#63)
- La base ADES permet de consulter et d'extraire les données par code_reseau. (#63)
- Les réseaux de mesure ont des fiches consultables publiquement sur ades.eaufrance.fr (ex: 0400000020 pour le réseau Bretagne). (#63)
- Le filtrage par code_reseau est jugé plus pratique que par nom_reseau. (#63)
- Les utilisateurs peuvent utiliser des listes de codes BSS comme solution de contournement en l'absence de filtrage par réseau. (#63)
- Le format GeoJSON n'est pas implémenté pour le endpoint `/analyses` de l'API Qualité des nappes d'eau souterraines. (#186)
- L'utilisation du paramètre `format=geojson` sur le endpoint `/analyses` de l'API Qualité des nappes d'eau souterraines entraîne une réponse au format JSON standard, et non GeoJSON. (#186)
- Le endpoint `/stations` de l'API Qualité des nappes d'eau souterraines supporte le format GeoJSON. (#186)
- L'API Qualité des nappes d'eau souterraines fournit des données d'analyses et de stations. (#186)
- L'API Qualité des nappes peut nécessiter de nombreuses requêtes pour obtenir des métadonnées (années, producteurs, paramètres) par station, pouvant entraîner des résultats vides. (#204)
- Il existe une limitation à 20 000 résultats par requête sur l'API Qualité des nappes, nécessitant le fractionnement des requêtes. (#204)
- Un nouveau endpoint "_parametres" est prévu pour les APIs de qualité (rivières, nappes, eau potable) afin d'optimiser les interrogations. (#204)
- Le endpoint "_parametres" sera d'abord ajouté à l'API Qualité des cours d'eau. (#204)
- Les remarques de l'utilisateur concernant les métadonnées (années, producteurs, paramètres) seront prises en compte pour l'implémentation du endpoint "_parametres" sur l'API Qualité des nappes. (#204)
- Les utilisateurs de l'API Qualité des nappes ont besoin de connaître les années de données disponibles, les producteurs d'analyses et les paramètres analysés pour chaque station de mesure afin d'optimiser leurs requêtes. (#204)
- L'API Qualité des nappes d'eau souterraines ne permet pas actuellement de filtrer les données par 'code réseau'. (#210)
- Le filtrage par 'nom de réseau' est actuellement disponible dans l'API Qualité des nappes d'eau souterraines. (#210)
- Une demande d'évolution a été enregistrée pour ajouter le filtrage par 'code réseau' sur les deux endpoints de l'API Qualité des nappes d'eau souterraines. (#210)
- Les réseaux de surveillance de la qualité des nappes d'eau souterraines sont identifiables par un 'code réseau' en plus d'un 'nom de réseau'. (#210)
- Le champ "heure de prélèvement" n'est pas exposé dans l'API Hub'Eau 'Qualité des Nappes' pour les données d'analyses issues de la banque ADES. (#235)
- Le champ "heure de prélèvement" est présent sur la plateforme ADES pour les données d'analyses. (#235)
- Les exports SISE-EAUX (ARS) incluent le champ "heure de prélèvement". (#235)
- L'absence du champ "heure de prélèvement" dans l'API Hub'Eau empêche une comparaison précise avec les données SISE-EAUX. (#235)
- Plusieurs prélèvements peuvent avoir lieu le même jour sur un même captage ou station. (#235)
- Sans l'heure de prélèvement, les prélèvements multiples du même jour sur un même site peuvent être fusionnés ou confondus. (#235)
- L'heure de prélèvement est cruciale pour la traçabilité et la reconstitution fidèle des séries de mesures, notamment pour les analyses de dépassements, le suivi qualité et les diagnostics temporels. (#235)
- Les coordonnées des points d'eau retournées par les endpoints 'Analyses' et 'Stations' de l'API Qualité des nappes sont désormais floutées lorsqu'elles concernent un captage d'eau potable. (#270)
- Le floutage des coordonnées consiste à remplacer les coordonnées réelles du point d'eau par les coordonnées du chef-lieu de la commune sur laquelle le captage est implanté. (#270)
- Un nouveau champ 'precision_coordonnees' est disponible pour indiquer l'état de floutage d'un point d'eau. (#270)
- La valeur '0' pour le champ 'precision_coordonnees' indique des coordonnées réelles (précision inconnue). (#270)
- La valeur '18' pour le champ 'precision_coordonnees' indique des coordonnées floutées (coordonnées du chef-lieu de la commune). (#270)
- Le floutage des coordonnées des captages d'eau potable est appliqué en application des réglementations françaises et européennes. (#270)
- Le champ 'precision_coordonnees' repose sur la nomenclature Sandre 916. (#270)

### Historique des problèmes résolus

- ~~L'opération `qualite_nappes/stations` de l'API Qualité des nappes permet de récupérer des informations détaillées sur un point d'eau à partir de son code BSS. (#10)~~
- ~~L'API Qualité des nappes fournit des informations complètes sur les points d'eau de type qualitomètre, incluant des données géographiques, administratives et hydrogéologiques (ex: masses d'eau, entités BDLISA). (#10)~~
- ~~L'API Piézométrie fournissait, au moment de l'issue, moins d'informations sur les points d'eau (notamment les masses d'eau) que l'API Qualité des nappes. (#10)~~
- ~~Un code BSS (BSS_ID) identifie un point d'eau souterraine et peut être utilisé pour interroger ses caractéristiques. (#10)~~
- ~~Les points d'eau souterraine sont associés à des masses d'eau (codes_masse_eau_rap, codes_masse_eau_edl) et des entités hydrogéologiques BDLISA. (#10)~~
- ~~Les données de qualité des eaux souterraines proviennent de la base ADES. (#10)~~
- ~~L'API Qualité des nappes a rencontré un bug où l'attribut `count` variait pour une même requête. (#14)~~
- ~~Ce problème était dû à une désynchronisation des multiples copies de données utilisées par Hub'Eau pour augmenter la sécurité et les temps de réponse. (#14)~~
- ~~Le problème de désynchronisation des données a été corrigé par l'équipe Hub'Eau, assurant des résultats consistants. (#14)~~
- ~~L'attribut 'next' de la pagination est généré avec une URL même lorsque la page de données est vide, contrairement à la documentation qui indique 'null'. (#15)~~
- ~~Ce comportement est lié à des inconsistances dans le 'count' total des résultats renvoyés par l'API. (#15)~~
- ~~Lorsque le 'count' change sur la dernière page, l'API peut générer un 'next' infini et un 'last' nul. (#15)~~
- ~~Contournement possible : vérifier que `page * size` ne dépasse pas le 'count' obtenu lors du premier appel. (#15)~~
- ~~Contournement possible : utiliser de grandes valeurs pour 'size' (5000-20000) pour réduire le nombre de pages et l'impact des inconsistances de 'count'. (#15)~~
- ~~L'utilisation de très grandes valeurs pour 'size' peut potentiellement entraîner des timeouts. (#15)~~
- ~~L'API Qualité des nappes peut retourner un nombre total de résultats (count) incohérent pour une même requête si le paramètre size est modifié. (#42)~~
- ~~Les données Hub'Eau sont dupliquées sur plusieurs serveurs pour la tolérance aux pannes et l'accélération des réponses. (#42)~~
- ~~Des désynchronisations d'index entre les serveurs de données peuvent entraîner des incohérences dans les résultats des requêtes (ex: count incorrect). (#42)~~
- ~~La résolution des problèmes de désynchronisation d'index implique une ré-indexation complète des données. (#42)~~
- ~~Les stations de suivi des nappes sont identifiées par un bss_id (code BSS). (#42)~~
- ~~Les analyses de qualité des nappes peuvent être filtrées par code_param. (#42)~~
- ~~L'API Hub'Eau Qualité des nappes (endpoint /analyses) dispose d'un filtre `date_debut_prelevement` qui permet de récupérer les analyses dont la date de début de prélèvement est égale ou postérieure à la date spécifiée. (#52)~~
- ~~Les filtres `date_max_maj` et `date_min_maj` de l'API Qualité des nappes se réfèrent à la date de mise à jour des données et non à la date de prélèvement. (#52)~~
- ~~L'API Qualité des nappes ne propose pas de filtres `date_debut_prelevement_min` ou `date_debut_prelevement_max`. (#52)~~
- ~~Il est possible de filtrer les données de qualité des eaux souterraines par la date de début de prélèvement pour n'obtenir que les données les plus récentes ou celles d'une période spécifique. (#52)~~
- ~~La multiplication des paramètres `page` et `size` dans les requêtes Hub'Eau ne peut excéder 20 000 enregistrements (profondeur d'accès aux résultats). (#57)~~
- ~~Dépasser la limite `page * size > 20000` entraîne une erreur `InvalidRequest` avec le code `ValidatePageDepth`. (#57)~~
- ~~Cette limite est imposée pour ne pas surcharger le serveur. (#57)~~
- ~~Pour récupérer plus de 20 000 enregistrements, il faut découper la requête en utilisant des critères plus discriminants, comme `date_debut_prelevement`. (#57)~~
- ~~L'API peut retourner des URLs erronées dans les attributs 'last' et 'next' lorsque la limite `page * size` est dépassée. (#57)~~
- ~~Certaines stations (ex: BSS000LGJB) peuvent avoir un très grand nombre de mesures (plus de 20 000). (#57)~~
- ~~L'API qualite_nappes pouvait retourner un nombre variable d'enregistrements pour une même requête exécutée à quelques secondes d'intervalle. (#79)~~
- ~~L'anomalie de consistance des résultats pour l'API qualite_nappes a été corrigée. (#79)~~
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
- ~~Le paramètre _format_=geojson permet d'obtenir des données au format GeoJSON via les API Hub'Eau. (#149)~~
- ~~Le format GeoJSON n'est pas implémenté pour toutes les API Hub'Eau ; dans ce cas, la syntaxe _format_=geojson retourne des données au format JSON standard. (#149)~~
- ~~Seules les données GeoJSON diffusées par certaines API Hub'Eau peuvent être chargées directement dans QGIS. (#149)~~
- ~~Sans automatisation des échanges de données, les couches chargées dans QGIS sont limitées à 20 000 entités. (#149)~~
- ~~L'utilisation des API Hub'Eau avec QGIS est un cas d'usage pour l'intégration de données hydrologiques dans un SIG. (#149)~~
- ~~Les données de qualité des nappes peuvent être filtrées par numéro de département (ex: num_departement=23). (#149)~~
- ~~L'argument 'fields' de l'API Qualité des nappes (endpoint /analyses) est une fonctionnalité expérimentale. (#214)~~
- ~~L'argument 'fields' de l'API Qualité des nappes (endpoint /analyses) nécessite l'utilisation des noms de champs exacts pour être pris en compte. (#214)~~
- ~~Des noms de champs incorrects (ex: 'code_parametre', 'resultat_numerique', 'date_prelevement') entraînent l'ignorance de l'argument 'fields' et le retour de toutes les données. (#214)~~
- ~~Les noms de champs corrects pour l'exemple donné sont 'code_param', 'resultat' et 'date_debut_prelevement'. (#214)~~
- ~~Les APIs Hub'Eau ne fournissent pas de concentrations journalières agrégées à l'échelle départementale pour des paramètres spécifiques comme le métolachlore ESA. (#220)~~
- ~~Le rôle de Hub'Eau est de donner accès aux données brutes ou semi-brutes, et non de fournir des analyses hydrologiques complexes ou des agrégations de données à l'échelle départementale. (#220)~~
- ~~L'estimation d'une concentration journalière globale pour un paramètre (ex: métolachlore ESA) sur un département entier à partir de mesures de stations multiples nécessite une méthodologie spécifique. (#220)~~
- ~~La simple moyenne des concentrations mesurées par toutes les stations un jour donné n'est pas nécessairement la méthode la plus pertinente pour estimer une concentration départementale globale. (#220)~~
- ~~Pour les questions méthodologiques concernant l'interprétation et l'agrégation des données de qualité de l'eau (eaux souterraines ou superficielles), il convient de contacter directement les équipes expertes d'Ades (eaux souterraines) ou de Naïades (eaux superficielles). (#220)~~
- ~~L'API Qualité des nappes peut être fréquemment inaccessible (1 à 3 fois par semaine) pendant plusieurs heures (4 à 5 heures). (#231)~~
- ~~Des sollicitations intensives et des collectes massives de données à un rythme soutenu dégradent les performances de l'API Qualité des nappes. (#231)~~
- ~~Hub'Eau peut bloquer des adresses IP en cas de sollicitations excessives dégradant l'API. (#231)~~
- ~~L'API Qualité des nappes est utilisée pour des requêtes 'lourdes' et longues à exécuter. (#231)~~
- ~~Le changelog de l'API Qualité des nappes pour la version 1.3.0 était initialement manquant. (#269)~~
- ~~La documentation de l'API Qualité des nappes a été mise à jour pour inclure les changements de la version 1.3.0. (#269)~~
- ~~La version 1.3.0 de l'API Qualité des nappes introduit le floutage des coordonnées des captages AEP. (#269)~~
- ~~Le floutage des coordonnées des captages AEP s'effectue au niveau du chef-lieu de la commune. (#269)~~
- ~~L'API Hub'Eau 'Qualité des nappes' peut subir des chargements partiels de données depuis ADES suite à des anomalies dans les traitements d'alimentation. (#271)~~
- ~~Ces anomalies peuvent entraîner une sous-estimation significative du nombre d'analyses disponibles via l'API par rapport à la source ADES. (#271)~~
- ~~Les problèmes de volumétrie sont généralement résolus après correction des traitements d'alimentation. (#271)~~
- ~~Les données de qualité des nappes de Hub'Eau sont issues du système ADES. (#271)~~
- ~~Les points de mesure des nappes sont identifiés par un code BSS (ex: BSS000JGAH). (#271)~~
- ~~La volumétrie des analyses pour un point BSS peut évoluer dans le temps (ex: pour BSS000JGAH, de 80 000 à plus de 100 000 analyses en un an). (#271)~~

### Issues sources

- **#10** caractéristiques hydrogéologiques  — L'API Qualité des nappes permet de récupérer des informations hydrogéologiques détaillées pour un code BSS, incluant les masses d'eau, contrairement à l'API Piézométrie qui était plus limitée à l'époque de l'issue. `[résolu]`
- **#14** [API Qualité des nappes d'eau souterraine] Nombre de résultats aléatoire — L'API Qualité des nappes a connu un bug où l'attribut `count` variait pour une même requête à cause d'une désynchronisation des copies de données, problème qui a été résolu. `[résolu]`
- **#15** L'attribut 'next' est toujours généré même sans page suivante — L'API Hub'Eau génère un attribut 'next' non nul même sans page suivante, un comportement lié à des inconsistances de comptage, avec des contournements possibles. `[résolu]`
- **#42** [API Qualité Nappe] — Cette issue révèle que l'API Qualité des nappes peut présenter des incohérences dans le count des résultats dues à des désynchronisations d'index entre les serveurs de données, résolues par une ré-indexation. `[résolu]`
- **#51** API Qualité eau souterraine — L'API Qualité des nappes ne fournit pas les champs 'laboratoire', 'préleveur' ni le 'support de l'analyse', ce dernier pouvant être reconstitué via le 'code fraction' et étant généralement 'eau' (code 3). `[information]`
- **#52** API Qualité eau souterraine — L'API Hub'Eau Qualité des nappes permet de filtrer les analyses par date de début de prélèvement (`date_debut_prelevement`) pour récupérer les données postérieures à une date donnée, évitant ainsi de télécharger tout l'historique. `[résolu]`
- **#57** [API qualite_nappes] Erreur avec la dernière page — L'API Hub'Eau `qualite_nappes` (et potentiellement d'autres) impose une limite de 20 000 enregistrements pour le produit `page * size`, nécessitant de découper les requêtes volumineuses avec des critères plus discriminants. `[résolu]`
- **#63** [API Piezométrie] Ajout d'un filtre par code réseau de mesure — L'API Piézométrie et l'API Qualité des nappes ne permettaient pas de filtrer par code réseau de mesure pour les stations, bien que l'information soit présente dans l'index sous-jacent et que la Qualité des nappes permette de filtrer par nom de réseau. `[information]`
- **#79** [api-qualite-nappes] nombre de résultats différents avec la même requête — L'API qualité-nappes présentait une anomalie où le nombre de résultats variait pour une même requête, problème qui a été résolu pour garantir la consistance des données. `[résolu]`
- **#132** API Hub'Eau - Piézométrie — Une régression technique a temporairement empêché l'utilisation de multiples valeurs séparées par des virgules pour certains paramètres (ex: code_bss) sur plusieurs APIs Hub'Eau (Piézométrie, Qualité des nappes, endpoints 'stations'), mais l'anomalie a été corrigée. `[résolu]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#149** Tutoriel utilisation des API avec QGIS information #2 by tvilmus was closed on Jul 5, 2022 — Cette issue explique comment obtenir des données GeoJSON via les API Hub'Eau en utilisant le paramètre _format_ pour une intégration dans QGIS, tout en précisant les limitations de ce format et du volume de données. `[résolu]`
- **#186** [API Qualité des nappes d'eau souterraines] Problème de connexion sur QGIS — Le endpoint `/analyses` de l'API Hub'Eau Qualité des nappes d'eau souterraines ne supporte pas le format GeoJSON et retourne du JSON même si le paramètre `format=geojson` est spécifié. `[information]`
- **#204** [API Qualité des nappes d'eau souterraines] Ajout d'élément à la liste des stations de mesure — L'issue met en évidence le besoin de métadonnées (années, producteurs, paramètres) pour les stations de qualité des nappes afin d'optimiser les requêtes et contourner la limite de 20 000 résultats, et Hub'Eau prévoit un nouveau endpoint "_parametres" pour les APIs de qualité, d'abord sur les cours d'eau. `[en_cours]`
- **#210** [API Qualité des nappes d'eau souterraines] Filtre par code réseau et endpoint réseau — L'API Qualité des nappes d'eau souterraines ne permet pas de filtrer par code réseau, seulement par nom de réseau, et une évolution est demandée pour ajouter ce filtre. `[en_cours]`
- **#214** [API Qualité des nappes] - argument fields non pris en compte (fonctionnalité expérimentale) — L'argument 'fields' de l'API Hub'Eau Qualité des nappes (endpoint /analyses) est une fonctionnalité expérimentale qui requiert l'utilisation des noms de champs exacts pour fonctionner correctement. `[résolu]`
- **#220** Question sur le calcul de la concentration journalière du métolachlore ESA du departement de Finistère de toutes les stations present. — Hub'Eau ne fournit pas de concentrations journalières agrégées à l'échelle départementale et redirige vers Ades ou Naïades pour les questions méthodologiques d'interprétation des données de qualité de l'eau. `[résolu]`
- **#231** [API Qualité des Nappes] Données fréquemment inaccessibles — L'API Qualité des nappes subit des indisponibilités fréquentes et des dégradations de performance dues à des sollicitations intensives, pouvant entraîner des blocages d'IP. `[résolu]`
- **#235** [API Qualité des Nappes] Manque du champ “heure de prélèvement” dans les données venant de ADES — L'API Hub'Eau 'Qualité des Nappes' ne fournit pas le champ "heure de prélèvement" des données ADES, ce qui limite la comparaison avec SISE-EAUX, la différenciation des prélèvements journaliers et la traçabilité des mesures. `[en_cours]`
- **#269** [API Qualité des nappes d'eau souterraine] - changelog manquant sur la 1.3.0 — La version 1.3.0 de l'API Qualité des nappes a introduit le floutage des coordonnées des captages AEP au niveau du chef-lieu de la commune, et la documentation a été mise à jour pour refléter ce changement. `[résolu]`
- **#270** [API Qualité des Nappes] Floutage des coordonnées de captages — L'API Qualité des nappes floute désormais les coordonnées des captages d'eau potable, les remplaçant par celles du chef-lieu de la commune, et un champ 'precision_coordonnees' indique l'état de floutage. `[information]`
- **#271** [Qualité des nappes] Incohérence de volumétrie entre Hub'Eau et ADES — L'API Hub'Eau 'Qualité des nappes' a rencontré une incohérence de volumétrie de données pour la station BSS000JGAH due à une anomalie dans les traitements d'alimentation depuis ADES, mais la situation a été rétablie. `[résolu]`

</details>
