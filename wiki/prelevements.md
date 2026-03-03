# Prélèvements en eau

> 12 issues analysées

## Guide

### Comportement actuel  
L'API Prélèvements en eau fonctionne en version v1, avec des endpoints principaux comme `/ouvrages` et `/chroniques`, retournant des données en format JSON. La pagination est limitée à 20 000 résultats maximum (page * size ≤ 20 000). Le paramètre `fields` est désormais stable et permet de filtrer les champs retournés. Les données sont mises à jour mensuellement et alignées sur la BNPE. Le nom des ouvrages est disponible dans les chroniques (#26).  

### Pièges à éviter  
La limite de 20 000 résultats peut bloquer des requêtes volumineuses (#136). L'endpoint `/chroniques` peut renvoyer un code 500 si le paramètre `fields` n'est pas utilisé (#249). Le code SIRET des établissements n'est pas disponible (#37). Les codes communes obsolètes peuvent rendre les recherches par département imparfaites (#136).  

### Bonnes pratiques  
Utilisez le paramètre `fields` pour éviter les erreurs 500 sur `/chroniques`. Vérifiez les codes BNPE pour les départements. Privilégiez le package R `hubeau` pour une intégration simplifiée (#137). Limitez les requêtes à des plages de dates et de départements récents pour éviter les limites de pagination.  

### Contexte métier  
Les codes BSS (Bassin de Surface) identifient des points de prélèvement, pas les ouvrages (#39). Le SANDRE (Système d'information sur les réseaux et les ouvrages) est une base de données hydrologiques utilisée pour les codes communes. Les données proviennent principalement de l'AELB (Agence de l'eau Loire-Bretagne) et sont alignées sur la BNPE (Base Nationale des Plans d'Établissement).  

### Évolutions récentes  
- **2026-02-16** (#274) : Correction de l'erreur 500 sur `/chroniques` sans dépendance au paramètre `fields`.  
- **2025-10-01** (#249) : Stabilisation de l'endpoint `/chroniques` après une période de dépendance temporaire au paramètre `fields`.  
- **2025-07-07** (#241) : En cours de résolution, une erreur interne a été signalée pour des requêtes spécifiques.  

### Historique notable  
- **2021** (#25, #27) : Le paramètre `fields` et le champ `libelle_precision_coord` ont été corrigés avec la version v1.  
- **2021** (#38) : Mise à jour vers v1 avec des données alignées sur la BNPE et des mises à jour mensuelles.  
- **2021** (#26) : Ajout du nom des ouvrages dans les chroniques pour une sélection géographique.  
- **2020** (#37) : Le code SIRET n'est pas diffusé en raison des contraintes de publication des données ouvertes.  
- **2020** (#39) : Correction planifiée du lien entre `code_bss_point_eau` et les ouvrages.

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- Dans la version beta, les coordonnées étaient fictives, rendant le champ 'libelle_precision_coord' inutile. (#27)
- Le code SIRET des établissements exploitants n'est pas disponible dans les données ouvertes de l'API Prélèvements en eau. (#37)
- Le code_bss_point_eau est associé au point de prélèvement plutôt qu'à l'ouvrage, ce qui entraîne une duplication des données. (#39)
- Un ouvrage peut comporter plusieurs points de prélèvement, chacun avec un code BSS unique, rendant impossible une association directe au niveau de l'ouvrage. (#39)
- L'API retourne un code 400 lorsque le produit des paramètres `page` * `size` dépasse 20 000. (#136)
- Le message d'erreur est en anglais et indique que la multiplication des paramètres `page` et `size` ne peut pas dépasser 20 000. (#136)
- Le comptage total des résultats est disponible dès la première requête, mais l'API ne bloque pas la requête tant que le seuil de 20 000 n'est pas atteint. (#136)
- Un code d'erreur spécifique est proposé pour améliorer la lisibilité et la gestion des erreurs liées à ce plafond. (#136)
- Le référentiel des codes communes/départements utilisé est celui de la BNPE, sans indication du millésime. (#136)
- Les codes communes obsolètes peuvent rendre la recherche par code département imparfaite, justifiant une augmentation du plafond de 20 000. (#136)
- Le package R 'hubeau' permet de requêter 10 des 12 APIs Hub'Eau via une syntaxe standardisée (`get_[API]_[Operation]`) (#137)
- Le package est disponible sur CRAN et GitHub, avec une documentation incluant des exemples et une vignette (#137)
- L'OFB DR Normandie utilise le package pour générer des rapports mensuels sur l'écoulement des cours d'eau en Bretagne (#137)
- Une vignette illustre l'utilisation de l'API 'Écoulement' avec des cartes et graphiques synthétiques (#137)
- L'API 'prélèvements/chroniques' a retourné un 'internal server error' lors de la requête avec les paramètres annee=2018 et code_departement=28 le 7 juillet 2025. (#241)
- Le paramètre 'fields' doit être utilisé avec des champs spécifiques pour éviter l'erreur 500. (#274)

### Historique des problèmes résolus

- ~~Le paramètre 'fields' était expérimental et instable dans la version beta de l'API, entraînant des valeurs null pour des champs comme la longitude et la latitude. (#25)~~
- ~~Le passage de l'API en version v1 a corrigé ce problème et stabilisé le comportement du paramètre 'fields'. (#25)~~
- ~~L'API des prélèvements en eau a été mise à jour pour inclure le nom de l'ouvrage dans l'opération 'chroniques'. (#26)~~
- ~~Le nom de l'ouvrage de prélèvement est désormais disponible dans l'API, permettant une sélection géographique directe. (#26)~~
- ~~Le champ 'libelle_precision_coord' de l'API /vbeta/prelevements/referentiel/points_prelevement était toujours null en raison d'un bug, corrigé lors du passage à la version v1 en 2021. (#27)~~
- ~~L'API Prélèvements en eau était en version bêta avec des données incomplètes et des millésimes obsolètes (arrêtés en 2016). (#38)~~
- ~~La version v1 de l'API a été déployée en juin 2021, avec des mises à jour mensuelles et des données alignées sur la BNPE. (#38)~~
- ~~La version bêta de l'API présentait un retard de mise à jour des données par rapport à la source principale (AELB) et un sous-échantillonnage des ouvrages (6872 vs 8508 en Pays de la Loire). (#38)~~
- ~~Le champ code_entite_hydrogeo était mal renseigné dans la version bêta de l'API mais sera corrigé dans la version finale. (#39)~~
- ~~La requête 'ouvrages' de l'API Prélèvements en eau retournait un count 0 avant la correction. (#71)~~
- ~~L'endpoint 'chroniques' de l'API Prélèvements en eau a connu des instabilités avec des erreurs 500, nécessitant temporairement l'ajout du paramètre 'fields' pour obtenir des résultats. (#249)~~
- ~~Le problème a été corrigé, permettant à nouveau l'accès à l'endpoint sans paramètre 'fields'. (#249)~~
- ~~La requête de l'API 'prélèvements chroniques' renvoyait un code erreur 500 lors de la requête sur l'ensemble des champs, mais le problème a été résolu. (#274)~~

### Issues sources

- **#25** [API Prélèvements en eau] - Erreur lors de la récupération des ouvrages (2021-06-16) — Le paramètre 'fields' de l'API Prélèvements en eau a eu des problèmes de stabilité dans la version beta, mais a été corrigé avec la mise à jour en version v1.
- **#26** [API Prélèvement en eau] nom de l'ouvrage dans les chroniques (2021-06-16) — L'API des prélèvements en eau a été mise à jour pour inclure le nom des ouvrages dans les chroniques, facilitant la sélection géographique.
- **#27** [API Prélèvements en eau] - Champs libelle_precision_coord toujours null (2021-06-16) — Le champ 'libelle_precision_coord' de l'API Prélèvements en eau était incorrectement null en version beta, mais le bug a été résolu avec la mise à jour vers la version v1 en 2021.
- **#37** [API Prélèvement] code SIRET des établissements de prélèvement (2020-06-26) — Le code SIRET des établissements n'est pas diffusé par l'API Prélèvements en eau en raison des contraintes de publication des données ouvertes.
- **#38** [API Prélèvements] actualisation des données (2021-06-16) — L'API Prélèvements en eau a été mise à jour en v1 en juin 2021, résolvant les problèmes de complétude et de mise à jour des données.
- **#39** [API Prélèvement] Suggestion d'association du code_bss à l'ouvrage plutôt qu'au point de prélèvement (2020-08-06) — L'API Prélèvements en eau associe incorrectement le code_bss_point_eau au point de prélèvement plutôt qu'à l'ouvrage, avec une correction planifiée pour la version finale.
- **#71** [API prélèvements] Aucune donnée dans la réponse de la requête "ouvrages" ? (2021-07-21) — L'API 'Prélèvements en eau' a temporairement renvoyé des données vides pour l'endpoint 'ouvrages', mais le problème a été corrigé.
- **#136** API Prélèvements - retourne code 400 sur dépassement page * size (2023-05-02) — L'API Prélèvements en eau de Hub'Eau limite les résultats à 20 000 enregistrements, avec un retour de code 400 non explicite et un besoin d'amélioration de la gestion des erreurs.
- **#137** Package R pour requêter les APIs hubeau (2023-05-30) — Un package R permettant d'accéder à 10 APIs Hub'Eau a été publié, avec des exemples d'utilisation et une intégration dans des rapports hydrologiques.
- **#241** Accès impossible aux prélèvements via l'API - "internal error" retourné ce 07 juillet 2025 (2025-07-07) — Une erreur serveur a été signalée le 7 juillet 2025 lors de l'accès à l'API des prélèvements pour le département 28 et l'année 2018.
- **#249** [API Prélèvements en eau] endpoint "chroniques": Erreur 500 sur toutes les requêtes (2025-10-01) — L'endpoint 'chroniques' de l'API Prélèvements en eau a connu des instabilités techniques résolues, avec une période de dépendance temporaire au paramètre 'fields' pour obtenir des résultats.
- **#274** [API Prélèvements en eau] get prelevements chroniques -> Error 500 (2026-02-16) — L'API 'prélèvements chroniques' a connu une erreur 500 lors de requêtes non filtrées, résolue par l'utilisation du paramètre 'fields' ou la correction technique.

</details>
