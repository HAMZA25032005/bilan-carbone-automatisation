# État de l'art : automatisation du Bilan Carbone

*Recherche du 26/10/2026. Sources en fin de document. Attention : la plupart des sources sont des sites d'éditeurs, donc commerciales. Ne retenir que ce qui se recoupe.*

---

## 1. Ce que le marché a appris

1. **L'automatisation fonctionne quand la donnée est physique.** C'est le cas de l'énergie (kWh), des carburants (L), des distances (km) et du fret (t.km). Quand il ne reste qu'un montant en euros, le ratio monétaire porte souvent **80 % d'incertitude**, et l'empreinte suit les prix plutôt que la réalité (Kabaun, Tennaxia, ADEME).
2. **Le plafond d'automatisation se décide en amont**, dans la qualité des exports et des contrats de données avec les prestataires (agence de voyage, loueur, fournisseur d'énergie), pas dans le logiciel (Kabaun).
3. **Certaines décisions restent humaines** : le périmètre, les exclusions, les seuils de coupure, les hypothèses d'estimation, la validation d'un facteur d'émission (FE), le recalcul d'une année de référence (Kabaun, Decarbo'Solution).
4. **L'IA propose, l'humain valide, et tout est tracé.** Tous les éditeurs sérieux convergent sur ce principe : Kabaun « Klem », Sweep « Sweepy », Carbon+Alt+Delete, Persefoni. L'IA sert à suggérer un FE, à classer une dépense, à lire une facture et à détecter des anomalies. Elle ne calcule jamais le chiffre final sans validation.
5. **La traçabilité est l'argument n°1** : remonter de chaque chiffre à sa ligne source, à son unité, au FE et à sa version, à la pièce justificative, à son auteur et à sa date (Kabaun, Zei, Normative, exigences d'audit CSRD).
6. **La reproductibilité se teste** : rejouer le même import doit redonner le même total. Tout écart doit pouvoir s'expliquer (Kabaun).

---

## 2. Climatip, l'outil déjà payé par TDF

Climatip est un éditeur toulousain. Ce qu'il revendique, à vérifier avec l'administrateur Climatip de TDF :

| Capacité annoncée | Conséquence pour nous |
|---|---|
| Collecte directe depuis le SI, via API et exports, « sans template spécifique » | Il existe peut-être un **import plus riche que l'Excel**, à demander |
| **Comptabilité Carbone Analytique** : ventilation par activité, site, équipe, client ou fournisseur, alignée sur le contrôle de gestion | ⚠️ **Climatip sait peut-être déjà ventiler par axe analytique (LP, BU)**. Il faut vérifier avant de reconstruire la démultiplication |
| Sondages auprès des contributeurs, en nombre illimité | Climatip peut **déjà couvrir une partie de la collecte** |
| Auditabilité : chaque indicateur s'explique à partir des données sources et des calculs intermédiaires | Bon point pour l'audit |
| Gestion de projet du bilan (tâches documentées, capitalisation d'une année sur l'autre) | À connaître |
| Restitutions BEGES, GHG Protocol, ISO 14064 | Climatip produit déjà les rapports réglementaires |

**À faire avant de figer l'architecture** : un échange avec l'administrateur Climatip ou l'éditeur (démo gratuite via Next Decision), autour de 5 questions :

1. Quels formats d'import (Excel, CSV, API) et quel modèle de colonnes ?
2. Climatip peut-il appliquer lui-même des **clés de répartition par LP et par BU** ?
3. Climatip peut-il **réexporter** les résultats en CO2e par ligne, pour Power BI et les contrôles ?
4. Quel module de collecte par contributeurs propose-t-il ?
5. Quel historique et quelle piste d'audit conserve-t-il ?

> Principe du brief : ne pas reconstruire ce que Climatip fait. La bonne position de notre solution est probablement celle d'un **hub de préparation, de contrôle et de traçabilité en amont de Climatip**, plus un **retour des résultats pour l'analyse**.

---

## 3. Les fonctionnalités des logiciels du marché qui nous servent

On ne cherche pas à recréer un logiciel de Bilan Carbone, puisque Climatip existe. On reprend uniquement les briques qui comblent les manques entre l'Excel actuel et Climatip.

| # | Fonctionnalité | Vue chez | Intérêt pour TDF | Horizon |
|---|---|---|---|---|
| 1 | **Import Excel avec assistant de mapping des colonnes**, conversion des unités, détection des doublons avant intégration | Kabaun, Zei | Ingérer les matrices actuelles sans copier-coller | Déc. 2026 |
| 2 | **Statut « à valider »** sur toute donnée non confirmée | Zei | Circuit data owner, puis équipe ESG, puis Pilote | Déc. 2026 |
| 3 | **Contrôle de cohérence par rapport à N-1**, avec alerte sur les écarts importants | Zei, Kabaun, Aktio | Les matrices ont déjà une colonne « delta vs N-1 » à exploiter | Déc. 2026 |
| 4 | **Chaque donnée rattachée à sa preuve, à son auteur, à sa date, avec historique** | Zei, Kabaun, Aktio | Les matrices ont déjà des colonnes « Preuve » et « Auditabilité » | Déc. 2026 |
| 5 | **Rejouabilité** : même entrée, même total | Kabaun | Test de non-régression contre la fusion 2025 | Déc. 2026 |
| 6 | **Indicateurs de qualité** : part en monétaire, taux de lignes à revoir, incertitude par poste | Kabaun, Bilan Carbone V9 | Tableau de bord qualité pour la Pilote | Déc. 2026 |
| 7 | **Suivi de l'avancement de la collecte** par contributeur et par domaine, relances | Sami, Zei | Moins de relances manuelles | Déc. 2026 si simple, sinon 2027 |
| 8 | **Pré-remplissage à partir de N-1** : dupliquer les activités de l'année précédente | Aktio | Le data owner ne met à jour que les valeurs | 2027 |
| 9 | **Saisie unique réutilisée** pour plusieurs référentiels (Bilan Carbone, CSRD, GRESB…) | Zei, Sweep | Le classeur contient déjà un lien vers une matrice GRESB | 2027 |
| 10 | **Suggestion par IA, validée par un humain** (catégorie, FE, anomalie expliquée) | Kabaun, Sweep, Persefoni | Sous réserve de l'autorisation des outils d'IA par TDF | 2027 |
| 11 | **Connecteurs directs** (fournisseur d'énergie, cartes carburant, agence de voyage) | Kabaun, Société Générale | L'électricité est le poste le plus automatisable | 2027+ |

---

## 4. La méthode, ce qu'il faut respecter

### Répartition (la « démultiplication »)

D'après le GHG Protocol (Scope 3 Standard, chapitre 8), dans des résumés secondaires :

- On ne répartit que lorsque l'émission n'est mesurée qu'à un niveau global (un site, un contrat) alors qu'elle sert plusieurs produits.
- **La clé doit être un inducteur mesurable** : masse, volume, énergie, surface, unités produites ou valeur. Il vaut mieux un inducteur **physique** qu'un chiffre d'affaires lorsqu'il explique mieux la consommation.
- **Les parts doivent faire 100 %.**
- **On ne change pas de clé d'une période à l'autre sans documenter pourquoi.**

Conséquence pour nous :
- les clés deviennent un **référentiel versionné par campagne**, avec la source et la justification de chaque clé ;
- un test automatique vérifie la somme à 100 % ;
- la zone (Hexagone, Corse, DOM) devient un **champ explicite**, au lieu d'être déduite d'un mot dans un libellé.

### Incertitude et qualité
- La méthode **Bilan Carbone® impose de renseigner l'incertitude** par poste. BEGES et GHG Protocol la rendent facultative (Tennaxia). La V9 combine une approche qualitative et une approche quantitative.
- Ordres de grandeur : un compteur bien étalonné donne 1 à 2 % d'incertitude, une donnée estimée ou extrapolée 10 à 30 %, un FE de la Base Carbone 5 à 50 %, un ratio monétaire jusqu'à 80 %.
- Les matrices TDF ont déjà des colonnes « incertitude » (0 %, 5 %, 15 %, 30 %…). Il faut les rendre **obligatoires et contrôlées**.

### Erreurs classiques à contrôler automatiquement
- Double comptage (carburant compté en Scope 1 et en Scope 3, énergie refacturée).
- Confusion d'unités, montants TTC au lieu de HT.
- Facteurs figés à l'import, millésime ignoré.
- Méthode Scope 2 implicite : il faut à la fois le *location-based* et le *market-based* dès qu'il y a des garanties d'origine.

---

## 5. Contexte réglementaire, l'argument « audit »

- **CSRD après l'Omnibus** (adoption fin 2025, directive 2026/470) : sont concernées les entreprises de **plus de 1 000 salariés ET plus de 450 M€ de chiffre d'affaires**. La transposition française est attendue au plus tard en mars 2027. *TDF dépasse probablement ces seuils : à confirmer en interne.*
- Si TDF est concernée, le volet E1 passe sous **assurance limitée**. Les auditeurs testent les **processus et les contrôles** derrière chaque chiffre : sources documentées, propriétaire de chaque donnée, logique de calcul, justificatifs, séparation des tâches, piste d'audit (Deloitte, EY, Coolset ; normes ISAE 3410 et ISO 14064-3).
- **BEGES réglementaire** : tous les 3 ans pour les organisations de plus de 500 salariés.

> **Argument pour le dossier Snowflake** : la traçabilité n'est pas un « plus ». Elle devient une **exigence d'audit**, et un Excel recopié chaque année ne la satisfait pas.

---

## 6. Briques techniques repérées

| Brique | Ce que ça apporte | Source |
|---|---|---|
| **Streamlit in Snowflake** | Formulaires de saisie qui écrivent directement dans Snowflake, avec l'utilisateur tracé (`st.user`) et les mêmes règles de gouvernance que les données | Documentation Snowflake |
| **Snowflake + données ESG du Marketplace** | Architecture de référence AWS + Snowflake d'un « sustainability data fabric » : ingestion, contrôles qualité, catalogue | AWS Guidance |
| **Microsoft Fabric, Sustainability data solutions** | Modèle de données ESG Microsoft (plus de 400 tables) et modèles Power BI | Microsoft Learn |
| **Base Empreinte (ADEME)** | Plus de 60 000 FE ; une API est annoncée par des tiers mais pas confirmée officiellement | Projet Celsius |
| **Automatisation des données énergétiques** | Société Générale : collecte automatique de l'énergie sur environ 30 pays, pilotée conjointement par l'Immobilier et l'IT | ESG Post |

---

## 7. Délais observés
- Un grand groupe sur un logiciel SaaS met **3 à 6 mois** pour un premier déploiement (Greenly).
- Normative annonce **4 à 8 semaines** pour un premier calcul complet.
- Notre fenêtre jusqu'à mi/fin décembre (environ 7 semaines) impose de se concentrer sur l'aval : ingestion, contrôles, répartition, export, traçabilité.

---

## 8. Questions ouvertes nées de cette recherche
1. Climatip peut-il faire lui-même la répartition analytique par LP et par BU ? *(question décisive)*
2. Climatip a-t-il une API ou un import CSV documenté, et peut-il réexporter les résultats ?
3. TDF entre-t-elle dans le périmètre CSRD post-Omnibus, et qui est l'organisme tiers indépendant (OTI) ?
4. Les CO2e calculés dans l'Excel (colonne « Émissions ») servent-ils de contrôle par rapport à Climatip, ou d'autre chose ?
5. Le *market-based* Scope 2 (garanties d'origine) est-il traité ?

---

## Sources
- Kabaun, *Automatiser le bilan carbone* : https://www.kabaun.com/post/automatiser-bilan-carbone
- Zelio Impact, *Les 6 meilleurs logiciels de bilan carbone en 2025* : https://zelio-impact.com/index.php/2025/07/25/les-6-meilleurs-logiciels-de-bilan-carbone-en-2025-guide-comparatif-complet/
- Decarbo'Solution : https://decarbosolution.ai/automatisation-du-bilan-carbone-logiciel-et-expertise-humaine/
- Sami, guide : https://www.sami.eco/blog/guide-logiciel-bilan-carbone
- Zei : https://zei-world.com/
- Sweep : https://www.sweep.net/fr
- Normative : https://normative.io/
- Persefoni : https://www.persefoni.com/fr
- Aktio, questions à se poser : https://www.aktio.cc/ressources/logiciel-bilan-carbone ; https://www.aktio.cc/
- Carbon+Alt+Delete, IA et bilan carbone : https://www.carbonaltdelete.eu/fr/insights/l-ia-au-service-du-bilan-carbone/
- Tennaxia, guide Bilan Carbone : https://www.tennaxia.com/blog/bilan-carbone-2022-le-guide-complet
- Tennaxia, incertitude : https://www.tennaxia.com/en/blog/tout-savoir-sur-lincertitude-dans-la-mesure-de-lempreinte-carbone
- ABC, solutions et outils : https://abc-transitionbascarbone.fr/agir/nos-solutions-et-outils/
- Société Générale (page en accès 403) ; résumé : https://esgpost.com/societe-generale-deploys-automated-energy-data-system-to-accelerate-decarbonisation/
- Climatip : https://climatip.fr/cca/ ; https://climatip.fr/en/ghg-emissions-and-climate-strategy/ ; https://www.next-decision.fr/solutions/data-rse-esg/bilan-carbone/climatip ; https://adopteunlogicielfrancais.fr/climatip/
- Répartition GHG Protocol (résumé Deloitte DART) : https://dart.deloitte.com/USDART/home/publications/deloitte/additional-deloitte-guidance/greenhouse-gas-protocol-reporting-considerations/chapter-6-ghg-protocol-scope-3/6-5-allocating-emissions
- Assurance CSRD : https://coolset.com/academy/csrd-compliance-audit ; https://www.ey.com/en_ie/insights/sustainability/csrd-prep-voluntary-assurance-for-esg-reporting
- Seuils CSRD Omnibus : https://portail-rse.beta.gouv.fr/csrd/seuils-csrd-omnibus-criteres-d-application/
- Streamlit in Snowflake, formulaire avec écriture : https://docs.snowflake.com/en/developer-guide/streamlit/getting-started/example-crud-app
- AWS + Snowflake, sustainability data fabric : https://docs.aws.amazon.com/solutions/building-a-sustainability-data-fabric-with-snowflake-on-aws/
- Microsoft, sustainability architecture : https://learn.microsoft.com/en-us/industry/well-architected/sustainability/sustainability-architecture-overview
- Base Empreinte : https://projetcelsius.com/glossaire/base-carbone/
- Bilan Carbone V9 : https://www.hellio.com/actualites/evenements/version-9-bilan-carbone
