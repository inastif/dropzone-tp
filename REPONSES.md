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

## Partie 2 — Conteneuriser

### Pourquoi copier les fichiers de dépendances avant le code ? Que devient le cache des couches quand on modifie une ligne de code ?

Docker garde chaque étape du Dockerfile en cache. Quand un fichier copié change, cette étape et toutes les suivantes sont refaites. Si on copie `requirements.txt` (ou `package.json`) avant le code, une modification du code ne refait que la copie du code : l'installation des dépendances, qui est lente, reste en cache.

### Que contient l'image finale de l'API ? Les tests, le cache pip, le `.venv` local doivent-ils y être ?

Elle contient Python, les dépendances installées et le dossier `app/`. Rien d'autre. Les tests ne servent pas à faire tourner l'API, le cache pip prend de la place pour rien (`--no-cache-dir`) et le `.venv` local est fait pour le PC, pas pour le conteneur. Le `.dockerignore` et le build multi-stage les tiennent à l'écart.

### Pourquoi éviter de lancer un conteneur en root ? Pourquoi nginx écoute-t-il sur 8080 et pas 80 ?

Si quelqu'un exploite une faille de l'application, il a les droits de l'utilisateur qui la fait tourner. En root, il peut tout faire dans le conteneur, et c'est plus dangereux pour la machine. Sous Linux, seul root peut écouter sur un port en dessous de 1024 : nginx tourne sans root, donc il utilise 8080.

### Comment l'API trouve-t-elle la base dans Compose ? Pourquoi `localhost` ne marche pas entre conteneurs ?

Compose met les services sur un même réseau et chaque nom de service devient une adresse. L'API joint donc la base avec `db:5432` dans `DATABASE_URL`. Chaque conteneur a son propre `localhost`, qui le désigne lui-même : dans l'API, `localhost` c'est l'API, pas la base.

### Que se passe-t-il si l'API démarre avant que PostgreSQL soit prêt ?

Elle n'arrive pas à se connecter et plante au démarrage. Pour l'éviter, la base a un `healthcheck` (`pg_isready`) et l'API a `depends_on` avec `condition: service_healthy` : Compose attend que la base soit prête avant de lancer l'API.

### Où sont les données de la base après un arrêt de la stack ? Et après un arrêt avec suppression des volumes ?

Elles sont dans le volume `db-data`. Après `docker compose down`, le volume est gardé : au redémarrage, les données sont toujours là. Avec `docker compose down -v`, le volume est supprimé et les données sont perdues.

## Partie 3 — Intégration continue

### Pourquoi séparer lint, tests et E2E en jobs distincts plutôt qu'un seul gros job ? Qu'est-ce qui tourne en parallèle ?

Des jobs séparés tournent en même temps, donc la CI va plus vite. On voit aussi tout de suite quelle partie a échoué. Le lint, les tests backend et les tests frontend tournent en parallèle, puis l'E2E démarre après eux.

### Pourquoi l'E2E en dernier ? Combien de temps gagne-t-on quand le lint échoue ?

L'E2E est le plus long : il construit les images, lance toute la stack avec Docker Compose puis ouvre un navigateur. Ça ne sert à rien de le lancer si le code ne passe déjà pas le lint ou les tests unitaires. Quand le lint échoue, on gagne tout le temps de l'E2E, plusieurs minutes, et on a la réponse en moins d'une minute.

### Sur quel fichier se base la clé du cache ? Que se passe-t-il quand il change ?

Sur les fichiers de dépendances : `package-lock.json` pour npm, `requirements*.txt` pour pip. Quand ils changent, la clé change : l'ancien cache n'est plus utilisé, les dépendances sont retéléchargées et un nouveau cache est enregistré.

### De quels droits votre workflow a-t-il vraiment besoin ? Que pourrait faire un workflow compromis avec des droits en écriture ?

Il a seulement besoin de lire le code : `permissions: contents: read`. Avec des droits en écriture, un workflow compromis (par une action ou une dépendance piégée) pourrait pousser du code, modifier des tags ou des releases, ou publier des packages à notre nom.

### Pour un test E2E : comment être sûr qu'il ne dépend pas des données d'un autre test ?

Chaque test crée son propre drop par l'API avant d'ouvrir la page, puis travaille seulement sur ce drop. Il ne compte pas sur les données de démonstration ni sur ce qu'un autre test a fait avant lui.

### Quels tests unitaires font échouer la CI si quelqu'un casse la règle « jamais deux fois la dernière paire » ?

Les tests de `backend/tests/test_orders.py` : « la dernière paire rend le drop épuisé » et « commander un drop épuisé est refusé » (réponse `409`). Les tests existants le voient aussi en partie : `test_compute_status` dans `test_domain.py` (stock à 0 donne `sold_out`) et `test_list_drops_filtered_by_status` dans `test_drops.py`.

### Qu'est-ce qu'act ne sait pas reproduire de GitHub ?

act lance les jobs dans des conteneurs Docker sur le poste, pas sur les vraies machines de GitHub. Il ne reproduit pas tout : les images des runners sont plus légères, le cache et les artefacts ne marchent pas comme sur GitHub, le `GITHUB_TOKEN` et les secrets ne sont pas fournis, et les règles de protection de branche et les vérifications obligatoires n'existent pas en local.

## Partie 4 — Déploiement continu

### Pourquoi le CD ne relance-t-il pas les tests ? Qu'est-ce qui garantit que le commit tagué est sain ?

Les tests ont déjà tourné : on ne pose un tag que sur `main`, et rien n'entre dans `main` sans passer par une pull request avec la CI verte (le ruleset l'exige). Le commit tagué a donc déjà été testé. Relancer les tests ferait perdre du temps sans rien apporter.

### De quels droits chaque job a-t-il besoin ? Pourquoi les donner job par job plutôt qu'au workflow entier ?

- Images : lire le code (`contents: read`) et publier un package (`packages: write`).
- Pages : lire le code, publier sur Pages (`pages: write`) et prouver d'où vient le déploiement (`id-token: write`).
- Release : créer la release (`contents: write`).

En haut du workflow, `permissions: {}` ne donne rien par défaut. Chaque job n'a que ce dont il a besoin : si une action utilisée par un job est piégée, elle ne peut pas faire le travail des autres (par exemple, le job Pages ne peut pas modifier le dépôt).

### Faut-il créer un mot de passe pour pousser sur ghcr.io depuis GitHub Actions ?

Non. GitHub crée un jeton temporaire pour chaque run, `GITHUB_TOKEN`. Avec `packages: write`, il suffit pour se connecter à ghcr.io avec `docker/login-action`. Il n'y a aucun secret à créer ni à stocker.

### Pages sert le site sous /dropzone-tp/ et non à la racine : quelle conséquence pour les chemins des fichiers du front ? Et pour une URL comme /drops/3 rechargée ?

Par défaut, Vite écrit des chemins qui partent de la racine (`/assets/…`) : sur Pages, ils ne trouvent rien et la page reste blanche. On construit donc le front avec `--base=/dropzone-tp/`, et le routeur utilise la même base. Pour `/drops/3` rechargée, Pages ne connaît pas cette page et renvoie sa page 404 : on copie `index.html` en `404.html`, ce qui recharge l'application et laisse React afficher la bonne page.

### Sur Pages, il n'y a pas de nginx pour rediriger /api : comment le front connaît-il l'adresse de l'API ? Que montre la page si aucune API publique n'existe ?

L'adresse est fixée au moment du build avec `VITE_API_URL`, lue dans la variable de dépôt `PUBLIC_API_URL`. Sans API publique, la variable n'existe pas : le front vise une adresse qui ne répond pas, et la page affiche « L'API est injoignable ».

### Un rollback, c'est reconstruire l'ancienne version ou réutiliser l'ancienne image ? Qu'est-ce qui ne revient pas en arrière ?

On réutilise l'ancienne image, déjà publiée sur ghcr.io : on change `VERSION` et on relance Compose, sans aucun build. C'est rapide et on retrouve exactement ce qui tournait avant. Les données de la base, elles, ne reviennent pas en arrière : elles restent dans le volume. Si la nouvelle version avait changé le schéma de la base, l'ancienne version devrait encore savoir le lire.
