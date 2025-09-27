# Liste des quêtes

quests = [
    {
        "id": 1,
        "title": "🌾 Le champ stérile",
        "category": "Quêtes secondaires",
        "description": "Un paysan se plaint que ses récoltes ne poussent pas.",
        "dialogues": [
            "Paysan : Bonjour aventurier! Je suis un Paysan lambda et j'ai un problème et puisque vous êtes le seul aventurier c'est à vous que je vais m'adresser plutôt que de demander aux autres paysans du village !",
            "Paysan : Voici mon problème : mon champ de patates ne se porte pas très bien, et vu que je suis sûr que vous vous y connaissez ca va être à vous de m'aider !"
        ],
        "choices": [
            {
                "requirement": {"skill": "Boule de feu simple"},
                "text": "🕯️ Utiliser 'boule de feu' : Brûler le champ pour créer de la cendre comme engrais",
                "penalty": {"money": 200},
                "result_dialogues": [
                    "Paysan : ... C'était quoi l'idée derrière ? 'Faire de la cendre à utiliser comme engrais' ? D'accord, quand vous aurez deux minutes vous m'expliquerez sur quels plants je peux mettre cet engrais.",
                    "Vous allez me rembourser 200 deullars, taré va."
                ]
            },
            {
                "requirement": {"skill": "Colonne de flamme"},
                "text": "🔥 Utiliser 'Colonne de flammes' : Incinérer tout le champ et la terre présente afin de rendre le sol moins acide et le stériliser des maladies",
                "penalty": {"money": 350},
                "result_dialogues": [
                    "Paysan : ... C'était quoi l'idée derrière ? 'Rendre le sol moins acide et le stériliser des maladies' ? D'accord, je me rappelle pas vous avoir demandé un cours sur la gestion d'un terrain je crois m'y connaître un peu, surtout que vous avez oublié mais ici c'est des pommes de terre qui ont besoin de potassium, hors le potassium se volatilise a plus de 700° : donc y en a plus dans le sol.",
                    "Vous allez me rembourser 350 deullars, taré va."
                ]
            },
            {
                "requirement": {"skill": "Jet d'eau"},
                "text": "💧 Utiliser 'Jet d'eau' : Arroser le champ avec de l'eau magique",
                "reward": {"money": 100, "xp": 30},
                "result_dialogues": [
                    "Paysan : Ah, il fallait juste les arroser d'accord! Merci à vous, tenez prenez un peu d'argent en récompense !"
                ]
            },
            {
                "requirement": {"item": "Potion de soin"},
                "text": "🧪 Donner une potion de soin aux plantes",
                "result_dialogues": [
                    "Paysan : Vous... vous avez conscience que... euh... ca fonctionne pas pareil? J'aurais jamais pensé devoir expliquer ça à un aventurier... en plus vous en allez pas en avoir assez pour couvrir tout le champ... Laissez tomber, toute façon j'ai jamais voulu faire fermier ..."
                ]
            }
        ],
        "completed": False
    },
    {
        "id": 2,
        "title": "🥄 La pelle de l'aventure",
        "category": "Quêtes secondaires",
        "description": "Un villageois souahite vous solliciter.",
        "dialogues": [
            "Villageois : Monsieur l'aventurier, notre grand père nous as laissé un héritage dans ce terrain.",
            "Villageois : Cependant ce vieux sénile a cru bon de l'enterrer dans un coffre quelque part. Pouvez-vous nous aider?"
        ],
        "choices": [
            {
                "requirement":{"none"},
                "text": "💪 Creuser à la main",
                "result_dialogues": [
                    "Villageois : D'accord, du coup le plan c'est de creuser jusqu'aux côtes puis de faire demi-tour et de revenir par l'Armorique avant les premières gelées? Ouais non en fait oubliez ça, on va se débrouiller nous même... espèce de taré..."
                ]
            },
            {
                "requirement": {"skill": "Frappe de terre"},
                "text": "⛏️ Utiliser 'Frappe de terre' : Retourner le terrain à l'aide de la magie tellurique",
                "reward": {"money": 100, "xp": 30},
                "result_dialogues": [
                    "Paysan : Ah là je vois le coffre! Merci à vous aventurier! Voici une récompense !"
                ]
            },
            {
                "requirement": {"skill": "Séisme"},
                "text": "⛰️ Utiliser 'Séisme' : Créer une fissure tellurique pour trouver le coffre",
                "penalty": {"money": 500},
                "result_dialogues": [
                    "Paysan : ... C'est ma maison qui s'engouffre dans le trou là ? ... Vous savez remplir un constat ? Non ? Pas grave venez on va voir ca ensemble. Espèce de malade."
                ]
            },
        ],
        "completed": False
    },
    {
        "id": 3,
        "title": "⚔️ L'appel de l'aventure",
        "category": "Histoire principale",
        "description": "Le chef du village souhaites vous confier une mission.",
        "dialogues": [
            "Chef du village : Brave aventurier, nous avons besoin de votre aide...",
            "Chef du village : Une menace se lève au nord, un monstre de type 'boss' comme vous appelez."
            "Chef du village : Vous devez nous protéger !"
        ],
        "choices": [
            {
                "requirement":{"none"},
                "text": "💪 Disponible dans une future MAj ",
                #"reward": {"money": 300, "xp": 100},
                "completed": False
            }
        ],
        "completed": False
    }
]
