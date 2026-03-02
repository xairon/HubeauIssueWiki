# Poisson

> 17 issues analysées

## Guide

### Comportement actuel

L'API Hub'Eau "Poisson" est actuellement en version v1, ce qui a entraîné des changements potentiellement incompatibles avec les intégrations antérieures (#20). Elle a été enrichie de nouveaux endpoints pour diffuser les résultats des indicateurs IPR et IPR+, les données environnementales et contextuelles des opérations, ainsi que les données descriptives des stations de mesure (#159). Les données sont mises à jour quotidiennement depuis la base ASPE (#181). Le paramètre `size` permet de contrôler le nombre de résultats retournés, et des filtres comme `code_departement` peuvent être appliqués aux exports JSON et CSV (#226). L'endpoint `/etat_piscicole/operations` est couramment utilisé et inclut des informations sur l'opérateur via `operateur_libelle_aspe` (#223). La future API Hub'Eau "Hydrobiologie" est prévue pour diffuser des données sur les poissons, macroinvertébrés, diatomées et macrophytes, et permettra la recherche par nom d'espèce (#33).

### Pièges à éviter

L'API Poisson ne permet pas de récupérer directement les données d'un poisson par son nom, mais uniquement par son `code_espece_poisson` (#33). Les exports CSV directs de l'API sont partiels, limités à 5000 lignes par défaut, nécessitant l'utilisation du paramètre `size` ou d'outils gérant la pagination (#226). Il existe des écarts de complétude des données entre l'API Hub'Eau Poisson et la base ASPE, en raison de règles de gestion spécifiques (données en cours de saisie, règles propres à certains bassins) (#223, #226). Certaines données ASPE, notamment celles sous maîtrise d'ouvrage de l'Agence de l'eau Loire-Bretagne, ne sont diffusées qu'après validation de niveau 2 ou si elles datent de plus d'un an (#181). Les champs de coordonnées (`coordonnee_x_point_prelevement`, `coordonnee_y_point_prelevement`) sont temporairement diffusés avec une précision réduite (une décimale au lieu de deux) en raison d'une anomalie en cours de correction (#251). Enfin, l'endpoint `etat_piscicole/operations` peut présenter une incohérence dans les données de faciès, où le nombre de libellés ne correspond pas toujours au nombre de valeurs des attributs numériques associés, ce qui peut mener à des erreurs d'interprétation (#275).

### Bonnes pratiques

Pour rechercher des données par nom d'espèce, utilisez l'endpoint `/code_espece_poisson` pour obtenir la correspondance entre nom et code OFB, ou l'API Référentiel du SANDRE pour des correspondances plus complexes (nom latin, nom commun) (#33). Utilisez le code OFB (champ "code") pour interroger l'endpoint `/poissons`, et non le code SANDRE (champ "code_taxon") (#33). Pour les utilisateurs R, le package `hubeau` (disponible sur le CRAN) est recommandé car il gère automatiquement la pagination et simplifie les requêtes (`get_poisson_operation(...)`) (#137, #226). En cas de données manquantes ou d'incohérences, consultez la page d'accueil de l'API pour le périmètre des données ASPE diffusées et contactez le service gestionnaire de la base ASPE si nécessaire (#181).

### Contexte métier

L'API Hub'Eau Poisson est alimentée par la base de données ASPE (Application de Suivi des Pêches Électriques) de l'OFB, qui est la source des données de pêche électrique (#148, #181, #226). Les données ASPE sont également consultables sur le site aspe.eaufrance.fr, et l'API fonctionne sur une copie de cette base (#148). L'API expose des informations sur 195 espèces de poissons, les opérations de pêche électrique, les stations de mesure, et des indicateurs comme l'IPR et l'IPR+ (#33, #159, #223). Les "faciès" décrivent des zones homogènes d'un cours d'eau avec des attributs quantitatifs (profondeur, granulométrie, végétation), essentiels pour l'interprétation des opérations piscicoles (#275). Les codes OFB sont les identifiants primaires des espèces dans l'API Poisson, distincts des codes SANDRE (#33). La saisie des données dans ASPE est effectuée par les producteurs de données, ce qui peut entraîner des variations dans la complétude des données nationales (#226).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Hub'Eau Poisson est passée en version v1, entraînant des changements incompatibles avec les intégrations précédentes. (#20)
- Le démonstrateur `poissons.html` a cessé de fonctionner suite à la mise à jour de l'API Poisson vers la v1. (#20)
- L'API Poisson a été enrichie de trois nouveaux endpoints. (#159)
- L'API Poisson diffuse désormais les résultats des indicateurs IPR et IPR+. (#159)
- L'API Poisson diffuse désormais les données environnementales et contextuelles des opérations. (#159)
- L'API Poisson diffuse désormais les données descriptives des stations de mesure. (#159)
- Les indicateurs IPR et IPR+ sont disponibles avec leurs métriques associées. (#159)
- Les données environnementales et contextuelles des opérations sont désormais accessibles via l'API Poisson. (#159)
- Les données descriptives des stations de mesure sont désormais accessibles via l'API Poisson. (#159)
- L'export CSV direct de l'API Hub'Eau Poisson (ex: /operations.csv) est partiel et ne retourne qu'un maximum de 5000 lignes par défaut. (#226)
- Le paramètre `size` peut être utilisé pour contrôler le nombre de résultats retournés par l'API (ex: `?size=10`). (#226)
- Les filtres (ex: `code_departement=38`) peuvent être appliqués aussi bien aux exports JSON qu'aux exports CSV de l'API Hub'Eau Poisson. (#226)
- Le package R `hubeau` (disponible sur le CRAN) est recommandé pour les utilisateurs R car il gère automatiquement la pagination des résultats de l'API. (#226)
- Les données de l'API Hub'Eau Poisson proviennent de la base de données ASPE (Application de Suivi des Pêches Électriques). (#226)
- Il existe des écarts de complétude des données (nombre d'opérations, producteurs de données) entre l'API Hub'Eau Poisson, les exports directs d'ASPE et les compilations locales (ex: FDAAPPMA 38). (#226)
- Environ 10 opérations sur 625 disponibles dans ASPE pour le département 38 ne sont pas diffusées via Hub'Eau en raison de règles de gestion spécifiques (données en cours de saisie, règles propres à certains bassins). (#226)
- Seuls les producteurs de données saisissent directement leurs informations dans ASPE, soit manuellement, soit via des imports en masse. (#226)
- Les comptes rendus de pêche (CR de pêche) transmis aux DDT et à l'OFB ne sont pas systématiquement intégrés dans la base ASPE, ce qui limite la centralisation nationale des données. (#226)
- Les utilisateurs expriment le besoin d'intégrer dans ASPE des données partielles (ex: sans code SANDRE, ou uniquement des informations globales) et des opérations spécifiques comme les pêches de sauvegarde/sauvetage qui ne rentrent pas dans les formats standards actuels. (#226)
- Un portail cartographique pour les données ASPE et des liens entre les bases ASPE et FNPF - WebPDPG sont à l'étude. (#226)
- Les champs `coordonnee_x_point_prelevement` et `coordonnee_y_point_prelevement` de l'API Poisson sont temporairement diffusés avec une seule décimale de précision au lieu de deux. (#251)
- L'anomalie affectant la précision des coordonnées est en cours de correction par l'équipe Aspe. (#251)
- La précision des coordonnées géographiques des points de prélèvements est temporairement réduite dans les données de l'API Poisson. (#251)
- L'API Hub'Eau Poisson (endpoint `etat_piscicole/operations`) peut retourner des listes de faciès (ex: `facies_libelle_type`) dont le nombre d'éléments est supérieur au nombre d'éléments des attributs numériques associés (ex: `facies_profondeur_moyenne`), indiquant une incohérence des données. (#275)
- Cette incohérence affecte tous les champs relatifs aux faciès, notamment `facies_profondeur_moyenne`, `facies_importance_relative`, `facies_code_granulo_dominante`, `facies_libelle_granulo_dominante`, `facies_vegetation_dominante`, et `facies_pourcentage_recouvrement_vegetation`. (#275)
- L'équipe Hub'eau a reproduit le comportement et a ouvert un ticket interne pour corriger la cohérence des données exposées par l'API. (#275)
- Les données d'opérations piscicoles incluent des informations sur les 'faciès', qui sont des zones homogènes d'un cours d'eau caractérisées par leur type (ex: 'Courant', 'Plat', 'Profonds') et des attributs quantitatifs (profondeur moyenne, importance relative, granulométrie dominante, végétation dominante, etc.). (#275)
- Une opération piscicole peut ne pas avoir de données relevées pour tous les types de faciès potentiellement listés dans les libellés. (#275)

### Historique des problèmes résolus

- ~~L'API Poisson contraint la requête des stations par espèce et celle des poissons par station, empêchant l'importation de résultats pour plusieurs stations ou espèces simultanément. (#1)~~
- ~~L'API Poisson ne permet pas de distinguer les présences par opération (date de pêche) pour les lieux de pêche. (#1)~~
- ~~L'API Poisson ne permet pas d'afficher l'ensemble des stations pour les poissons avec leurs coordonnées. (#1)~~
- ~~L'API Poisson ne fournit pas directement les effectifs et poids par espèce et par opération avec les coordonnées de station, date de pêche, cours d'eau, protocole et code espèce dans une seule requête. (#1)~~
- ~~Des stations de pêche (notamment 4411022 à 4411033) sont mal géoréférencées pour l'anguille européenne. (#1)~~
- ~~Pour l'analyse de l'évolution de la répartition et des effectifs d'espèces, il est nécessaire de disposer des présences par opération (date de pêche) et des coordonnées de toutes les stations. (#1)~~
- ~~Les données souhaitées pour l'analyse des poissons incluent les effectifs et poids par espèce et par opération, avec les informations de station (coordonnées, cours d'eau, protocole) et la date de pêche. (#1)~~
- ~~Avant correction, le format des dates dans les réponses GEOJSON de l'API Poisson était un timestamp entier (ex: "589593600000"), tandis que le format JSON standard était "YYYY-MM-DD" (ex: "1988-09-07"). (#3)~~
- ~~Cette incohérence de format de date entre JSON et GEOJSON pour l'API Poisson a été identifiée comme un bug. (#3)~~
- ~~Le bug concernant le format des dates dans les réponses GEOJSON de l'API Poisson a été corrigé. (#3)~~
- ~~Les données de la BDMAP (Base de Données des Milieux Aquatiques et de la Pêche) contiennent les résultats de pêche par espèce. (#3)~~
- ~~Ces données peuvent être utilisées pour analyser l'évolution de la répartition des espèces de poissons. (#3)~~
- ~~L'API Poissons a été mise à jour en version 1. (#4)~~
- ~~Les attributs 'Méthode de prospection', 'Moyen de Prospection' et 'Nombre de passages' ont été ajoutés à l'API Poissons. (#4)~~
- ~~L'interprétation des résultats de pêche électrique nécessite de distinguer les protocoles de pêche (méthode, moyen, nombre de passages). (#4)~~
- ~~La BDMAP (Banque de Données sur les Milieux Aquatiques et la Pêche) est une source de données de pêche incluant des détails sur les protocoles. (#4)~~
- ~~L'API Poissons est désormais alimentée par la banque ASPE de l'OFB (Office Français de la Biodiversité). (#4)~~
- ~~L'API Poisson (opérations code_espece_poisson et poissons) ne remontait pas le nom_commun pour certains codes d'espèces (BLN, LPX, ATH, COR) et genres (PHX, GOX, BBX, CAX). (#30)~~
- ~~Le champ nom_poisson était vide ("") pour ces codes avant correction. (#30)~~
- ~~La correction a été appliquée pour les opérations code_espece_poisson et poissons, ajoutant les noms communs manquants. (#30)~~
- ~~Pour les codes correspondant à des genres (PHX, GOX, BBX, CAX), le nom_commun reste vide, le nom_latin étant utilisé. (#30)~~
- ~~Les codes d'espèces BLN, LPX, ATH, COR correspondent respectivement à Blageon, Lamproie, Athérine, Corégone. (#30)~~
- ~~Les codes PHX, GOX, BBX, CAX correspondent à des genres pour lesquels l'espèce n'a pas pu être déterminée. (#30)~~
- ~~Pour les genres, le nom commun n'est pas fourni, seul le nom latin est pertinent. (#30)~~
- ~~L'API Hub'Eau "Poisson" (endpoint `/poissons`) ne permet pas de récupérer les données d'un poisson par son nom, seulement par son `code_espece_poisson`. (#33)~~
- ~~L'endpoint `/code_espece_poisson` de l'API "Poisson" permet d'obtenir la liste des correspondances entre codes OFB, codes SANDRE, noms latins et français des espèces. (#33)~~
- ~~Le code à utiliser dans l'endpoint `/poissons` est le code OFB (champ "code") et non le code SANDRE (champ "code_taxon"). (#33)~~
- ~~La future API Hub'Eau "Hydrobiologie" permettra d'interroger les données par le nom de l'espèce. (#33)~~
- ~~L'API Référentiel du SANDRE (`api.sandre.eaufrance.fr/referentiels/v1/apt.json`) peut être utilisée pour faire la correspondance nom-code. (#33)~~
- ~~Avec l'API SANDRE, on peut filtrer par nom latin (`NomLatinAppelTaxon`) pour obtenir le code OFB (sous `CodeAlternatifAp` où `OrgCdAlternatif="ASPE"`). (#33)~~
- ~~Avec l'API SANDRE, on peut filtrer par nom commun (`//LbNomCommunAppelTaxon`) en utilisant une expression XPath dans le paramètre `filter`. (#33)~~
- ~~L'endpoint `/code_espece_poisson` répertorie 195 espèces de poissons. (#33)~~
- ~~Les codes OFB sont utilisés par l'API Hub'Eau "Poisson" pour identifier les espèces. (#33)~~
- ~~La future API Hub'Eau "Hydrobiologie" diffusera des données sur les poissons, les macroinvertébrés, les diatomées et les macrophytes. (#33)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~
- ~~L'API Poisson v1.0 peut présenter un décalage de données par rapport à la source ASPE officielle (aspe.eaufrance.fr). (#148)~~
- ~~L'API Poisson fonctionne sur une copie de la base de données ASPE. (#148)~~
- ~~La chaîne d'alimentation des données de l'API Poisson a nécessité une vérification et une actualisation manuelle. (#148)~~
- ~~Une évolution de l'API Poisson est en préparation, incluant trois endpoints supplémentaires. (#148)~~
- ~~La chaîne d'alimentation de l'API Poisson sera améliorée lors de cette évolution. (#148)~~
- ~~Les mises à jour de la base de données ASPE pour l'API Poisson ne sont pas encore entièrement automatisées ou régulières. (#148)~~
- ~~Les données ASPE (Action de Surveillance Piscicole de l'Environnement) sont disponibles via l'API Poisson de Hub'Eau. (#148)~~
- ~~Les données ASPE sont également consultables sur le site aspe.eaufrance.fr. (#148)~~
- ~~Il peut exister une divergence temporelle entre les données ASPE disponibles sur le site officiel et celles exposées par l'API Hub'Eau. (#148)~~
- ~~La mise à jour des données Hub'eau depuis la base ASPE est programmée quotidiennement. (#181)~~
- ~~Le traitement de mise à jour des données Hub'eau depuis la base ASPE peut être bloqué, entraînant un retard dans la disponibilité des données. (#181)~~
- ~~Le périmètre des données ASPE diffusées via l'API sera précisé sur la page d’accueil de l’API. (#181)~~
- ~~La base ASPE est la source des données de l'API Poissons. (#181)~~
- ~~Les données de certaines opérations ASPE sont soumises à des contrôles avant leur diffusion via Hub'Eau. (#181)~~
- ~~Les données ASPE sous maîtrise d'ouvrage de l’agence de l’eau Loire-Bretagne (AELB) doivent être validées niveau 2 ou datées de plus d'un an pour être diffusées via Hub'Eau. (#181)~~
- ~~Si une opération ASPE est sous maîtrise d'ouvrage AELB, validée niveau 1 et réalisée l'année en cours, elle ne sera pas diffusée via Hub'Eau tant qu'elle n'est pas validée niveau 2 ou datée de plus d'un an. (#181)~~
- ~~En cas de données manquantes, il est conseillé de contacter le service gestionnaire de la base ASPE. (#181)~~
- ~~L'API Poisson (endpoint /etat_piscicole/operations) est interrogée avec le paramètre code_departement. (#223)~~
- ~~Une potentielle incomplétude des données d'opérations de pêche électrique est constatée via l'API par rapport à une autre source (ASPE). (#223)~~
- ~~La question est posée de l'existence de restrictions de données diffusées par l'API Poisson. (#223)~~
- ~~Le script R fourni illustre l'utilisation des librairies httr et jsonlite pour interroger l'API, parser le JSON et convertir les colonnes de type liste en chaînes de caractères. (#223)~~
- ~~Les données concernent les opérations de pêche électrique. (#223)~~
- ~~ASPE est une source de référence pour les données d'opérations de pêche électrique, potentiellement plus complète que l'API Hub'Eau pour certains cas. (#223)~~
- ~~Le département de l'Isère est identifié par le code 38. (#223)~~
- ~~Les données incluent des informations sur l'opérateur via la colonne operateur_libelle_aspe. (#223)~~
- ~~La valeur du champ objectifs_operations dans l'API Poisson était tronquée dans sa définition et dans le Swagger. (#255)~~
- ~~Le libellé tronqué pour le champ objectifs_operations dans l'API Poisson a été corrigé. (#255)~~
- ~~Le code 'RNSORMCE' pour le champ objectifs_operations dans l'API Poisson correspond à 'Réseau National de Suivi des Opérations de Restauration hydroMorphologiques des Cours d'Eau'. (#255)~~
- ~~Initialement, les champs historiques WAMA de l'API Poisson (notamment l'endpoint stations) étaient vides ou limités aux points de prélèvement non sandrifiés. (#256)~~
- ~~L'API Poisson a été mise à jour pour valoriser les codes et libellés WAMA pour les cas applicables. (#256)~~
- ~~Après la mise à jour, environ 85% des points de prélèvement, 90% des opérations, 90% des observations et 90% des opérations associées à des indicateurs sont renseignés avec un code WAMA. (#256)~~
- ~~WAMA est l'ancienne application de gestion des observations piscicoles, remplacée par ASPE en 2018. (#256)~~
- ~~Les codes et libellés WAMA sont des données historiques d'observations piscicoles. (#256)~~
- ~~Un point de prélèvement 'sandrifié' est associé à un code station et/ou point de prélèvement Sandre. (#256)~~
- ~~La documentation de l'API Poisson, endpoint "indicateurs", pour le champ "iprplus_libelle_classe" contenait une erreur, affichant des valeurs numériques au lieu des libellés textuels réels. (#257)~~
- ~~L'erreur de documentation concernant le champ "iprplus_libelle_classe" de l'API Poisson (endpoint "indicateurs") a été corrigée. (#257)~~
- ~~Le champ "iprplus_libelle_classe" de l'API Poisson (endpoint "indicateurs") renvoie des libellés textuels descriptifs (ex: "Très bon", "Bon") et non des codes numériques. (#257)~~

### Issues sources

- **#1** API Poissons et Tableau Software — L'issue met en évidence des limitations de l'API Poisson concernant la granularité des requêtes (par station/espèce uniquement), le manque de distinction par opération de pêche et de coordonnées pour toutes les stations, ainsi qu'un problème de géoréférencement pour certaines stations d'anguille. `[résolu]`
- **#3** Format de date GEOJSON — Un bug concernant l'incohérence du format des dates (timestamp entier en GEOJSON vs YYYY-MM-DD en JSON) pour l'API Poisson a été signalé et corrigé. `[résolu]`
- **#4** Protocole de pêche manquant pour l'API Poissons — L'API Poissons a été mise à jour en version 1, intégrant les informations de protocole de pêche (méthode, moyen, nombre de passages) essentielles à l'interprétation des résultats, et est désormais alimentée par la banque ASPE de l'OFB. `[résolu]`
- **#20** [API Poissons] — L'API Hub'Eau Poisson est passée en version v1, nécessitant l'adaptation des applications et démonstrateurs existants. `[information]`
- **#30** [API Poisson] Code poisson BLN - nom_poisson — L'API Poisson a été corrigée pour afficher les noms communs des espèces BLN, LPX, ATH, COR, tandis que les codes de genre (PHX, GOX, BBX, CAX) continuent de n'afficher que le nom latin. `[résolu]`
- **#33** Récupération données poisson depuis son nom — L'API Hub'Eau "Poisson" ne permet pas de rechercher par nom d'espèce mais uniquement par code OFB, nécessitant l'utilisation de l'endpoint `/code_espece_poisson` ou de l'API SANDRE pour la correspondance nom-code, en attendant la future API Hydrobiologie. `[résolu]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#148** [API Poisson] Date de maj de données ASPE ? — L'API Poisson a rencontré un décalage de données ASPE en 2023, résolu manuellement, et sa chaîne d'alimentation sera améliorée lors d'une prochaine évolution de l'API. `[résolu]`
- **#159** L'API poisson s'enrichit de trois nouveaux endpoints — L'API Poisson a été mise à jour avec trois nouveaux endpoints pour diffuser les indicateurs IPR/IPR+, les données environnementales des opérations et les données descriptives des stations de mesure. `[information]`
- **#181** [API Poissons] Fréquence de moissonage de la base ASPE — Cette issue clarifie que les données de l'API Poissons (base ASPE) sont mises à jour quotidiennement, mais que certaines données peuvent être absentes en raison de règles de validation spécifiques, notamment pour les opérations sous maîtrise d'ouvrage de l'Agence de l'eau Loire-Bretagne. `[résolu]`
- **#223** [ API Poisson ] Export de données via l'API URL et Rstudio : manque t'il des données ? — L'issue soulève une potentielle incomplétude des données d'opérations de pêche électrique de l'API Poisson pour le département de l'Isère par rapport à la source ASPE, interrogeant sur d'éventuelles restrictions de diffusion. `[résolu]`
- **#226** [ API Poisson ] liaison API avec Naîades et APSE — Cette issue met en lumière les écarts de complétude des données de l'API Hub'Eau Poisson par rapport à sa source (ASPE) et aux compilations locales, expliquant ces différences par les règles de diffusion et les méthodes de saisie d'ASPE, tout en fournissant des détails techniques sur l'utilisation de l'API. `[information]`
- **#251** [API Poisson] précision des coordonnées des points de prélèvements — L'API Poisson diffuse temporairement les coordonnées des points de prélèvements avec une précision réduite (une décimale au lieu de deux) en raison d'une anomalie Aspe en cours de correction. `[en_cours]`
- **#255** [API Poisson] - Imprécision du swagger pour les valeurs du champ objectifs_operations — L'issue signale et confirme la correction d'une troncature du libellé 'RNSORMCE – Réseau National de Suivi des Opérations de Restauration hydroMorphologiques des Cours d'Eau' pour le champ objectifs_operations de l'API Poisson, clarifiant ainsi sa signification complète. `[résolu]`
- **#256** [API Poisson] - champs WAMA inutiles — L'API Poisson a été mise à jour pour inclure les codes et libellés historiques WAMA, enrichissant ainsi les données sur les points de prélèvement, opérations et observations piscicoles. `[résolu]`
- **#257** [API Poisson] - errreur de la documentation sur les valeurs attendues — L'API Poisson utilise des libellés textuels pour le champ "iprplus_libelle_classe" de l'endpoint "indicateurs", et une erreur de documentation affichant des codes numériques a été corrigée. `[résolu]`
- **#275** [API Poisson] problème sur description des faciès — L'API Hub'Eau Poisson présente une incohérence où le nombre de faciès listés dans les libellés ne correspond pas toujours au nombre de valeurs pour les attributs numériques des faciès associés, ce qui peut entraîner des erreurs d'interprétation des données. `[en_cours]`

</details>
