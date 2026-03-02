# Prélèvements en eau

## Particularités techniques

- L'utilisation du filtre `fields` sur l'API Prélèvements en eau (version vbeta) pouvait entraîner la perte de certaines informations, notamment les coordonnées géographiques (longitude, latitude), qui devenaient nulles. (#25)
- La propriété `fields` était expérimentale et instable dans la version vbeta de l'API Prélèvements en eau. (#25)
- Les URLs de l'API ont évolué de `/api/vbeta/` à `/api/v1/`. (#25)
- L'API Prélèvements en eau a connu une longue phase beta avant de passer en version 1 (production). (#26)
- L'opération 'chroniques' de l'API Prélèvements en eau inclut désormais le nom de l'ouvrage de prélèvement. (#26)
- Les coordonnées géographiques sont disponibles pour les points de prélèvement et les ouvrages. (#26)
- La codification des usages a été simplifiée dans l'API Prélèvements en eau. (#26)
- Les ouvrages de prélèvement incluent désormais l'identifiant local (code producteur), le point de prélèvement référent et les noms des plans d'eau (hors BD Carthage). (#26)
- Le champ `libelle_precision_coord` était toujours null pour l'opération `/vbeta/prelevements/referentiel/points_prelevement` de l'API Prélèvements en eau. (#27)
- Dans la version beta de l'API Prélèvements en eau, les champs `libelle_precision_coord` étaient inutiles car toutes les coordonnées étaient fictives. (#27)
- L'API Prélèvements en eau ne fournit pas le code SIRET de l'établissement exploitant l'ouvrage. (#37)
- L'API Prélèvements en eau est passée de version bêta à v1 stable en juin 2021. (#38)
- Le passage à la v1 de l'API Prélèvements en eau a inclus une actualisation des données. (#38)
- La v1 de l'API Prélèvements en eau apporte les coordonnées géographiques des ouvrages et points de prélèvement. (#38)
- La v1 de l'API Prélèvements en eau assure une mise à jour mensuelle des données. (#38)
- Des informations complémentaires sur la v1 de l'API Prélèvements en eau sont disponibles sur la page d'actualités Hub'Eau (https://hubeau.eaufrance.fr/news/api-prelevements-en-eau-passage-en-v1). (#38)
- Le champ code_entite_hydrogeo n'est pas correctement renseigné dans l'API Prélèvements en eau (endpoint ouvrages) pour le type SOUT dans la version beta. (#39)
- Le champ code_entite_hydrogeo sera corrigé dans la version définitive de l'API Prélèvements en eau. (#39)
- Le code_bss_point_eau est présent dans les résultats d'un prélèvement. (#39)
- Le code_bss_point_eau ne peut pas être remonté au niveau de l'ouvrage car un ouvrage peut avoir plusieurs points de prélèvement, chacun avec son propre code_bss_point_eau. (#39)
- Le BRGM fournit un exemple d'appel de l'API Hub'Eau avec R pour les données piézométriques, disponible sur GitHub à l'adresse https://github.com/BRGM/hubeau/blob/master/code_examples/Trac%C3%A9%20d'une%20chronique%20pi%C3%A9zom%C3%A9trique%20avec%20R.ipynb. (#62)
- Le BRGM prévoit de publier d'autres exemples de code R pour l'API Hub'Eau sur son dépôt GitHub à l'adresse https://github.com/BRGM/hubeau/tree/master/code_examples. (#62)
- Un package R nommé `hubeau` est développé par INRAE pour interroger les APIs Hub'Eau. (#62)
- Le package R `hubeau` inclut une fonction générique d'interrogation et des fonctions spécifiques par API/opération, retournant les résultats sous forme de data.frame. (#62)
- Le package R `hubeau` prend en charge initialement les APIs 'Prélèvements en eau' et 'Indicateurs des services'. (#62)
- Le package R `hubeau` est disponible sur GitHub à l'adresse https://github.com/inrae/hubeau et sa documentation à https://inrae.github.io/hubeau/. (#62)
- La limite de 20 000 enregistrements (`page * size`) est mentionnée dans la section "Limitations" de la documentation de l'API Prélèvements. (#136)
- Le champ `count` de la première page de résultats peut être utilisé pour détecter si une requête dépassera la limite de 20 000 enregistrements. (#136)
- La documentation Swagger de l'API Prélèvements décrit un code 400 comme une "requête incorrecte", ce qui est imprécis pour le cas de dépassement de la limite `page * size`. (#136)
- Un contournement pour la limite de 20 000 enregistrements consiste à fragmenter les requêtes en utilisant des plages de codes communes. (#136)
- Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)
- Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)
- La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)
- Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)
- Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)
- Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)
- Le même appel API fonctionnait la semaine précédant le 07/07/2025. (#241)
- Lors d'une période d'instabilité de l'endpoint `/prelevements/chroniques`, l'ajout du paramètre `fields` (ex: `fields=code_ouvrage,annee,volume`) pouvait servir de contournement pour obtenir des résultats. (#249)
- L'endpoint `/prelevements/chroniques` est désormais stable et ne nécessite plus la spécification du paramètre `fields`. (#249)
- Cette anomalie affectait certaines APIs Hub'Eau lors de requêtes demandant l'ensemble des champs. (#274)
- L'anomalie a été résolue, et l'interrogation de l'API Prélèvements en eau sans le paramètre `fields` est de nouveau fonctionnelle. (#274)

## Informations métier

- L'API Prélèvements en eau permet de récupérer des informations sur les ouvrages (structures) de prélèvement. (#25)
- Les ouvrages sont identifiés par un `code_ouvrage` (ex: OPR0000065205). (#25)
- Les coordonnées géographiques (longitude, latitude) sont des informations importantes associées aux ouvrages. (#25)
- Les coordonnées des points de prélèvement et des ouvrages liés à l'Alimentation en Eau Potable (AEP) sont floutées au centroïde de la commune pour des raisons de confidentialité. (#26)
- Les coordonnées des points de prélèvement dans la version beta de l'API Prélèvements en eau étaient fictives. (#27)
- Le champ `libelle_precision_coord` est lié à la précision des coordonnées réelles. (#27)
- Le code SIRET de l'établissement exploitant un ouvrage de prélèvement n'est pas une donnée ouverte et n'est pas diffusé par BNPE ni par Hub'Eau. (#37)
- Avant la v1, l'API Prélèvements en eau avait des données moins complètes (nombre d'ouvrages, millésimes) que le jeu de données data.eaufrance.fr (ex: 6872 ouvrages vs 8508 pour Pays de la Loire, millésimes s'arrêtant à 2016 alors que l'AELB fournissait 2019). (#38)
- La v1 de l'API Prélèvements en eau contient les mêmes données que celles de la BNPE (Banque Nationale des Prélèvements en Eau). (#38)
- Un ouvrage peut être composé de plusieurs points de prélèvement. (#39)
- Le code_bss_point_eau est une information spécifique à un point de prélèvement. (#39)
- Le type SOUT (Souterrain) est associé au code_entite_hydrogeo. (#39)
- L'API Prélèvements en eau dispose d'un référentiel des ouvrages (`/referentiel/ouvrages`) liés aux prélèvements. (#71)
- L'API Prélèvements utilise le référentiel des communes/départements de la BNPE, dont le millésime n'est pas spécifié. (#136)
- Interroger l'API Prélèvements par codes communes est délicat en raison du risque de rater des ouvrages liés à des codes obsolètes. (#136)
- L'interrogation par codes départements est une méthode recommandée pour récupérer les données d'ouvrages de l'API Prélèvements. (#136)
- Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)
- L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)
- Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)
- L'API "Prélèvements en eau" permet de récupérer les chroniques de prélèvements. (#241)
- Les données de prélèvements peuvent être filtrées par année et par code de département. (#241)
- Le format GeoJSON est supporté pour les chroniques de prélèvements. (#241)
- L'endpoint `/prelevements/chroniques` permet d'accéder aux données chroniques de prélèvements en eau. (#249)
- Les données de prélèvements en eau peuvent être filtrées par `bbox` (zone géographique), `annee` (année), `code_departement` (code du département). (#249)
- Des champs comme `code_ouvrage`, `annee`, `volume` sont disponibles pour les données de prélèvements en eau. (#249)
- Les données de prélèvements chroniques de l'API Hub'Eau incluent des informations détaillées sur l'ouvrage (code, nom, URI, coordonnées, commune, département), l'année, le volume, l'usage, les statuts et qualifications du volume, le statut et mode d'obtention de l'instruction, le caractère écrasant du prélèvement, et le producteur de la donnée. (#274)

## Problèmes connus

- Une solution temporaire pour contourner le problème était de ne pas utiliser le filtre `fields` et de récupérer l'ensemble des champs. (#25)
- Le problème a été résolu avec le passage de l'API Prélèvements en eau à la version v1. (#25)
- Un bug sur les codes des entités hydrogéologiques a été corrigé dans l'API Prélèvements en eau. (#26)
- L'opération `/vbeta/prelevements/referentiel/ouvrages` de l'API Prélèvements en eau n'était pas affectée par le problème du champ `libelle_precision_coord` null. (#27)
- Le bug du champ `libelle_precision_coord` null a été corrigé lors du passage de l'API Prélèvements en eau de la version beta à la version v1. (#27)
- L'API Hub'Eau présente des bugs connus, mentionnés dans les issues #72 et #74. (#62)
- L'endpoint `/api/v1/prelevements/referentiel/ouvrages` de l'API Prélèvements en eau a rencontré un bug où il retournait `count 0` (aucune donnée). (#71)
- Le bug de l'endpoint `/api/v1/prelevements/referentiel/ouvrages` a été corrigé. (#71)
- L'API Prélèvements retourne un code HTTP 400 si le produit des paramètres `page * size` dépasse 20 000, avec un message d'erreur indiquant cette limite. (#136)
- L'API Hub'Eau `/api/v1/prelevements/chroniques` a retourné une "internal server error" (erreur 500) le 07/07/2025. (#241)
- L'erreur s'est produite pour une requête incluant les paramètres `annee=2018`, `code_departement=28` et `format=geojson`. (#241)
- L'endpoint `/prelevements/chroniques` de l'API Prélèvements en eau a connu des périodes d'indisponibilité ou d'instabilité, retournant des erreurs 500. (#249)
- L'API Prélèvements en eau (endpoint chroniques) a temporairement renvoyé une erreur 500 lors de requêtes ne spécifiant pas le paramètre `fields`. (#274)
- Un contournement temporaire consistait à utiliser le paramètre `fields` en listant explicitement les champs désirés pour éviter l'erreur 500. (#274)

---

## Issues sources

- **#25** [API Prélèvements en eau] - Erreur lors de la récupération des ouvrages — L'API Prélèvements en eau (vbeta) présentait un bug où le filtre `fields` causait la perte des coordonnées géographiques des ouvrages, problème résolu avec le passage de l'API à la version v1. `[résolu]`
- **#26** [API Prélèvement en eau] nom de l'ouvrage dans les chroniques — L'API Hub'Eau Prélèvements en eau est passée en version 1, intégrant le nom de l'ouvrage dans les chroniques, les coordonnées géographiques (floutées pour l'AEP), une simplification des usages, et des identifiants supplémentaires pour les ouvrages. `[résolu]`
- **#27** [API Prélèvements en eau] - Champs libelle_precision_coord toujours null — L'API Prélèvements en eau présentait un bug où le champ `libelle_precision_coord` était toujours null pour les points de prélèvement en version beta, en raison de coordonnées fictives, et ce problème a été résolu avec le passage à la version v1. `[résolu]`
- **#37** [API Prélèvement] code SIRET des établissements de prélèvement — L'API Prélèvements en eau ne diffuse pas le code SIRET des établissements de prélèvement car cette donnée n'est pas ouverte et n'est pas fournie par BNPE. `[information]`
- **#38** [API Prélèvements] actualisation des données — L'API Prélèvements en eau est passée en v1 en juin 2021, résolvant les problèmes d'incomplétude des données en s'alignant sur la BNPE, offrant des mises à jour mensuelles et incluant les coordonnées géographiques des ouvrages. `[résolu]`
- **#39** [API Prélèvement] Suggestion d'association du code_bss à l'ouvrage plutôt qu'au point de prélèvement — L'issue clarifie que le champ code_entite_hydrogeo est manquant pour les ouvrages de type souterrain dans l'API Prélèvements en eau (version beta) et sera corrigé, et explique pourquoi le code_bss_point_eau ne peut pas être associé à l'ouvrage. `[résolu]`
- **#62** Utilisation de l'API dans R / Package dédié ? — Cette issue a mené au développement et à la publication du package R `hubeau` par INRAE pour interroger les APIs Hub'Eau, complété par des exemples de code R du BRGM et la mention de bugs existants dans l'API. `[résolu]`
- **#71** [API prélèvements] Aucune donnée dans la réponse de la requête "ouvrages" ? — Un bug empêchait l'API Prélèvements en eau de retourner des données pour le référentiel des ouvrages, mais il a été corrigé. `[résolu]`
- **#136** API Prélèvements - retourne code 400 sur dépassement page * size — L'API Prélèvements limite la récupération des données à 20 000 enregistrements (`page * size`), retournant une erreur 400 au-delà, et suggère des méthodes d'interrogation par département ou par plages de communes pour gérer cette limitation et les référentiels. `[en_cours]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#241** Accès impossible aux prélèvements via l'API - "internal error" retourné ce 07 juillet 2025 — L'API Prélèvements en eau a rencontré une erreur interne (500) sur l'endpoint `/chroniques` le 07/07/2025 pour des requêtes spécifiques (département 28, année 2018, format GeoJSON), alors que la requête fonctionnait précédemment. `[résolu]`
- **#249** [API Prélèvements en eau] endpoint "chroniques": Erreur 500 sur toutes les requêtes — L'endpoint `/prelevements/chroniques` de l'API Prélèvements en eau a rencontré des instabilités récurrentes provoquant des erreurs 500, avec un contournement temporaire via le paramètre `fields`, avant une résolution finale. `[résolu]`
- **#274** [API Prélèvements en eau] get prelevements chroniques -> Error 500 — L'API Prélèvements en eau a rencontré et résolu une erreur 500 sur l'endpoint chroniques lorsque le paramètre `fields` n'était pas spécifié, avec un contournement temporaire disponible. `[résolu]`
