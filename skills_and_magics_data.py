skills_and_magics = [
    {
        "name": "Magie élémentaire Feu",
        "type": "magic",
        "description": "Lance une gerbe de feu qui peut brûler la cible.",
        "damage_min": 15,
        "damage_max": 30,
        "bonuses": [
            {"effect": "burn", "chance": 0.5, "duration": 2, "damage_per_turn": 5}
        ],
        "maluses": [
            {"effect": "no_effect", "condition": "target is wet"}
        ],
        "conditions": []
    },
    {
        "name": "Magie élémentaire Eau",
        "type": "magic",
        "description": "Éclat d'eau qui peut ralentir les ennemis et réduire leur précision.",
        "damage_min": 10,
        "damage_max": 20,
        "bonuses": [
            {"effect": "stun", "condition": "if mana >= 30", "duration": 1}
        ],
        "maluses": [],
        "conditions": []
    },
    {
        "name": "Magie élémentaire Terre",
        "type": "magic",
        "description": "Projection de terre qui peut étourdir les ennemis et réduire leur précision.",
        "damage_min": 10,
        "damage_max": 20,
        "bonuses": [
            {"effect": "stun", "condition": "if mana >= 30", "duration": 1}
        ],
        "maluses": [],
        "conditions": []
    },
    {
        "name": "Magie élémentaire Air",
        "type": "magic",
        "description": "Bourrasque pouvant repousser les ennemis et réduire leur précision.",
        "damage_min": 10,
        "damage_max": 20,
        "bonuses": [
            {"effect": "stun", "condition": "if mana >= 30", "duration": 1}
        ],
        "maluses": [],
        "conditions": []
    },
    {
        "name": "Magie psychique",
        "type": "magic",
        "description": "Décharge mentale pouvant étourdir si lancé avec suffisamment de mana.",
        "damage_min": 10,
        "damage_max": 20,
        "bonuses": [
            {"effect": "stun", "condition": "if mana >= 30", "duration": 1}
        ],
        "maluses": [],
        "conditions": []
    },
    {
        "name": "Coup puissant",
        "type": "physical",
        "description": "Attaque physique puissante.",
        "damage_min": 20,
        "damage_max": 45,
        "bonuses": [
            {"effect": "armor_break", "chance": 0.2, "duration": 1}
        ],
        "maluses": [
            {"effect": "fatigue", "value": 10}
        ],
        "conditions": []
    }
    # Ajoutez d'autres magies/compétences ici...
]
