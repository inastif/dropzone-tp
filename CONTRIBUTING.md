# Contribuer à DropZone

## Le principe

`main` est protégée : on ne pousse jamais directement dessus. Chaque changement passe par une branche et une pull request.

## Nommer les branches

Format : `type/description-courte`, en minuscules avec des tirets.

| Type | Pour quoi | Exemple |
|---|---|---|
| `feat/` | une nouvelle fonctionnalité | `feat/filtre-prix` |
| `fix/` | une correction de bug | `fix/stock-negatif` |
| `docs/` | de la documentation | `docs/readme-lancement` |
| `ci/` | la CI ou le déploiement | `ci/workflow-tests` |
| `chore/` | le reste (dépendances, config) | `chore/maj-dependances` |

## Écrire les commits

On suit [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```text
type: description courte au présent
```

Types utilisés : `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `build`, `chore`.

Exemples :

```text
feat: ajoute le filtre par prix
fix: empêche de commander un drop épuisé
docs: complète le README
```

Un changement qui casse la compatibilité prend un `!` : `feat!: change le format de l'API`.

## Cycle d'une pull request

1. Partir de `main` à jour : `git switch main` puis `git pull`.
2. Créer sa branche : `git switch -c feat/ma-fonctionnalite`.
3. Faire ses commits, puis vérifier en local (lint et tests, voir le README).
4. Pousser la branche : `git push -u origin feat/ma-fonctionnalite`.
5. Ouvrir une pull request vers `main` et remplir le modèle.
6. Merger quand tout est vert, avec un message de merge conventionnel.
7. Supprimer la branche.

## Versions

On suit [semver](https://semver.org/lang/fr/) (`MAJEUR.MINEUR.CORRECTIF`) :

- `fix` : le CORRECTIF augmente (`0.1.0` → `0.1.1`) ;
- `feat` : le MINEUR augmente (`0.1.0` → `0.2.0`) ;
- changement cassant (`!`) : le MAJEUR augmente (`0.1.0` → `1.0.0`).

Chaque version a un tag annoté (`git tag -a v0.2.0 -m "v0.2.0"`) et une entrée dans le [CHANGELOG](CHANGELOG.md).
