import tkinter as tk
from tkinter import messagebox
import random
import requests
import os
import zipfile
import sys
import shutil

CURRENT_VERSION = "0.0.8.2"

def check_for_update():
    download_url = "https://github.com/FoZIkks/myprojectedrpg/releases/latest/download/projectrpg.exe"  # or .exe

    try:
        response = requests.get(version_url)
        latest_version = response.text.strip()

        if latest_version > CURRENT_VERSION:
            print(f"Nouvelle version disponible ({latest_version}) — mise à jour en cours...")
            update_game(download_url)
        else:
            print("✅ Jeu à jour.")
    except Exception as e:
        print(f"Erreur de vérification de mise à jour : {e}")


def update_game(download_url):
    try:
        # Download the new zip/exe
        r = requests.get(download_url, stream=True)
        with open("update.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        # Unzip and overwrite files
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall("update_temp")

        for item in os.listdir("update_temp"):
            s = os.path.join("update_temp", item)
            d = os.path.join(".", item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        shutil.rmtree("update_temp")
        os.remove("update.zip")
        print("Mise à jour terminée. Redémarrage...")
        restart_game()

    except Exception as e:
        print(f"Erreur pendant la mise à jour: {e}")

def restart_game():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Check des maj
check_for_update()

# Global variables
money = 1000
purchased_items = []
selected_items = []
fusion_results = []

fusion_recipes = {
    frozenset(["Coup simple", "Hache de guerre"]): {
        "result": "Frappe simple à la hachet",
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
    frozenset(["Potion de soin", "Bombe l\u00e9g\u00e8re"]): "Bombe de soin",
    frozenset(["Potion de soin", "Bombe lourde"]): "Bombe puissante de soin",
    frozenset(["Potion de soin", "Bombe fumig\u00e8ne"]): "Bombe de fumée soignante",
    frozenset(["Potion de soin", "Filet"]): "Filet soignant",
    frozenset(["Potion de poison", "Potion de poison"]): "Potion de poison puissante",
    frozenset(["Potion de poison", "Bombe l\u00e9g\u00e8re"]): "Bombe de poison",
    frozenset(["Potion de poison", "Bombe lourde"]): "Bombe puissante de poison",
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
    }

}


enemy_types = [
    {"name": "Gobelin", "hp": 80, "damage_range": (5, 15), "resistances": {}, "weaknesses": {"piercing": 1.5}, "weight": 3},
    {"name": "Salamandre", "hp": 100, "damage_range": (5, 15), "resistances": {"fire": 0.5},"weaknesses": {"water": 1.5}, "weight": 1},
    {"name": "Ogre", "hp": 150, "damage_range": (10, 25), "resistances": {}, "weaknesses": {"magic": 1.25},"weight": 2},
    {"name": "Spectre", "hp": 70, "damage_range": (5, 10), "resistances": {"magic": 0.7}, "weaknesses": {"contondant": 2.0}, "weight": 1},
    {"name": "Mark Zuckerberg", "hp": 100, "damage_range": (15, 20), "resistances": {"contondant": 0.7}, "weaknesses": {"magic": 2.0}, "weight": 1},
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
    if selected_set in fusion_recipes:
         recipe = fusion_recipes[selected_set]
    
    # If the recipe is a dictionary with a "result", it's a skill fusion
    if isinstance(recipe, dict) and "result" in recipe:
        result = recipe["result"]
        fusion_results.append(result)

        # Remove used items if they are from the item shop
        for item in selected_items:
            if item in itemshop_items and item in purchased_items:
                purchased_items.remove(item)

        # Update UI
        for widget in items_frame.winfo_children():
            widget.destroy()
        for item in purchased_items:
            tk.Button(
                items_frame,
                text=item,
                font=("Verdana", 10),
                command=lambda i=item: toggle_item_display(i, display_label),
            ).pack(side=tk.LEFT, padx=5)

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

    items_frame = tk.Frame(skills_window)
    items_frame.pack(pady=10)

    if purchased_items:
        tk.Label(skills_window, text="Cliquez sur un élément pour l'ajouter à la fusion :", font=("Verdana", 12)).pack(pady=10)
        for item in purchased_items:
            tk.Button(
                items_frame, 
                text=item, 
                font=("Verdana", 10), 
                command=lambda i=item: add_to_fusion(i, display_label)
            ).pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(skills_window, text="Aucun élément acheté pour le moment.", font=("Verdana", 12)).pack(pady=20)

    result_label = tk.Label(skills_window, text="", font=("Verdana", 12), wraplength=500)
    result_label.pack(pady=10)

    fusion_button = tk.Button(
        skills_window, 
        text="Fusion", 
        font=("Verdana", 12), 
        command=lambda: handle_fusion(display_label, result_label, items_frame)
    )
    fusion_button.pack(pady=10)

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
        resistance = current_enemy["resistances"].get(skill_data["element"], 1.0)
        weakness_bonus = 1.0

        # Check for element or damage type weaknesses
        if skill_data["element"] in current_enemy.get("weaknesses", {}):
            weakness_bonus *= current_enemy["weaknesses"][skill_data["element"]]
            log_message (f"{current_enemy['name']} semble faible face à l'attaque!")
        if skill_data["damage_type"] in current_enemy.get("weaknesses", {}):
            weakness_bonus *= current_enemy["weaknesses"][skill_data["damage_type"]]

        actual_damage = int(base_damage * resistance * weakness_bonus)


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
