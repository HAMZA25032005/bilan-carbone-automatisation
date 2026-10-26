# Brief projet — Automatisation du Bilan Carbone TDF

## Qui je suis
Hamza, alternant (contrat de professionnalisation) chez **TDF** (Montrouge), poste « Chargé de projets Data RSE » — en pratique du data engineering : pipelines, automatisation, dashboards Power BI à venir. Étudiant ingénieur Data Science & IA (CESI). Je suis à l'aise en Python/data (Python pas encore confirmé sur mon poste TDF : prévois une option sans Python ou dis-moi précisément quoi installer), mais **pas expert des outils Microsoft low-code** (Power Automate, Forms…) : si tu en proposes, explique pas à pas.

Ma tutrice : **Anne-Isabelle Le Nagard**, Pilote Bilan Carbone (responsable de la méthodologie de calcul du groupe). Elle valide les orientations.
Interlocuteur IT : **Samy**, équipe Systèmes d'Information et Data.

## Le problème à résoudre
TDF produit chaque année un **Bilan Carbone** (partie **E – Environnement** de l'ESG uniquement), **publié fin février**. La collecte 2026 **vient de commencer**. **La solution doit être automatisée et opérationnelle mi/fin décembre 2026** (objectifs annuels) et servir à la campagne en cours.

Aujourd'hui le processus est largement manuel :
1. Des **data owners internes** (métiers + équipe ESG) remplissent des données d'activité dans un **fichier Excel** conçu par ma tutrice.
2. Ces données alimentent une **matrice physique** et une **matrice monétaire**.
3. Il existe des **matrices individuelles** (une par domaine, ex. `VEVE-DEPL`) qui sont fusionnées en une **matrice globale**.
4. Dans la matrice de fusion, chaque donnée saisie est **démultipliée par Ligne de Produit** (1 ligne saisie → ~20 lignes). Ce n'est pas aléatoire : ça suit des **règles** que ma tutrice applique aujourd'hui via un prompt dans Claude pour Excel. Ce n'est donc ni automatisé ni industrialisé.
5. La matrice de fusion comporte aussi **6 colonnes de calcul** (formules propres).
6. Le résultat doit ensuite alimenter **Climatip**.

**Mon objectif : automatiser de bout en bout la collecte → le traitement (dont la démultiplication) → la centralisation des données du Bilan Carbone**, pour que ce soit fiable, traçable, reproductible chaque année, et nettement moins dépendant du copier-coller.

## Contraintes et décisions déjà actées (à respecter)
- **Compatibilité Snowflake, principe clé du projet** : la cible est Snowflake (environnement sécurisé, pas SharePoint). Nous ne sommes pas encore priorisés pour l'accès, mais les retours sont positifs (la cheffe du pôle en a parlé à la direction). **Tout doit être conçu dès le départ pour migrer vers Snowflake sans réécriture** : modèle de données relationnel propre, SQL standard et portable, transformations séparées du stockage. En attendant, la solution doit tourner **sans Snowflake**.
- **Collecte en cours** : la saisie 2026 a déjà démarré avec le fichier Excel actuel. Pour cette campagne, la valeur est surtout **en aval** (validation, démultiplication, fusion, export Climatip, traçabilité). La solution doit pouvoir **ingérer les fichiers Excel actuels**.
- **Climatip** : TDF paie une licence (plateforme de calcul d'empreinte carbone). **Ne pas recalculer en interne ce que Climatip fournit** (facteurs d'émission, calcul CO2e). Le calcul des émissions est délégué à Climatip. J'ai maintenant un **accès complet** (tout le Bilan Carbone et tout le contenu Climatip). Le **format d'entrée des données dans Climatip** (API, fichier d'import, saisie) est à confirmer avec ma tutrice : en attendant, isole l'export Climatip dans une couche paramétrable.
- **Démultiplication** : doit être faite **automatiquement, avant l'envoi vers Climatip**.
- Les **6 colonnes de calcul** doivent être conservées dans le flux de fusion.
- Deux populations de saisie : **data owners métier** (peu techniques, il faut que ce soit simple pour eux) et **équipe ESG** (plus experte).

## Référentiels manquants / points ouverts
- Liste des **~20 Lignes de Produit (LP)**.
- **Table de clés territoire × LP** (aujourd'hui sur un OneDrive personnel).
- **Transcodage BU ↔ LP** (via les outils MIS / Hélios).
- Les **règles exactes de démultiplication** sont à formaliser avec ma tutrice (elles existent dans son prompt).
- Question ouverte : la matrice individuelle est-elle le **support de saisie** (avant démultiplication) ou de **restitution** (après) ?

## Ce que j'ai déjà exploré (contexte, PAS une direction imposée)
J'ai testé une première piste (formulaires Microsoft Forms par domaine + fusion Power Query). Techniquement ça marchait (12 matrices extraites, fusion de 11 736 lignes conformes, mapping validé à 17/17 sur un domaine), **mais Forms est abandonné** : ce n'est pas la bonne solution. J'avais aussi esquissé un modèle de données cible (saisies sources, référentiel LP, référentiel territoires, clés de répartition, table de répartition calculée).

👉 **Considère tout ça comme un historique, pas comme une base à prolonger.** Je ne veux pas que tu t'enfermes dans Forms / Power Query / Excel parce que je les ai testés.

## Ce que j'attends de toi
- **Sois créatif et force de proposition.** Repars du besoin, pas de mes premières idées. Si tu vois une architecture plus simple, plus robuste ou plus impressionnante, propose-la — même si elle remet en cause ce que j'ai fait.
- Critères pour juger une solution :
  1. **Facile à implémenter** par moi, alternant, dans l'écosystème TDF (Microsoft 365, Climatip, Power BI, puis Snowflake) d'ici mi/fin décembre.
  2. **Marquante** : quelque chose de démontrable qui montre clairement le gain à ma tutrice, à l'IT et à la direction, et qui renforce le dossier Snowflake.
  3. **Simple pour les data owners** qui saisissent.
  4. **Maintenable** d'une année sur l'autre, traçable (qui a saisi quoi, quand, quelle version des règles).
- Commence par me poser les questions qui manquent, puis propose **2-3 architectures contrastées** avec leurs compromis avant de coder.
- Si tu ne connais pas une contrainte TDF, demande-moi plutôt que de supposer.
- Pour tout ce qui touche à des données réelles TDF : pas de données sensibles en dur dans le code, prévois des jeux de test fictifs.

## Volumes connus
- 12 matrices individuelles, 11 736 lignes après fusion (~600 saisies avant démultiplication).

## Fonctionnement entre sessions
- Ce fichier est la **source de vérité** du projet. Quand une décision est prise, mets-le à jour (section « Journal des décisions ») pour que la session suivante reparte du bon endroit.
- Travaille uniquement sur **données fictives** tant que l'usage de vraies données TDF n'est pas validé.

## Journal des décisions
- Forms abandonné.
- Cible de stockage : Snowflake, compatibilité exigée dès le départ.
- Calcul des émissions délégué à Climatip.
- 2026-10-26 — **Architecture C retenue** : fichiers Excel actuels en entrée (aucun changement pour les data owners en 2026), cœur en **Python + dbt + DuckDB** (SQL portable ; migration Snowflake = changer de *target* dans `transformation/profiles.yml`). Power Platform (option B) écartée : démultiplication non portable vers Snowflake. Nouvelle interface de saisie envisagée pour la campagne 2027 seulement.
- 2026-10-26 — Python OK sur poste / VS Code (non bloquant).
- 2026-10-26 — Climatip : la tutrice importe des fichiers Excel ; CSV probablement accepté, à confirmer. Export isolé dans `config/export_climatip.yml` + `models/export/exp_climatip.sql`.
- 2026-10-26 — Règles de démultiplication : la tutrice va les fournir et les expliquer. Elles seront stockées comme **données** (`ref_regle_demultiplication` + `ref_cle_repartition`), pas comme code.
- 2026-10-26 — Squelette livré et fonctionnel sur données fictives : ingestion tracée, contrôles, démultiplication, anomalies, export, tests dbt (10/10 verts).

## Actions urgentes (chemin critique)
1. Séance avec la tutrice sous 2 semaines : obtenir le prompt de démultiplication + un exemple réel « 1 saisie → ~20 lignes » + les formules des 6 colonnes de calcul.
2. Récupérer les référentiels : liste des LP, table clés territoire × LP (OneDrive), transcodage BU ↔ LP (MIS/Hélios).
3. Prévenir Samy (SI & Data) dès maintenant : présenter le projet comme le prototype Snowflake.
4. Récupérer un fichier Excel de saisie réel (anonymisé ou structure seule) pour caler `config/mapping_excel.yml`.

