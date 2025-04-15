import tkinter as tk
from tkinter import messagebox
import random

# Global variables
money = 1000
purchased_items = []
selected_items = []
fusion_results = []

fusion_recipes = {
    frozenset(["Coup simple", "Hache de guerre"]): {
        "result": "Frappe simple à la hache",
        "damage": 25,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre hache !"
    },
    frozenset(["Coup simple", "Arc"]): {
        "result": "Tir simple",
        "damage": 20,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous tirez avec votre arc !"
    },
    frozenset(["Coup simple", "Bouclier"]): {
        "result": "Coup de bouclier",
        "damage": 15,
        "damage_type": "contondant",
        "element": "force",
        "description": "Vous frappez avec votre bouclier !"
    },
    frozenset(["Coup simple", "Épée courte"]): {
        "result": "Frappe à l'épée",
        "damage": 20,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre épée !"
    },
    frozenset(["Coup simple", "Épée longue"]): {
        "result": "Frappe à l'épée longue",
        "damage": 25,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous frappez avec votre longue épée !"
    },
    frozenset(["Coup simple", "Dague"]): {
        "result": "Coup de dague",
        "damage": 15,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous assénez un coup avec votre dague !"
    },
    frozenset(["Coup puissant", "Épée courte"]): {
        "result": "Frappe lourde à l'épée",
        "damage": 45,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez lourdement votre épée !"
    },
    frozenset(["Coup puissant", "Épée longue"]): {
        "result": "Frappe lourde à l'épée longue",
        "damage": 50,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez lourdement votre épée longue !"
    },
    frozenset(["Coup puissant", "Dague"]): {
        "result": "Poignardage lourd",
        "damage": 25,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous lacérez avec votre dague !"
    },
    frozenset(["Coup puissant", "Hache de guerre"]): {
        "result": "Abattage de hache",
        "damage": 45,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous abattez votre hache !"
    },
    frozenset(["Coup puissant", "Arc"]): {
        "result": "Tir violent",
        "damage": 40,
        "damage_type": "piercing",
        "element": "force",
        "description": "Vous décochez une flèche à pleine puissance !"
    },
    frozenset(["Coup puissant", "Bouclier"]): {
        "result": "Pillonage de bouclier",
        "damage": 25,
        "damage_type": "contondant",
        "element": "force",
        "description": "Vous abbattez votre bouclier violemment !"
    },
    frozenset(["Parade", "Épée courte"]): {
        "result": "Parade à l'épée",
        "damage": 10,
        "damage_type": "slashing",
        "element": "force",
        "description": "Vous prenez une posture défensive à l'épée!"
    },
    frozenset(["Parade", "Épée longue"]): {
        "result": "Parade avec épée lourde",
        "damage": 15,
        "damage_type": "slashing",
        "element": "force",
        "description": "
    },
    frozenset(["Parade", "Dague"]): {
        "result": "Blocage à la dague",
        "damage": 5,
        "damage_type": "piercing",
        "element": "force"
    },
    frozenset(["Parade", "Hache de guerre"]): {
        "result": "Blocage à la hache",
        "damage": 15,
        "damage_type": "slashing",
        "element": "force"
    },
    frozenset(["Parade", "Arc"]): {
        "result": "Blocage avec l'arc",
        "damage": 10,
        "damage_type": "slashing",
        "element": "force"
    },
    frozenset(["Parade", "Bouclier"]): {
        "result": "Blocage au bouclier",
        "damage": 5,
        "damage_type": "contondant",
        "element": "force"
    },
    frozenset(["Coup simple", "Magie élémentaire Feu"]): {
        "result": "Boule de feu simple",
        "damage": 25,
        "damage_type": "magic",
        "element": "fire"
    },
    frozenset(["Coup simple", "Magie élémentaire Air"]): {
        "result": "Bourrasque",
        "damage": 20,
        "damage_type": "magic",
        "element": "wind"
    },
    frozenset(["Coup simple", "Magie élémentaire Eau"]): {
        "result": "Jet d'eau",
        "damage": 20,
        "damage_type": "magic",
        "element": "water"
    },
    frozenset(["Coup simple", "Magie élémentaire Terre"]): {
        "result": "Frappe de terre",
        "damage": 20,
        "damage_type": "magic",
        "element": "earth"
    },
    frozenset(["Coup simple", "Magie d'illusion"]): {
        "result": "Illusion simple",
        "damage": 0,
        "damage_type": "state",
        "element": "illusion"
    },
    frozenset(["Coup simple", "Magie psychique"]): {
        "result": "Décharge mentale",
        "damage": 10,
        "damage_type": "magic",
        "element": "psychic"
    },
    frozenset(["Coup puissant", "Magie élémentaire Feu"]): {
        "result": "Colonne de flamme",
        "damage": 45,
        "damage_type": "magic",
        "element": "fire"
    },
    frozenset(["Coup puissant", "Magie élémentaire Air"]): {
        "result": "Tornade",
        "damage": 40,
        "damage_type": "magic",
        "element": "wind"
    },
    frozenset(["Coup puissant", "Magie élémentaire Eau"]): {
        "result": "Tsunami",
        "damage": 40,
        "damage_type": "magic",
        "element": "water"
    },
    frozenset(["Coup puissant", "Magie élémentaire Terre"]): {
        "result": "Séisme",
        "damage": 40,
        "damage_type": "magic",
        "element": "earth"
    },
    frozenset(["Coup puissant", "Magie d'illusion"]): {
        "result": "Image rémanente",
        "damage": 0,
        "damage_type": "state",
        "element": "illusion"
    },
    frozenset(["Coup puissant", "Magie psychique"]): {
        "result": "Emprise mentale",
        "damage": 20,
        "damage_type": "magic",
        "element": "psychic"
    },
    frozenset(["Parade", "Magie élémentaire Feu"]): {
        "result": "Bouclier de feu",
        "damage": 15,
        "damage_type": "magic",
        "element": "fire"
    },
    frozenset(["Parade", "Magie élémentaire Air"]): {
        "result": "Bouclier d'air",
        "damage": 10,
        "damage_type": "magic",
        "element": "wind"
    },
    frozenset(["Parade", "Magie élémentaire Eau"]): {
        "result": "Bouclier d'eau",
        "damage": 10,
        "damage_type": "magic",
        "element": "eau"
    },
    frozenset(["Parade", "Magie élémentaire Terre"]): {
        "result": "Bouclier de terre",
        "damage": 10,
        "damage_type": "magic",
        "element": "earth"
    },
    frozenset(["Parade", "Magie d'illusion"]): {
        "result": "Illusion du bras",
        "damage": 0,
        "damage_type": "state",
        "element": "psychic"
    },
    frozenset(["Parade", "Magie psychique"]): "Perturbation psychique",
    frozenset(["Magie élémentaire Feu", "Magie élémentaire Feu"]): "Feu éternel",
    frozenset(["Magie élémentaire Feu", "Magie élémentaire Air"]): "Tempête de feu",
    frozenset(["Magie élémentaire Feu", "Magie élémentaire Eau"]): "Vapeur",
    frozenset(["Magie élémentaire Feu", "Magie élémentaire Terre"]): "Coulée de lave",
    frozenset(["Magie élémentaire Air", "Magie élémentaire Air"]): "Cyclone",
    frozenset(["Magie élémentaire Air", "Magie élémentaire Eau"]): "Déluge",
    frozenset(["Magie élémentaire Air", "Magie élémentaire Terre"]): "Poussière",
    frozenset(["Magie élémentaire Eau", "Magie élémentaire Eau"]): "Tsunami",
    frozenset(["Magie élémentaire Eau", "Magie élémentaire Terre"]): "Coulée de boue",
    frozenset(["Magie élémentaire Terre", "Magie élémentaire Terre"]): "Contrôle sismique",
    frozenset(["Magie élémentaire Feu", "Épée courte"]): "Épée à la lame enflammée",
    frozenset(["Magie élémentaire Feu", "Épée longue"]): "Épée longue brûlante",
    frozenset(["Magie élémentaire Feu", "Dague"]): "Dague embrasée",
    frozenset(["Magie élémentaire Feu", "Hache de guerre"]): "Hache flamboyante",
    frozenset(["Magie élémentaire Feu", "Arc"]): "Arc rougeoyant",
    frozenset(["Magie élémentaire Feu", "Bouclier"]): "Bouclier imprégné de flammes",
    frozenset(["Magie élémentaire Air", "Épée courte"]): "Épée entourée d'un zéphyr",
    frozenset(["Magie élémentaire Air", "Épée longue"]): "Épée a deux main portée par le vent",
    frozenset(["Magie élémentaire Air", "Dague"]): "Dague du vent",
    frozenset(["Magie élémentaire Air", "Hache de guerre"]): "Hache des bourrasques",
    frozenset(["Magie élémentaire Air", "Arc"]): "Arc des alizés",
    frozenset(["Magie élémentaire Air", "Bouclier"]): "Bouclier porté par le vent",
    frozenset(["Magie élémentaire Eau", "Épée courte"]): "Épée de la source",
    frozenset(["Magie élémentaire Eau", "Épée longue"]): "Épée de la cascade",
    frozenset(["Magie élémentaire Eau", "Dague"]): "Dague des profondeurs",
    frozenset(["Magie élémentaire Eau", "Hache de guerre"]): "Hache des marées",
    frozenset(["Magie élémentaire Eau", "Arc"]): "Arc des courants",
    frozenset(["Magie élémentaire Eau", "Bouclier"]): "Bouclier alourdis par l'eau",
    frozenset(["Magie élémentaire Terre", "Épée courte"]): "Épée des saillies rocheuses",
    frozenset(["Magie élémentaire Terre", "Épée longue"]): "Épée des falaises",
    frozenset(["Magie élémentaire Terre", "Dague"]): "Dague des désert",
    frozenset(["Magie élémentaire Terre", "Hache de guerre"]): "Hache des fissures",
    frozenset(["Magie élémentaire Terre", "Arc"]): "Arc des plaines",
    frozenset(["Magie élémentaire Terre", "Bouclier"]): "Bouclier massif de terre",
    frozenset(["Potion de soin", "Potion de soin"]): "Potion de soin supérieure",
    frozenset(["Potion de soin", "Potion de poison"]): "Potion de poison auto soignant",
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

}

itemshop_items = ["Potion de soin", "Potion de poison", "Bombe l\u00e9g\u00e8re", "Bombe lourde", "Bombe fumig\u00e8ne", "Filet"]

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
        result = recipe["result"]
        damage = recipe["damage"]
        damage_type = recipe["damage_type"]
        element = recipe["element"]

        if result in fusion_results:
            result_label.config(
                text="Échec de la fusion : Cette fusion a déjà été réalisée.", fg="red"
            )
        else:
            fusion_results.append(result)

            # Remove only one instance of each item used in fusion (if it's a shop item)
            for item in selected_items:
                if item in itemshop_items and item in purchased_items:
                    purchased_items.remove(item)

            # Update the items display
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
                text=f"Fusion réussie ! Vous avez créé : {result}\n"
                     f"Statistiques :\n"
                     f"Dégâts : {damage}\n"
                     f"Élément : {element}",
                fg="green"
            )
    else:
        result_label.config(
            text="Échec de la fusion : La combinaison actuelle ne donne aucun résultat.",
            fg="red",
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
    rpg_window.geometry("600x500")

    tk.Label(rpg_window, text="Combat RPG", font=("Verdana", 16)).pack(pady=10)

    combat_frame = tk.Frame(rpg_window)
    combat_frame.pack(pady=10)

    log_text = tk.Text(rpg_window, height=15, width=60, state=tk.DISABLED)
    log_text.pack(pady=10)

    fight_counter = {"count": 0}
    player_hp = {"value": 100}
    enemy_hp = {"value": 100}

    def log_message(message):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

    def start_next_fight():
        if fight_counter["count"] >= 5:
            log_message("🎉 Vous avez remporté les 5 combats !")
            return
        fight_counter["count"] += 1
        player_hp["value"] = 100
        enemy_hp["value"] = 50 + fight_counter["count"] * 10
        update_health()
        log_message(f"⚔️ Combat {fight_counter['count']} commencé !")

    def update_health():
        player_hp_label.config(text=f"Votre HP : {player_hp['value']}")
        enemy_hp_label.config(text=f"Ennemi HP : {enemy_hp['value']}")

    def attack():
        if player_hp["value"] <= 0 or enemy_hp["value"] <= 0:
            return

        player_damage = random.randint(10, 25)
        enemy_hp["value"] -= player_damage
        log_message(f"💥 Vous infligez {player_damage} de dégâts à l'ennemi.")
        if enemy_hp["value"] <= 0:
            log_message(f"✅ Ennemi vaincu !")
            start_next_fight()
            return

        enemy_damage = random.randint(5, 15)
        player_hp["value"] -= enemy_damage
        log_message(f"⚠️ L'ennemi vous inflige {enemy_damage} de dégâts.")
        if player_hp["value"] <= 0:
            log_message(f"💀 Vous avez été vaincu.")
        
        update_health()

    player_hp_label = tk.Label(combat_frame, text=f"Votre HP : {player_hp['value']}", font=("Verdana", 12))
    player_hp_label.pack(pady=5)

    enemy_hp_label = tk.Label(combat_frame, text=f"Ennemi HP : {enemy_hp['value']}", font=("Verdana", 12))
    enemy_hp_label.pack(pady=5)

    attack_button = tk.Button(combat_frame, text="Attaquer", font=("Verdana", 12), command=attack)
    attack_button.pack(pady=10)

    start_next_fight()

def open_military_window():
    ShopWindow("Entra\u00eeneur militaire", ["Coup simple : 100", "Coup puissant : 250", "Parade : 250"])

def open_magic_window():
    ShopWindow("Ma\u00eetre magicien", ["Magie \u00e9l\u00e9mentaire Feu : 200", "Magie \u00e9l\u00e9mentaire Air : 200", "Magie \u00e9l\u00e9mentaire Eau : 200", "Magie \u00e9l\u00e9mentaire Terre : 200", "Magie d'illusion : 300", "Magie psychique : 300"])

def open_milishop_window():
    ShopWindow("Marchand militaire", ["\u00c9p\u00e9e courte : 200", "\u00c9p\u00e9e longue : 350", "Dague : 200", "Hache de guerre : 250", "Arc : 250", "Bouclier : 350"])

def open_itemshop_window():
    ShopWindow("Marchand d'objets", ["Potion de soin : 50", "Potion de poison : 50", "Bombe l\u00e9g\u00e8re : 100", "Bombe lourde : 250", "Bombe fumig\u00e8ne : 100", "Filet : 100"])

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
