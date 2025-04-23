import tkinter as tk
from tkinter import messagebox
import random

CURRENT_VERSION = "0.0.8"

# Global variables
money = 1000
purchased_items = []
selected_items = []
fusion_results = []
enemy_status_effects = {}

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


enemy_types = [
    {"name": "Gobelin", "hp": 80, "damage_range": (5, 15), "resistances": {}, "weaknesses": {"piercing": 1.5}, "weight": 3},
    {"name": "Salamandre", "hp": 100, "damage_range": (5, 15), "resistances": {"fire": 0.5},"weaknesses": {"water": 1.5}, "weight": 1},
    {"name": "Ogre", "hp": 150, "damage_range": (10, 25), "resistances": {"contondant": 2.0}, "weaknesses": {"magic": 1.25},"weight": 2},
    {"name": "Spectre", "hp": 70, "damage_range": (5, 10), "resistances": {"contondant": 0.7}, "weaknesses": {"magic": 2.0}, "weight": 1},
]


itemshop_items = ["Potion de soin", "Potion de poison", "Potion de mana", "Potion de repos", "Bombe l\u00e9g\u00e8re", "Bombe lourde", "Bombe fumig\u00e8ne", "Filet"]

# Function to update the main window with purchased items and fusion results
def update_main_window():
    purchases_label.config(text=f"Items achet\u00e9s : {', '.join(purchased_items)}")
    fusions_label.config(text=f"Fusions r\u00e9alis\u00e9es : {', '.join(fusion_results)}" if fusion_results else "Fusions r\u00e9alis\u00e9es : Aucun")
    main_money_label.config(text=f"Argent : {money} deullars")

# Reset the game state
def reset_game():
    global money, purchased_items, selected_items, fusion_results
    money = 1000
    purchased_items.clear()
    selected_items.clear()
    fusion_results.clear()
    update_main_window()

# Open the inventaire window
def open_inventaire_window():
    inventaire_window = tk.Toplevel(window)
    inventaire_window.title("Inventaire")
    inventaire_window.geometry("400x300")

    tk.Label(inventaire_window, text="Fusions R\u00e9alis\u00e9es", font=("Verdana", 14)).pack(pady=10)

    if fusion_results:
        for fusion in fusion_results:
            tk.Label(inventaire_window, text=fusion, font=("Verdana", 12)).pack(anchor="w", padx=20, pady=5)
    else:
        tk.Label(inventaire_window, text="Aucune fusion r\u00e9alis\u00e9e", font=("Verdana", 12)).pack(pady=20)

class ShopWindow:
    def __init__(self, title, button_texts):
        self.window = tk.Toplevel(window)
        self.window.title(title)
        self.window.geometry("600x500")

        # Display money
        self.money_label = tk.Label(self.window, text=f"Argent: {money} deullars", font=("Verdana", 12))
        self.money_label.pack(pady=10)

        # Title label
        tk.Label(self.window, text=f"Bienvenue chez le {title}", font=("Verdana", 14)).pack(pady=20)

        # Buttons
        for text in button_texts:
            item_name, cost = text.split(" : ")
            cost = int(cost)
            tk.Button(
                self.window, 
                text=text, 
                font=("Verdana", 10), 
                command=lambda t=item_name, c=cost: self.handle_purchase(t, c)
            ).pack(pady=5)

    def handle_purchase(self, item_name, cost):
        global money
        # Check if the item has already been purchased and is not from the itemshop
        if item_name in purchased_items and item_name not in itemshop_items:
            messagebox.showwarning("Achat refusé", f"Vous avez déjà acheté {item_name}.")
            return

        if money >= cost:
            money -= cost
            purchased_items.append(item_name)
            update_main_window()
            self.money_label.config(text=f"Argent: {money} deullars")
        else:
            messagebox.showerror("Erreur", "Pas assez d'argent !")


def toggle_item_display(item_name, display_label):
    if item_name in selected_items:
        selected_items.remove(item_name)
    else:
        selected_items.append(item_name)
    display_label.config(text=", ".join(selected_items) if selected_items else "Aucun \u00e9l\u00e9ment s\u00e9lectionn\u00e9")

def handle_fusion(display_label, result_label, items_frame):
    global fusion_results
    selected_set = frozenset(selected_items)
    
    if selected_set not in fusion_recipes:
        result_label.config(
            text="Échec de la fusion : combinaison inconnue.",
            fg="red"
        )
        return

    recipe = fusion_recipes[selected_set]
    
    # If the recipe is a dictionary with a "result", it's a skill fusion
    if isinstance(recipe, dict) and "result" in recipe:
        result = recipe["result"]
        if result not in fusion_results:
            fusion_results.append(result)

        # Remove used items if they are from the item shop
        for item in selected_items:
            if item in itemshop_items and item in purchased_items:
                purchased_items.remove(item)

        # Update UI
        # Get all available items including enchanted fusion results
        all_items = purchased_items.copy()

        # Add enchanted weapons
        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion and val.get("enchanted", False):
                    if fusion not in all_items:
                        all_items.append(fusion)

        for widget in items_frame.winfo_children():
            widget.destroy()

        # Rebuild the categorized layout
        categories = {
            "🗡️ Armes & équipement": [],
            "🔮 Magies & techniques": [],
            "✨ Objets enchantés": [],
            "🧪 Consommables": []
        }

        for item in purchased_items:
            if item in itemshop_items:
                categories["🧪 Consommables"].append(item)
            elif "Magie" in item or item in ["Coup simple", "Coup puissant", "Parade"]:
                categories["🔮 Magies & techniques"].append(item)
            else:
                categories["🗡️ Armes & équipement"].append(item)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("enchanted", False):
                        categories["✨ Objets enchantés"].append(fusion)
                    elif val.get("consumable", False):
                        categories["🧪 Consommables"].append(fusion)

        for category, items in categories.items():
            if items:
                tk.Label(items_frame, text=category, font=("Verdana", 11, "bold")).pack(pady=(10, 0), anchor="w")

                category_frame = tk.Frame(items_frame)
                category_frame.pack(pady=5, fill="x", padx=10)

                for i, item in enumerate(items):
                    btn = tk.Button(
                        category_frame,
                        text=item,
                        font=("Verdana", 10),
                        width=20,
                        command=lambda i=item: toggle_item_display(i, display_label)
                    )
                    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")



        update_main_window()
        result_label.config(
            text=f"Fusion réussie ! Vous avez créé : {result}",
            fg="green"
        )

    # If it's a string, it's a simple item result
    elif isinstance(recipe, str):
        result = recipe
        fusion_results.append(result)
        for item in selected_items:
            if item in itemshop_items and item in purchased_items:
                purchased_items.remove(item)
        update_main_window()
        result_label.config(
            text=f"Fusion réussie ! Vous avez créé : {result}",
            fg="green"
        )
    else:
        result_label.config(
            text="Échec de la fusion : format de recette inattendu.",
            fg="red"
        )

    # Clear the selected items
    selected_items.clear()
    display_label.config(text="Aucun élément sélectionné")

def add_to_fusion(item_name, display_label):
    selected_items.append(item_name)
    display_label.config(text=", ".join(selected_items))


# Fonction pour effacer la sélection
def clear_selection(display_label):
    selected_items.clear()
    display_label.config(text="Aucun élément sélectionné")

# Fenêtre de création de compétences
def open_skills_creation_window():
    skills_window = tk.Toplevel()
    skills_window.title("Création des compétences")
    skills_window.geometry("900x600")

    tk.Label(skills_window, text="Création des compétences", font=("Verdana", 14)).pack(pady=20)

    display_label = tk.Label(skills_window, text="Aucun élément sélectionné", font=("Verdana", 12), wraplength=500)
    display_label.pack(pady=10)

    clear_button = tk.Button(
        skills_window,
        text="Effacer la sélection",
        font=("Verdana", 10),
        command=lambda: clear_selection(display_label)
    )
    clear_button.pack(pady=5)

    # Scrollable area wrapper
    scroll_area = tk.Frame(skills_window)
    scroll_area.pack(fill="both", expand=True)

    # Canvas for scrolling
    canvas = tk.Canvas(scroll_area)
    scrollbar = tk.Scrollbar(scroll_area, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Categorize items
    categories = {
        "🗡️ Armes & équipement": [],
        "🔮 Magies & techniques": [],
        "✨ Objets enchantés": [],
        "🧪 Consommables": []
    }

    for item in purchased_items:
        if item in itemshop_items:
            categories["🧪 Consommables"].append(item)
        elif "Magie" in item or item in ["Coup simple", "Coup puissant", "Parade"]:
            categories["🔮 Magies & techniques"].append(item)
        else:
            categories["🗡️ Armes & équipement"].append(item)

    for fusion in fusion_results:
        for key, val in fusion_recipes.items():
            if isinstance(val, dict) and val.get("result") == fusion:
                if val.get("enchanted", False):
                    categories["✨ Objets enchantés"].append(fusion)
                elif val.get("consumable", False):
                    categories["🧪 Consommables"].append(fusion)

    # Display categorized items in grid layout
    for category, items in categories.items():
        if items:
            tk.Label(scrollable_frame, text=category, font=("Verdana", 11, "bold")).pack(pady=(10, 0), anchor="w")

            category_frame = tk.Frame(scrollable_frame)
            category_frame.pack(pady=5, fill="x", padx=10)

            for i, item in enumerate(items):
                btn = tk.Button(
                    category_frame,
                    text=item,
                    font=("Verdana", 10),
                    width=20,
                    command=lambda i=item: add_to_fusion(i, display_label)
                )
                btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")

    # Bottom panel for result and fusion button
    bottom_frame = tk.Frame(skills_window)
    bottom_frame.pack(pady=10)

    result_label = tk.Label(bottom_frame, text="", font=("Verdana", 12), wraplength=600)
    result_label.pack(pady=5)

    fusion_button = tk.Button(
        bottom_frame,
        text="Fusion",
        font=("Verdana", 12),
        command=lambda: handle_fusion(display_label, result_label, scrollable_frame)
    )
    fusion_button.pack(pady=5)

def open_rpg_ui_window():
    rpg_window = tk.Toplevel(window)
    rpg_window.title("RPG Combat")
    rpg_window.geometry("1200x900")

    main_frame = tk.Frame(rpg_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

    tk.Label(left_frame, text="Combat RPG", font=("Verdana", 16)).pack(pady=10)

    combat_frame = tk.Frame(left_frame)
    combat_frame.pack(pady=10)

    bars_frame = tk.Frame(left_frame)
    bars_frame.pack(pady=10)

    def show_floating_text(parent, text, color="red", duration=800):
        floating = tk.Label(parent, text=text, fg=color, font=("Verdana", 14, "bold"))
        floating.place(x=100, y=100)  # Adjust as needed
        dy = -2
        steps = duration // 50

        def animate(step=0):
            if step < steps:
                floating.place_configure(y=100 + dy * step)
                floating.after(50, animate, step + 1)
            else:
                floating.destroy()
        animate()

    def update_skills_display():
    # Clear previous widgets
        for widget in right_frame.winfo_children():
            widget.destroy()

        tk.Label(right_frame, text="Compétences disponibles", font=("Verdana", 12, "bold")).pack(pady=5)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("consumable", False):
                        # It's an item, not a skill — skip here
                        break
                    # Otherwise it's a skill
                    frame = tk.Frame(right_frame, bd=1, relief=tk.SOLID)
                    frame.pack(pady=3, fill=tk.X)
                    tk.Label(frame, text=fusion, font=("Verdana", 10, "bold")).pack(anchor="w")
                    tk.Label(frame, text=f"Dégâts: {val.get('damage', 0)}", font=("Verdana", 9)).pack(anchor="w")
                    tk.Label(frame, text=f"Coût: {val.get('mana_cost', 0)} mana, {val.get('fatigue_cost', 0)} fatigue", font=("Verdana", 9)).pack(anchor="w")
                    tk.Button(frame, text="Utiliser", font=("Verdana", 9), command=lambda v=val: use_skill(v)).pack(pady=2)

        tk.Label(right_frame, text="Objets disponibles", font=("Verdana", 12, "bold")).pack(pady=5)
        update_item_display()

    def apply_status_effect(name, target, duration, damage_per_turn, element):
        target[name] = {
        "duration": duration,
        "damage_per_turn": damage_per_turn,
        "element": element
    }
        
    def process_status_effects():
        to_remove = []
        for effect, data in enemy_status_effects.items():
            enemy_hp["value"] -= data["damage_per_turn"]
            log_message(f"🔥 {current_enemy['name']} subit {data['damage_per_turn']} dégâts de {effect}.")
            show_floating_text(window, data["damage_per_turn"], "orange")
            data["duration"] -= 1
            if data["duration"] <= 0:
                to_remove.append(effect)
        for effect in to_remove:
            del enemy_status_effects[effect]


    def start_next_fight():
        if fight_counter["count"] >= 5:
            log_message("🎉 Vous avez remporté les 5 combats !")
            return
        fight_counter["count"] += 1

        enemy_type = random.choices(enemy_types, weights=[e['weight'] for e in enemy_types])[0]
        current_enemy.update(enemy_type)

        # player_hp["value"] = 100
        # player_mana["value"] = 100
        #player_fatigue["value"] = 0
        enemy_hp["value"] = enemy_type["hp"]
        enemy_status_effects.clear()

        update_bars()
        log_message(f"⚔️ Combat {fight_counter['count']} commencé contre {current_enemy['name']} !")
        update_skills_display()


    def create_bar(label_text, color):
        container = tk.Frame(bars_frame)
        container.pack(pady=5)
        label = tk.Label(container, text=label_text, font=("Verdana", 10))
        label.pack(side=tk.LEFT, padx=5)
        canvas = tk.Canvas(container, width=200, height=20, bg="grey")
        canvas.pack(side=tk.LEFT)
        bar = canvas.create_rectangle(0, 0, 200, 20, fill=color)
        value_label = tk.Label(container, text="100/100", font=("Verdana", 10))
        value_label.pack(side=tk.LEFT, padx=5)
        return canvas, bar, value_label


    player_hp_canvas, player_hp_bar, player_hp_label = create_bar("Santé joueur", "green")
    enemy_hp_canvas, enemy_hp_bar, enemy_hp_label = create_bar("Santé ennemi", "red")
    mana_canvas, mana_bar, mana_label = create_bar("Mana joueur", "blue")
    fatigue_canvas, fatigue_bar, fatigue_label = create_bar("Fatigue joueur", "orange")


    log_text = tk.Text(left_frame, height=15, width=60, state=tk.DISABLED)
    log_text.pack(pady=10)

    fight_counter = {"count": 0}
    player_hp = {"value": 100}
    player_mana = {"value": 100}
    player_fatigue = {"value": 0}
    enemy_hp = {"value": 100}
    current_enemy = {"name": "", "resistances": {}, "damage_range": (5, 15)}

    def update_bars():
        def set_bar(canvas, bar, label, value, max_value):
            percent = max(min(value / max_value, 1), 0)
            canvas.coords(bar, 0, 0, 200 * percent, 20)
            label.config(text=f"{value}/{max_value}")
        set_bar(player_hp_canvas, player_hp_bar, player_hp_label, player_hp["value"], 100)
        set_bar(enemy_hp_canvas, enemy_hp_bar, enemy_hp_label, enemy_hp["value"], 100)
        set_bar(mana_canvas, mana_bar, mana_label, player_mana["value"], 100)
        set_bar(fatigue_canvas, fatigue_bar, fatigue_label, player_fatigue["value"], 100)
        update_item_display()


    def log_message(message, flash=False):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

        if flash:
            def flash_color(count=0):
                color = "yellow" if count % 2 == 0 else "white"
                log_text.config(bg=color)
                if count < 4:
                    log_text.after(150, flash_color, count + 1)
                else:
                    log_text.config(bg="white")
            flash_color()


    def enemy_attack():
        process_status_effects()
        if enemy_hp["value"] <= 0:
            return
        damage = random.randint(*current_enemy["damage_range"])
        player_hp["value"] -= damage
        log_message(f"⚠️ {current_enemy['name']} vous inflige {damage} de dégâts.")
        show_floating_text(rpg_window, damage, "red")
        if player_hp["value"] <= 0:
            log_message(f"💀 Vous avez été vaincu.")

    def use_skill(skill_data):
        if player_mana["value"] < skill_data["mana_cost"] or player_fatigue["value"] + skill_data["fatigue_cost"] > 100:
            messagebox.showwarning("Pas assez de ressources", "Pas assez de mana ou trop de fatigue.")
            return

        base_damage = skill_data["damage"]
        modifier = 1.0
        element = skill_data["element"]
        damage_type = skill_data["damage_type"]

        # Apply resistance or weakness, not both
        if element in current_enemy.get("resistances", {}):
            modifier *= current_enemy["resistances"][element]
            log_message(f"{current_enemy['name']} résiste à cette attaque.")
        elif element in current_enemy.get("weaknesses", {}):
            modifier *= current_enemy["weaknesses"][element]
            log_message(f"{current_enemy['name']} est faible face à cette attaque !")

        # Optionally also consider damage_type
        if damage_type in current_enemy.get("weaknesses", {}):
            modifier *= current_enemy["weaknesses"][damage_type]
            log_message(f"{current_enemy['name']} est vulnérable au type {damage_type} !")
        elif damage_type in current_enemy.get("resistances", {}):
            modifier *= current_enemy["resistances"][damage_type]
            log_message(f"{current_enemy['name']} est résistant au type {damage_type}.")

        actual_damage = int(base_damage * modifier)

        log_message (f"🌀 Vous utilisez : {skill_data['result']}")
        log_message (f"{skill_data['description']}")
        log_message (f"💥 Vous infligez {actual_damage} points de dégâts à {current_enemy['name']} !")
        if skill_data["element"] in current_enemy.get("weaknesses", {}):
            log_message (f"{current_enemy['name']} semble faible face à cette attaque !")
        if skill_data["damage_type"] in current_enemy.get("weaknesses", {}):
            log_message (f"{current_enemy['name']} semble peu sensible à cette attaque !")
        show_floating_text(rpg_window, actual_damage, "red")


        enemy_hp["value"] -= actual_damage
        player_mana["value"] -= skill_data["mana_cost"]
        player_fatigue["value"] += skill_data["fatigue_cost"]
        if skill_data["element"] == "fire":
            apply_status_effect("burn", enemy_status_effects, duration=3, damage_per_turn=5, element="fire")
            log_message(f"🔥 {current_enemy['name']} est en feu !")


        if enemy_hp["value"] <= 0:
            log_message(f"✅ {current_enemy['name']} vaincu !")
            start_next_fight()
        else:
            log_message("⏳ L'ennemi se prépare à attaquer...")
            rpg_window.after(2000, enemy_attack)
        update_bars()

    item_frames = []

    def update_item_display():
        for frame in item_frames:
            frame.destroy()
        item_frames.clear()

        # Merge purchased_items with item-like fusion results
        all_items = list(purchased_items)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion and val.get("consumable", False):
                    if fusion not in all_items:
                        all_items.append(fusion)

        for item in all_items:
            if item in itemshop_items or item in fusion_results:
                frame = tk.Frame(right_frame, bd=1, relief=tk.SOLID)
                frame.pack(pady=3, fill=tk.X)
                item_frames.append(frame)
                tk.Label(frame, text=item, font=("Verdana", 10)).pack(anchor="w")
                tk.Button(frame, text="Utiliser", font=("Verdana", 9), command=lambda i=item: use_item(i)).pack(pady=2)

    def use_item(item):
        # First: check if it's a consumable fusion
        is_consumable_fusion = False
        for recipe in fusion_recipes.values():
            if isinstance(recipe, dict) and recipe.get("result") == item and recipe.get("consumable"):
                is_consumable_fusion = True
                break

        # Handle regular shop items
        if item in purchased_items:
            purchased_items.remove(item)
        elif not is_consumable_fusion:
            log_message(f"❌ Vous ne possédez pas {item}.")
            return

        # Handle item effects
        if item == "Potion de soin":
            player_hp["value"] = min(100, player_hp["value"] + 25)
            log_message("🧪 Vous utilisez une potion de soin et récupérez 25 PV.")
        elif item == "Potion de soin supérieure":
            player_hp["value"] = min(100, player_hp["value"] + 50)
            log_message("🧪 Vous utilisez une potion de soin supérieure et récupérez 50 PV.")
        elif item == "Potion de mana":
            player_mana["value"] = min(100, player_mana["value"] + 50)
            log_message("🧪 Vous utilisez une potion de mana et récupérez 50 de mana.")
        elif item == "Potion de repos":
            player_fatigue["value"] = max(0, player_fatigue["value"] - 50)
            log_message("🧪 Vous utilisez une potion de repos et récupérez 50 de fatigue.")
        elif item == "Potion de récupération":
            player_fatigue["value"] = max(0, player_fatigue["value"] - 50)
            player_mana["value"] = min(100, player_mana["value"] + 50)
            log_message("🧪 Vous utilisez une potion de récupération : +50 mana, -50 fatigue.")
        else:
            log_message(f"❓ {item} n'a pas encore d'effet implémenté.")

        enemy_attack()
        update_bars()

    def attack():
        if player_hp["value"] <= 0 or enemy_hp["value"] <= 0:
            return
        damage = random.randint(10, 25)
        enemy_hp["value"] -= damage
        log_message(f"💥 Vous infligez {damage} de dégâts à {current_enemy['name']}.")
        player_mana["value"] -= 10
        player_fatigue["value"] += 15
        if enemy_hp["value"] <= 0:
            log_message(f"✅ {current_enemy['name']} vaincu !")
            start_next_fight()
        else:
            log_message("⏳ L'ennemi se prépare à attaquer...")
            rpg_window.after(2000, enemy_attack)
        update_bars()

    tk.Button(combat_frame, text="Attaque basique", font=("Verdana", 12), command=attack).pack(pady=5)

    update_skills_display()

    tk.Label(right_frame, text="Objets disponibles", font=("Verdana", 12, "bold")).pack(pady=5)
    update_item_display()

    start_next_fight()

def open_military_window():
    ShopWindow("Entra\u00eeneur militaire", ["Coup simple : 100", "Coup puissant : 250", "Parade : 250"])

def open_magic_window():
    ShopWindow("Ma\u00eetre magicien", ["Magie \u00e9l\u00e9mentaire Feu : 200", "Magie \u00e9l\u00e9mentaire Air : 200", "Magie \u00e9l\u00e9mentaire Eau : 200", "Magie \u00e9l\u00e9mentaire Terre : 200", "Magie d'illusion : 300", "Magie psychique : 300"])

def open_milishop_window():
    ShopWindow("Marchand militaire", ["\u00c9p\u00e9e courte : 200", "\u00c9p\u00e9e longue : 350", "Dague : 200", "Hache de guerre : 250", "Arc : 250", "Bouclier : 350"])

def open_itemshop_window():
    ShopWindow("Marchand d'objets", ["Potion de soin : 50", "Potion de poison : 50", "Potion de mana : 100", "Potion de repos : 100", "Bombe l\u00e9g\u00e8re : 100", "Bombe lourde : 250", "Bombe fumig\u00e8ne : 100", "Filet : 100"])

# Main window
window = tk.Tk()
window.title("Project RPG")
window.geometry("800x700")

main_label = tk.Label(window, text="Cr\u00e9ation des comp\u00e9tences", font=("Verdana", 18))
main_label.pack(pady=20)

main_money_label = tk.Label(window, text=f"Argent : {money} deullars", font=("Verdana", 12))
main_money_label.pack(pady=10)

purchases_label = tk.Label(window, text="Items achet\u00e9s : ", font=("Verdana", 12), wraplength=600, justify="center")
purchases_label.pack(pady=10)

fusions_label = tk.Label(window, text="Fusions r\u00e9alis\u00e9es : Aucun", font=("Verdana", 12), wraplength=600, justify="center")
fusions_label.pack(pady=10)

# Add buttons
military_button = tk.Button(window, text="Entra\u00eeneur militaire", font=("Verdana", 12), command=open_military_window)
military_button.pack(pady=5)

magician_button = tk.Button(window, text="Ma\u00eetre magicien", font=("Verdana", 12), command=open_magic_window)
magician_button.pack(pady=5)

milishop_button = tk.Button(window, text="Marchand militaire", font=("Verdana", 12), command=open_milishop_window)
milishop_button.pack(pady=5)

itemshop_button = tk.Button(window, text="Marchand d'objets", font=("Verdana", 12), command=open_itemshop_window)
itemshop_button.pack(pady=5)

skills_button = tk.Button(window, text="Cr\u00e9ation des comp\u00e9tences", font=("Verdana", 12), command=open_skills_creation_window)
skills_button.pack(pady=20)

rpg_button = tk.Button(window, text="Partir \u00e0 l'attaque", font=("Verdana", 12), command=open_rpg_ui_window)
rpg_button.pack(pady=10)

reset_button = tk.Button(window, text="R\u00e9initialiser le jeu", font=("Verdana", 12), bg="red", fg="white", command=reset_game)
reset_button.pack(pady=10)

inventaire_button = tk.Button(window, text="Inventaire", font=("Verdana", 12), command=open_inventaire_window)
inventaire_button.pack(pady=10)

window.mainloop()
