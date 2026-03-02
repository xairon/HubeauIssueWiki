# Phytopharmaceutiques

## Particularités techniques

- La version 1 de l'API vente et achat de produits phytopharmaceutiques est en ligne. (#201)
- La documentation de l'API est disponible à l'adresse https://hubeau.eaufrance.fr/page/api-vente-et-achat-de-produits-phytopharmaceutiques. (#201)
- Les APIs Hub'Eau ne fournissent pas de concentrations journalières agrégées à l'échelle départementale pour des paramètres spécifiques comme le métolachlore ESA. (#220)
- Le rôle de Hub'Eau est de donner accès aux données brutes ou semi-brutes, et non de fournir des analyses hydrologiques complexes ou des agrégations de données à l'échelle départementale. (#220)
- L'actualisation des données de l'API Vente et achat de produits phytopharmaceutiques se fait par remplacement intégral. (#232)
- Une rétroactivité est possible sur les trois dernières années lors de l'actualisation des données de l'API Vente et achat de produits phytopharmaceutiques. (#232)

## Informations métier

- L'API diffuse des données ouvertes sur les ventes et achats de produits phytopharmaceutiques. (#201)
- Les données proviennent des déclarations annuelles des distributeurs agréés. (#201)
- Les données incluent les quantités de produits et de substances actives vendues ou achetées. (#201)
- Les données de ventes sont disponibles depuis 2008. (#201)
- Les données d'achats sont disponibles depuis 2013. (#201)
- Les données sont collectées par les agences de l'eau pour la redevance pour pollutions diffuses. (#201)
- Les données sont bancarisées par l'Office français de la biodiversité dans la Banque Nationale des Ventes de produits phytopharmaceutiques (BNV-D) Traçabilité. (#201)
- C'est la treizième API Hub'eau. (#201)
- L'estimation d'une concentration journalière globale pour un paramètre (ex: métolachlore ESA) sur un département entier à partir de mesures de stations multiples nécessite une méthodologie spécifique. (#220)
- La simple moyenne des concentrations mesurées par toutes les stations un jour donné n'est pas nécessairement la méthode la plus pertinente pour estimer une concentration départementale globale. (#220)
- Pour les questions méthodologiques concernant l'interprétation et l'agrégation des données de qualité de l'eau (eaux souterraines ou superficielles), il convient de contacter directement les équipes expertes d'Ades (eaux souterraines) ou de Naïades (eaux superficielles). (#220)
- Les données 2023 issues de la banque nationale BNV-D Traçabilité sont désormais exposées par l'API Hub’eau Vente et achat de produits phytopharmaceutiques. (#232)
- Les données de ventes de produits phytopharmaceutiques couvrent la période de 2008 à 2023 inclus. (#232)
- Les données de ventes de produits phytopharmaceutiques sont proposées avec les niveaux de regroupement France entière, région et département. (#232)
- Les données d'achats de produits phytopharmaceutiques couvrent la période de 2013 à 2023 inclus. (#232)
- Les données d'achats de produits phytopharmaceutiques sont proposées avec les niveaux de regroupement France entière, région, département et zone postale. (#232)

---

## Issues sources

- **#201** [API vente et achat PPP] mise en ligne de la version 1 — L'API vente et achat de produits phytopharmaceutiques (la treizième API Hub'eau) est en ligne en version 1, offrant des données sur les quantités de produits et substances actives vendues (depuis 2008) et achetées (depuis 2013), issues des déclarations des distributeurs et bancarisées par l'OFB. `[information]`
- **#220** Question sur le calcul de la concentration journalière du métolachlore ESA du departement de Finistère de toutes les stations present. — Hub'Eau ne fournit pas de concentrations journalières agrégées à l'échelle départementale et redirige vers Ades ou Naïades pour les questions méthodologiques d'interprétation des données de qualité de l'eau. `[résolu]`
- **#232** [API Vente et achat de PPP] Mise en ligne des données 2023 — L'API Hub'eau Vente et achat de produits phytopharmaceutiques a été mise à jour avec les données 2023, couvrant les ventes de 2008 à 2023 et les achats de 2013 à 2023, avec des niveaux de regroupement géographiques spécifiques et une actualisation par remplacement intégral avec rétroactivité sur 3 ans. `[information]`
