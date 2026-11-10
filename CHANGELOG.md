# Changelog

Toutes les évolutions notables du projet sont notées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet suit [semver](https://semver.org/lang/fr/).

## [Non publié]

## [0.2.1] - 2026-11-10

### Corrigé

- L'API annonçait encore la version 0.1.0 (`/health`, `/docs`) : les numéros de version de l'API et du front suivent maintenant la version publiée.

## [0.2.0] - 2026-11-10

### Ajouté

- Images Docker de l'API (multi-stage, utilisateur non-root) et du front (build Node, service par nginx sur le port 8080).
- `compose.yml` : base PostgreSQL 16 avec volume et healthcheck, API et front.
- `.env.example` : modèle des variables d'environnement.
- Section « Lancer le projet avec Docker » dans le README.
- Tests des commandes côté API (`test_orders.py`), test Vitest du composant `DropCard` et scénarios Playwright des commandes.
- Workflow d'intégration continue (`ci.yml`) : lint, tests backend, tests frontend, puis E2E ; badge dans le README.
- Workflow de déploiement continu (`cd.yml`), déclenché par un tag `v*` : images publiées sur ghcr.io, front publié sur GitHub Pages, release avec des notes générées.
- `compose.release.yml` : lancer une version publiée à partir des images du registre, et revenir à la précédente.

### Sécurité

- Les jobs de la CI sont des vérifications obligatoires pour merger dans `main`.

## [0.1.0] - 2026-11-09

### Ajouté

- Application de départ : API FastAPI et front React (liste des drops, détail, commande).
- `AUDIT.md` : audit du dépôt.
- `REPONSES.md` : réponses aux questions du TP.
- `CONTRIBUTING.md`, `CHANGELOG.md` et modèle de pull request.
- Section « Contribuer » dans le README.

### Sécurité

- Branche `main` protégée : pull request obligatoire, push forcé et suppression interdits.

[Non publié]: https://github.com/inastif/dropzone-tp/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/inastif/dropzone-tp/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/inastif/dropzone-tp/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/inastif/dropzone-tp/releases/tag/v0.1.0
