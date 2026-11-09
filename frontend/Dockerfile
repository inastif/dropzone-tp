# Image du front DropZone, en deux étapes.

# --- Étape 1 : construire le front avec Node ---
FROM node:24-alpine AS build

WORKDIR /app

# Dépendances d'abord, pour profiter du cache des couches.
COPY package.json package-lock.json .npmrc ./
RUN npm ci

COPY . .
# URL de l'API vue par le navigateur, fixée au moment du build.
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- Étape 2 : servir les fichiers statiques avec nginx ---
FROM nginxinc/nginx-unprivileged:1.29-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
