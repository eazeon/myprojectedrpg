# Liste des quêtes

quests = [
    {
        "id": 1,
        "title": "🌾 Le champ stérile",
        "category": "Quêtes secondaires",
        "description": "Un villageois se plaint que ses récoltes ne poussent pas.",
        "dialogues": [
            "Villageois : Bonjour aventurier! Je suis un villageois lambda et j'ai un problème et puisque vous êtes le seul aventurier c'est à vous que je vais m'adresser plutôt que de demander aux autres paysans du village !",
            "Villageois : Voici mon problème : mon champ ne se porte pas très bien, et vu que je suis sûr que vous vous y connaissez ca va être à vous de m'aider !"
        ],
        "choices": [
            {
                "requirement": {"skill": "Boule de feu simple"},
                "text": "🔥 Brûler le champ pour créer de la cendre comme engrais",
                "penalty": {"money": 200},
                "result_dialogues": [
                    "Villageois : ... C'était quoi votre idée derrière ? 'Faire de la cendre à utiliser comme engrais' ? D'accord, quand vous aurez deux minutes vous m'expliquerez sur quels plants je peux mettre cet engrais. Taré va...",
                    "Villageois : Vous allez me rembourser cette récolte d'habitude je les vends pour 100... euh non 200 deullars."
                ]
            },
            {
                "requirement": {"skill": "Jet d'eau"},
                "text": "💧 Arroser le champ avec de l'eau magique",
                "reward": {"money": 100, "xp": 30},
                "result_dialogues": [
                    "Villageois : Merci ! Mes champs sont sauvés grâce à vous."
                ]
            },
            {
                "requirement": {"item": "Potion de soin"},
                "text": "🧪 Donner une potion de soin aux plantes",
                "result_dialogues": [
                    "Villageois : Hmmm... ça n’a pas vraiment aidé, mais merci pour l’effort."
                ]
            }
        ],
        "completed": False
    },
    {
        "id": 2,
        "title": "⚔️ L'appel de l'aventure",
        "category": "Histoire principale",
        "description": "Le chef du village vous confie une mission importante.",
        "dialogues": [
            "Chef du village : Brave aventurier, nous avons besoin de votre aide...",
            "Chef du village : Une menace se lève au nord, et vous seul pouvez enquêter."
        ],
        "choices": [
            {
                "requirement": {"skill": "Frappe à l'épée"},
                "text": "💪 Promettre de protéger le village avec votre lame",
                "reward": {"money": 300, "xp": 100}
            }
        ],
        "completed": False
    }
]
