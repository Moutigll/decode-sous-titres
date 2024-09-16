Après avoir essayé de télécharger les sous-titres, je me suis retrouvé avec plein de carrés blancs, mais j'ai essayé d'une autre manière. J'ai rechargé la page YouTube et étudié les requêtes dans l'inspecteur de réseau des outils de développement et j'ai remarqué que, lorsqu'on active les sous-titres pour la première fois, le navigateur fait une requête GET à l'adresse https://www.youtube.com/api/timedtext et le résultat est un fichier rempli de code de 18,5 Mo.

En étudiant la structure du fichier, j'ai pu me rendre compte que c'était un fichier JSON contenant des données, et qu'il avait une structure fonctionnant ainsi : Une première partie était une liste appelée "pen" qui définissait un nombre important de couleurs comme ceci :

```
"fcForeColor": 11901595,
"foForeAlpha": 254,
"boBackAlpha": 0
"fcForeColor" contient une valeur RGB sous forme décimale.
```

Ensuite, en regardant plus loin dans le fichier (à la ligne 368408), on peut voir un tableau de données appelé "events". La liste de données se présente ainsi :
```
"tStartMs": 0,
"dDurationMs": 83
```
Ce qui nous donne un temps de départ et une durée, puis une section "segs" qui ressemble à ceci :

```
"segs": [ 
  { "utf8": "█" }, 
  { "utf8": "█", "pPenId": 2 }, 
  { "utf8": "█", "pPenId": 3 }, 
  { "utf8": "█", "pPenId": 4 }
]
```

Qui contient donc des caractères "█" et leur associe une couleur grâce à la position d'une couleur "foForeAlpha" dans la liste au début.

Enfin, il y avait une donnée "wpWinPosId" avec une valeur qui correspond en réalité à la position de la ligne par rapport à l'axe Y. Ce schéma se répète ensuite de la ligne 368408 à la ligne 1059158 pour couvrir l'intégralité de la vidéo.

Grâce à toutes ces informations, j'ai pu créer un script Python qui utilise JSON pour extraire les données et Pygame pour les afficher, ce qui m'a permis de reconstituer la vidéo. Il y a cependant quelques artefacts dont je n'ai pas compris l'origine.
