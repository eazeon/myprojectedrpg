# Liste des quêtes

quests = [
    {
        "id": 1,
        "title": "🌾 Le champ stérile",
        "category": "Quêtes secondaires",
        "description": "Un villageois se plaint que ses récoltes ne poussent pas.",
        "dialogues": [
            "Villageois : Bonjour aventurier! Je suis un villageois lambda et j'ai un problème et puisque vous êtes le seul aventurier c'est à vous que je vais m'adresser plutôt que de demander aux autres paysans du village !",
            "Villageois : Voici mon problème : mon champ de patates ne se porte pas très bien, et vu que je suis sûr que vous vous y connaissez ca va être à vous de m'aider !"
        ],
        "choices": [
            {
                "requirement": {"skill": "Boule de feu simple"},
                "text": "🕯️ Utiliser 'boule de feu' : Brûler le champ pour créer de la cendre comme engrais",
                "penalty": {"money": 200},
                "result_dialogues": [
                    "Villageois : ... C'était quoi l'idée derrière ? 'Faire de la cendre à utiliser comme engrais' ? D'accord, quand vous aurez deux minutes vous m'expliquerez sur quels plants je peux mettre cet engrais.",
                    "Vous allez me rembourser 200 deullars, taré va."
                ]
            },
            {
                "requirement": {"skill": "Colonne de flamme"},
                "text": "🔥 Utiliser 'Colonne de flammes' : Incinérer tout le champ et la terre présente afin de rendre le sol moins acide et le stériliser des maladies",
                "penalty": {"money": 350},
                "result_dialogues": [
                    "Villageois : ... C'était quoi l'idée derrière ? 'Rendre le sol moins acide et le stériliser des maladies' ? D'accord, je me rappelle pas vous avoir demandé un cours sur la gestion d'un terrain je crois m'y connaître un peu, surtout que vous avez oublié mais ici c'est des pommes de terre qui ont besoin de potassium, hors le potassium se volatilise a plus de 700° : donc y en a plus dans le sol.",
                    "Vous allez me rembourser 350 deullars, taré va."
                ]
            },
            {
                "requirement": {"skill": "Jet d'eau"},
                "text": "💧 Utiliser 'Jet d'eau' : Arroser le champ avec de l'eau magique",
                "reward": {"money": 100, "xp": 30},
                "result_dialogues": [
                    "Villageois : Ah, il fallait juste les arroser d'accord! Merci à vous, tenez prenez un peu d'argent en récompense !"
                ]
            },
            {
                "requirement": {"item": "Potion de soin"},
                "text": "🧪 Donner une potion de soin aux plantes",
                "result_dialogues": [
                    "Villageois : Vous... vous avez conscience que... euh... ca fonctionne pas pareil? J'aurais jamais pensé devoir expliquer ça à un aventurier... en plus vous en allez pas en avoir assez pour couvrir tout le champ... Laissez tomber, toute façon j'ai jamais voulu faire fermier ..."
                ]
            }
        ],
        "completed": False
    },
    {
        "id": 2,
        "title": "⚔️ L'appel de l'aventure",
        "category": "Histoire principale",
        "description": "Le chef du village souhaites vous confier une mission.",
        "dialogues": [
            "Chef du village : Brave aventurier, nous avons besoin de votre aide...",
            "Chef du village : Une menace se lève au nord, et vous seul pouvez enquêter."
        ],
        "choices": [
            {
                "text": "💪 Promettre de protéger le village avec votre lame",
                "reward": {"money": 300, "xp": 100}
            }
        ],
        "completed": False
    }
]
