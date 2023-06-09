# CrunchyTrackApi

## Utilisation de l'API

### POST
- Avec l'url ``` /save ```, vous pouvez envoyer via la méthode POST un fichier json.

- Le fichier JSon devra être sous ce format :
#### `Pour un seul anime`
```
{
    "username": "Pablo",
    "data": [
        {
            "Anime": {
                "Title": "SAO",
                "EpisodeName": "Le Monde de l'épée",
                "EpisodeNumber": "1",
                "EpisodeLink": "https://www.crunchyroll.com/fr/sword-art-online/episode-1-the-world-of-swords-600565"
            }
        }
    ]
}
```
#### `Pour plusieurs animes`
```
{
    "username": "Pablo",
    "data": [
        {
            "Anime": {
                "Title": "SAO",
                "EpisodeName": "Le Monde de l'épée",
                "EpisodeNumber": "1",
                "EpisodeLink": "https://www.crunchyroll.com/fr/sword-art-online/episode-1-the-world-of-swords-600565"
            }
        },
        {
            "Anime": {
                "Title": "SAO",
                "EpisodeName": "Beater",
                "EpisodeNumber": "2",
                "EpisodeLink": "https://www.crunchyroll.com/fr/sword-art-online/episode-2-beater-600567"
            }
        }
    ]
}
```

