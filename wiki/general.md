# Général

## Particularités techniques

- Le tutoriel vidéo original pour l'utilisation des API Hub'Eau avec QGIS (spécifiquement pour les stations qualité) n'est plus disponible. (#2)
- La vidéo a été rendue privée puis jugée obsolète par l'équipe Hub'Eau. (#2)
- Il n'existe pas de nouvelle vidéo de démonstration de l'utilisation des API Hub'Eau dans QGIS à la date du dernier commentaire (octobre 2022). (#2)
- La spécification Swagger des APIs Hub'Eau contenait des propriétés "allowEmptyValues: false" non conformes à la spécification Swagger, empêchant la génération de clients API. (#19)
- Les noms d'objets dans la spécification Swagger (ex: "Résultat d'une rêquete sur les chroniques") n'étaient pas optimaux pour la génération de code, rendant le code client potentiellement "douteux". (#19)
- Cette limite est imposée pour ne pas surcharger le serveur. (#57)
- Pour récupérer plus de 20 000 enregistrements, il faut découper la requête en utilisant des critères plus discriminants, comme `date_debut_prelevement`. (#57)
- L'API peut retourner des URLs erronées dans les attributs 'last' et 'next' lorsque la limite `page * size` est dépassée. (#57)
- Le BRGM fournit un exemple d'appel de l'API Hub'Eau avec R pour les données piézométriques, disponible sur GitHub à l'adresse https://github.com/BRGM/hubeau/blob/master/code_examples/Trac%C3%A9%20d'une%20chronique%20pi%C3%A9zom%C3%A9trique%20avec%20R.ipynb. (#62)
- Le BRGM prévoit de publier d'autres exemples de code R pour l'API Hub'Eau sur son dépôt GitHub à l'adresse https://github.com/BRGM/hubeau/tree/master/code_examples. (#62)
- Un package R nommé `hubeau` est développé par INRAE pour interroger les APIs Hub'Eau. (#62)
- Le package R `hubeau` inclut une fonction générique d'interrogation et des fonctions spécifiques par API/opération, retournant les résultats sous forme de data.frame. (#62)
- Le package R `hubeau` prend en charge initialement les APIs 'Prélèvements en eau' et 'Indicateurs des services'. (#62)
- Le package R `hubeau` est disponible sur GitHub à l'adresse https://github.com/inrae/hubeau et sa documentation à https://inrae.github.io/hubeau/. (#62)
- Le code source des APIs Hub'Eau n'est pas disponible sur GitHub. (#89)
- L'utilisation de wildcards `*` dans les paramètres de recherche n'est pas systématiquement implémentée dans les APIs Hub'Eau. (#101)
- Les wildcards sont disponibles dans certains champs de type code (par exemple, les codes entités de l'API Hydrométrie). (#101)
- Les wildcards ne sont pas supportées pour le paramètre `libelle_lieusurv` de l'API Surveillance des eaux littorales. (#101)
- L'API Température des cours d'eau inclut un paramètre 'en_service' pour les stations. (#108)
- Il est proposé d'ajouter un paramètre 'en_service' aux stations des autres APIs Hub'Eau. (#108)
- Les APIs et le site web Hub'Eau ont été indisponibles suite à un incident survenu le 14 mai 2023 au soir. (#143)
- Le service a été rétabli le 15 mai 2023 à 12h20. (#143)
- Le paramètre _format_=geojson permet d'obtenir des données au format GeoJSON via les API Hub'Eau. (#149)
- Le format GeoJSON n'est pas implémenté pour toutes les API Hub'Eau ; dans ce cas, la syntaxe _format_=geojson retourne des données au format JSON standard. (#149)
- Seules les données GeoJSON diffusées par certaines API Hub'Eau peuvent être chargées directement dans QGIS. (#149)
- Sans automatisation des échanges de données, les couches chargées dans QGIS sont limitées à 20 000 entités. (#149)
- Les schémas des données (descriptifs des variables) pour les APIs Hub'Eau sont disponibles dans la section `Models` en bas de chaque page d'accueil d'une API. (#156)
- Une intervention de maintenance sur l’infrastructure technique d’Hub’eau a été planifiée. (#176)
- L'intervention a eu lieu le mardi 23/07/2024 entre 9h et 17h. (#176)
- Cette opération a induit des interruptions de services tournantes sur l’ensemble des API Hub'Eau. (#176)
- Chaque interruption de service ne devait pas dépasser 1h30. (#176)
- L'intervention est terminée et toutes les API Hub'Eau sont de nouveau opérationnelles depuis le 23/07/2024 à 16h46. (#176)
- L'ensemble des APIs Hub'Eau a été momentanément indisponible le 4 septembre 2024. (#185)
- Les APIs Hub'Eau ont été rétablies et sont de nouveau disponibles le 4 septembre 2024. (#185)
- Un incident peut perturber l'accès général aux API Hub'Eau et au domaine eaufrance.fr. (#205)
- Le port 443 est le port standard utilisé pour la connexion aux API Hub'Eau. (#205)
- Une opération de maintenance a entraîné une interruption de service de l'ensemble des API Hub'Eau. (#218)
- L'interruption de service était prévue le lundi 17 mars 2025, entre 12h et 15h. (#218)
- L'intervention est terminée et toutes les API Hub'Eau sont de nouveau disponibles. (#218)
- La feuille de route Hub'eau ne prévoit pas la création d'une API exposant des données météorologiques. (#234)
- Hub'eau n'a pas connaissance d'API tierces servant des données météorologiques. (#234)
- Le portail API de Météo-France (portail-api.meteofrance.fr) est suggéré comme source pour les données météorologiques. (#234)
- La taille maximale autorisée pour le paramètre `size` est 20 000. (#236)
- Un maximum de 20 000 valeurs de retour peut être récupéré, quelle que soit la taille de la page. (#236)
- Le paramètre `size` par défaut est 1 000 si non spécifié. (#236)
- Si le paramètre `size` est omis dans l'URL, la limite de 20 000 résultats ne semble pas fonctionner comme prévu, permettant d'accéder à un nombre de pages supérieur à la limite implicite. (#236)
- La limitation à 20 000 résultats est une politique générale des API Hub'eau mise en place pour préserver les performances et la disponibilité. (#236)
- Une interruption de service de l'ensemble des API Hub'Eau était planifiée le 24/06/2025 entre 12h et 15h pour une opération de maintenance. (#237)
- L'intervention de maintenance a été terminée plus tôt que prévu, et toutes les API étaient disponibles avant 11h52 le 24/06/2025. (#237)
- Un incident distinct de la maintenance a affecté la disponibilité des données hydrométriques temps réel. (#237)
- Une interruption de service de l'ensemble des API Hub'Eau a été planifiée pour maintenance. (#248)
- L'interruption a eu lieu le mardi 02/09/2025 entre 12h et 14h. (#248)
- Le service de toutes les API Hub'Eau a été rétabli le 02/09/2025 à 12h14:34Z. (#248)
- Une page de statut globale est disponible à l'adresse https://hubeau.eaufrance.fr/status pour visualiser l'état en temps réel de tous les endpoints des API Hub'eau. (#258)
- Des pages de statut spécifiques à chaque endpoint fournissent des détails sur les temps de réponse, les incidents et l'historique sur 12 mois. (#258)
- La plateforme Hub'eau envoie des notifications à l'équipe technique en cas d'incident détecté pour une résolution rapide. (#258)
- L'API Hub'Eau renvoie un code HTTP 206 (Partial Content) pour les réponses paginées. (#261)
- Ce comportement peut empêcher la lecture des données paginées dans certains clients comme DuckDB (via la fonction read_json). (#261)
- L'utilisation du code HTTP 206 pour la pagination est considérée comme non conforme aux standards HTTP (RFC 7233) et aux bonnes pratiques REST, car il est réservé aux requêtes avec en-tête Range. (#261)
- La pagination REST standard utilise généralement le code HTTP 200, indiquant les pages suivantes via un champ 'next' ou des en-têtes 'Link' (RFC 5988). (#261)
- Une interruption de service a été planifiée pour toutes les API Hub'Eau les 17 et 18 février 2026 entre 12h et 14h. (#273)
- Toutes les API Hub'Eau étaient susceptibles d'être indisponibles pendant ces périodes en raison d'une opération technique. (#273)
- Le service a été rétabli et toutes les API sont disponibles depuis le 18 février 2026 à 12h38. (#273)

## Informations métier

- Un tutoriel pour afficher des stations qualités dans QGIS à partir des API Hub'Eau avait été réalisé par AQUASYS suite à un Hackathon. (#2)
- L'API Piézométrie (niveaux_nappes) fournit des données de chroniques (séries temporelles) pour les niveaux de nappe. (#19)
- Certaines stations (ex: BSS000LGJB) peuvent avoir un très grand nombre de mesures (plus de 20 000). (#57)
- Les APIs Hub'Eau distinguent les champs de type 'libellé' et 'code' pour les paramètres de recherche. (#101)
- Le paramètre `libelle_lieusurv` permet de rechercher des lieux de surveillance dans l'API Surveillance des eaux littorales. (#101)
- Actuellement, le statut 'hors service' d'une station est déduit de la présence d'une date de fin renseignée. (#108)
- Le concept de station 'en service' est une information clé pour l'utilisation des données hydrologiques. (#108)
- L'utilisation des API Hub'Eau avec QGIS est un cas d'usage pour l'intégration de données hydrologiques dans un SIG. (#149)
- Les données de qualité des nappes peuvent être filtrées par numéro de département (ex: num_departement=23). (#149)
- Dans l'API Qualité des cours d'eau, pour l'endpoint `condition_environnementale_pc`, l'attribut `resultat` correspond au 'Résultat de la mesure du paramètre environnemental (résultat direct si le paramètre est quantitatif ou code si le paramètre est qualitatif)'. (#156)
- Hub'eau ne couvre pas les données de pluviométrie ou météorologiques dans son périmètre actuel. (#234)
- Les données des entités météorologiques disponibles sur hydro.eaufrance.fr ne sont pas accessibles via une API Hub'eau. (#234)
- Le site Naïades (naiades.eaufrance.fr) propose un export de données historiques sur les températures des cours d'eau comme alternative à l'API. (#236)
- L'export de données de Naïades peut contenir des dates incorrectes à la fin du fichier. (#236)
- Les données hydrométriques temps réel ont été manquantes à partir du 23/06/2025 fin de journée. (#237)
- L'alimentation des données hydrométriques temps réel a été rétablie le 24/06/2025 avant 11h52. (#237)

## Problèmes connus

- L'API Piézométrie (niveaux_nappes) avait un endpoint `chroniques.csv` dont le `produces` indiquait un format binaire/stream (CSV) mais référençait un schéma d'objet (`Chronique_pi_zom_trique`), causant une erreur de génération de client. (#19)
- Dépasser la limite `page * size > 20000` entraîne une erreur `InvalidRequest` avec le code `ValidatePageDepth`. (#57)
- L'API Hub'Eau présente des bugs connus, mentionnés dans les issues #72 et #74. (#62)
- Les problèmes de connexion aux API Hub'Eau peuvent se manifester par une absence de résolution DNS pour hubeau.eaufrance.fr. (#205)
- L'API ajoute `size=1000` aux liens "next" dans la réponse JSON, ce qui peut provoquer une erreur si `page` * `size` dépasse 20 000 (ex: page 21 avec size 1000). (#236)

## Tips d'utilisation

- La multiplication des paramètres `page` et `size` dans les requêtes Hub'Eau ne peut excéder 20 000 enregistrements (profondeur d'accès aux résultats). (#57)
- La multiplication des paramètres `page` * `size` ne peut pas dépasser 20 000 pour l'API Température des cours d'eau. (#236)

---

## Issues sources

- **#2** Tutoriel utilisation des API avec QGIS — L'issue informe que le tutoriel vidéo pour utiliser les API Hub'Eau avec QGIS est obsolète et n'est plus disponible, sans remplacement actuel. `[information]`
- **#19** [Toutes APIs] Multiples erreurs lors de la génération d'un client à partir de la documentation Swagger — Des erreurs dans la spécification Swagger des APIs Hub'Eau, notamment des propriétés non conformes et des noms d'objets inadaptés, empêchaient la génération correcte de clients API, particulièrement pour l'API Piézométrie. `[résolu]`
- **#57** [API qualite_nappes] Erreur avec la dernière page — L'API Hub'Eau `qualite_nappes` (et potentiellement d'autres) impose une limite de 20 000 enregistrements pour le produit `page * size`, nécessitant de découper les requêtes volumineuses avec des critères plus discriminants. `[résolu]`
- **#62** Utilisation de l'API dans R / Package dédié ? — Cette issue a mené au développement et à la publication du package R `hubeau` par INRAE pour interroger les APIs Hub'Eau, complété par des exemples de code R du BRGM et la mention de bugs existants dans l'API. `[résolu]`
- **#89** Mettre les API sur github — Hub'Eau n'a pas l'intention de partager le code source de ses APIs sur GitHub, ce qui limite les contributions externes au développement des APIs. `[résolu]`
- **#101** Utilisation de Wildcards * dans les recherches (un classic) — Les wildcards `*` ne sont pas systématiquement supportées dans les APIs Hub'Eau, étant limitées à certains champs de type code comme les codes entités de l'API Hydrométrie, mais non disponibles pour les libellés. `[information]`
- **#108** [API Qualité de l'eau] Paramètre de station en service — L'issue propose d'ajouter un paramètre 'en_service' aux stations des APIs Hub'Eau, à l'instar de l'API Température, pour simplifier la détermination du statut opérationnel des stations. `[en_cours]`
- **#143** Site et API indisponibles 15/05/2023 — Un incident général a rendu les APIs et le site web Hub'Eau indisponibles le 15 mai 2023, avec un retour à la normale à 12h20 le même jour. `[résolu]`
- **#149** Tutoriel utilisation des API avec QGIS information #2 by tvilmus was closed on Jul 5, 2022 — Cette issue explique comment obtenir des données GeoJSON via les API Hub'Eau en utilisant le paramètre _format_ pour une intégration dans QGIS, tout en précisant les limitations de ce format et du volume de données. `[résolu]`
- **#156** Qualité des cours d'eau ,nomenclature des variables utilisées — Cette issue explique où trouver les descriptions des variables pour les APIs Hub'Eau (section Models) et fournit la définition de l'attribut `resultat` pour l'API Qualité des cours d'eau. `[résolu]`
- **#176** [Toutes API] Intervention de maintenance le 23/07 en journée — Une intervention de maintenance a eu lieu le 23/07/2024, entraînant des interruptions de service tournantes sur l'ensemble des API Hub'Eau, mais l'opération est maintenant terminée et les services sont rétablis. `[résolu]`
- **#185** [toutes API] Service indisponible — Un dysfonctionnement a rendu l'ensemble des APIs Hub'Eau indisponible pendant une courte période le 4 septembre 2024, avant que le service ne soit rétabli. `[résolu]`
- **#205** [API] Problème de connection depuis hier 14h — Un incident général a perturbé l'accès aux API Hub'Eau et au domaine eaufrance.fr, se manifestant par des problèmes de connexion et de résolution DNS, mais a été résolu. `[résolu]`
- **#218** [toutes API]  interruption de service lun. 17/03/2025 12h-15h — Une opération de maintenance a provoqué une interruption de service de toutes les API Hub'Eau le 17 mars 2025 de 12h à 15h, et le service a été rétabli. `[résolu]`
- **#234** API Pluviométrie — Hub'Eau ne propose pas d'API pour les données de pluviométrie ou météorologiques et oriente les utilisateurs vers Météo-France pour ces informations. `[résolu]`
- **#236** [API Température des cours d'eau] Problème lié à la pagination de l'API — L'API Température des cours d'eau impose une limite de 20 000 résultats (`page` * `size`), mais cette limite est contournable ou mal appliquée si le paramètre `size` est omis, et l'export alternatif de Naïades présente des problèmes de qualité de données. `[en_cours]`
- **#237** [toutes API] interruption de service mar. 24/06/2025 12h-15h — Une maintenance planifiée pour toutes les API Hub'Eau le 24/06/2025 a été terminée plus tôt que prévu, et un incident distinct ayant causé un manque de données hydrométriques temps réel a également été résolu le même jour. `[résolu]`
- **#248** [toutes API] interruption de service mar. 02/09/2025 12h-14h — Cette issue annonce et confirme la résolution d'une interruption de service planifiée pour maintenance de l'ensemble des API Hub'Eau le 02/09/2025. `[résolu]`
- **#258** [toutes API] tableau de bord — Hub'Eau a mis en place un tableau de bord de statut en temps réel pour toutes ses APIs, incluant des pages détaillées par endpoint et un système de notification d'incidents pour l'équipe technique. `[information]`
- **#261** HTTP 206 renvoyé pour des données paginées : flux non lisible dasn DuckDB par exemple — L'API Hub'Eau retourne un code HTTP 206 pour les réponses paginées, ce qui est non conforme aux standards HTTP pour la pagination et pose des problèmes de lecture avec certains clients comme DuckDB. `[en_cours]`
- **#273** [toutes API] interruption de service mar. 17/02/2026 et mer. 18/02/2026 12h-14h — Une interruption de service planifiée pour toutes les API Hub'Eau les 17 et 18 février 2026 entre 12h et 14h a eu lieu et a été résolue. `[résolu]`
