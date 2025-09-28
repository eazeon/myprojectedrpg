# myprojectedrpg
Bienvenue dans MyProjectRPG !

Je vous présente aujourd'hui ce projet sur lequel je travaille depuis quelques mois.
Tout a commencé quand j'ai imaginé la mécanique de fusion de compétence, qui permettrait à chaque joueur de choisir son style de jeu (plutôt attaques, plutôt magie, plutôt polyvalent, etc).

Idéalement j'aurais voulu implémenter cette mécanique dans un vrai grand RPG en 3D avec des animations, mais tout seul je ne pourrais pas aller très loin.

Alors en attendant j'ai choisi de réaliser ce concept de fusion en utilisant du python (car c'est le plus simple à utiliser pour moi, n'étant pas un grand programmeur) et en étendant la mécanique de fusions aux objets habituellement disponibles dans les RPG (avec d'autres plus originaux).

Je vous laisse découvrir, en espérant que vous prendrez plaisir à expérimenter !

Note sur l'IA : Oui j'ai utilisé l'IA pour générer du code, via ChatGPT. Je maîtrise un peu la programmation mais ca n'est pas mon vrai travail et je préfère orienter mes efforts de maîtrise de programmation vers Unity pour faire des jeux plus complexes et intéressants. Utiliser l'IA m'a fait gagner un temps phénoménal et sans ça je ne suis pas sûr que j'aurais pu un jour vous proposer cette expérience de jeu. Je tiens néamoins à clarifier un point : TOUTES LES IDEES DE GAME DESIGN viennent de MOI et UNIQUEMENT de MOI. L'IA n'a jamais participé à une décision créative, et m'a uniquement fourni un (solide) support technique.

----------

# Manuel de jeu
Le but de ce jeu tourne autour de la mécanique de fusion.
Vous pouvez acheter des techniques de combat, des armes, des formes de magie et des objets. Ensuite libre à vous de choisir comment fusionner ces éléments.
Voyez ce jeu comme un FTL : les actions vous sont décrites a l'écrit, a vous d'utiliser votre imagination pour visualiser ce qu'il se passe et façonner votre personnage !

Exemple : fusionner la compétence "Coup simple" et "Magie élémentaire de feu" vous donne la compétence "Boule de feu simple".
Je vous laisse découvrir les différentes fusions et vous amuser avec ;)

De même, vous avez des objets consommables à votre disposition que vous pouvez aussi fusionner pour de nouveaux effets.

Une fois paré au combat vous n'avez plus qu'a cliquer sur "Partir à l'attaque", ce qui déclenchera une phase de combat contre 5 ennemis aléatoires.
Chaque ennemi est vulnérable à un type de dégâts (contondant, perçant, coupant, magique) et peut être résistant a un type de dégât en particulier.
Battre un ennemi vous octroie des pièces et de l'XP globale.
Utiliser une compétence physique vous octroie de l'XP de force et une compétence magique vous octroie de l'XP magique.
Une fois les 5 ennemis battus, la fenêtre se ferme. Si vous êtes battus ou si vous quittez le combat (en fermant la fenêtre de combat), vous devrez d'abord vous reposer à l'auberge avant de repartir au combat sinon vous entrez au combat avec un malus de vie/mana/fatigue.
Vous pouvez ensuite améliorer vos stats en cliquant sur le bouton assez explicite "Améliorer vos stats" où vous pourrez échanger de l'XP globale contre de la santé, de l'XP de force contre + de fatigue max ou un boost de dégâts de force, et de l'XP magique pour améliorer votre mana max ou un boost de dégâts en magie.

Vous pouvez aussi désormais accéder à certaines quêtes (deux pour le moment) grâce au bouton des quêtes!
(more to come)

----------

# Problèmes connus
- Lorsque l'on chercher à fusionner des objets il est possible que la mécanique de fusion rencontre quelques problèmes : fermer et rouvrir la fenêtre devrait permettre de nouveau de fusionner sans soucis
