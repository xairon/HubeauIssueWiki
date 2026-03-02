# Température des cours d'eau

> 8 issues analysées

## Guide

### Comportement actuel

L'API "Température des cours d'eau" offre deux endpoints principaux : `/api/v1/temperature/chronique` pour accéder aux mesures et `/api/v1/temperature/station` pour les informations sur les stations (#110, #124). Les données sont disponibles en formats JSON et CSV. Chaque mesure inclut des attributs détaillés comme le code et libellé du paramètre, la date et heure de mesure (avec distinction AM/PM), le résultat, l'unité et la qualification (#6, #18). L'endpoint `/station` permet de filtrer les résultats par `code_departement` (#124). La pagination par défaut utilise un `size` de 1 000 résultats par page, et les réponses d'erreur sont structurées avec des champs `code`, `message` et `field_errors` (#91, #236).

### Pièges à éviter

La principale limitation est la non-récence des données : les plus récentes datent de 2021, car de nombreuses stations de mesure ont cessé leur activité autour de 2013 (#110). La pagination est un point de vigilance : la multiplication `page` * `size` ne doit pas dépasser 20 000 résultats, et la taille maximale du paramètre `size` est de 20 000. L'API peut générer des liens "next" avec un `size` par défaut de 1 000, ce qui peut entraîner des erreurs si la page suivante dépasse la limite globale (#236). De plus, l'export de données historiques via le site Naïades, bien qu'une alternative, peut contenir des dates incorrectes en fin de fichier (#236).

### Bonnes pratiques

Pour une intégration facilitée en R, utilisez le package `hubeau` (disponible sur le CRAN), qui permet de requêter l'API Température des cours d'eau et d'autres APIs Hub'Eau avec une syntaxe simplifiée (`get_temperature_chronique(...)`) et est bien documenté (#137). Lors de requêtes paginées, spécifiez toujours le paramètre `size` explicitement et surveillez la limite de 20 000 résultats pour éviter les erreurs et les comportements inattendus (#236). Soyez conscient de la fraîcheur des données : les informations les plus récentes datent de 2021, ce qui peut impacter la pertinence pour des analyses contemporaines (#110).

### Contexte métier

Les données de température des cours d'eau proviennent principalement du système d'information sur l'eau Naïades. Elles sont enrichies d'attributs de qualification et d'unité essentiels pour une interprétation hydrologique précise (#6, #18). Il est important de noter que le manque de données récentes (post-2021) est dû à l'arrêt progressif de nombreuses stations de mesure de température des cours d'eau autour de 2013, reflétant une évolution dans la stratégie de suivi des températures des cours d'eau (#110).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Température des cours d'eau retourne des données, mais les plus récentes datent de 2021. (#110)
- L'endpoint `https://hubeau.eaufrance.fr/api/v1/temperature/chronique` peut être utilisé pour consulter les données de température. (#110)
- La plupart des données de température des cours d'eau disponibles via Hub'Eau sont anciennes. (#110)
- De nombreuses stations de mesure de température des cours d'eau ont été arrêtées autour de 2013, expliquant le manque de données récentes. (#110)
- Les utilisateurs recherchent activement des sources de données plus récentes pour la température de l'eau en France. (#110)
- La multiplication des paramètres `page` * `size` ne peut pas dépasser 20 000 pour l'API Température des cours d'eau. (#236)
- La taille maximale autorisée pour le paramètre `size` est 20 000. (#236)
- Un maximum de 20 000 valeurs de retour peut être récupéré, quelle que soit la taille de la page. (#236)
- Le paramètre `size` par défaut est 1 000 si non spécifié. (#236)
- L'API ajoute `size=1000` aux liens "next" dans la réponse JSON, ce qui peut provoquer une erreur si `page` * `size` dépasse 20 000 (ex: page 21 avec size 1000). (#236)
- Si le paramètre `size` est omis dans l'URL, la limite de 20 000 résultats ne semble pas fonctionner comme prévu, permettant d'accéder à un nombre de pages supérieur à la limite implicite. (#236)
- La limitation à 20 000 résultats est une politique générale des API Hub'eau mise en place pour préserver les performances et la disponibilité. (#236)
- Le site Naïades (naiades.eaufrance.fr) propose un export de données historiques sur les températures des cours d'eau comme alternative à l'API. (#236)
- L'export de données de Naïades peut contenir des dates incorrectes à la fin du fichier. (#236)

### Historique des problèmes résolus

- ~~Avant le 15/06/2018, l'opération `chronique.csv` de l'API Température des cours d'eau ne retournait que les 10 premiers champs, laissant les 9 champs suivants (ex: `code_parametre`, `resultat`, `libelle_qualification`) vides. (#6)~~
- ~~La version JSON de l'opération `chronique` de l'API Température des cours d'eau retournait correctement tous les champs, contrairement à la version CSV. (#6)~~
- ~~Le bug concernant les champs manquants dans `chronique.csv` a été corrigé dans la version beta-1 de l'API Température des cours d'eau, mise en ligne le 15/06/2018. (#6)~~
- ~~Les données de température des cours d'eau de l'API Hub'Eau incluent des attributs détaillés tels que le code et libellé du paramètre, la date et heure de mesure, le résultat, l'unité et la qualification de la mesure. (#6)~~
- ~~Les champs `code_parametre`, `libelle_parametre`, `date_mesure_temp`, `heure_mesure_temp`, `resultat`, `code_unite`, `symbole_unite`, `code_qualification`, `libelle_qualification` sont des informations essentielles pour l'analyse des chroniques de température. (#6)~~
- ~~L'API Température des cours d'eau présentait un bug où l'horodatage des observations ne distinguait pas AM et PM. (#18)~~
- ~~Un bug concernant des années erronées dans les données de l'API Température des cours d'eau a été corrigé. (#18)~~
- ~~Le bug d'horodatage AM/PM dans l'API Température des cours d'eau a été corrigé lors d'une mise à jour du 26 avril 2019. (#18)~~
- ~~Les données d'origine de température dans Naiades incluent correctement la distinction AM/PM. (#18)~~
- ~~L'API Température des cours d'eau a été mise à jour en juillet 2019 pour inclure 1,3 million de données de 2017, 1 million de 2018 et 80 000 de 2019 (jusqu'au 11 juin). (#18)~~
- ~~L'API `temperature/chronique` a retourné des mesures avec des dates futures (ex: 2045/2046). (#21)~~
- ~~Les erreurs de données ont été corrigées lors d'une mise à jour des données (27 avril 2019). (#21)~~
- ~~Des mesures de température contenaient des dates incorrectes (dans le futur). (#21)~~
- ~~Plus de 30 000 entrées incorrectes ont été identifiées. (#21)~~
- ~~Le problème était potentiellement lié à la station 03047445. (#21)~~
- ~~L'API Température des cours d'eau a pu générer une erreur 'Internal server error' pour certaines requêtes. (#91)~~
- ~~La réponse d'erreur de l'API inclut les champs 'code', 'message' et 'field_errors'. (#91)~~
- ~~L'API de température des cours d'eau a rencontré une erreur HTTP 500 sur la route `/api/v1/temperature/station`. (#124)~~
- ~~L'erreur affectait les formats JSON et CSV de l'API de température des cours d'eau. (#124)~~
- ~~L'API de température des cours d'eau est de nouveau disponible en JSON et CSV après résolution de l'erreur. (#124)~~
- ~~La route `/api/v1/temperature/station` de l'API de température des cours d'eau supporte des paramètres tels que `code_departement`, `size`, `exact_count`, `format` et `pretty`. (#124)~~
- ~~Les données de température des cours d'eau peuvent être filtrées par code départemental (ex: 45). (#124)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~

### Issues sources

- **#6** [Température] Opération chronique.csv ne retourne pas tous les champs — L'opération `chronique.csv` de l'API Température des cours d'eau ne retournait pas tous les champs, un bug corrigé dans la version beta-1 du 15/06/2018. `[résolu]`
- **#18** [API TEMPERATURE] - horodatage AM PM erroné — L'API Température des cours d'eau a corrigé un bug d'horodatage AM/PM et des erreurs d'années, et a mis à jour ses données pour inclure les années 2017, 2018 et une partie de 2019. `[résolu]`
- **#21** [API température] Données incorrectes — L'API Température des cours d'eau a présenté un bug où plus de 30 000 mesures contenaient des dates futures incorrectes, potentiellement liées à la station 03047445, et ces erreurs ont été corrigées lors d'une mise à jour des données en avril 2019. `[résolu]`
- **#91** [API Températures des cours d'eau] Internal server error — L'API Température des cours d'eau a rencontré une erreur interne du serveur pour une requête spécifique, mais l'issue a été résolue. `[résolu]`
- **#110** [API Temperature] pas de données — L'API Température des cours d'eau contient des données dont les plus récentes datent de 2021, principalement en raison de l'arrêt de nombreuses stations de mesure autour de 2013, ce qui génère des interrogations chez les utilisateurs sur la disponibilité de données plus récentes. `[information]`
- **#124** Erreur 500 sur la route chronique de l'api de récupération des températures d'eau — L'API de température des cours d'eau a rencontré une erreur HTTP 500 affectant les formats JSON et CSV, mais le problème a été résolu et l'API est de nouveau fonctionnelle. `[résolu]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#236** [API Température des cours d'eau] Problème lié à la pagination de l'API — L'API Température des cours d'eau impose une limite de 20 000 résultats (`page` * `size`), mais cette limite est contournable ou mal appliquée si le paramètre `size` est omis, et l'export alternatif de Naïades présente des problèmes de qualité de données. `[en_cours]`

</details>
