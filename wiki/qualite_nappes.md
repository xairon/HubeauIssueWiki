# Qualité des nappes

> 20 issues analysées

## Guide

### Comportement actuel

L'API Qualité des nappes permet d'accéder aux données via des endpoints comme `/stations` et `/analyses`, en utilisant des codes BSS pour identifier les stations. Les résultats incluent des données géographiques (longitude, latitude), administratives (code INSEE) et des informations sur les masses d'eau associées. La pagination est gérée via l'attribut `next`, mais il peut être généré même sans page suivante (#15). Le format GeoJSON n'est pas supporté sur l'endpoint `analyses` (#186), et les requêtes sont limitées à 20 000 résultats maximum par appel (#57). Le paramètre `fields` exige des noms de champs précis (ex: `code_param` au lieu de `code_parametre`) (#214).

### Pièges à éviter

- **Pagination incorrecte** : L'attribut `next` peut être généré même si aucune page suivante n'existe, ce qui peut entraîner des boucles infinies. Vérifiez toujours si `data` est vide avant d'appliquer `next`.  
- **Limite de 20 000 résultats** : Les requêtes dépassant cette limite retournent une erreur `InvalidRequest`. Utilisez des tranches de 10 000 éléments pour accéder à de grandes quantités de données (#57).  
- **Absence de l'heure de prélèvement** : Les données de ADES ne transmettent pas le champ `heure de prélèvement`, rendant impossible la distinction de prélèvements simultanés sur une même station (#235).  
- **Format GeoJSON non supporté sur `analyses`** : Utiliser `format=geojson` sur cet endpoint retourne un JSON standard, pas un GeoJSON (#186).

### Bonnes pratiques

Utilisez le paramètre `date_debut_prelevement` pour filtrer les analyses par date, évitant de charger l'ensemble de l'historique (#52). Pour des volumes importants, fractionnez les requêtes en tranches de 10 000 éléments. Vérifiez la disponibilité des données via des sources externes comme ADES ou Naïades pour les paramètres spécifiques (ex: PFAS) (#217). Si des métadonnées comme les années de mesure sont manquantes, consultez directement les organismes gestionnaires (#204).

### Contexte métier

Les codes BSS identifient les stations de mesure, tandis que les codes SANDRE standardisent les paramètres analytiques. Les données proviennent principalement de ADES et de réseaux comme 0400000020 (Bretagne, BRGM). Les masses d'eau sont associées aux stations via des codes comme `codes_masse_eau_rap`. Les stations de captage d'eau potable ont leurs coordonnées floutées pour des raisons de sécurité (#270).

### Évolutions récentes

- **2026-02-02** : Floutage des coordonnées des captages d'eau potable, remplacées par celles du chef-lieu de la commune (#270).  
- **2025-06-02** : Absence du champ `heure de prélèvement` dans les données de ADES, limitant la précision des analyses (#235).  
- **2025-05-14** : Impossibilité de filtrer directement les données PFAS via l'API, nécessitant des requêtes par groupe de paramètres (#217).  
- **2024-09-05** : Format GeoJSON non supporté sur l'endpoint `analyses` (#186).

### Historique notable

- **2025-02-17** : Correction du bug liant le paramètre `fields` à des noms de champs précis (ex: `code_param` au lieu de `code_parametre`) (#214).  
- **2021-02-04** : Ajout du filtre `date_debut_prelevement` pour sélectionner les analyses par date (#52).  
- **2019-02-06** : Correction d'une désynchronisation des données entraînant des variations aléatoires du nombre de résultats (#14).  
- **2020-08-19** : Réindexation des serveurs pour résoudre les incohérences de `count` dues à la duplication des données (#42).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API Qualité des eaux souterraines permet de récupérer des informations via l'endpoint '/stations' en utilisant un code BSS. (#10)
- L'API Piézométrie fournit moins d'informations sur les masses d'eau comparée à l'API Qualité des eaux souterraines. (#10)
- L'attribut 'next' est généré dans l'URL de réponse même lorsque la page suivante n'existe pas (par exemple, lorsque 'data' est vide). (#15)
- L'API ne fournit pas les champs 'laboratoire' et 'préleveur' pour les données de qualité des nappes. (#51)
- Le code de support n'est pas renvoyé par l'API car il peut être déduit du code fraction (ex. 3, 22, 23 → code support 3). (#51)
- Le code de support est toujours égal à 3 (eau) selon les informations fournies par l'API. (#51)
- La station BSS000LGJB a 21 347 mesures disponibles, nécessitant une pagination avec des tranches de 10 000 éléments. (#57)
- L'API Piézométrie ne permet pas actuellement de filtrer les stations ou chroniques par code réseau de mesure, bien que les données des réseaux soient présentes dans l'index interne (liste_code_reseau, liste_mnemo_reseau, liste_nom_reseau). (#63)
- Dans l'API Qualité des nappes, le paramètre 'code_reseau' est absent pour la requête 'stations', mais disponible pour 'analyses'. (#63)
- Les réseaux de mesure (ex: 0400000020) sont associés à des stations via des codes réseau, et ces informations sont déjà stockées dans l'index Hub'Eau. (#63)
- Le réseau 0400000020 (Bretagne, MO BRGM) est régulièrement intégré dans les données ADES et consultable via une fiche publique. (#63)
- Le paramètre '_format' permet d'obtenir du GeoJSON via les URLs API, mais cette fonctionnalité n'est pas systématiquement implémentée sur toutes les APIs. (#149)
- Les couches chargées dans QGIS via les APIs sont limitées à 20000 entités sans automatisation des échanges de données. (#149)
- Le format GeoJSON n'est pas implémenté sur l'endpoint 'analyses' de l'API Qualité des nappes. L'utilisation de 'format=geojson' retourne un format JSON au lieu de GeoJSON. (#186)
- L'API Qualité des nappes ne fournit pas actuellement des informations sur les années de mesure, les producteurs ou les paramètres analysés pour chaque station. (#204)
- Un endpoint _parametres_ est en cours de développement pour les APIs de qualité (rivières et nappes) afin d'optimiser les requêtes. (#204)
- L'absence de données sur les années de mesure et les producteurs oblige les utilisateurs à effectuer des requêtes supplémentaires pour identifier les stations pertinentes. (#204)
- L'API Hub'eau ne permet pas de filtrer directement les données par critère PFAS, uniquement par groupe de paramètres. (#217)
- Les paramètres PFAS sont gérés par le référentiel analytique Sandre et l'organisme Aquaref, et non directement disponibles via l'API Hub'eau. (#217)
- L'API Hub'Eau ne fournit pas de méthode de calcul automatisée pour agréger les concentrations de polluants mesurées par plusieurs stations sur une journée donnée. (#220)
- La concentration journalière globale d'un paramètre comme le métolachlore ESA nécessite une approche métier spécifique, non standardisée par l'API, et dépend des besoins opérationnels (ex: moyenne, interpolation spatiale). (#220)
- Les données de qualité de l'eau (paramètres chimiques) sont collectées par des stations hétérogènes en termes de localisation et de fréquence de mesure, ce qui complique l'agrégation temporelle/spatiale. (#220)
- L'API est fréquemment inaccessible (4 à 5 heures de downtime 1 à 3 fois par semaine) en raison de sollicitations massives et intensives. (#231)
- La réponse technique mentionne un possible blocage d'IP si le problème persiste. (#231)
- L'utilisateur effectue des requêtes régulières et lourdes depuis plusieurs mois sur l'API. (#231)
- L'API Qualité des nappes ne transmet pas le champ 'heure de prélèvement' provenant de la source ADES. (#235)
- L'absence de l'heure de prélèvement empêche la comparaison précise avec les données de SISE-EAUX (ARS). (#235)
- Plusieurs prélèvements sur la même station le même jour sont fusionnés sans l'heure, perdant leur distinction. (#235)
- L'heure est nécessaire pour la traçabilité et la reconstitution des séries de mesures. (#235)
- Les coordonnées des captages d'eau potable sont remplacées par celles du chef-lieu de la commune dans les endpoints _Analyses_ et _Stations_ de l'API Qualité des nappes. (#270)
- Le champ `precision_coordonnees` utilise la valeur 18 pour indiquer que les coordonnées sont floutées (code Sandre 916). (#270)
- La réglementation française et européenne impose le floutage des coordonnées des captages d'eau potable pour protéger leur localisation. (#270)
- Les coordonnées floutées peuvent affecter l'analyse spatiale des données hydrologiques liées aux captages. (#270)

### Historique des problèmes résolus

- ~~Un point BSS peut être associé à une masse d'eau via des codes comme 'codes_masse_eau_rap' et 'noms_masse_eau_rap'. (#10)~~
- ~~Les données incluent des informations géographiques (longitude, latitude) et administratives (code INSEE, nom de commune). (#10)~~
- ~~L'API Qualité des nappes présentait une désynchronisation entre les copies de données, entraînant des variations aléatoires du nombre de résultats (attribut count) pour les mêmes paramètres de requête. (#14)~~
- ~~La duplication des données sur plusieurs serveurs peut entraîner une désynchronisation des index, provoquant des incohérences dans les résultats de l'API (ex. : count différent selon la valeur du paramètre size). (#42)~~
- ~~L'API Qualité des nappes permet de filtrer les données par la date de prélèvement via le paramètre 'date_debut_prelevement'. (#52)~~
- ~~L'API impose une limite de 20 000 enregistrements par requête (page * size), ce qui empêche la récupération de plus de 20 000 résultats même si la pagination suggère une page supérieure. (#57)~~
- ~~Une erreur 'InvalidRequest' est retournée dès que le produit de 'page' et 'size' dépasse 20 000. (#57)~~
- ~~L'API qualité-nappes présentait une instabilité dans le nombre de résultats renvoyés pour des requêtes identiques, due à un bug corrigé. (#79)~~
- ~~L'argument 'fields' de l'API ne filtre pas les résultats comme prévu si les noms des champs ne correspondent pas exactement aux noms attendus par l'API (ex. 'code_parametre' doit être 'code_param') (#214)~~
- ~~La version 1.3.0 de l'API a introduit un floutage des coordonnées des captages AEP (eau potable) pour protéger la localisation précise des sources. (#269)~~
- ~~Le floutage des coordonnées des captages AEP réduit la précision géospatiale des données, impactant les analyses de proximité ou de vulnérabilité des nappes phréatiques. (#269)~~
- ~~Un problème de chargement partiel des données a été identifié dans l'alimentation de Hub'Eau à partir des données ADES, entraînant une sous-estimation temporaire du nombre d'analyses renvoyées par l'API. (#271)~~

### Issues sources

- **#10** caractéristiques hydrogéologiques  (2018-10-08) — L'API Qualité des nappes permet de récupérer des caractéristiques hydrogéologiques via un code BSS, y compris les masses d'eau associées.
- **#14** [API Qualité des nappes d'eau souterraine] Nombre de résultats aléatoire (2019-02-06) — L'API Qualité des nappes a eu un problème de désynchronisation des données corrigé en 2019, affectant la fiabilité des résultats retournés.
- **#15** L'attribut 'next' est toujours généré même sans page suivante (2018-12-18) — L'API Hub'Eau génère incorrectement l'attribut 'next' lorsqu'il n'y a pas de page suivante, affectant la navigation paginée des résultats.
- **#42** [API Qualité Nappe] (2020-08-19) — Un bug lié à la désynchronisation des index entre serveurs a été corrigé par une re-indexation complète, résolvant les incohérences de count dans l'API Qualité des nappes.
- **#51** API Qualité eau souterraine (2021-02-04) — L'API Qualité des nappes ne fournit pas les informations sur le laboratoire, le préleveur et le code de support, ce qui limite les métadonnées disponibles pour les utilisateurs.
- **#52** API Qualité eau souterraine (2021-02-09) — L'API Qualité des nappes inclut un filtre 'date_debut_prelevement' pour sélectionner les analyses selon la date de prélèvement, résolvant le besoin initial d'accéder aux dernières données sans récupérer l'ensemble de l'historique.
- **#57** [API qualite_nappes] Erreur avec la dernière page (2021-04-08) — L'API Qualité des nappes limite les requêtes à 20 000 résultats maximum, nécessitant des appels fractionnés pour accéder à l'intégralité des données.
- **#63** [API Piezométrie] Ajout d'un filtre par code réseau de mesure (2021-08-31) — Demande d'ajout d'un filtre par code réseau de mesure dans l'API Piézométrie, avec mention de la disponibilité des données réseau dans l'index interne et d'une limitation actuelle dans l'API Qualité des nappes.
- **#79** [api-qualite-nappes] nombre de résultats différents avec la même requête (2022-07-21) — Une instabilité dans le nombre de résultats de l'API qualité-nappes a été corrigée, garantissant désormais des résultats cohérents pour des requêtes identiques.
- **#149** Tutoriel utilisation des API avec QGIS information #2 by tvilmus was closed on Jul 5, 2022 (2023-12-15) — Les utilisateurs doivent utiliser le paramètre '_format=geojson' dans les URLs API pour obtenir des données GeoJSON compatibles avec QGIS, tout en étant conscients des limitations de format et de volume de données.
- **#186** [API Qualité des nappes d'eau souterraines] Problème de connexion sur QGIS (2024-09-05) — L'endpoint 'analyses' de l'API Qualité des nappes ne prend pas en charge le format GeoJSON, contrairement à d'autres endpoints comme celui des stations.
- **#204** [API Qualité des nappes d'eau souterraines] Ajout d'élément à la liste des stations de mesure (2024-12-12) — L'issue demande l'ajout de métadonnées (années, producteurs, paramètres) pour les stations de mesure de la Qualité des nappes afin d'améliorer l'efficacité des requêtes API.
- **#214** [API Qualité des nappes] - argument fields non pris en compte (fonctionnalité expérimentale) (2025-02-17) — L'API Qualité des nappes nécessite l'utilisation de noms de champs précis pour le paramètre 'fields', comme 'code_param' au lieu de 'code_parametre'.
- **#217** Absence de data PFAS de la platforme https://pdh.cnrs.fr/fr/datasets/ france_naiades sur hub'eau (2025-05-14) — L'API Hub'eau ne permet pas de sélectionner directement les données PFAS, nécessitant des requêtes supplémentaires par groupe de paramètres et une consultation externe pour les détails des paramètres.
- **#220** Question sur le calcul de la concentration journalière du métolachlore ESA du departement de Finistère de toutes les stations present. (2025-05-14) — L'issue met en évidence l'absence de méthode standardisée dans l'API Hub'Eau pour calculer des concentrations journalières agrégées de polluants, nécessitant une consultation directe des organismes gestionnaires (Ades/Naïades).
- **#231** [API Qualité des Nappes] Données fréquemment inaccessibles (2025-05-06) — L'API Qualité des nappes subit des downtimes récurrents en raison de sollicitations massives, affectant sa disponibilité.
- **#235** [API Qualité des Nappes] Manque du champ “heure de prélèvement” dans les données venant de ADES (2025-06-02) — L'API Qualité des nappes manque le champ 'heure de prélèvement' provenant de ADES, limitant la précision des analyses et la comparaison avec d'autres sources de données.
- **#269** [API Qualité des nappes d'eau souterraine] - changelog manquant sur la 1.3.0 (2026-02-02) — La mise à jour 1.3.0 de l'API Qualité des nappes implémente un floutage des coordonnées des captages AEP pour des raisons de sécurité.
- **#270** [API Qualité des Nappes] Floutage des coordonnées de captages (2026-02-02) — L'API Qualité des nappes floute les coordonnées des captages d'eau potable en les remplaçant par celles du chef-lieu de la commune, avec un indicateur de précision spécifique.
- **#271** [Qualité des nappes] Incohérence de volumétrie entre Hub'Eau et ADES (2026-02-09) — Une incohérence de volumétrie entre Hub'Eau et ADES pour une station a été résolue après une anomalie de chargement des données, maintenant les résultats alignés.

</details>
