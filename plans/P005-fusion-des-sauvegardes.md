# P005 — Fusion des sauvegardes

- **Statut** : à mûrir (priorité basse, 6 oct. 2026).
- **Origine** : sponsor, 6 oct. 2026.

## Besoin
Restaurer un export **sans écraser** la progression déjà présente sur l'appareil (utile si un même
enfant joue sur plusieurs appareils).

## Ce qui est déjà tranché
- Pas de synchronisation en ligne : iCloud (CloudKit JS : compte Apple Developer 99 $/an),
  Cloudflare Workers + D1 (le plus solide, gratuit), Supabase (pause après une semaine), Firebase :
  toutes lèvent « statique, aucun tiers, aucun compte » pour un besoin couvert par l'export.
- En attendant : ne restaurer l'export d'un enfant que sur un appareil vide ou le sien, car la
  restauration remplace tout.

## Lien
À reprendre avec P003 (export plus simple à partager), qui touche le même écran.

## Feed-back
(sans objet)
