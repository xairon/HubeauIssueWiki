# Phytopharmaceutiques

> 2 issues analysées

## Guide

### Comportement actuel  
L'API 'Vente et achat de produits phytopharmaceutiques' (version 1) fournit des données sur les quantités de produits phytopharmaceutiques vendus (2008-2023) et achetés (2013-2023), regroupées à plusieurs niveaux géographiques (France, région, département, zone postale). Les données sont accessibles via des endpoints distincts pour les ventes et les achats, en format JSON. La pagination est nécessaire pour les grandes périodes, et les paramètres clés incluent l'année, le niveau géographique et le type de produit (#201, #232).  

### Pièges à éviter  
Les données sont mises à jour par remplacement intégral, ce qui peut rendre les anciennes versions inaccessibles. Les utilisateurs doivent vérifier la rétroactivité des trois dernières années pour éviter des lacunes. De plus, les niveaux géographiques diffèrent entre ventes (3) et achats (4), ce qui peut compliquer les analyses croisées.  

### Bonnes pratiques  
Utilisez toujours les paramètres de regroupement géographique les plus précis possibles pour éviter une perte d'information. Vérifiez régulièrement les mises à jour de 2023 pour bénéficier des dernières données. Complétez les analyses avec des contextes métiers, comme la redevance pour pollutions diffuses, pour mieux interpréter les quantités de substances actives.  

### Contexte métier  
Les données servent à calculer la redevance pour pollutions diffuses, liée aux usages agricoles de produits phytopharmaceutiques. Les agences de l'eau collectent les déclarations annuelles des distributeurs, puis l'Office français de la biodiversité bancarise ces données. Les substances actives sont des composants chimiques responsables de la pollution, et leurs quantités influencent les redevances.  

### Évolutions récentes  
- **2025-05-09** : Mise en ligne des données 2023, avec des niveaux géographiques étendus (4 pour les achats) et une rétroactivité sur trois ans (#232).  
- **2024-11-25** : Lancement de la version 1 de l'API, couvrant les ventes depuis 2008 et les achats depuis 2013 (#201).  

### Historique notable  
*Rien de notable.*

---

<details>
<summary><strong>Archive détaillée</strong> — Tous les faits bruts extraits des issues</summary>

### Faits actuels

- L'API 'Vente et achat de produits phytopharmaceutiques' est désormais disponible en version 1 sur la plateforme Hub'Eau. (#201)
- Les données proviennent des déclarations annuelles des distributeurs agréés, collectées par les agences de l'eau et bancarisées par l'Office français de la biodiversité. (#201)
- Les données couvrent les ventes depuis 2008 et les achats depuis 2013, utilisées pour calculer la redevance pour pollutions diffuses. (#201)
- Les données décrivent les quantités de produits et de substances actives vendues ou achetées à l'échelle nationale. (#201)
- L'API propose des données avec des niveaux de regroupement géographique differents pour les ventes (3 niveaux) et les achats (4 niveaux) (#232)
- Les données ont été mises à jour par remplacement intégral avec rétroactivité possible sur les trois dernières années (#232)
- Les données de ventes couvrent la période 2008-2023 avec regroupement à la France, région et département (#232)
- Les données d'achats couvrent la période 2013-2023 avec regroupement à la France, région, département et zone postale (#232)

### Issues sources

- **#201** [API vente et achat PPP] mise en ligne de la version 1 (2024-11-25) — La version 1 de l'API 'Vente et achat de produits phytopharmaceutiques' est mise en ligne, fournissant des données sur les quantités de produits phytopharmaceutiques depuis 2008 et 2013.
- **#232** [API Vente et achat de PPP] Mise en ligne des données 2023 (2025-05-09) — Les données de vente et d'achat de produits phytopharmaceutiques pour 2023 sont désormais disponibles via l'API Hub'eau avec des périodes et granularités géographiques spécifiques.

</details>
