# LML Events

## Historique

| Auteur    |  Date    | Version  | Modification |
|:----------|:--------:|:--------:|:-------------|
|kevin.carrillo@campus.academy | 30/04/23 | 1.0.a | Mise en place des bases de la plateforme.|

## Sommaire

1. Introduction
2. Outils
3. Fonctionalités
4. Tests
5. Déploiement
6. Compatibilité

## Introduction

LML Events est une association présidée par Léo LECLERC. Elle a pour objectif de promouvoir la VR (réalité virtuelle) au travers d'évènements.

L'association compte trois créateurs: Léo LECLERC, Léa et Maël. Elle a été fondée en mars 2023 en tant que ...

Afin de gagner en visibilité, l'association a besoin d'une plateforme permettant d'expliquer sa mission, de promouvoir les évènements auxquels elle participe, a participé et participera, et enfin de proposer des produits pour financer ses actions.

Le manque de bénévoles entraine l'association a choisir de ne pas vouloir modérer le contenu de leur plateforme.

## Outils

Cette plateforme a été conçue en Django 4.1.7 (Framework Python) avec Python 3.11.

Elle utilise les RabbitMQ en tant que broker, Celery en tant que worker monitoré par Flower et Redis en tant que Cache.

Pour la base de donnée, elle utilise PostgreSQL.

Enfin, pour la partie front, elle utilise Bootstrap 5 et Fontawesome, mais aussi Javascript, Ajax, HTML 5 et CSS 3.

## Fonctionalités

**La plateforme permet aujourd'hui :**

- La double authentification par SMS ;
- L'affichage de la liste des produits par catégories ;
- L'affichage du détail d'un produit ;
- La page d'accueil ;
- La page About ;
- La page de partenaires ;
- Le footer ;
- Le header ;
- Les news ;
- La page d'administration ;
- Le panier ;
- L'achat de commandes.

**La plateforme n'a pas encore :**

- La vérification des mails ;
- La version finale du visuel ;
- Le CRM ;
- Seule l'application des news utilise un CMS (l'adapter pour intégrer également l'application pages) ;
- Les statistiques (Matomo) ;
- Le RGPD n'est pas encore totalement respecté ;
- Les cadres légaux ne sont pas encore adaptés ;
- La gestion des cookies.

## Tests

Dans un souci de célérité, nous n'avons pas encore implémenté de tests. Voici les tests à faire par catégorie.

**Tests unitaire :**

- application pages ;
- application cart ;
- application news ;
- application shop ;
- application payment ;
- application users ;
- application orders ;
- application coupons ;
- application config ;
- application utils.

*Ces tests nécessitent de tester :*

- *Cas passant ;*
- *Cas non passant ;*
- *Cas limites (0, null, None, blank, min, max) ;*
- *Formats ;*
- *Types différents.*

**Tests fuzzers :**

- application pages ;
- application cart ;
- application news ;
- application shop ;
- application payment ;
- application users ;
- application orders ;
- application coupons ;
- application config ;
- application utils.

**Tests environnement (Github actions) :**

- Dependabot ;
- Matrice ;
- Utilisation de nos propres runners (docker).

**Tests de non régression (Github actions + coverage) :**

- branch dev -> branch integration ;
- branch integration -> branch recette ;
- branch recette -> branch production.

**Tests end to end (Selenium) :**

- Templates pages ;
- Templates users ;
- Templates admin ;
- Templates orders ;
- Templates payment ;
- Templates products ;
- Template base ;
- Template cart ;
- Template footer ;
- Templates email.

Enfin, la documentation doit être auto générée par Sphinx et graphviz lors du push de la branche integration sur la branche recette et lors de la mise en production de la recette.

## Déploiement

Le déploiement doit s'effectuer uniquement après avoir testé avec succès le projet depuis la branche recette via Github actions. On respecte ainsi le processus CI/CD.

On ne créer aucune fonctionalité sur les branches production, recette ou integration.

La nomenclature des commit devra suivre celle-ci :

```Text
Features (<module>): <comments>
Fix (<module>): <comments>
Improve (<module>): <comments>
```

Voici un schéma de l'arborescence de Git/Github:

```Text
└── production
    └──  recette
         ├── Fix
         |    ├── <dev 1>/<feature 1>
         |    └── <dev 1>/<feature 2>
         └── integration
              ├── Fix
              |    └── <dev 3>/<feature 3>
              ├── Features
              |    ├── <dev 1>/<feature 5>
              |    └── <dev 2>/<feature 6>
              └── Improves
                   └── <dev 4>/<feature 4>
```

## Compatibilité

La plateforme doit être fonctionnelle sur tous les OS, tous les navigateurs et tous les supports (mobile, desktop).
