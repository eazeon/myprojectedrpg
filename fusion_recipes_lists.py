# Fichier de listes des recettes disponibles à la fusion
# Template pour fusion de compétences
"""
    frozenset(["1erIngrédient", "2emeIngrédient"]): {
        "result": "Nom",
        "damage": 0,
        "damage_type": "TypeDeDegat", # Type de dégat existant : contondant / slashing / piercing / magic
        "element": "ElementDeDegat", # Les attaques physiques infligent des dégats de 'force', les attaques magiques des dégats de type fire / wind / water / earth / illusion / psychic
        "description": "VotreDescription",
        "mana_cost": 0, # Tant qu'il y a de la magie impliquée utilisation du mana
        "fatigue_cost": 0 # Tant qu'il y a des coups physiques impliqués utilisation de fatigue
    },
"""


fusion_recipes = {
    frozenset(["Coup simple", "Hache de guerre"]): {
        "result": "Frappe simple à la hache",
        "damage": 25,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre hache !",
        "mana_cost": 0,
        "fatigue_cost": 15
    },
    frozenset(["Coup simple", "Arc"]): {
        "result": "Tir simple",
        "damage": 20,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous tirez avec votre arc !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Coup simple", "Bouclier"]): {
        "result": "Coup de bouclier",
        "damage": 15,
        "damage_type": "contondant",
        "element": "force",
        "description": "Vous frappez avec votre bouclier !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Coup simple", "Épée courte"]): {
        "result": "Frappe à l'épée",
        "damage": 20,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre épée !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Coup simple", "Épée longue"]): {
        "result": "Frappe à l'épée longue",
        "damage": 25,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre longue épée !",
        "mana_cost": 0,
        "fatigue_cost": 15
    },
    frozenset(["Coup simple", "Dague"]): {
        "result": "Coup de dague",
        "damage": 15,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous assénez un coup avec votre dague !",
        "mana_cost": 0,
        "fatigue_cost": 5
    },
    frozenset(["Coup puissant", "Épée courte"]): {
        "result": "Frappe lourde à l'épée",
        "damage": 45,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez lourdement votre épée !",
        "mana_cost": 0,
        "fatigue_cost": 20
    },
    frozenset(["Coup puissant", "Épée longue"]): {
        "result": "Frappe lourde à l'épée longue",
        "damage": 50,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez lourdement votre épée longue !",
        "mana_cost": 0,
        "fatigue_cost": 25
    },
    frozenset(["Coup puissant", "Dague"]): {
        "result": "Poignardage lourd",
        "damage": 25,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous lacérez avec votre dague !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Coup puissant", "Hache de guerre"]): {
        "result": "Abattage de hache",
        "damage": 45,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez votre hache !",
        "mana_cost": 0,
        "fatigue_cost": 25
    },
    frozenset(["Coup puissant", "Arc"]): {
        "result": "Tir violent",
        "damage": 40,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous décochez une flèche à pleine puissance !",
        "mana_cost": 0,
        "fatigue_cost": 20
    },
    frozenset(["Coup puissant", "Bouclier"]): {
        "result": "Pillonage de bouclier",
        "damage": 25,
        "damage_type": "contondant",
        "element": "force",
        "description": "Vous abbattez votre bouclier violemment !",
        "mana_cost": 0,
        "fatigue_cost": 15
    },
    frozenset(["Parade", "Épée courte"]): {
        "result": "Parade à l'épée",
        "damage": 10,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous prenez une posture défensive à l'épée!",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Épée longue"]): {
        "result": "Parade avec épée lourde",
        "damage": 15,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous prenez une posture défensive à l'épée longue!",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Dague"]): {
        "result": "Blocage à la dague",
        "damage": 5,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous prenez une posture défensive à la dague !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Hache de guerre"]): {
        "result": "Blocage à la hache",
        "damage": 15,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous prenez une posture défensive à la hache !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Arc"]): {
        "result": "Blocage avec l'arc",
        "damage": 10,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous prenez une posture défensive à l'arc !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Bouclier"]): {
        "result": "Blocage au bouclier",
        "damage": 5,
        "damage_type": "contondant",
        "element": "force",
        "description": "Vous prenez une posture défensive au bouclier !",
        "mana_cost": 0,
        "fatigue_cost": 10
    },
    frozenset(["Coup simple", "Magie élémentaire Feu"]): {
        "result": "Boule de feu simple",
        "damage": 25,
        "damage_type": "magic",
        "element": "fire",
        "description": "Vous lancez une boule de feu simple!",
        "mana_cost": 15,
        "fatigue_cost": 0
    },
    frozenset(["Coup simple", "Magie élémentaire Air"]): {
        "result": "Bourrasque",
        "damage": 20,
        "damage_type": "magic",
        "element": "wind",
        "description": "Vous lancez une bourrasque !",
        "mana_cost": 10,
        "fatigue_cost": 0
    },
    frozenset(["Coup simple", "Magie élémentaire Eau"]): {
        "result": "Jet d'eau",
        "damage": 20,
        "damage_type": "magic",
        "element": "water",
        "description": "Vous projetez un jet d'eau !",
        "mana_cost": 10,
        "fatigue_cost": 0
    },
    frozenset(["Coup simple", "Magie élémentaire Terre"]): {
        "result": "Frappe de terre",
        "damage": 20,
        "damage_type": "magic",
        "element": "earth",
        "description": "Vous projetez une motte de terre !",
        "mana_cost": 10,
        "fatigue_cost": 0
    },
    frozenset(["Coup simple", "Magie d'illusion"]): {
        "result": "Illusion simple",
        "damage": 0,
        "damage_type": "state",
        "element": "illusion",
        "description": "Vous projetez une illusion simple !",
        "mana_cost": 10,
        "fatigue_cost": 0
    },
    frozenset(["Coup simple", "Magie psychique"]): {
        "result": "Décharge mentale",
        "damage": 10,
        "damage_type": "magic",
        "element": "psychic",
        "description": "Vous projetez une décharge mentale !",
        "mana_cost": 15,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie élémentaire Feu"]): {
        "result": "Colonne de flamme",
        "damage": 45,
        "damage_type": "magic",
        "element": "fire",
        "description": "Vous faites s'élever une colonne de flammes !",
        "mana_cost": 25,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie élémentaire Air"]): {
        "result": "Tornade",
        "damage": 40,
        "damage_type": "magic",
        "element": "wind",
        "description": "Vous condensez une tornade !",
        "mana_cost": 20,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie élémentaire Eau"]): {
        "result": "Tsunami",
        "damage": 40,
        "damage_type": "magic",
        "element": "water",
        "description": "Vous déversez un tsunami !",
        "mana_cost": 20,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie élémentaire Terre"]): {
        "result": "Séisme",
        "damage": 40,
        "damage_type": "magic",
        "element": "earth",
        "description": "Vous façonnez un séisme !",
        "mana_cost": 20,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie d'illusion"]): {
        "result": "Image rémanente",
        "damage": 0,
        "damage_type": "state",
        "element": "illusion",
        "description": "Vous créez une image rémanent de vous-même !",
        "mana_cost": 20,
        "fatigue_cost": 0
    },
    frozenset(["Coup puissant", "Magie psychique"]): {
        "result": "Emprise mentale",
        "damage": 20,
        "damage_type": "magic",
        "element": "psychic",
        "description": "Vous prenez contrôle de votre ennemi !",
        "mana_cost": 20,
        "fatigue_cost": 0
    },
    frozenset(["Parade", "Magie élémentaire Feu"]): {
        "result": "Bouclier de feu",
        "damage": 15,
        "damage_type": "magic",
        "element": "fire",
        "description": "Vous prenez une posture défensive avec vos flammes !",
        "mana_cost": 15,
        "fatigue_cost": 5
    },
    frozenset(["Parade", "Magie élémentaire Air"]): {
        "result": "Bouclier d'air",
        "damage": 10,
        "damage_type": "magic",
        "element": "wind",
        "description": "Vous prenez une posture défensive avec vos bourrasques !",
        "mana_cost": 10,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Magie élémentaire Eau"]): {
        "result": "Bouclier d'eau",
        "damage": 10,
        "damage_type": "magic",
        "element": "eau",
        "description": "Vous prenez une posture défensive avec votre eau !",
        "mana_cost": 10,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Magie élémentaire Terre"]): {
        "result": "Bouclier de terre",
        "damage": 10,
        "damage_type": "magic",
        "element": "earth",
        "description": "Vous prenez une posture défensive renforcée par la terre !",
        "mana_cost": 10,
        "fatigue_cost": 10
    },
    frozenset(["Parade", "Magie d'illusion"]): {
        "result": "Illusion du bras",
        "damage": 0,
        "damage_type": "state",
        "element": "psychic",
        "description": "Vous invoquez une image illusoire de votre bras armé !",
        "mana_cost": 20,
        "fatigue_cost": 5
    },
    frozenset(["Potion de soin", "Potion de soin"]): {
        "result": "Potion de soin supérieure",
        "description": "Une potion a la régénération de PV bien plus importante.",
        "consumable": True
    },
    frozenset(["Potion de soin", "Potion de poison"]): {
        "result": "Potion de poison auto-soignant",
        "description": "Une potion qui vous infige des dégâts mais vous soigne..?",
        "consumable": True
    },
    frozenset(["Potion de soin", "Bombe l\u00e9g\u00e8re"]) :{
        "result": "Bombe de soin",
        "description": "Une bombe qui vous infige des dégâts par le souffle de l'explosion mais vous soigne..?",
        "consumable": True
    },
    frozenset(["Potion de soin", "Bombe lourde"]): {
        "result": "Bombe de soin puissante",
        "description": "Une grosse bombe qui vous infige des dégâts par le souffle de l'explosion mais vous soigne..?",
        "consumable": True
    },
    frozenset(["Potion de soin", "Bombe fumig\u00e8ne"]): {
        "result": "Bombe de fumée de soin",
        "description": "Une bombe qui libère une fumée qui vous soigne et empêche les attaques de vous ou des ennemis.",
        "consumable": True
    },
    frozenset(["Potion de soin", "Filet"]): {
        "result": "Filet de soin",
        "description": "Un filet qui ligote votre ennemi mais le soigne...?",
        "consumable": True
    },
    frozenset(["Potion de poison", "Potion de poison"]): {
        "result": "Potion de poison fort",
        "description": "Une potion qui provoque un empoisonnement fort.",
        "consumable": True
    },
    frozenset(["Potion de poison", "Bombe l\u00e9g\u00e8re"]): {
        "result": "Bombe de poison",
        "description": "Une bombe qui empoisonne votre ennemi",
        "consumable": True
    },
    frozenset(["Potion de poison", "Bombe lourde"]): {
        "result": "Potion de bombe puissante",
        "description": "Une bombe puissante qui provoque un empoisonnement.",
        "consumable": True
    },
    frozenset(["Potion de poison", "Bombe fumig\u00e8ne"]): "Bombe de fumée empoisonnante",
    frozenset(["Potion de poison", "Filet"]): "Filet empoisonné",
    frozenset(["Bombe l\u00e9g\u00e8re", "Bombe l\u00e9g\u00e8re"]): "Bombe lourde",
    frozenset(["Bombe l\u00e9g\u00e8re", "Bombe lourde"]): "Bombe lourde puissante",
    frozenset(["Bombe l\u00e9g\u00e8re", "Bombe fumig\u00e8ne"]): "Bombe de fumée explosive",
    frozenset(["Bombe l\u00e9g\u00e8re", "Filet"]): "Filet explosif",
    frozenset(["Bombe lourde", "Bombe lourde"]): "Bombe massive",
    frozenset(["Bombe lourde", "Bombe fumig\u00e8ne"]): "Bombe lourde de fumée explosive",
    frozenset(["Bombe lourde", "Filet"]): "Filet explosif",
    frozenset(["Bombe fumig\u00e8ne", "Bombe fumig\u00e8ne"]): "Bombe lourde de fumée",
    frozenset(["Bombe fumig\u00e8ne", "Filet"]): "Filet enfumé",
    frozenset(["Filet", "Filet"]): "Filet tentaculaire",
    frozenset(["Potion de mana", "Potion de repos"]): {
        "result": "Potion de récupération",
        "consumable": True
    },
    frozenset(["Épée courte", "Magie élémentaire Feu"]): {
    "result": "Épée enflammée",
    "description": "Une épée courte enveloppée de flammes.",
    "enchanted": True
    },
    frozenset(["Arc", "Magie élémentaire Air"]): {
        "result": "Arc tempétueux",
        "description": "Un arc alimenté par le vent.",
        "enchanted": True
    }
}
