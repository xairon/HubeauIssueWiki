# Qualité de l'eau potable

> 17 issues analysées

## Guide

### Comportement actuel

L'API Qualité de l'eau potable est en version 1 (v1) et conserve le même périmètre fonctionnel que sa version bêta (#90). L'endpoint `resultats_dis` permet des filtrages précis par `code_commune`, `code_parametre_se`, `date_min_prelevement` et `date_max_prelevement`, avec la possibilité de sélectionner des champs spécifiques via le paramètre `fields` (#111). Pour obtenir la dernière mesure d'un paramètre, utilisez les paramètres `sort=desc` et `size=1` (#84). Les recherches par libellé (`libelle_parametre_...`) sont permissives (texte partiel, insensible à la casse et aux accents), tandis que celles par code (`code_parametre_...`) sont strictes (#141). L'API retourne les données par 'analyse' (le `count` de la réponse reflète ce nombre) et les champs `reseaux.code` et `reseaux.nom` peuvent être multivalués (#211, #174). L'ordre des colonnes dans les réponses CSV est fixe et ne dépend pas de l'ordre spécifié dans `fields` (#119). La date de dernière ingestion des données est affichée sur la page web de l'API Hub'Eau (#90, #266).

### Pièges à éviter

Une anomalie majeure impacte actuellement l'ensemble des données de l'API, concernant des associations incorrectes entre prélèvements amont et Unités de Distribution (UDI) aval. Les mises à jour sont suspendues jusqu'à correction complète, prévue mi-avril au plus tôt (#276). La fraîcheur des données est limitée : elles sont mises à jour mensuellement (vers le 15 ou 16 du mois) et concernent le mois N-2, ce qui peut créer un décalage avec les fichiers sources (#90, #155). Le filtrage direct des UDIs par département est impossible, et la recherche par `code_commune` est limitée à 20 codes Insee par requête, rendant les requêtes départementales complexes (#128). L'API ne fournit pas de fonctions d'agrégation pour les prélèvements uniques ou les listes de paramètres uniques, ni de descriptions détaillées des réseaux (#211, #139, #174). Enfin, récupérer la dernière mesure pour plusieurs paramètres différents nécessite des requêtes distinctes pour chaque paramètre (#84).

### Bonnes pratiques

Pour des recherches précises de paramètres, privilégiez les codes Sandre (`code_parametre`) ou CAS (`code_parametre_cas`) plutôt que les libellés (#141). Lors du traitement des données CSV, fiez-vous aux en-têtes de colonne, car leur ordre est fixe et indépendant du paramètre `fields` (#119). Pour compter les prélèvements uniques ou filtrer par département, il est nécessaire de traiter la réponse côté client (unicité sur `code_prelevement`) ou d'utiliser l'API Geo de la DINUM pour obtenir les codes Insee des communes, en gérant la pagination pour la limite de 20 codes par requête (#211, #128). Le package R `hubeau` est recommandé pour les utilisateurs R, simplifiant l'accès à l'API (#137). Pour des analyses complexes ou des détails sur les réseaux, les fichiers sources disponibles sur data.gouv.fr restent une alternative précieuse (#211, #174).

### Contexte métier

Les données de qualité de l'eau potable proviennent des fichiers publiés par la DGS (Direction Générale de la Santé) sur data.gouv.fr, avec des améliorations de fraîcheur prévues par le Ministère de la Santé à l'avenir (#84, #266, #276). Les paramètres de mesure sont identifiés par leur `code_parametre_se` (code SISE-Eaux), mais les codes Sandre (`code_parametre`, ex: 1302 pour le pH) ou CAS (`code_parametre_cas`) sont préférables pour l'interopérabilité des données (#84, #141, #139). Les données sont structurées par 'analyse', ce qui signifie qu'un même prélèvement (`code_prelevement` unique) peut contenir plusieurs analyses (#211, #155). Les Unités de Distribution (UDI) sont identifiées par les codes Insee des communes, les données sources n'incluant pas directement les codes ou libellés des départements d'implantation des UDI (#128). Les champs de conformité sont censés être uniformes pour un même prélèvement, car ils proviennent d'une source unique (#172).

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API `/vbeta/qualite_eau_potable/communes_udi` ne dispose pas de paramètre direct pour filtrer les Unités de Distribution (UDI) par département (ex: `nom_departement` ou `code_departement`). (#128)
- La version beta de l'API Hub'Eau Qualité de l'eau potable limite le nombre de codes Insee pour le critère de recherche `code_commune` à 20 items par requête. (#128)
- Un contournement pour filtrer les UDIs par département consiste à utiliser l'API Geo de la DINUM pour obtenir la liste des codes Insee des communes d'un département, puis à les passer au paramètre `code_commune` de l'API Hub'Eau. (#128)
- La limite de 20 codes Insee par requête rend le filtrage complet par département difficile, car un département peut contenir un grand nombre de communes (environ 400). (#128)
- L'équipe Hub'Eau étudiera la possibilité d'augmenter la limite du paramètre `code_commune` pour la version stable de l'API Qualité de l'eau potable. (#128)
- Les données ouvertes consommées par l'API Qualité de l'eau potable (issues de data.gouv.fr) n'intègrent pas les codes ou libellés des départements d'implantation des unités de distribution (UDI). (#128)
- Les codes Insee des communes sont utilisés pour identifier les unités de distribution (UDI). (#128)
- L'API ne fournit pas actuellement de fonctionnalité pour obtenir une liste unique (sans doublon) des paramètres mesurés (ex: code_parametre_se, libelle_parametre_maj) pour une commune, un réseau et une période données. (#139)
- Une évolution de l'API est demandée pour ajouter cette fonctionnalité. (#139)
- Les utilisateurs ont besoin d'identifier les paramètres uniques mesurés dans les données de qualité de l'eau potable, filtrés par commune, réseau et période. (#139)
- Les identifiants de paramètres incluent 'code_parametre_se' et 'libelle_parametre_maj'. (#139)
- L'API Qualité des nappes peut nécessiter de nombreuses requêtes pour obtenir des métadonnées (années, producteurs, paramètres) par station, pouvant entraîner des résultats vides. (#204)
- Il existe une limitation à 20 000 résultats par requête sur l'API Qualité des nappes, nécessitant le fractionnement des requêtes. (#204)
- Un nouveau endpoint "_parametres" est prévu pour les APIs de qualité (rivières, nappes, eau potable) afin d'optimiser les interrogations. (#204)
- Le endpoint "_parametres" sera d'abord ajouté à l'API Qualité des cours d'eau. (#204)
- Les remarques de l'utilisateur concernant les métadonnées (années, producteurs, paramètres) seront prises en compte pour l'implémentation du endpoint "_parametres" sur l'API Qualité des nappes. (#204)
- Les utilisateurs de l'API Qualité des nappes ont besoin de connaître les années de données disponibles, les producteurs d'analyses et les paramètres analysés pour chaque station de mesure afin d'optimiser leurs requêtes. (#204)
- L'API Qualité de l'eau potable (endpoint `resultats_dis`) retourne les données par 'analyse', et non par 'prélèvement'. (#211)
- La variable `count` de la réponse de l'API Qualité de l'eau potable (endpoint `resultats_dis`) indique le nombre d'analyses, et non le nombre de prélèvements uniques. (#211)
- L'ajout d'une fonction d'agrégation ou d'unicité directement dans les APIs Hub'Eau n'est pas prévu à court terme. (#211)
- Pour obtenir le nombre de prélèvements uniques, il est nécessaire de parcourir l'intégralité de la réponse et d'appliquer une opération d'unicité sur le champ `code_prelevement` côté client. (#211)
- Les données de qualité de l'eau potable sont structurées par 'analyse', ce qui signifie qu'un même prélèvement peut contenir plusieurs analyses. (#211)
- Pour des analyses statistiques complexes ou des agrégations non supportées par l'API, les fichiers sources disponibles sur data.gouv.fr sont une alternative recommandée (ex: https://www.data.gouv.fr/fr/datasets/resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune/). (#211)
- Le producteur ne déposera pas de données complémentaires pour l'API Qualité de l'eau potable tant que la correction de l'anomalie n'est pas terminée. (#276)
- Les prochaines données corrigées pour l'API Qualité de l'eau potable seront disponibles mi-avril au mieux. (#276)
- Une anomalie a été constatée dans les données de résultats du contrôle sanitaire de l'eau distribuée commune par commune, utilisées pour alimenter l'API Qualité de l'eau potable. (#276)
- L'anomalie impacte l'ensemble des données de l'API Qualité de l'eau potable. (#276)
- L'anomalie concerne des prélèvements réalisés sur des installations amont qui continuaient à être associés à des Unités de Distribution d'eau (UDI) aval alors que le lien n'existait plus. (#276)
- La correction de l'anomalie est en cours et l'ensemble des données historiques sera rattrapé et corrigé. (#276)
- La source des données est le jeu de données 'resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune' disponible sur data.gouv.fr. (#276)

### Historique des problèmes résolus

- ~~Pour récupérer la dernière mesure d'un paramètre, il faut ajouter les paramètres de requête sort=desc et size=1. (#84)~~
- ~~L'API ne permet pas de récupérer la dernière mesure pour plusieurs paramètres différents (ex: SO4 et PH) en une seule requête pour une même localisation ; des requêtes multiples sont nécessaires. (#84)~~
- ~~L'API est en version bêta et les retours d'utilisateurs sont activement recherchés pour identifier les besoins. (#84)~~
- ~~Les paramètres de mesure sont identifiés par leur code SISE-Eaux (code_parametre_se). (#84)~~
- ~~La source des données sur l'eau potable est le site solidarites-sante.gouv.fr. (#84)~~
- ~~Le Ministère de la Santé prévoit de mettre à disposition des webservices qui permettront à Hub'Eau de diffuser des données sur l'eau potable plus fraîches à l'avenir. (#84)~~
- ~~La date de dernière ingestion des données est affichée sur la page web de l'API Qualité de l'eau potable (https://hubeau.eaufrance.fr/page/api-qualite-eau-potable). (#90)~~
- ~~L'API Qualité de l'eau potable est passée en version 1 (v1) en août (après juillet 2022). (#90)~~
- ~~La version 1 de l'API Qualité de l'eau potable a le même périmètre fonctionnel que la version bêta. (#90)~~
- ~~Les données de qualité de l'eau potable sont mises à jour tous les 15 du mois. (#90)~~
- ~~Les données de qualité de l'eau potable disponibles concernent le mois N-2 (où N est le mois actuel). (#90)~~
- ~~L'endpoint `resultats_dis` de l'API Qualité de l'eau potable renvoyait une erreur "Internal server error" si le paramètre `fields` était omis dans la requête. (#111)~~
- ~~La réponse d'erreur spécifique était `{"code": "Internal server error", "message": "", "field_errors": null}`. (#111)~~
- ~~Le problème a été résolu par un redémarrage de l'API. (#111)~~
- ~~L'endpoint `resultats_dis` permet de filtrer les résultats par `code_commune`, `code_parametre_se`, `date_min_prelevement` et `date_max_prelevement`. (#111)~~
- ~~`ACRYL` est un exemple de `code_parametre_se` utilisé pour filtrer les données. (#111)~~
- ~~Des champs comme `date_prelevement` et `resultat_numerique` peuvent être spécifiés via le paramètre `fields`. (#111)~~
- ~~L'endpoint `/vbeta/qualite_eau_potable/resultats_dis` a été signalé comme temporairement indisponible. (#113)~~
- ~~Un utilisateur a identifié un problème potentiel lors de l'utilisation du paramètre `sort=asc` avec l'endpoint `/vbeta/qualite_eau_potable/resultats_dis`. (#113)~~
- ~~Le fonctionnement normal de l'endpoint `/vbeta/qualite_eau_potable/resultats_dis`, y compris avec le paramètre `sort=asc`, a été confirmé ultérieurement. (#113)~~
- ~~L'ordre des colonnes dans les fichiers CSV retournés par l'API Qualité de l'eau potable est fixe et ne respecte pas l'ordre spécifié dans le paramètre 'fields'. (#119)~~
- ~~Le paramètre 'fields' sert uniquement à sélectionner les colonnes à inclure, pas à définir leur ordre. (#119)~~
- ~~L'ordre des colonnes dans les réponses CSV de l'API Qualité de l'eau potable devrait rester stable, y compris lors du passage à la version 1 de l'API. (#119)~~
- ~~Il est recommandé de se baser sur les en-têtes de colonne plutôt que sur leur position numérique pour le traitement des données. (#119)~~
- ~~Le package R `hubeau` version 0.4.0 est disponible sur le CRAN. (#137)~~
- ~~Le package `hubeau` permet de requêter 10 des 12 APIs Hub'Eau. (#137)~~
- ~~La syntaxe des fonctions de requête du package `hubeau` est `get_[API]_[Operation](champ1 = valeur1, champ2 = valeur2...)`. (#137)~~
- ~~Le package `hubeau` est documenté avec des exemples d'utilisation et des vignettes. (#137)~~
- ~~Le code source du package `hubeau` est disponible sur GitHub à l'adresse `https://github.com/inrae/hubeau`. (#137)~~
- ~~Les éléments descriptifs du package R `hubeau` ont été ajoutés à la page de réutilisations GitHub du projet Hub'eau (`https://github.com/BRGM/hubeau/tree/master/re-utilisations`) et non sur le site éditorial. (#137)~~
- ~~Le package R `hubeau` couvre les APIs suivantes : Écoulement des cours d'eau, Hydrométrie, Indicateurs des services, Piézométrie, Poisson, Prélèvements en eau, Qualité de l'eau potable, Qualité des nappes d'eau souterraines, Température des cours d'eau. (#137)~~
- ~~L'OFB DR Normandie utilise le package R `hubeau` pour réaliser un rapport de situation mensuelle de l'écoulement des cours d'eau des bassins versants bretons. (#137)~~
- ~~Une vignette du package `hubeau` propose une application sur l'API Écoulement, incluant la réalisation de cartes et de graphiques synthétiques. (#137)~~
- ~~Les champs de l'API Hub'Eau de type libelle_parametre_... effectuent des recherches permissives (texte partiel, insensible à la casse et aux accents). (#141)~~
- ~~Les champs de l'API Hub'Eau de type code_parametre_... effectuent des recherches strictes. (#141)~~
- ~~Pour rechercher un paramètre spécifique sans ambiguïté, il est recommandé d'utiliser les champs code_parametre (code Sandre) ou code_parametre_cas (code CAS) plutôt que les libellés. (#141)~~
- ~~Le code Sandre pour le paramètre pH est 1302. (#141)~~
- ~~Le champ code_parametre_se correspond à un code spécifique à l'application SISE-Eaux. (#141)~~
- ~~Les codes Sandre (code_parametre) et CAS (code_parametre_cas) sont préférables pour l'interopérabilité des données. (#141)~~
- ~~L'actualisation des données de l'API Qualité de l'eau potable est effectuée mensuellement, généralement dans la journée du 15. (#155)~~
- ~~Lors des mises à jour mensuelles, les données de l'API sont remplacées par le contenu des fichiers sources, qui peuvent contenir des analyses antérieures au mois écoulé. (#155)~~
- ~~Des prélèvements récents peuvent ne pas être immédiatement disponibles via l'API avant la prochaine mise à jour mensuelle, même s'ils sont présents dans les fichiers sources (ex: DIS_RESULT.txt). (#155)~~
- ~~La disponibilité des données via l'API peut être décalée par rapport à leur présence dans les fichiers sources (data.gouv.fr) en raison du cycle de mise à jour mensuel. (#155)~~
- ~~Les données de qualité de l'eau potable sont identifiées par un `code_prelevement` unique (ex: 07200134324). (#155)~~
- ~~Les données de l'API Qualité de l'eau potable sont basées sur des fichiers sources comme DIS_RESULT.txt. (#155)~~
- ~~L'API `/api/v1/qualite_eau_potable/resultats_dis` présentait un bug où les champs de conformité (`conformite_references_pc_prelevement`, `conformite_references_bact_prelevement`, `conformite_limites_pc_prelevement`, `conformite_limites_bact_prelevement`) pouvaient être incohérents pour un même prélèvement. (#172)~~
- ~~Ce bug a été corrigé et n'est plus reproductible après un rechargement des données effectué le 15/05/2024. (#172)~~
- ~~Avant la correction, il était recommandé aux utilisateurs d'implémenter des stratégies de mitigation (ex: prendre le "pire cas") pour gérer l'incohérence des données de conformité. (#172)~~
- ~~Les champs de conformité (`conformite_references_pc_prelevement`, `conformite_references_bact_prelevement`, `conformite_limites_pc_prelevement`, `conformite_limites_bact_prelevement`) sont censés être uniformes pour un prélèvement donné, car ils proviennent d'une source unique (data.gouv.fr). (#172)~~
- ~~L'API Hub'Eau /qualite_eau_potable/resultats_dis peut retourner des champs 'reseaux.code' et 'reseaux.nom' multivalués pour un même résultat. (#174)~~
- ~~L'erreur 'Column names `reseaux.code` and `reseaux.nom` must not be duplicated' provient du package R 'hubeau' et non de l'API Hub'Eau. (#174)~~
- ~~L'API Hub'Eau ne propose pas d'endpoint pour obtenir des descriptions détaillées des réseaux d'eau potable (UGE, distributeurs, MOA, géométrie UDI). (#174)~~
- ~~Pour des descriptions détaillées des réseaux d'eau potable, il est recommandé de consulter les données brutes sur data.gouv.fr ou de contacter le service producteur. (#174)~~
- ~~L'API Hub'Eau 'Qualité de l'eau potable' a connu une période d'indisponibilité le 2025-07-12. (#244)~~
- ~~Le service de l'API 'Qualité de l'eau potable' a été rétabli le 2025-07-12. (#244)~~
- ~~Les informations sur la fréquence de mise à jour de l'API Qualité de l'eau potable sont disponibles dans la section 'présentation' de la page dédiée à l'API sur le site Hub'Eau. (#266)~~
- ~~Les données de l'API Qualité de l'eau potable sont mises à jour le 15 ou 16 de chaque mois. (#266)~~
- ~~Les données de l'API Qualité de l'eau potable proviennent des fichiers publiés par la DGS (Direction Générale de la Santé). (#266)~~

### Issues sources

- **#84** /vbeta/qualite_eau_potable/resultats_dis dernière mesure par paramètre — L'API Qualité de l'eau potable permet d'obtenir la dernière mesure d'un paramètre via les paramètres sort=desc et size=1, mais requiert des requêtes multiples pour plusieurs paramètres, et des améliorations de la fraîcheur des données sont prévues par le Ministère de la Santé. `[résolu]`
- **#90** [API QUALITÉ DE L'EAU POTABLE] - date des données — Cette issue informe sur l'affichage de la date de dernière ingestion des données de l'API Qualité de l'eau potable, sa fréquence de mise à jour (N-2, le 15 du mois) et son passage en v1 avec un périmètre fonctionnel identique à la bêta. `[résolu]`
- **#111** [API Qualité de l'eau] Error: Internal Server Error — L'API Qualité de l'eau potable (endpoint `resultats_dis`) a temporairement renvoyé une erreur "Internal server error" lorsque le paramètre `fields` était absent de la requête, un problème résolu par un redémarrage. `[résolu]`
- **#113** [API Qualité de l'eau] Error: Internal Server Error — Un utilisateur a signalé une erreur serveur et un problème avec le paramètre `sort=asc` sur l'API Qualité de l'eau potable, mais le fonctionnement normal a été confirmé et le problème résolu. `[résolu]`
- **#119** [API QUALITÉ DE L'EAU POTABLE] — L'API Hub'Eau Qualité de l'eau potable renvoie les colonnes CSV dans un ordre fixe, indépendant de l'ordre spécifié dans le paramètre 'fields', et cet ordre est stable. `[résolu]`
- **#128** API qualité eau potable — L'API Qualité de l'eau potable ne permet pas de filtrer directement les UDIs par département et la recherche par `code_commune` est limitée à 20 items, nécessitant un contournement via l'API Geo et une future étude d'augmentation de cette limite. `[information]`
- **#137** Package R pour requêter les APIs hubeau — Le package R `hubeau` version 0.4.0 est disponible sur le CRAN, permettant de requêter 10 des 12 APIs Hub'Eau avec une syntaxe simplifiée, et est utilisé par l'OFB pour des rapports mensuels sur l'écoulement des cours d'eau. `[résolu]`
- **#139** [API QUALITÉ DE L'EAU POTABLE] Liste paramètres uniques (sans doublon) — L'issue demande une évolution de l'API Qualité de l'eau potable pour obtenir une liste unique des paramètres mesurés pour une commune, un réseau et une période donnés. `[en_cours]`
- **#141** [API QUALITÉ DE L'EAU POTABLE] recherche contenu parametre "PH". Anomalie ? — Cette issue clarifie le comportement de recherche des paramètres par libellé (permissif) et par code (strict) dans l'API Qualité de l'eau potable, recommandant l'utilisation des codes Sandre pour une recherche précise et interopérable. `[résolu]`
- **#155** [API QUALITÉ DE L'EAU POTABLE] numéro de prélèvement non trouvé — L'API Qualité de l'eau potable est mise à jour mensuellement autour du 15, ce qui peut entraîner un décalage entre la disponibilité des données dans les fichiers sources et leur accès via l'API. `[résolu]`
- **#172** [API Qualité de l'eau] bug sur les conformités — Un bug de cohérence des données a été identifié et corrigé dans l'API Qualité de l'eau potable, où les champs de conformité pour un même prélèvement pouvaient différer selon le paramètre, alors qu'ils devraient être identiques. `[résolu]`
- **#174** [API : QUALITE EAU POTABLE] Erreur sur interrogation par réseau — L'erreur 'Column names `reseaux.code` and `reseaux.nom` must not be duplicated' lors de l'interrogation de l'API Hub'Eau Qualité Eau Potable provient du package R gérant les champs réseau multivalués, et l'API ne fournit pas de descriptions détaillées des réseaux. `[résolu]`
- **#204** [API Qualité des nappes d'eau souterraines] Ajout d'élément à la liste des stations de mesure — L'issue met en évidence le besoin de métadonnées (années, producteurs, paramètres) pour les stations de qualité des nappes afin d'optimiser les requêtes et contourner la limite de 20 000 résultats, et Hub'Eau prévoit un nouveau endpoint "_parametres" pour les APIs de qualité, d'abord sur les cours d'eau. `[en_cours]`
- **#211** [API : QUALITE EAU POTABLE] Besoin de calculer le nombre de prelevement sans parcourir response.data — L'API Qualité de l'eau potable ne permet pas de compter directement les prélèvements uniques car elle retourne les données par analyse, et l'ajout de fonctions d'agrégation n'est pas prévu à court terme, suggérant l'utilisation des fichiers sources de data.gouv pour ce type d'analyse. `[information]`
- **#244** [API : QUALITE EAU POTABLE] service HS — L'API Hub'Eau 'Qualité de l'eau potable' a connu une indisponibilité temporaire le 2025-07-12, qui a été résolue le même jour. `[résolu]`
- **#266** [API qualite_eau_potable] Données non mises à jour — L'API Qualité de l'eau potable est mise à jour le 15 ou 16 de chaque mois à partir des fichiers de la DGS, une information disponible sur la page de l'API. `[résolu]`
- **#276** [API Qualité de l'eau potable] anomalie dans les données sources — Une anomalie majeure affectant l'ensemble des données de l'API Qualité de l'eau potable est en cours de correction, entraînant une suspension des mises à jour jusqu'à mi-avril au plus tôt. `[en_cours]`

</details>
