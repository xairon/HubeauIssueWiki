# Piézométrie

> 31 issues analysées

## Guide

### Comportement actuel  
L'API Piézométrie propose des endpoints comme `chroniques` (données agrégées journalières) et `chroniques_tr` (données en temps réel). Les formats de réponse incluent JSON, CSV et GeoJSON (en cours d'ajout) (#140). La pagination utilise les paramètres `size` et `page`, mais le tri (`sort`) se fait par `code_bss` au lieu de la date (#163). Les filtres incluent `code_bss`, `bbox` (format `xmin,ymin,xmax,ymax`) et `fields` (pour sélectionner des champs spécifiques, avec une dépendance entre `timestamp_mesure` et `date_mesure`) (#178, #180).

### Pièges à éviter  
Le paramètre `date_fin_mesure` inclut uniquement les données jusqu'à 0h du jour spécifié, nécessitant d'ajouter 1 jour pour couvrir la journée complète (#259). Le filtre `fields` ne renvoie pas `timestamp_mesure` sans `date_mesure` (#178). L'absence de format GeoJSON pour `chroniques_tr` limite l'intégration dans les applications cartographiques (#140). Le tri par `code_bss` rend impossible la récupération des dernières mesures de plusieurs stations en une seule requête (#163).

### Bonnes pratiques  
Privilégiez `code_bss` pour les données historiques et `bss_id` pour les stations (#59). Ajustez `date_fin_mesure` en ajoutant 1 jour pour inclure les données du jour entier (#259). Utilisez `chronique_tr` pour les requêtes multi-stations (#130). Vérifiez les paramètres par défaut dans la console de test (ex: `code_bss=07548X0009/F`) et supprimez-les si inutiles (#180).

### Contexte métier  
Les codes BSS (Base de Stations de Surveillance) identifient les points de mesure. Les anciens codes (ex: `00271X0002/P2`) coexistent avec les nouveaux (ex: `BSS001KJRF`), mais les chroniques historiques restent accessibles via les anciens codes (#59). Les données `chroniques` sont corrigées (ex: dérive de capteur), tandis que `chroniques_tr` sont brutes. L'altitude du repère de mesure (via l'API `Stations`) est nécessaire pour calculer la profondeur de la nappe (#34).

### Évolutions récentes  
- **2026-01-21** : Correction du comportement de `date_fin_mesure` (en cours) (#259).  
- **2025-10-21** : Ajout de `code_continuite` et `nom_continuite` pour les ruptures de continuité (#43).  
- **2025-05-05** : Mise à jour des filtres par code réseau (en cours) (#230).  
- **2024-12-11** : Référencement du projet SUBLIM pour des simulations hydrologiques (#203).  
- **2024-08-13** : Correction du paramètre `fields` pour `timestamp_mesure` (#178).  

### Historique notable  
- **2025-10-21** : Mise à jour de l'API pour inclure `code_continuite` (#43).  
- **2022-07-21** : Correction de la synchronisation avec ADES (#22).  
- **2021-06-08** : Activation du support CORS pour les requêtes cross-origin (#61).  
- **2020-03-18** : Ajout des métadonnées sur la continuité des courbes (#31).  
- **2019-01-22** : Résolution des erreurs de génération de client Swagger via la version 2.9.0 de Springfox (#19).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Dans l'API 'niveaux_nappes', le endpoint 'chroniques.csv' déclare 'produces' pour un format CSV mais référence un schéma d'objet ('Chronique_pi_zom_trique'), créant un conflit entre le type de données attendu et le schéma de réponse. (#19)
- Certains noms d'objets dans la documentation (ex: 'Résultat d'une rêquete sur les chroniques') sont mal adaptés au code, ce qui peut entraîner des erreurs de génération ou une mauvaise lisibilité. (#19)
- Les données de liaison entre masses d'eau et piézomètres provenaient initialement de la base Waterbase Quantity de l'EEA. (#29)
- Certains piézomètres présentent des ruptures dans les chroniques en raison d'un suivi irrégulier (#31)
- Le visualiseur en ligne de Hub'Eau ne gère pas les informations de continuité car il a été développé avant la disponibilité de ces champs. (#43)
- La station 02465X0061/F a connu une rupture de continuité le 03/05/2012, visible dans ADES mais non dans le visualiseur Hub'Eau. (#43)
- L'endpoint 'chroniques' de l'API Piézométrie ne supporte pas le paramètre 'bss_id' et génère une erreur 'code BSS ne peut pas être null' lors de sa tentative d'utilisation. (#49)
- Le paramètre 'code_bss' fonctionne correctement avec l'endpoint 'chroniques', contrairement à 'bss_id' qui est accepté par 'chroniques_tr'. (#49)
- Les utilisateurs doivent privilégier le paramètre 'code_bss' pour accéder aux données de chroniques via l'API Piézométrie, malgré l'existence d'un paramètre alternatif ('bss_id') dans d'autres endpoints. (#49)
- La période d'activité des stations piézométriques n'est pas mise à jour fréquemment, ce qui peut entraîner des résultats incohérents lors de requêtes proches de la date actuelle. (#50)
- Les données de disponibilité des stations piézométriques sont retardées de plusieurs mois par rapport à la date actuelle, affectant la pertinence des requêtes temporelles. (#50)
- L'API 'stations' utilise le paramètre 'bss_id' pour les nouveaux codes BSS, tandis que l'API 'chroniques' ne prend en charge que les anciens codes BSS via le paramètre 'code_bss'. (#59)
- Les chroniques historiques ne sont pas accessibles avec les nouveaux codes BSS, uniquement les chroniques temps réel (chroniques_tr) le sont. (#59)
- La date de dernière mesure renvoyée par l'API 'stations' diffère de celle disponible dans les chroniques. (#59)
- Les stations possèdent deux types de codes BSS : anciens (ex: 05202X0099/P) et nouveaux (ex: BSS001KJRF), avec des usages differents selon les APIs. (#59)
- Les données de chroniques historiques sont limitées aux anciens codes BSS, ce qui restreint l'accès aux données récentes pour certaines stations. (#59)
- L'API Piézométrie ne permet pas actuellement de filtrer les stations ou chroniques par code réseau de mesure, bien que les données des réseaux soient présentes dans l'index interne (liste_code_reseau, liste_mnemo_reseau, liste_nom_reseau). (#63)
- Dans l'API Qualité des nappes, le paramètre 'code_reseau' est absent pour la requête 'stations', mais disponible pour 'analyses'. (#63)
- Les réseaux de mesure (ex: 0400000020) sont associés à des stations via des codes réseau, et ces informations sont déjà stockées dans l'index Hub'Eau. (#63)
- Le réseau 0400000020 (Bretagne, MO BRGM) est régulièrement intégré dans les données ADES et consultable via une fiche publique. (#63)
- Le projet FrenchWaters utilise l'API Piézométrie pour visualiser des données sur les nappes phréatiques en France (#64)
- L'API Piézométrie ne met pas à jour immédiatement les données des stations, entraînant une absence de résultats pour certaines dates récentes. (#93)
- Les données de stations piézométriques peuvent présenter un délai de mise à jour, ce qui explique l'absence de résultats pour les dates postérieures au 21 décembre 2021 dans certaines requêtes. (#93)
- Les données 'temps réel' de l'API Piézométrie sont brutes et non corrigées. (#96)
- La profondeur temporelle des données 'temps réel' est actuellement non limitée, mais une limitation à 1 an est envisagée. (#96)
- Le endpoint 'chroniques' agrège les données sur une journée (généralement la valeur maximale du niveau NGF). (#96)
- Les données 'chroniques' peuvent être corrigées (ex. dérive de capteur, nivellement du repère). (#96)
- La fréquence de mise à jour des données 'chroniques' dépend des producteurs, qui ne transmettent pas toujours rapidement leurs données. (#96)
- Les stations concernées incluent des codes BSS comme 06995C0208/S1, 06995C0271/S et 07224X0102/S (#116)
- L'endpoint 'chronique_tr' fonctionne correctement pour des requêtes multi-stations, suggérant une différence de traitement entre les deux endpoints. (#130)
- L'API Piézométrie ne permet pas de filtrer les données par date de mise à jour, obligeant à télécharger l'intégralité des données à chaque synchronisation (#131)
- L'API Hydrométrie dispose d'un champ 'date de production' mais ne permet pas de filtrer les requêtes sur cette date (#131)
- Les utilisateurs doivent régulièrement télécharger l'intégralité des données piezométriques pour rester à jour, ce qui est inefficace (#131)
- La fonctionnalité de filtrage par date de mise à jour est demandée pour optimiser la synchronisation des données (#131)
- Le code BSS (Base de Stations de Surveillance) est utilisé pour identifier des points de mesure piézométriques, et la capacité à interroger plusieurs codes simultanément est essentielle pour des analyses multi-stations. (#132)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- L'API Piézométrie ne propose pas actuellement de format GeoJSON pour les chroniques en temps réel (#140)
- Les utilisateurs demandent un format spatial (GeoJSON) pour accéder aux données piézométriques en temps réel, facilitant l'intégration dans des applications cartographiques (#140)
- Le paramètre 'sort' (asc/desc) trie les résultats par 'code_bss' au lieu de la date de mesure (#163)
- Le paramètre 'size' contrôle la taille de la page de résultats, mais ne limite pas les résultats par station (#163)
- Pour obtenir les dernières mesures de plusieurs piézomètres, il faut effectuer une requête par station (#163)
- La console de test de l'API Piézométrie inclut une valeur par défaut pour le paramètre code_bss (07548X0009/F), mais cette valeur n'est pas appliquée par l'API elle-même. (#180)
- Lors de l'utilisation de la console de test, si un bss_id est spécifié, le code_bss par défaut est automatiquement ajouté à l'URL, nécessitant une suppression manuelle de l'un des deux paramètres pour éviter des résultats inattendus. (#180)
- Le projet SUBLIM utilise les données hydrologiques de l'API Hub'Eau pour simuler les débits des cours d'eau et les niveaux piézométriques via des réseaux de neurones artificiels. (#203)
- Le service SUBLIM intègre des données météorologiques historiques (ERA5) et prévisionnelles (CEP/ECMWF 0.25°) en complément des données Hub'Eau. (#203)
- L'API Piézométrie nécessite encore l'ancien code BSS pour télécharger les chroniques, alors que le nouveau bss_id est disponible pour les stations. (#207)
- Le bss_id est l'identifiant officiel des points d'eau depuis 2016, mais n'est pas encore utilisable pour accéder aux chroniques via l'API. (#207)
- L'API Piézométrie ne permet pas actuellement de filtrer les stations par code(s) de réseau (ex. 0102400001). (#230)
- Les requêtes avec des codes BSS anciens (ex. 00471X0095/PZ2013) utilisent uniquement les 10 premiers caractères pour identifier un point, mais l'API traite l'ensemble du code. (#230)
- Les nouveaux codes BSS (ex. BSS003RMMC) ne contiennent pas de désignation, mais l'API continue d'appliquer un format imitant l'ancien (avec '/X') pour les anciens codes. (#230)
- Les codes de réseau (ex. 0102400001) sont des identifiants clés pour localiser des stations piézométriques, mais ils ne sont pas exposés via l'API actuelle. (#230)
- Les codes BSS anciens (ex. 00471X0095/PZ2013) contiennent une désignation non pertinente (ex. '/PZ2013') qui n'est pas toujours stockée dans les bases de données. (#230)
- Les nouveaux codes BSS (ex. BSS003RMMC) n'incluent pas de désignation, contrairement aux anciens codes, ce qui crée une incohérence dans le format. (#230)
- Le paramètre `date_fin_mesure` inclut les données uniquement jusqu'à 0h du jour spécifié, au lieu d'inclure toutes les mesures du jour entier. (#259)
- Pour inclure les données d'une date de fin, l'utilisateur doit ajouter 1 jour à la date spécifiée, ce qui peut introduire des données non souhaitées si une mesure existe à 0h le lendemain. (#259)
- Le comportement de l'API est incohérent entre les stations : certaines incluent la date de fin, d'autres non, même pour la même plage de dates. (#259)
- Les utilisateurs risquent de manquer des données récentes si la date de fin n'est pas ajustée correctement (ajout de 1 jour). (#259)
- La documentation actuelle est ambiguë sur le traitement des dates (avec ou sans composante horaire). (#259)
- L'API Piézométrie retourne uniquement des libellés textuels (ex: 'Donnée contrôlée niveau 1') pour les champs 'statut' et 'qualification', sans fournir les codes associés (ex: 1, 2, 3, 4). (#260)
- Les codes pour 'statut' et 'qualification' existent selon les nomenclatures SANDRE, mais ne sont pas exposés par l'API. (#260)
- Les codes SANDRE pour 'statut' (ex: 1 à 4 ou Mnémonique) et 'qualification' (0 à 4) permettent une réduction significative du volume de données exportées par rapport aux libellés textuels. (#260)
- L'utilisation de codes plutôt que de libellés est cruciale pour optimiser les performances des exports de données via l'API. (#260)

### Historique des problèmes résolus

- ~~La présence de 'allowEmptyValues: false' dans la documentation Swagger génère des erreurs de génération du client, mais ce problème est résolu à partir de la version 2.9.0 de springfox/springfox. (#19)~~
- ~~La mise à jour différée des collections Hub'Eau a été corrigée, permettant désormais une synchronisation en temps réel avec ADES. (#22)~~
- ~~Des données piézométriques étaient temporairement absentes dans Hub'Eau par rapport à ADES, comme pour le point d'eau 00271X0002/P2 au 02/01/2019. (#22)~~
- ~~L'API Piézométrie a été mise à jour pour inclure le code, le nom et l'URI de la masse d'eau captée (version état des lieux). (#29)~~
- ~~La liaison entre les piézomètres et les masses d'eau (état des lieux) est désormais disponible via l'API Piézométrie. (#29)~~
- ~~L'API ne retournait pas initialement d'information sur la continuité des courbes de mesure (#31)~~
- ~~Un exemple dans la documentation technique était désuet après la mise à jour de l'API (#31)~~
- ~~Les données incluent désormais des informations sur la continuité des courbes, le producteur, la nature de la mesure et la profondeur de l'eau (#31)~~
- ~~Les unités des champs 'niveau_nappe_eau' et 'profondeur_nappe' sont respectivement en mètres NGF et en mètres par rapport au repère de mesure. (#34)~~
- ~~La documentation de l'API 'Piézométrie' a été mise à jour pour inclure les informations sur les unités. (#34)~~
- ~~Le niveau de la nappe (niveau_nappe_eau) correspond à l'altitude du point de mesure en mètres NGF (Nivellement Général de la France). (#34)~~
- ~~La profondeur de la nappe (profondeur_nappe) est calculée comme la différence entre l'altitude du repère de mesure et le niveau de la nappe. (#34)~~
- ~~L'altitude du repère de mesure peut être trouvée via l'API 'Stations' ou les fiches ADES/BSSEAU, et peut varier dans le temps en raison de travaux ou de changements d'organismes. (#34)~~
- ~~La précision des altitudes (altitude_station, altitude_repère) est généralement de l'ordre du mètre, tandis que celle des profondeurs est de l'ordre du centimètre. (#34)~~
- ~~L'API Piézométrie inclut les champs 'code_continuite' et 'nom_continuite' pour indiquer les ruptures de continuité. (#43)~~
- ~~Le graphique d'évolution a été supprimé pour permettre l'affichage du lien du détail du point de mesure sur les écrans de faible définition (#54)~~
- ~~L'API Piézométrie de Hub'Eau inclut l'en-tête 'access-control-allow-origin: *' dans les réponses, permettant les requêtes cross-origin depuis n'importe quel domaine. (#61)~~
- ~~Le blocage signalé par l'utilisateur est probablement lié à une gestion asynchrone incorrecte des composants côté client, et non à un manque d'en-tête CORS serveur. (#61)~~
- ~~L'API Piézométrie a connu une absence de données chroniques pour certaines stations entre début juin 2022 et fin juin 2022 (#116)~~
- ~~Les données ont été partiellement disponibles à partir du 30 juin 2022 (#116)~~
- ~~Le manque de données a été temporaire et a disparu d'ici la fin juin 2022 (#116)~~
- ~~L'endpoint 'chronique' de l'API Piézométrie retourne des résultats vides lors de requêtes avec plusieurs stations (code_bss), même si les paramètres sont valides et que la même requête fonctionne pour une seule station. (#130)~~
- ~~L'API ne permettait pas la recherche simultanée de plusieurs codes BSS (séparés par des virgules) avant la migration technique de décembre 2022, ce qui a été corrigé en mars 2023. (#132)~~
- ~~L'API Piézométrie utilise un seul paramètre 'bbox' au format 'xmin,ymin,xmax,ymax' au lieu de quatre paramètres séparés (bbox1, bbox2, etc.) (#144)~~
- ~~Le paramètre 'fields' de l'API Piézométrie ne retournait pas le champ 'timestamp_mesure' correctement sans la présence du champ 'date_mesure' dans la liste des champs demandés. (#178)~~
- ~~Les API Hydrométrie et Piézométrie ont connu un dysfonctionnement temporaire entraînant une erreur 500 lors de leur appel. (#184)~~
- ~~Le service a été rétabli après intervention des équipes techniques. (#184)~~

### Issues sources

- **#19** [Toutes APIs] Multiples erreurs lors de la génération d'un client à partir de la documentation Swagger (2019-01-22) — L'issue met en évidence des erreurs techniques dans la documentation Swagger de l'API Piézométrie, notamment des incohérences entre les types de données déclarés et les schémas de réponse, ainsi que des problèmes de nommage des objets.
- **#22** [API Hydro] données manquantes par rapport à ADES (2019-06-07) — La synchronisation des données piézométriques entre ADES et Hub'Eau a été corrigée, résolvant les disparités temporelles.
- **#29** [API Piézométrie] - ajout des codes masses d'eau (requête et résultat) (2020-02-19) — L'API Piézométrie a été mise à jour pour permettre la liaison avec les masses d'eau (état des lieux), résolvant un besoin technique et métier exprimé en 2019.
- **#31** API Piézométrie: Chroniques et chroniqes_tr (2020-03-18) — L'API Piézométrie a été mise à jour pour inclure des informations sur la continuité des chroniques et d'autres métadonnées, améliorant la fiabilité des données hydrologiques.
- **#34** [Niveaux nappes] - Quelles unités ? (2020-04-03) — L'issue précise les unités des données de niveau et de profondeur des nappes d'eau (mètres NGF et mètres relatifs au repère) et explique comment déterminer le repère de mesure via les APIs et les fiches ADES/BSSEAU.
- **#43** Gestion des continuités pour l'API Piézométrie (2020-09-21) — L'API Piézométrie inclut les informations de continuité via des champs spécifiques, mais le visualiseur en ligne ne les affiche pas.
- **#49** Bug sur l'API piézo pour chroniques (2022-07-21) — L'API Piézométrie présente une incohérence dans la gestion des paramètres BSS entre les endpoints 'chroniques' et 'chroniques_tr', nécessitant une utilisation spécifique de 'code_bss' pour éviter les erreurs.
- **#50** Liste des stations piézométriques (2021-02-05) — La mise à jour tardive des périodes d'activité des stations piézométriques explique les disparités dans les résultats des requêtes API selon la date de recherche.
- **#54** [Démonstrateur piézo] problème d'affichage (2022-07-05) — Un problème d'affichage lié à la résolution des écrans a été corrigé en supprimant le graphique d'évolution pour afficher le lien vers le détail des mesures.
- **#59** API  Piézométrie   - bug codes bss et api station (2022-07-21) — L'API de piézométrie de Hub'Eau présente une incohérence entre les paramètres 'code_bss' et 'bss_id' selon les endpoints, avec une limitation des chroniques historiques aux anciens codes BSS.
- **#61** [API Piezométrie] Blocage d’une requête multiorigines (Cross-Origin Request) (2021-06-08) — L'API Piézométrie de Hub'Eau est configurée pour autoriser les requêtes cross-origin, et le problème signalé provient probablement d'une erreur de gestion asynchrone côté client.
- **#63** [API Piezométrie] Ajout d'un filtre par code réseau de mesure (2021-08-31) — Demande d'ajout d'un filtre par code réseau de mesure dans l'API Piézométrie, avec mention de la disponibilité des données réseau dans l'index interne et d'une limitation actuelle dans l'API Qualité des nappes.
- **#64** [API Piezometrie] Une réutilisation à référencer (2021-06-11) — Cette issue signale une utilisation de l'API Piézométrie par le projet FrenchWaters, qui a été ajoutée à la liste des réutilisations officielles.
- **#93** API Piézométrie - aucune station depuis le 23 décembre (2022-01-10) — L'API Piézométrie de Hub'Eau présente un délai de mise à jour des données, entraînant une absence de résultats pour certaines dates récentes.
- **#96** Profondeur temporelle des données piézométriques (2022-01-28) — L'API Piézométrie fournit des données brutes non corrigées en temps réel, tandis que les données 'chroniques' sont agrégées et peuvent être corrigées, avec une mise à jour dépendante des producteurs.
- **#116** [API Piézométrie] Absence de chronique depuis début juin (2022-07-21) — L'API Piézométrie a connu une interruption temporaire des données chroniques pour certaines stations en juin 2022, résolue avant la fin du mois.
- **#130** [API Piézométrie] fonction chronique (2023-05-30) — L'endpoint 'chronique' de l'API Piézométrie présente un comportement anormal pour les requêtes multi-stations, mais ce problème est résolu via l'endpoint 'chronique_tr'.
- **#131** [API Piézométrie] Synchronisation des données (2025-08-20) — L'API Piézométrie manque d'une fonctionnalité de filtrage par date de mise à jour, rendant les synchronisations inefficaces, alors que cette fonctionnalité est en cours d'étude pour l'API Hydrométrie.
- **#132** API Hub'Eau - Piézométrie (2023-03-13) — L'API Piézométrie de Hub'Eau a temporairement perdu la capacité à filtrer plusieurs codes BSS simultanément, mais cette fonctionnalité a été rétablie en mars 2023.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#140**  [API Piézométrie] Proposer le format GeoJSON pour les chroniques en temps réel (2023-04-15) — Une demande d'extension de l'API Piézométrie pour inclure le format GeoJSON dans les chroniques en temps réel a été proposée.
- **#144** [API Piézométrie] bug avec paramètre bbox ? (2023-05-25) — L'API Piézométrie nécessite un paramètre 'bbox' unique au format 'xmin,ymin,xmax,ymax' pour filtrer les stations par emprise géographique.
- **#163** [API Piézométrie] Ordre de tri (2024-02-26) — L'API Piézométrie trie les résultats par code_bss au lieu de la date, rendant impossible la récupération des dernières mesures de plusieurs stations en une seule requête.
- **#178** [API Piézométrie] Erreur dans le critère field  (2024-10-17) — L'API Piézométrie a corrigé un bug où le champ 'timestamp_mesure' n'était pas renvoyé correctement sans l'inclusion du champ 'date_mesure' dans les requêtes.
- **#180** Imprécision dans la documentation API Piézo / chroniques_tr (2024-08-13) — La documentation de l'API Piézométrie indique une valeur par défaut pour code_bss, mais cette valeur n'est active que dans l'interface de test et non dans l'API elle-même, ce qui peut entraîner des résultats inattendus si l'utilisateur ne retire pas le paramètre.
- **#184** [API Hydrométrie] [API piézométrie] Erreur de connexion a hub'eau (2024-09-11) — Les API Hydrométrie et Piézométrie de Hub'Eau ont été temporairement indisponibles en raison d'un dysfonctionnement technique, résolu par les équipes.
- **#203** [Site Web] Demande de référencement sur la page "Cas d'usage". (2024-12-11) — Le projet SUBLIM est un exemple d'utilisation des API Hub'Eau pour des simulations hydrologiques basées sur l'intelligence artificielle.
- **#207** [Piézométrie] Ajout du paramètre bss_id (2025-10-21) — L'API Piézométrie ne permet pas encore d'utiliser le bss_id (identifiant officiel depuis 2016) pour télécharger les chroniques, contrairement aux stations.
- **#230** [API piezométrie] Requête par réseaux et indices (2025-05-05) — L'API Piézométrie nécessite une amélioration pour permettre les requêtes par code de réseau et une meilleure gestion des codes BSS anciens et nouveaux.
- **#259** [API piezométrie] param date_fin_mesure au comportement pas comme attendu (2026-01-21) — L'API Piézométrie de Hub'Eau ne traite pas les dates de fin comme des bornes inclusives, entraînant des erreurs de récupération de données.
- **#260** [API piezométrie] Ajout des CODES en plus des libellés des champs qualifiant les données (2025-10-21) — L'API Piézométrie devrait ajouter des codes SANDRE pour les champs 'statut' et 'qualification' afin de réduire le volume des données exportées et d'améliorer les performances.

</details>
