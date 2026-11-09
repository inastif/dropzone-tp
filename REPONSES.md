# Réponses aux questions

## Partie 1 — Remettre le dépôt d'aplomb

### Que se passe-t-il si quelqu'un pousse directement un code cassé sur `main` ? Comment l'empêcher ?

Le code cassé arrive tout de suite sur la branche principale, et tout le monde le récupère. On l'empêche en protégeant `main` avec un ruleset : pas de push direct, pull request obligatoire. Plus tard, la CI devra aussi être verte avant le merge.

### Quels fichiers ne doivent jamais être commités ? Le `.gitignore` les couvre-t-il tous ?

Les secrets (`.env`), les dépendances installées (`.venv/`, `node_modules/`), les fichiers générés (`dist/`, caches, rapports de tests) et la base de données locale (`*.db`). Oui, le `.gitignore` les couvre tous.

### Quelle différence entre un tag léger et un tag annoté ? Lequel pour une version ?

Un tag léger est juste un nom posé sur un commit. Un tag annoté contient en plus un auteur, une date et un message. Pour une version, on utilise un tag annoté : `git tag -a v0.1.0 -m "v0.1.0"`.

### Un nouveau bouton, c'est un `feat` ou un `fix` ? Quel numéro de version change ?

C'est un `feat`, car c'est une nouvelle fonctionnalité. Avec semver, c'est le numéro du milieu (MINOR) qui change : `0.1.0` devient `0.2.0`.
