# Changelog

Toutes les évolutions notables du projet sont notées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet suit [semver](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- Images Docker de l'API (multi-stage, utilisateur non-root) et du front (build Node, service par nginx sur le port 8080).
- `compose.yml` : base PostgreSQL 16 avec volume et healthcheck, API et front.
- `.env.example` : modèle des variables d'environnement.
- Section « Lancer le projet avec Docker » dans le README.

## [0.1.0] - 2026-11-09

### Ajouté

- Application de départ : API FastAPI et front React (liste des drops, détail, commande).
- `AUDIT.md` : audit du dépôt.
- `REPONSES.md` : réponses aux questions du TP.
- `CONTRIBUTING.md`, `CHANGELOG.md` et modèle de pull request.
- Section « Contribuer » dans le README.

### Sécurité

- Branche `main` protégée : pull request obligatoire, push forcé et suppression interdits.

[Non publié]: https://github.com/inastif/dropzone-tp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/inastif/dropzone-tp/releases/tag/v0.1.0
