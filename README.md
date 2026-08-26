# 🎵 Spotify CSV to MP3 Downloader (Simple Edition)

Un outil Python ultra-simple et cross-platform (Windows, macOS, Linux) pour convertir vos playlists exportées depuis Spotify en fichiers MP3 via des recherches automatisées YouTube.

## 🌟 Fonctionnalités Principales

* Système d'historique anti-doublons (100% fiable) : Génère un fichier downloaded_history.txt basé directement sur les lignes exactes du CSV. Même si YouTube renomme le fichier MP3 différemment, le script saura que le titre a déjà été traité et le sautera (0ms de requête réseau).
* Double vérification locale : Analyse également les fichiers .mp3 déjà présents dans le dossier de destination pour éviter les téléchargements redondants.
* Pause automatique Anti-Rate-Limit (HTTP 429) : Si YouTube temporise votre adresse IP après une série de requêtes, le script entre automatiquement en pause de sécurité pendant 60 secondes avant de reprendre tout seul.
* Parseur CSV universel : Compatible avec les exports d'Exportify (séparateurs "," ou ";").

---

## 📦 Prérequis & Installation

1. Python 3.8+
2. FFmpeg (Nécessaire pour convertir l'audio extrait en fichier .mp3)

### Installation sous Windows (PowerShell)

# 1. Installer FFmpeg
winget install "FFmpeg (Essential Build)"

# 2. Installer les dépendances Python
pip install yt-dlp colorama

---

## 🚀 Utilisation

Lancez simplement la commande avec le fichier CSV et le dossier de destination souhaité :

python3 spotify_to_mp3.py .\mon_fichier.csv .\MesMusiques

### Paramètres optionnels

* Changer les délais de pause entre les requêtes (par défaut 2 à 5 secondes) :
python3 spotify_to_mp3.py .\mon_fichier.csv .\MesMusiques --sleep-min 3 --sleep-max 6

* Mode d'affichage détaillé pour le débogage (-v) :
python3 spotify_to_mp3.py .\mon_fichier.csv .\MesMusiques -v

---

## 📂 Gestion des Blocages YouTube

Si vous téléchargez de très grosses playlists (plus de 50-100 morceaux d'un coup) :
1. YouTube risque de bloquer temporairement votre adresse IP (erreur HTTP Error 429).
2. Le script affichera un avertissement jaune "⚠️ RATE LIMIT DETECTED..." et patientera 60 secondes.
3. Vous pouvez interrompre le script à tout moment avec CTRL + C.
4. Quand vous relancerez le script plus tard, il reprendra exactement là où il s'est arrêté grâce à l'historique texte, sans retélécharger un seul morceau.

---

## 📜 License

Distribué sous la licence MIT. Voir LICENSE pour plus de détails.
