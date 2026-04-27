import tkinter as tk
from tkinter import messagebox
import random
import os
import csv

from fusion_recipes_lists import fusion_recipes
from enemy_types_lists import enemy_types
from quests_list import quests
from gui_appearance import *

CURRENT_VERSION = "0.2.5"
VERSION_NAME = "Pre-Alpha - Bug fixes & QoL"

SAVE_FILE = "save.csv"
player_name = ""

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


money = 0
purchased_items = []
selected_items = []
fusion_results = []
enemy_status_effects = {}
player_status_effects = {}
last_combat_result = {"lost": False}

player_xp = {
    "global": 0,
    "force": 0,
    "magic": 0
}

player_stats = {
    "max_hp": 100,
    "max_mana": 100,
    "max_fatigue": 100,
    "force_bonus": 1.0,
    "magic_bonus": 1.0
}


def initialize_save():
    global money, purchased_items, fusion_results, player_xp, player_stats, player_name

    if not os.path.exists(SAVE_FILE):
        # Demander le nom du joueur
        import tkinter.simpledialog
        player_name = tkinter.simpledialog.askstring("Nouveau joueur", "Entrez votre nom :")
        if not player_name:
            player_name = "Joueur"

        # Message d'accueil
        if player_name == "devzeon":
            messagebox.showinfo("Bienvenue maître dev", f"Bonjour Maître Devzeon, nous ne vous avions pas reconnu. Nous avons rempli vos stats. Passez un bon débogage")
            money = 1000000
            player_xp["global"] = 10000
            player_xp["force"] = 10000
            player_xp["magic"] = 10000

            player_stats["max_hp"] = 250
            player_stats["max_mana"] = 250
            player_stats["max_fatigue"] = 250
            player_stats["force_bonus"] = 1.0
            player_stats["magic_bonus"] = 1.0

        else:
            messagebox.showinfo("Bienvenue", f"Bienvenue, {player_name} ! Préparez-vous pour l'aventure.")
            money = 1000
            player_xp["global"] = 0
            player_xp["force"] = 0
            player_xp["magic"] = 0

            player_stats["max_hp"] = 100
            player_stats["max_mana"] = 100
            player_stats["max_fatigue"] = 100
            player_stats["force_bonus"] = 1.0
            player_stats["magic_bonus"] = 1.0
        
        
        # Créer un fichier de sauvegarde vide avec les valeurs par défaut
        with open(SAVE_FILE, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "money", "purchased_items", "fusion_results", "xp_global", "completed_quests", "xp_force", "xp_magic",
                             "max_hp", "max_mana", "max_fatigue", "force_bonus", "magic_bonus"])
            completed_ids = [str(q["id"]) for q in quests if q["completed"]]
            writer.writerow([
                player_name, money, ";".join(purchased_items), ";".join(fusion_results), ";".join(completed_ids),
                player_xp["global"], player_xp["force"], player_xp["magic"],
                player_stats["max_hp"], player_stats["max_mana"], player_stats["max_fatigue"],
                player_stats["force_bonus"], player_stats["magic_bonus"]
            ])
    else:
        # Charger les données du fichier
        with open(SAVE_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = next(reader)

            player_name = data.get("name", "Joueur")
            money = safe_int(data.get("money"), 0)

            purchased_items[:] = data["purchased_items"].split(";") if data.get("purchased_items") else []
            fusion_results[:] = data["fusion_results"].split(";") if data.get("fusion_results") else []

            # 🔹 Safe conversions
            player_xp["global"] = safe_int(data.get("xp_global"), 0)
            player_xp["force"] = safe_int(data.get("xp_force"), 0)
            player_xp["magic"] = safe_int(data.get("xp_magic"), 0)

            player_stats["max_hp"] = safe_int(data.get("max_hp"), 100)
            player_stats["max_mana"] = safe_int(data.get("max_mana"), 100)
            player_stats["max_fatigue"] = safe_int(data.get("max_fatigue"), 100)
            player_stats["force_bonus"] = safe_float(data.get("force_bonus"), 1.0)
            player_stats["magic_bonus"] = safe_float(data.get("magic_bonus"), 1.0)


            # 🔹 Load completed quests if present
            if "completed_quests" in data:
                completed_ids = data.get("completed_quests", "").split(";")
                for q in quests:
                    if str(q["id"]) in completed_ids:
                        q["completed"] = True

            if 'player_name_label' in globals():
                player_name_label.config(text=f"{player_name}")


def save_game():
    with open(SAVE_FILE, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "name", "money", "purchased_items", "fusion_results",
            "xp_global", "xp_force", "xp_magic",
            "max_hp", "max_mana", "max_fatigue",
            "force_bonus", "magic_bonus",
        ])
        writer.writerow([
            player_name,
            money,
            ";".join(purchased_items),
            ";".join(fusion_results),
            player_xp["global"],
            player_xp["force"],
            player_xp["magic"],
            player_stats["max_hp"],
            player_stats["max_mana"],
            player_stats["max_fatigue"],
            player_stats["force_bonus"],
            player_stats["magic_bonus"]
        ])

# Global variables
purchased_items = []
selected_items = []
fusion_results = []
enemy_status_effects = {}
player_status_effects = {}

itemshop_items = ["Potion de soin", "Potion de poison", "Potion de mana", "Potion de repos", "Bombe l\u00e9g\u00e8re", "Bombe lourde", "Bombe fumig\u00e8ne", "Filet"]

# Function to update the main window with purchased items and fusion results
def update_main_window():
    main_money_label.config(text=f"Argent : {money} deullars")

# Reset the game state
def reset_game():
    global money, purchased_items, selected_items, fusion_results
    money = 1000
    purchased_items.clear()
    selected_items.clear()
    fusion_results.clear()
    update_main_window()
    player_xp = {
        "global": 0,
        "force": 0,
        "magic": 0
    }
    player_stats = {
        "max_hp": 100,
        "max_mana": 100,
        "max_fatigue": 100,
        "force_bonus": 1.0,
        "magic_bonus": 1.0
    }

def inn_rest():
    global money, last_combat_result
    INN_COST = 25  # or whatever you already use

    if money >= INN_COST:
        money -= INN_COST

        # ✅ Full restore
        player_stats["current_hp"] = player_stats["max_hp"]
        player_stats["current_mana"] = player_stats["max_mana"]
        player_stats["current_fatigue"] = 0

        # ✅ Clear penalty from last defeat
        last_combat_result["lost"] = False

        messagebox.showinfo("Repos", "Vous vous reposez à l'auberge.\n💤 Vous êtes totalement rétabli !")
        update_main_window()
    else:
        messagebox.showwarning("Pas assez d'argent", "Vous n'avez pas assez d'argent pour vous reposer.")


    
def open_inventaire_window():
    inventaire_window = tk.Toplevel(window)
    inventaire_window.title("Inventaire")
    inventaire_window.geometry(f"{WINDOW_WIDTH_INVENTORY}x{WINDOW_HEIGHT_INVENTORY}")
    inventaire_window.transient(window)
    inventaire_window.grab_set()
    inventaire_window.focus_set()

    inventaire_window.configure(bg=COLOR_LIGHT_BG)
    
    # Create two sections: Fusions and Items
    sections_frame = tk.Frame(inventaire_window, bg="#fff9ec")
    sections_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ SECTION 1: FUSIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    tk.Label(sections_frame, text="📖 Fusions Réalisées", font=("Verdana", 14, "bold"), bg="#fff9ec").pack(pady=10, anchor="w")

    scroll_canvas = tk.Canvas(sections_frame, bg="#fff9ec", highlightthickness=0, height=300)
    scroll_frame = tk.Frame(scroll_canvas, bg="#fff9ec")
    scrollbar = tk.Scrollbar(sections_frame, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y", pady=(20, 0))
    scroll_canvas.pack(side="left", fill="both", expand=True, pady=(0, 10))
    scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

    if fusion_results:
        for fusion in fusion_results:
            # Recherche des infos pour cette fusion
            fusion_info = None
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    fusion_info = val
                    break

            # Affichage du nom de la fusion
            tk.Label(
                scroll_frame,
                text=f"• {fusion}",
                font=("Verdana", 12, "bold"),
                bg="#fff9ec",
                anchor="w"
            ).pack(fill="x", padx=20, pady=(8, 0))

            # Si c'est une compétence (pas un consommable ni un objet enchanté)
            if fusion_info and not fusion_info.get("consumable", False) and not fusion_info.get("enchanted", False):
                desc = fusion_info.get("description", "Pas de description")
                mana_cost = fusion_info.get("mana_cost", 0)
                fatigue_cost = fusion_info.get("fatigue_cost", 0)
                damage_type = fusion_info.get("damage_type", "inconnu")
                element = fusion_info.get("element", "aucun")

                # Effets spéciaux
                effect_text = ""
                effect = fusion_info.get("effect")
                if effect:
                    etype = effect.get("type", "")
                    if etype:
                        effect_text = f"Effet : {etype}"
                        if etype == "poison":
                            effect_text += f" ({effect.get('damage_per_turn', 0)}/tour pendant {effect.get('duration', 0)} tours)"
                        elif etype == "stun":
                            effect_text += f" (étourdit {effect.get('duration', 0)} tours)"
                        elif etype == "dodge":
                            effect_text += f" (esquive {effect.get('duration', 0)} attaques)"
                        elif etype == "damage_reduction":
                            effect_text += f" (réduit les dégâts de moitié pour {effect.get('duration', 0)} tours)"

                # Description
                tk.Label(
                    scroll_frame,
                    text=f"   {desc}",
                    font=("Verdana", 10),
                    bg="#fff9ec",
                    anchor="w",
                    wraplength=450,
                    justify="left"
                ).pack(fill="x", padx=40)

                # Coût
                tk.Label(
                    scroll_frame,
                    text=f"   Coût : {mana_cost} mana, {fatigue_cost} fatigue",
                    font=("Verdana", 9, "italic"),
                    bg="#fff9ec",
                    anchor="w"
                ).pack(fill="x", padx=40)

                # Type de dégâts et élément
                # Afficher les dégâts
                damage = fusion_info.get("damage", 0)
                tk.Label(
                    scroll_frame,
                    text=f"   Dégâts : {damage}",
                    font=("Verdana", 9),
                    bg="#fff9ec",
                    anchor="w"
                ).pack(fill="x", padx=40)


                # Effets spéciaux s'il y en a
                if effect_text:
                    tk.Label(
                        scroll_frame,
                        text=f"   {effect_text}",
                        font=("Verdana", 9),
                        bg="#fff9ec",
                        anchor="w"
                    ).pack(fill="x", padx=40)

    else:
        tk.Label(
            scroll_frame,
            text="Aucune fusion réalisée",
            font=("Verdana", 12),
            bg="#fff9ec"
        ).pack(pady=20)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ SECTION 2: ITEMS & CONSOMMABLES ━━━━━━━━━━━━━━━━━
    tk.Label(sections_frame, text="🧪 Objets & Consommables", font=("Verdana", 14, "bold"), bg="#fff9ec").pack(pady=10, anchor="w")
    
    # Count items and show with quantities
    items_canvas = tk.Canvas(sections_frame, bg="#fff9ec", highlightthickness=0, height=250)
    items_frame = tk.Frame(items_canvas, bg="#fff9ec")
    items_scrollbar = tk.Scrollbar(sections_frame, orient="vertical", command=items_canvas.yview)
    items_canvas.configure(yscrollcommand=items_scrollbar.set)
    
    items_scrollbar.pack(side="right", fill="y")
    items_canvas.pack(side="left", fill="both", expand=True)
    items_canvas.create_window((0, 0), window=items_frame, anchor="nw")
    
    items_frame.bind("<Configure>", lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all")))
    
    if purchased_items:
        # Count items
        item_counts = {}
        for item in purchased_items:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        # Display with counts
        for item, count in sorted(item_counts.items()):
            count_text = f"  x{count}" if count > 1 else ""
            tk.Label(
                items_frame,
                text=f"• {item}{count_text}",
                font=("Verdana", 11),
                bg="#fff9ec",
                anchor="w"
            ).pack(fill="x", padx=20, pady=3)
    else:
        tk.Label(
            items_frame,
            text="Aucun objet",
            font=("Verdana", 11),
            bg="#fff9ec"
        ).pack(pady=20)



class ShopWindow:
    def __init__(self, title, button_texts):
        self.window = tk.Toplevel(window)
        self.window.title(title)
        self.window.geometry(f"{WINDOW_WIDTH_SHOP}x{WINDOW_HEIGHT_SHOP}")

        # Display money
        self.window.configure(bg=COLOR_LIGHT_BG_CREAM)

        self.money_label = tk.Label(self.window, text=f"💰 Argent : {money} deullars", font=FONT_WINDOW_SMALL, bg=COLOR_LIGHT_BG_CREAM)
        self.money_label.pack(pady=10)

        tk.Label(self.window, text=f"🏪 Bienvenue chez le {title}", font=FONT_WINDOW_TITLE, bg=COLOR_LIGHT_BG_CREAM).pack(pady=10)

        frame = tk.Frame(self.window, bg=COLOR_LIGHT_BG_CREAM)
        frame.pack(pady=5)

        for text in button_texts:
            item_name, cost = text.split(" : ")
            cost = int(cost)
            btn = tk.Button(
                frame,
                text=f"{item_name} - {cost} 💰",
                font=FONT_WINDOW_TINY,
                width=40,
                bg="#f0e6d6",
                command=lambda t=item_name, c=cost: self.handle_purchase(t, c)
            )
            btn.pack(pady=4)


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


def format_selected_items_display(items_list):
    """Format the selected items display with counts (e.g., 'Potion x2, Épée x1')"""
    if not items_list:
        return "Aucun \u00e9l\u00e9ment s\u00e9lectionn\u00e9"
    
    # Count occurrences of each item
    item_counts = {}
    for item in items_list:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    # Format as "Item x count"
    formatted_items = [f"{item} x{count}" if count > 1 else item for item, count in item_counts.items()]
    return ", ".join(formatted_items)

def get_fusion_recipe(selected_items_list):
    """
    Find a fusion recipe that matches the selected items.
    Tries both frozenset (original format) and sorted tuple approaches.
    """
    if not selected_items_list:
        return None
    
    # Try frozenset first (original recipe format)
    try:
        recipe_key = frozenset(selected_items_list)
        if recipe_key in fusion_recipes:
            return fusion_recipes[recipe_key]
    except:
        pass
    
    # Try sorted tuple (supports duplicates like Potion x2)
    try:
        recipe_key = tuple(sorted(selected_items_list))
        # Check if any frozenset in fusion_recipes matches when converted to sorted tuple
        for key, value in fusion_recipes.items():
            if isinstance(key, (frozenset, set)):
                if tuple(sorted(key)) == recipe_key:
                    return value
    except:
        pass
    
    return None

def toggle_item_display(item_name, display_label):
    if item_name in selected_items:
        selected_items.remove(item_name)
    else:
        selected_items.append(item_name)
    display_label.config(text=format_selected_items_display(selected_items))

def handle_fusion(display_label, result_label, items_frame):
    global fusion_results
    
    # Get the recipe using the flexible matching function
    recipe = get_fusion_recipe(selected_items)
    
    if recipe is None:
        result_label.config(
            text="Échec de la fusion : combinaison inconnue.",
            fg="red"
        )
        selected_items.clear()
        display_label.config(text=format_selected_items_display(selected_items))
        return
    
    # If the recipe is a dictionary with a "result", it's a skill fusion
    if isinstance(recipe, dict) and "result" in recipe:
        result = recipe["result"]
        is_skill = not recipe.get("consumable", False) and not recipe.get("enchanted", False)

        if is_skill and result in fusion_results:
            result_label.config(
                text="Fusion existe déjà !",
                fg="orange"
            )
            selected_items.clear()
            display_label.config(text=format_selected_items_display(selected_items))
            return
        
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

    # Effacer de la sélection les éléments
    selected_items.clear()
    display_label.config(text=format_selected_items_display(selected_items))


# Fenêtre de création de compétences
def open_skills_creation_window():
    global selected_items
    selected_items.clear()  # Clear any previous selections
    
    skills_window = tk.Toplevel()
    skills_window.title("Création des compétences")
    skills_window.geometry(f"{WINDOW_WIDTH_SKILLS}x{WINDOW_HEIGHT_SKILLS}")
    skills_window.transient(window)
    skills_window.grab_set()
    skills_window.focus_set()

    skills_window.configure(bg=COLOR_LIGHT_BG_BLUE)
    tk.Label(skills_window, text="🔮 Création des compétences", font=("Verdana", 14, "bold"), bg="#eef7ff").pack(pady=20)

    # Selection display
    display_label = tk.Label(skills_window, text=format_selected_items_display(selected_items), font=("Verdana", 12), wraplength=500)
    display_label.pack(pady=10)

    # Clear button
    clear_button = tk.Button(
        skills_window,
        text="Effacer la sélection",
        font=("Verdana", 10),
        command=lambda: (selected_items.clear(), display_label.config(text=format_selected_items_display(selected_items)), refresh_grid())
    )
    clear_button.pack(pady=5)

    # Scrollable area for items
    scroll_area = tk.Frame(skills_window)
    scroll_area.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(scroll_area, bg="#eef7ff", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_area, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#eef7ff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_grid():
        """Refresh the item grid display"""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Count available items (unique items only)
        available_items = {}
        for item in purchased_items:
            available_items[item] = available_items.get(item, 0) + 1
        
        # Count currently selected items
        selected_item_counts = {}
        for item in selected_items:
            selected_item_counts[item] = selected_item_counts.get(item, 0) + 1
        
        # Categorize items by unique name
        categories = {
            "🗡️ Armes & équipement": [],
            "🔮 Magies & techniques": [],
            "✨ Objets enchantés": [],
            "🧪 Consommables": []
        }

        for item in sorted(set(purchased_items)):  # Use set to get unique items
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
                    break

        # Display categorized items with +/- buttons and counts
        for category, items in categories.items():
            if items:
                tk.Label(scrollable_frame, text=category, font=("Verdana", 11, "bold"), bg="#eef7ff").pack(pady=(10, 0), anchor="w", padx=10)

                category_frame = tk.Frame(scrollable_frame, bg="#eef7ff")
                category_frame.pack(pady=5, fill="x", padx=10)

                for i, item in enumerate(items):
                    available_count = available_items.get(item, 0)
                    selected_count = selected_item_counts.get(item, 0)
                    
                    item_frame = tk.Frame(category_frame, bg="#fff7f0", relief=tk.RAISED, bd=1)
                    item_frame.grid(row=i // 2, column=(i % 2) * 2, padx=5, pady=5, sticky="ew", columnspan=2)
                    
                    # Item name with available count
                    item_display = f"{item}  (Disponible: {available_count})"
                    tk.Label(item_frame, text=item_display, font=("Verdana", 10), bg="#fff7f0", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
                    
                    # Minus button
                    tk.Button(
                        item_frame,
                        text="−",
                        font=("Verdana", 12, "bold"),
                        width=3,
                        bg="#ffcccc",
                        command=lambda i=item: (selected_items.remove(i) if i in selected_items else None, display_label.config(text=format_selected_items_display(selected_items)))
                    ).pack(side=tk.LEFT, padx=2, pady=5)
                    
                    # Plus button - only enabled if we have more available
                    def make_add_command(item_name, avail_count):
                        def add_item():
                            # Recalculate current selected count dynamically (not from cached value)
                            current_selected = sum(1 for item in selected_items if item == item_name)
                            if current_selected < avail_count:
                                selected_items.append(item_name)
                                display_label.config(text=format_selected_items_display(selected_items))
                            else:
                                messagebox.showwarning("Limite atteinte", f"Vous ne pouvez pas sélectionner plus de {avail_count} {item_name}(s).")
                        return add_item
                    
                    plus_button = tk.Button(
                        item_frame,
                        text="+",
                        font=("Verdana", 12, "bold"),
                        width=3,
                        bg="#ccffcc",
                        command=make_add_command(item, available_count)
                    )
                    plus_button.pack(side=tk.LEFT, padx=2, pady=5)

    # Initial grid refresh
    refresh_grid()

    # Bottom panel for result and fusion button
    bottom_frame = tk.Frame(skills_window, bg="#eef7ff")
    bottom_frame.pack(pady=10, fill=tk.X)

    result_label = tk.Label(bottom_frame, text="", font=("Verdana", 12), wraplength=600)
    result_label.pack(pady=5)

    fusion_button = tk.Button(
        bottom_frame,
        text="🔥 Fusionner",
        font=("Verdana", 16, "bold"),
        bg="#ffaa00",
        command=lambda: (handle_fusion(display_label, result_label, scrollable_frame), refresh_grid())
    )
    fusion_button.pack(pady=5)

def open_rpg_ui_map_window():
    map_window = tk.Toplevel(window)
    map_window.title("Carte du monde")
    map_window.geometry(f"{WINDOW_WIDTH_MAP}x{WINDOW_HEIGHT_MAP}")
    map_window.configure(bg=COLOR_LIGHT_BG_SOFT)
    map_window.transient(window)
    map_window.grab_set()
    map_window.focus_set()

    tk.Label(map_window, text="🗺️ Carte du monde", font=("Verdana", 14, "bold"), bg="#fffaf0").pack(pady=10)

    canvas = tk.Canvas(map_window, width=800, height=500, bg="#e0d8c3", highlightthickness=0)
    canvas.pack(pady=10)

    canvas.create_rectangle(0, 0, 800, 500, fill="#c2e0ff")
    canvas.create_oval(100, 100, 300, 300, fill="#9be58c")

    locations = [
        {"name": "Village d'Audébu'", "x": 200, "y": 200},
        {"name": "Forêt mystique", "x": 400, "y": 150},
        {"name": "Votre campement", "x": 450, "y": 200},
        {"name": "Donjon ancien", "x": 600, "y": 300},
    ]

    def go_to_location(location):
        messagebox.showinfo("Voyage", f"Vous voyagez vers {location['name']} !")

    for loc in locations:
        btn = tk.Button(canvas, text=loc["name"], bg="white", command=lambda l=loc: go_to_location(l))
        canvas.create_window(loc["x"], loc["y"], window=btn)

    tk.Button(map_window, text="Fermer la carte", font=("Verdana", 12), command=map_window.destroy).pack(pady=10)

def open_rpg_quests_window():
    quests_window = tk.Toplevel(window)
    quests_window.title("📜 Quêtes")
    quests_window.geometry(f"{WINDOW_WIDTH_QUESTS}x{WINDOW_HEIGHT_QUESTS}")
    quests_window.configure(bg=COLOR_LIGHT_BG_SOFT)
    quests_window.transient(window)
    quests_window.grab_set()
    quests_window.focus_set()

    tk.Label(quests_window, text="📜 Journal de quêtes", font=("Verdana", 14, "bold"), bg="#fffaf0").pack(pady=10)

    categories = {}
    for quest in quests:
        if not quest["completed"]:  # only show unfinished quests
            cat = quest.get("category", "Divers")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(quest)

    # Display quests per category
    for cat, qlist in categories.items():
        tk.Label(quests_window, text=cat, font=("Verdana", 12, "bold"), bg="#fffaf0").pack(pady=(15, 5), anchor="w", padx=20)
        for quest in qlist:
            tk.Button(
                quests_window,
                text=quest["title"],
                font=("Verdana", 11),
                width=50,
                anchor="w",
                command=lambda q=quest: open_quests_dialogue(q)
            ).pack(pady=2, padx=40, anchor="w")

def complete_quest_choice(quest, choice, dialogue_win, parent_window):
    global money

    if "reward" in choice:
        reward = choice["reward"]
        money += reward.get("money", 0)
        player_xp["global"] += reward.get("xp", 0)
    if "penalty" in choice:
        penalty = choice["penalty"]
        money -= penalty.get("money", 0)
        player_xp["global"] -= penalty.get("xp", 0)

    quest["completed"] = True

    # Create a larger result window instead of messagebox
    result_window = tk.Toplevel(parent_window)
    result_window.title("📜 Résultat de la quête")
    result_window.geometry("600x450")
    result_window.configure(bg="#fffaf0")
    result_window.transient(parent_window)
    result_window.grab_set()
    result_window.focus_set()

    # Title
    tk.Label(result_window, text="✅ Quête complétée !", font=("Verdana", 16, "bold"), bg="#fffaf0", fg="green").pack(pady=20)

    # Quest title
    tk.Label(result_window, text=quest["title"], font=("Verdana", 13, "bold"), bg="#fffaf0").pack(pady=10)

    # Choice made
    tk.Label(result_window, text=f"Vous avez choisi :\n{choice['text']}", font=("Verdana", 11, "italic"), bg="#fffaf0", wraplength=550).pack(pady=10, padx=20)

    # Build result text
    if "result_dialogues" in choice:
        msg = "\n".join(choice["result_dialogues"])
        tk.Label(result_window, text=msg, font=("Verdana", 10), bg="#fffaf0", wraplength=550, justify="left").pack(pady=15, padx=20)
    else:
        # Build rewards/penalties text
        rewards_text = ""
        if "reward" in choice:
            reward = choice["reward"]
            rewards_text += f"✅ Récompenses :\n"
            if reward.get("money", 0) > 0:
                rewards_text += f"  💰 +{reward.get('money', 0)} deullars\n"
            if reward.get("xp", 0) > 0:
                rewards_text += f"  ✨ +{reward.get('xp', 0)} XP\n"
        
        if "penalty" in choice:
            penalty = choice["penalty"]
            rewards_text += f"❌ Pénalités :\n"
            if penalty.get("money", 0) > 0:
                rewards_text += f"  💰 -{penalty.get('money', 0)} deullars\n"
            if penalty.get("xp", 0) > 0:
                rewards_text += f"  ✨ -{penalty.get('xp', 0)} XP\n"

        if rewards_text:
            tk.Label(result_window, text=rewards_text, font=("Verdana", 10), bg="#fffaf0", justify="left").pack(pady=15, padx=20, anchor="w")

    # Close button
    def close_and_refresh():
        result_window.destroy()
        dialogue_win.destroy()
        update_main_window()
        save_game()
        # Refresh quests window if it exists
        for w in parent_window.winfo_children():
            if isinstance(w, tk.Toplevel) and w.title() == "📜 Quêtes":
                w.destroy()
                open_rpg_quests_window()
                break

    tk.Button(
        result_window,
        text="Fermer",
        font=("Verdana", 12),
        bg="#dcecf5",
        command=close_and_refresh
    ).pack(pady=20)


def open_quests_dialogue(quest):
    dialogue_win = tk.Toplevel(window)
    dialogue_win.title(quest["title"])
    dialogue_win.geometry("600x400")
    dialogue_win.configure(bg="#fffaf0")
    dialogue_win.transient(window)
    dialogue_win.grab_set()
    dialogue_win.focus_set()

    dialogue_label = tk.Label(dialogue_win, text="", font=("Verdana", 12), wraplength=550, bg="#fffaf0", justify="left")
    dialogue_label.pack(pady=20)

    next_button = tk.Button(dialogue_win, text="➡️ Suivant", font=("Verdana", 11))
    next_button.pack(pady=10)

    state = {"index": 0}

    def show_next():
        if state["index"] < len(quest["dialogues"]):
            dialogue_label.config(text=quest["dialogues"][state["index"]])
            state["index"] += 1
        else:
            # End of dialogues → show choices
            next_button.destroy()
            show_choices()

    def show_choices():
        tk.Label(dialogue_win, text="Que voulez-vous faire ?", font=("Verdana", 12, "bold"), bg="#fffaf0").pack(pady=10)

        has_option = False
        for choice in quest["choices"]:
            can_do = False
            if "skill" in choice["requirement"] and choice["requirement"]["skill"] in fusion_results:
                can_do = True
            if "item" in choice["requirement"] and choice["requirement"]["item"] in purchased_items:
                can_do = True
            if "none" in choice["requirement"]:
                can_do = True

            if can_do:
                has_option = True
                tk.Button(
                    dialogue_win,
                    text=choice["text"],
                    font=("Verdana", 11),
                    wraplength=500,
                    command=lambda c=choice, q=quest, w=dialogue_win: complete_quest_choice(q, c, w, window)
                ).pack(pady=5, fill="x", padx=20)

        if not has_option:
            tk.Label(dialogue_win, text="❌ Vous n'avez pas encore les compétences ou objets requis.", font=("Verdana", 10, "italic"), bg="#fffaf0").pack(pady=10)

    next_button.config(command=show_next)
    show_next()  # show first dialogue


def open_rpg_ui_window():
    global last_combat_result


    # --- RPG Combat Window Redesign ---
    rpg_window = tk.Toplevel(window)
    rpg_window.title("⚔️ Combat RPG")
    rpg_window.geometry(f"{WINDOW_WIDTH_COMBAT}x{WINDOW_HEIGHT_COMBAT}")
    rpg_window.configure(bg=COLOR_COMBAT_BG)
    rpg_window.transient(window)
    rpg_window.grab_set()
    rpg_window.focus_set()

    main_frame = tk.Frame(rpg_window, bg=COLOR_COMBAT_BG)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Left: Player Panel
    left_frame = tk.Frame(main_frame, bg=COLOR_COMBAT_BG, bd=2, relief=tk.GROOVE)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Right: Enemy Panel
    right_panel = tk.Frame(main_frame, bg=COLOR_COMBAT_BG, bd=2, relief=tk.GROOVE)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Center: Combat Log and Actions
    center_frame = tk.Frame(main_frame, bg=COLOR_COMBAT_STATUS_BG, bd=2, relief=tk.RIDGE)
    center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=650)

    # --- Player Section ---
    player_title = tk.Label(left_frame, text="🧑 Joueur", font=FONT_COMBAT_TITLE, fg=COLOR_COMBAT_GREEN, bg=COLOR_COMBAT_BG)
    player_title.pack(pady=10)
    # Placeholder for portrait
    player_portrait = tk.Label(left_frame, text="[Portrait]", font=FONT_WINDOW_SMALL, fg=COLOR_COMBAT_GRAY, bg=COLOR_COMBAT_BG, width=12, height=6, relief=tk.RIDGE)
    player_portrait.pack(pady=5)

    bars_frame = tk.Frame(left_frame, bg=COLOR_COMBAT_BG)
    bars_frame.pack(pady=10)

    # --- Enemy Section ---
    enemy_title = tk.Label(right_panel, text="👹 Ennemi", font=FONT_COMBAT_TITLE, fg=COLOR_COMBAT_RED, bg=COLOR_COMBAT_BG)
    enemy_title.pack(pady=10)
    enemy_portrait = tk.Label(right_panel, text="[Portrait]", font=FONT_WINDOW_SMALL, fg=COLOR_COMBAT_GRAY, bg=COLOR_COMBAT_BG, width=12, height=6, relief=tk.RIDGE)
    enemy_portrait.pack(pady=5)

    enemy_bars_frame = tk.Frame(right_panel, bg="#23272e")
    enemy_bars_frame.pack(pady=10)

    # --- Status Section ---
    status_frame = tk.Frame(center_frame, bg="#181a20")
    status_frame.pack(pady=5, fill="x")

    player_status_text = None
    enemy_status_text = None

    # Close handler: mark combat as lost so next fight starts penalized
    def on_combat_close():
        if messagebox.askyesno("Quitter le combat",
                           "⚠️ Êtes-vous sûr de vouloir fuir ?\n"
                           "Vous perdrez automatiquement ce combat."):
            last_combat_result["lost"] = True
            messagebox.showinfo("Défaite", "Vous avez fui le combat et perdu la bataille...")
            rpg_window.destroy()

    rpg_window.protocol("WM_DELETE_WINDOW", on_combat_close)

    # Determine starting values (apply penalty if last combat was lost / escaped)
    if last_combat_result.get("lost", False):
        start_hp = max(1, int(player_stats["max_hp"] * 0.25))
        start_mana = max(0, int(player_stats["max_mana"] * 0.25))
        start_fatigue = int(player_stats["max_fatigue"] * 0.8)
        last_combat_result["lost"] = False
    else:
        start_hp = player_stats["max_hp"]
        start_mana = player_stats["max_mana"]
        start_fatigue = 0

    def update_status_display():
        if not rpg_window.winfo_exists():
            return
        def format_status(status_dict):
            if not status_dict:
                return "Aucun"
            lines = []
            for effect, data in status_dict.items():
                dur = data.get("duration", "?")
                if effect == "poison":
                    lines.append(f"☠️ Poison ({data['damage_per_turn']}/tour, {dur} tours)")
                elif effect == "burn":
                    lines.append(f"🔥 Brûlure ({data['damage_per_turn']}/tour, {dur} tours)")
                elif effect == "stun":
                    lines.append(f"💫 Étourdi ({dur} tours)")
                elif effect == "dodge":
                    lines.append(f"💨 Esquive ({dur} tours)")
                elif effect == "damage_reduction":
                    lines.append(f"🛡️ Réduction de dégâts ({dur} tours)")
                elif effect == "parade_stance":
                    lines.append(f"🪞 Parade parfaite ({dur} tours)")
                elif effect == "accuracy_down":
                    lines.append(f"🎯 Précision réduite ({dur} tours)")
                else:
                    lines.append(f"❓ {effect} ({dur} tours)")
            return "\n".join(lines)

        if player_status_text.winfo_exists():
            player_status_text.config(text=format_status(player_status_effects))
        if enemy_status_text.winfo_exists():
            enemy_status_text.config(text=format_status(enemy_status_effects))



    tk.Label(status_frame, text="🧍 Statuts joueur : ", font=("Verdana", 10, "bold"), fg="#00ff99", bg="#181a20", anchor="w", justify="left").pack(fill="x", padx=10)
    player_status_text = tk.Label(status_frame, text="", font=("Verdana", 9), fg="#cccccc", bg="#181a20", anchor="w", justify="left")
    player_status_text.pack(fill="x", padx=20)

    tk.Label(status_frame, text="👹 Statuts ennemi : ", font=("Verdana", 10, "bold"), fg="#ff5555", bg="#181a20", anchor="w", justify="left").pack(fill="x", padx=10)
    enemy_status_text = tk.Label(status_frame, text="", font=("Verdana", 9), fg="#cccccc", bg="#181a20", anchor="w", justify="left")
    enemy_status_text.pack(fill="x", padx=20)


    def show_floating_text(parent, text, color="red", duration=800):
        floating = tk.Label(parent, text=text, fg=color, font=("Verdana", 14, "bold"))
        floating.place(x=100, y=100)
        dy = -2
        steps = duration // 50

        def animate(step=0):
            if step < steps:
                floating.place_configure(y=100 + dy * step)
                floating.after(50, animate, step + 1)
            else:
                floating.destroy()
        animate()

    # --- Skills Frame for skills display ---
    if hasattr(open_rpg_ui_window, "skills_frame"):
        try:
            open_rpg_ui_window.skills_frame.destroy()
        except Exception:
            pass
    skills_frame = tk.Frame(center_frame, bg="#23272e")
    skills_frame.pack(pady=5, fill="x")
    open_rpg_ui_window.skills_frame = skills_frame

    def update_skills_display():
        for widget in skills_frame.winfo_children():
            widget.destroy()

        tk.Label(skills_frame, text="Compétences disponibles", font=("Verdana", 12, "bold"), fg="#44ccff", bg="#23272e").pack(pady=5)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("enchanted", False):
                        continue
                    if val.get("consumable", False):
                        break
                    frame = tk.Frame(skills_frame, bd=1, relief=tk.SOLID, bg="#23272e")
                    frame.pack(pady=3, fill=tk.X)
                    tk.Label(frame, text=fusion, font=("Verdana", 10, "bold"), fg="#eeeeee", bg="#23272e").pack(anchor="w")
                    tk.Label(frame, text=f"Dégâts: {val.get('damage', 0)}", font=("Verdana", 9), fg="#cccccc", bg="#23272e").pack(anchor="w")
                    tk.Label(frame, text=f"Coût: {val.get('mana_cost', 0)} mana, {val.get('fatigue_cost', 0)} fatigue", font=("Verdana", 9), fg="#cccccc", bg="#23272e").pack(anchor="w")
                    tk.Button(frame, text="Utiliser", font=("Verdana", 9), bg="#4444ff", fg="#fff", activebackground="#222288", command=lambda v=val: use_skill(v)).pack(pady=2)

        tk.Label(skills_frame, text="Objets disponibles", font=("Verdana", 12, "bold"), fg="#ffaa00", bg="#23272e").pack(pady=5)
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
            if "damage_per_turn" in data:
                enemy_hp["value"] -= data["damage_per_turn"]
                log_message(f"🔥 {current_enemy['name']} subit {data['damage_per_turn']} dégâts de {effect}.")
                show_floating_text(rpg_window, data['damage_per_turn'], "orange")
        
            data["duration"] -= 1
            if data["duration"] <= 0:
                to_remove.append(effect)

        for effect in to_remove:
            del enemy_status_effects[effect]


    def start_next_fight():
        # check victory condition
        if fight_counter["count"] >= 5:
            messagebox.showinfo("Victoire !", "🎉 Vous avez vaincu 5 monstres et réussi à vous échapper du donjon !")
            rpg_window.destroy()
            return

        # increment the counter once and grant XP for subsequent fights
        fight_counter["count"] += 1
        if fight_counter["count"] > 1:
            xp_gain = 50
            player_xp["global"] += xp_gain
            log_message(f"🏆 Vous gagnez {xp_gain} points d'expérience globale !")

        enemy_type = random.choices(enemy_types, weights=[e['weight'] for e in enemy_types])[0]
        current_enemy.update(enemy_type)
        enemy_hp["value"] = enemy_type.get("hp", 100)
        enemy_status_effects.clear()

        update_bars()
        update_status_display()
        log_message(f"⚔️ Combat {fight_counter['count']} commencé contre {current_enemy['name']} !")
        update_skills_display()


    def create_bar(label_text, color, max_value=100, parent=None):
        if parent is None:
            parent = bars_frame
        container = tk.Frame(parent, bg="#23272e")
        container.pack(pady=5)
        label = tk.Label(container, text=label_text, font=("Verdana", 10, "bold"), fg=color, bg="#23272e")
        label.pack(side=tk.LEFT, padx=5)
        width = max(200, int(max_value * 1.5))
        canvas = tk.Canvas(container, width=width, height=20, bg="#181a20", highlightthickness=0)
        canvas.pack(side=tk.LEFT)
        bar = canvas.create_rectangle(0, 0, width, 20, fill=color)
        value_label = tk.Label(container, text=f"{max_value}/{max_value}", font=("Verdana", 10), fg="#cccccc", bg="#23272e")
        value_label.pack(side=tk.LEFT, padx=5)
        return canvas, bar, value_label, width


    # initialize player/enemy values from computed starts (do NOT overwrite later)
    fight_counter = {"count": 0}
    player_hp = {"value": start_hp}
    player_mana = {"value": start_mana}
    player_fatigue = {"value": start_fatigue}
    enemy_hp = {"value": 0}
    current_enemy = {"name": "", "resistances": {}, "damage_range": (5, 15), "hp": 100}

    # create bars AFTER start values to get widths using max stats

    player_hp_canvas, player_hp_bar, player_hp_label, player_hp_width = create_bar("Santé", "#00ff99", player_stats["max_hp"], parent=bars_frame)
    mana_canvas, mana_bar, mana_label, mana_width = create_bar("Mana", "#3399ff", player_stats["max_mana"], parent=bars_frame)
    fatigue_canvas, fatigue_bar, fatigue_label, fatigue_width = create_bar("Fatigue", "#ffaa00", player_stats["max_fatigue"], parent=bars_frame)
    enemy_hp_canvas, enemy_hp_bar, enemy_hp_label, enemy_hp_width = create_bar("Santé", "#ff5555", 100, parent=enemy_bars_frame)



    log_text = tk.Text(center_frame, height=15, width=56, state=tk.DISABLED, bg="#181a20", fg="#eeeeee", font=("Consolas", 11), relief=tk.FLAT)
    log_text.pack(pady=10)

    def check_player_defeat(fight_window):
        if player_hp["value"] <= 0:
            player_hp["value"] = 0
            last_combat_result["lost"] = True
            messagebox.showinfo("💀 Défaite", "Vous vous évanouissez au milieu du donjon...")
            fight_window.destroy()
            return True
        return False

    def update_bars():
        def set_bar(canvas, bar, label, value, max_value, width):
            percent = max(min(value / max_value, 1), 0) if max_value > 0 else 0
            canvas.coords(bar, 0, 0, width * percent, 20)
            label.config(text=f"{value}/{max_value}")
        set_bar(player_hp_canvas, player_hp_bar, player_hp_label,
                player_hp["value"], player_stats["max_hp"], player_hp_width)
        set_bar(enemy_hp_canvas, enemy_hp_bar, enemy_hp_label,
                enemy_hp["value"], current_enemy.get("hp", 100), enemy_hp_width)
        set_bar(mana_canvas, mana_bar, mana_label,
                player_mana["value"], player_stats["max_mana"], mana_width)
        set_bar(fatigue_canvas, fatigue_bar, fatigue_label,
                player_fatigue["value"], player_stats["max_fatigue"], fatigue_width)

        update_item_display()


    def log_message(message, flash=False):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)


    def set_state_all_buttons_in(widget, state):
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                child.config(state=state)
            else:
                set_state_all_buttons_in(child, state)

    def disable_all_actions():
        attack_button.config(state="disabled")
        set_state_all_buttons_in(center_frame, "disabled")
        set_state_all_buttons_in(skills_frame, "disabled")

    def enable_all_actions():
        attack_button.config(state="normal")
        set_state_all_buttons_in(center_frame, "normal")
        set_state_all_buttons_in(skills_frame, "normal")


    def enemy_attack():
        # use the outer check_player_defeat so losses are recorded
        # gestion effets
        if "dodge" in player_status_effects:
            if player_status_effects["dodge"]["duration"] > 0:
                log_message("💨 Vous esquivez l'attaque de l'ennemi !")
                player_status_effects["dodge"]["duration"] -= 1
                if player_status_effects["dodge"]["duration"] <= 0:
                    del player_status_effects["dodge"]
                return
        if "stun" in enemy_status_effects:
            if enemy_status_effects["stun"]["duration"] > 0:
                log_message(f"😵 {current_enemy['name']} est trop étourdi pour attaquer !")
                enemy_status_effects["stun"]["duration"] -= 1
                if enemy_status_effects["stun"]["duration"] <= 0:
                    del enemy_status_effects["stun"]
                return
        if "accuracy_down" in enemy_status_effects:
            acc = enemy_status_effects["accuracy_down"]
            if random.random() < acc["chance_to_miss"]:
                log_message(f"💫 {current_enemy['name']} rate son attaque !")
                acc["duration"] -= 1
                if acc["duration"] <= 0:
                    del enemy_status_effects["accuracy_down"]
                return
            else:
                acc["duration"] -= 1
                if acc["duration"] <= 0:
                    del enemy_status_effects["accuracy_down"]

        process_status_effects()
        if enemy_hp["value"] <= 0:
            return
        damage = random.randint(*current_enemy["damage_range"])
        if "damage_reduction" in player_status_effects:
            dr = player_status_effects["damage_reduction"]
            damage = int(damage * dr["reduction_factor"])
            dr["duration"] -= 1
            log_message(f"🛡️ Réduction des dégâts active ! Les dégâts sont réduits à {damage}.")
            if dr["duration"] <= 0:
                del player_status_effects["damage_reduction"]
        
        damage = random.randint(*current_enemy["damage_range"])

        if "parade_stance" in player_status_effects:
            effect = player_status_effects["parade_stance"]
    
            reflected_damage = damage
            player_hp_blocked = damage 
            player_hp["value"] -= 0  

            enemy_hp["value"] -= reflected_damage

            log_message(f"🛡️ Parade parfaite ! Vous bloquez {player_hp_blocked} dégâts et les renvoyez à {current_enemy['name']}.")

            effect["duration"] -= 1
            if effect["duration"] <= 0:
                del player_status_effects["parade_stance"]
            update_bars()
            update_status_display()
            return

        log_message(f"⚠️ {current_enemy['name']} vous inflige {damage} de dégâts.")
        show_floating_text(rpg_window, damage, "red")
        player_hp["value"] -= damage
        if check_player_defeat(rpg_window):
            return
        update_bars()
        update_status_display()

    def use_skill(skill_data):
        disable_all_actions()
        if player_mana["value"] < skill_data["mana_cost"] or player_fatigue["value"] + skill_data["fatigue_cost"] > 100:
            messagebox.showwarning("Pas assez de ressources", "Pas assez de mana ou trop de fatigue.")
            enable_all_actions()
            return

        base_damage = skill_data["damage"]
        modifier = 1.0
        element = skill_data["element"]
        damage_type = skill_data["damage_type"]
        if element == "water" and "burn" in enemy_status_effects:
            del enemy_status_effects["burn"]
            log_message(f"💧 L'eau éteint les flammes de {current_enemy['name']} !")


        # Effets
        if "effect" in skill_data:
            effect = skill_data["effect"]
            target = effect.get("target")
            if effect["type"] == "stun" and target == "enemy":
                enemy_status_effects["stun"] = {"duration": effect["duration"]}
                log_message(f"😵 {current_enemy['name']} est étourdi pour {effect['duration']} tour(s) !")
            elif effect["type"] == "poison" and target == "enemy":
                apply_status_effect("poison", enemy_status_effects,
                                    duration=effect["duration"],
                                    damage_per_turn=effect["damage_per_turn"],
                                    element=effect.get("element", "unknown"))
                log_message(f"☠️ {current_enemy['name']} est empoisonné !")
            elif effect["type"] == "dodge" and target == "player":
                player_status_effects["dodge"] = {"duration": effect["duration"]}
                log_message("💨 Vous êtes prêt à esquiver la prochaine attaque !")
            elif effect["type"] == "parade_stance" and target == "player":
                player_status_effects["parade_stance"] = {
                    "duration": effect.get("duration", 1)
                }
                log_message("🛡️ Vous adoptez une posture de parade parfaite.")
            elif effect["type"] == "accuracy_down" and target == "enemy":
                duration = random.randint(*effect.get("duration_range", [2, 4]))
                enemy_status_effects["accuracy_down"] = {
                    "duration": duration,
                    "chance_to_miss": effect.get("chance_to_miss", 0.5)
                }
                log_message(f"🎯 {current_enemy['name']} est désorienté et pourrait rater ses attaques pendant {duration} tours !")


        # XP
        if skill_data["damage_type"] == "magic":
            player_xp["magic"] += 10
            log_message("✨ Vous gagnez 10 XP magique.")
        elif skill_data["damage_type"] in ["slashing", "piercing", "contondant"]:
            player_xp["force"] += 10
            log_message("💪 Vous gagnez 10 XP de force.")

        # Résistances/faiblesses
        if element in current_enemy.get("resistances", {}):
            modifier *= current_enemy["resistances"][element]
            log_message(f"{current_enemy['name']} résiste à l'élément {element}.")
        elif element in current_enemy.get("weaknesses", {}):
            modifier *= current_enemy["weaknesses"][element]
            log_message(f"{current_enemy['name']} est faible face à l'élément {element} !")
        elif damage_type in current_enemy.get("resistances", {}):
            modifier *= current_enemy["resistances"][damage_type]
            log_message(f"{current_enemy['name']} résiste au type {damage_type}.")
        elif damage_type in current_enemy.get("weaknesses", {}):
            modifier *= current_enemy["weaknesses"][damage_type]
            log_message(f"{current_enemy['name']} est faible face au type {damage_type} !")

        actual_damage = int(base_damage * modifier)

        log_message(f"🌀 Vous utilisez : {skill_data['result']}")
        log_message(f"{skill_data['description']}")
        log_message(f"💥 Vous infligez {actual_damage} points de dégâts à {current_enemy['name']} !")

        if modifier > 1.0:
            log_message("✅ L'attaque est très efficace !")
        elif modifier < 1.0:
            log_message("❌ L'attaque est peu efficace...")

        enemy_hp["value"] -= actual_damage
        player_mana["value"] -= skill_data["mana_cost"]
        player_fatigue["value"] += skill_data["fatigue_cost"]
        if skill_data["element"] == "fire":
            apply_status_effect("burn", enemy_status_effects, duration=3, damage_per_turn=5, element="fire")
            log_message(f"🔥 {current_enemy['name']} est en feu !")

        def continue_after_delay():
            global money
            if enemy_hp["value"] <= 0:
                log_message(f"✅ {current_enemy['name']} vaincu !")
                reward = current_enemy.get("bounty", 0)
                money += reward
                log_message(f"💰 Vous gagnez {reward} deullars en battant {current_enemy['name']} !")
                update_main_window()

                start_next_fight()
                update_status_display()
                enable_all_actions()
            else:
                log_message("⏳ L'ennemi se prépare à attaquer...")
                rpg_window.after(2000, enemy_attack)
                rpg_window.after(2500, enable_all_actions)
            update_bars()
            update_status_display()

        rpg_window.after(1000, continue_after_delay)

    item_frames = []

    def update_item_display():
        for frame in item_frames:
            frame.destroy()
        item_frames.clear()

        # --- Stack items by count ---
        from collections import Counter
        all_items = list(purchased_items)
        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("enchanted", False):
                        continue
                    if val.get("consumable", False):
                        if fusion not in all_items:
                            all_items.append(fusion)

        item_counts = Counter(all_items)
        unique_items = sorted(item_counts.keys())

        for item in unique_items:
            if item in itemshop_items or item in fusion_results:
                frame = tk.Frame(center_frame, bd=1, relief=tk.SOLID, bg="#23272e")
                frame.pack(pady=3, fill=tk.X, padx=10)
                item_frames.append(frame)
                # Item name + count
                display_name = f"{item} x{item_counts[item]}" if item_counts[item] > 1 else item
                tk.Label(frame, text=display_name, font=("Verdana", 11, "bold"), fg="#eeeeee", bg="#23272e").pack(side=tk.LEFT, padx=5)
                tk.Button(
                    frame,
                    text="Utiliser sur soi",
                    font=("Verdana", 9),
                    bg="#00ff99", fg="#23272e", activebackground="#00cc77",
                    command=lambda i=item: use_item(i, target="self")
                ).pack(pady=2, side=tk.LEFT, padx=5)
                tk.Button(
                    frame,
                    text="Jeter sur l'ennemi",
                    font=("Verdana", 9),
                    bg="#ff5555", fg="#23272e", activebackground="#cc2222",
                    command=lambda i=item: use_item(i, target="enemy")
                ).pack(pady=2, side=tk.LEFT, padx=5)

    def use_item(item, target="self"):
        disable_all_actions()

        # Check if item is a consumable fusion (from fusion_recipes_lists.py)
        fusion_data = None
        for recipe in fusion_recipes.values():
            if isinstance(recipe, dict) and recipe.get("result") == item and recipe.get("consumable"):
                fusion_data = recipe
                break

        # Remove from inventory if it's a consumable (either purchased or crafted)
        if item in purchased_items:
            purchased_items.remove(item)
        elif not fusion_data:
            log_message(f"❌ Vous ne possédez pas {item}.")
            enable_all_actions()
            return

        # Helper for applying effects
        def apply_consumable_effect():
            # Handle consumable effects defined in fusion_recipes_lists.py
            if fusion_data and "effect" in fusion_data:
                eff = fusion_data["effect"]
                etype = eff["type"]
                tgt = target  # use chosen target

                if etype == "heal":
                    heal_value = eff.get("value", 0)
                    if tgt == "self":
                        player_hp["value"] = min(player_stats["max_hp"], player_hp["value"] + heal_value)
                        log_message(f"🧪 Vous récupérez {heal_value} PV.")
                    else:
                        max_enemy_hp = current_enemy.get("hp", 100)
                        enemy_hp["value"] = min(max_enemy_hp, enemy_hp["value"] + heal_value)
                        log_message(f"Vous soignez {current_enemy['name']} de {heal_value} PV.")
                elif etype == "ressource_refill":
                    value = eff.get("value", 0)
                    if tgt == "self":
                        player_mana["value"] = min(player_stats["max_mana"], player_mana["value"] + value)
                        player_fatigue["value"] = max(0, player_fatigue["value"] - value)
                        log_message(f"🧪 Vous régénérez {value} mana et réduisez votre fatigue de {value}.")
                    else:
                        log_message(f"🤷 Vous jetez {item} sur {current_enemy['name']}... Aucun effet.")
                elif etype == "poison_stun":
                    if tgt == "enemy":
                        apply_status_effect("poison", enemy_status_effects,
                                            duration=eff.get("duration", 0),
                                            damage_per_turn=eff.get("damage_per_turn", 0),
                                            element=eff.get("element", "poison"))
                        enemy_status_effects["stun"] = {"duration": eff.get("stun_duration", 1)}
                        log_message(f"☠️ {current_enemy['name']} est empoisonné et étourdi !")
                    else:
                        apply_status_effect("poison", player_status_effects,
                                            duration=eff.get("duration", 0),
                                            damage_per_turn=eff.get("damage_per_turn", 0),
                                            element=eff.get("element", "poison"))
                        log_message(f"☠️ Vous vous êtes empoisonné et étourdi !")
                elif etype == "damage_reduction":
                    if tgt == "self":
                        player_status_effects["damage_reduction"] = {
                            "duration": eff.get("duration", 1),
                            "reduction_factor": eff.get("reduction_factor", 0.5)
                        }
                        log_message(f"🛡️ Vous bénéficiez d'une réduction de dégâts pendant {eff.get('duration', 1)} attaques !")
                    else:
                        # If you throw it at the enemy, maybe protect them instead
                        enemy_status_effects["damage_reduction"] = {
                            "duration": eff.get("duration", 1),
                            "reduction_factor": eff.get("reduction_factor", 0.5)
                        }
                        log_message(f"🛡️ {current_enemy['name']} bénéficie d'une réduction de dégâts pendant {eff.get('duration', 1)} attaques !")

                else:
                    log_message(f"❓ Effet {etype} non encore géré pour {item}.")
                return True
            return False

        # If the item is a fusion consumable and has an effect, apply it and skip the old hardcoded logic
        if fusion_data and apply_consumable_effect():
            def continue_after_delay():
                enemy_attack()
                update_bars()
                update_status_display()
                rpg_window.after(1500, enable_all_actions)
            rpg_window.after(1000, continue_after_delay)
            return

        # --- Hardcoded fallback for base items ---
        if item == "Potion de soin":
            if target == "self":
                player_hp["value"] = min(player_stats["max_hp"], player_hp["value"] + 25)
                log_message("🧪 Vous buvez une potion de soin et récupérez 25 PV.")
            else:
                max_enemy_hp = current_enemy.get("hp", 100)
                enemy_hp["value"] = min(max_enemy_hp, enemy_hp["value"] + 25)
                log_message(f"Vous lancez une potion de soin sur {current_enemy['name']} et il récupère 25 PV.")
        elif item == "Potion de soin supérieure":
            if target == "self":
                player_hp["value"] = min(player_stats["max_hp"], player_hp["value"] + 50)
                log_message("🧪 Vous buvez une potion de soin supérieure et récupérez 50 PV.")
            else:
                max_enemy_hp = current_enemy.get("hp", 100)
                enemy_hp["value"] = min(max_enemy_hp, enemy_hp["value"] + 50)
                log_message(f"Vous lancez une potion de soin supérieure sur {current_enemy['name']} et il récupère 50 PV.")
        elif item == "Potion de mana":
            if target == "self":
                player_mana["value"] = min(player_stats["max_mana"], player_mana["value"] + 50)
                log_message("🧪 Vous buvez une potion de mana et récupérez 50 de mana.")
            else:
                log_message(f"🤷 Vous jetez une potion de mana sur {current_enemy['name']}. Aucun effet.")
        elif item == "Potion de poison":
            if target == "self":
                player_hp["value"] -= 25
                log_message("☠️ Vous buvez une potion de poison. Vous perdez 25 PV !")
            else:
                enemy_hp["value"] -= 25
                log_message(f"☠️ Vous jetez une potion de poison sur {current_enemy['name']} ! Il perd 25 PV.")
        elif item == "Potion de repos":
            if target == "self":
                player_fatigue["value"] = max(0, player_fatigue["value"] - 50)
                log_message("🧪 Vous buvez une potion de repos et récupérez 50 de fatigue.")
            else:
                log_message(f"🤷 Vous jetez une potion de repos sur {current_enemy['name']}. Aucun effet.")
        elif item == "Bombe légère":
            if target == "enemy":
                enemy_hp["value"] -= 30
                log_message(f"💣 Vous lancez une bombe légère sur {current_enemy['name']} ! Il subit 30 dégâts.")
            else:
                log_message("🤷 Vous vous jetez une bombe légère dessus... Mauvaise idée !")
                player_hp["value"] -= 30
        elif item == "Bombe lourde":
            if target == "enemy":
                enemy_hp["value"] -= 50
                log_message(f"💥 Vous lancez une bombe lourde sur {current_enemy['name']} ! Il subit 50 dégâts.")
                if random.random() < 0.3:
                    enemy_status_effects["stun"] = {"duration": 1}
                    log_message(f"😵 {current_enemy['name']} est étourdi par l'explosion !")
            else:
                log_message("🤯 Vous vous explosez avec une bombe lourde ! Vous subissez 50 dégâts.")
                player_hp["value"] -= 50
        elif item == "Filet":
            if target == "enemy":
                enemy_status_effects["stun"] = {"duration": 2}
                log_message(f"🕸️ Vous piégez {current_enemy['name']} dans un filet ! Il ne pourra pas attaquer pendant 2 tours.")
            else:
                log_message("🤦 Vous vous empêtrer dans votre propre filet. Vous perdez un tour.")
                player_status_effects["stun"] = {"duration": 1}
        else:
            log_message(f"❓ {item} n'a pas encore d'effet implémenté.")

        # Continue combat after item use
        def continue_after_delay():
            enemy_attack()
            update_bars()
            update_status_display()
            rpg_window.after(1500, enable_all_actions)

        rpg_window.after(1000, continue_after_delay)

    def attack():
        disable_all_actions()

        if player_hp["value"] <= 0 or enemy_hp["value"] <= 0:
            enable_all_actions()
            return

        damage = random.randint(5, 15)
        enemy_hp["value"] -= damage
        log_message(f"💥 Vous infligez {damage} de dégâts à {current_enemy['name']}.")

        def continue_after_delay():
            global money
            if enemy_hp["value"] <= 0:
                log_message(f"✅ {current_enemy['name']} vaincu !")
                reward = current_enemy.get("bounty", 0)
                money += reward
                log_message(f"💰 Vous gagnez {reward} deullars en battant {current_enemy['name']} !")
                update_main_window()
                start_next_fight()
                update_status_display()
                enable_all_actions()
            else:
                log_message("⏳ L'ennemi se prépare à attaquer...")
                rpg_window.after(2000, enemy_attack)
                rpg_window.after(2500, enable_all_actions)
            update_bars()
            update_status_display()

        rpg_window.after(1000, continue_after_delay)


    # --- Action Buttons ---
    action_frame = tk.Frame(center_frame, bg="#181a20")
    action_frame.pack(pady=10)
    attack_button = tk.Button(action_frame, text="Attaque basique", font=("Verdana", 13, "bold"), bg="#4444ff", fg="#fff", activebackground="#222288", width=20, command=attack)
    attack_button.pack(pady=5)

    update_skills_display()
    tk.Label(center_frame, text="Objets disponibles", font=("Verdana", 12, "bold"), fg="#ffaa00", bg="#181a20").pack(pady=5)
    update_item_display()

    # start the first fight (will use start_hp/start_mana/start_fatigue)
    start_next_fight()

def open_upgrade_window():
    upgrade_window = tk.Toplevel(window)
    upgrade_window.title("📈 Améliorations")
    upgrade_window.geometry(f"{WINDOW_WIDTH_UPGRADE}x{WINDOW_HEIGHT_UPGRADE}")
    upgrade_window.configure(bg=COLOR_LIGHT_BG_LIGHT)
    upgrade_window.transient(window)
    upgrade_window.grab_set()
    upgrade_window.focus_set()

    tk.Label(upgrade_window, text="📈 Améliorations de personnage", font=("Verdana", 14, "bold"), bg="#f1f1f1").pack(pady=10)

    xp_frame = tk.Frame(upgrade_window, bg="#f1f1f1")
    xp_frame.pack(pady=5)

    def refresh_labels():
        for widget in xp_frame.winfo_children():
            widget.destroy()

        tk.Label(xp_frame, text=f"✨ XP global : {player_xp['global']}", font=("Verdana", 11), bg="#f1f1f1").pack(anchor="w", padx=20)
        tk.Label(xp_frame, text=f"💪 XP force : {player_xp['force']}", font=("Verdana", 11), bg="#f1f1f1").pack(anchor="w", padx=20)
        tk.Label(xp_frame, text=f"🔮 XP magie : {player_xp['magic']}", font=("Verdana", 11), bg="#f1f1f1").pack(anchor="w", padx=20)

    refresh_labels()

    def upgrade(stat, xp_type, cost, amount, display_name):
        if player_xp[xp_type] >= cost:
            player_xp[xp_type] -= cost
            player_stats[stat] += amount

            messagebox.showinfo("Succès", f"{display_name} augmenté de {amount} !")
            refresh_labels()
        else:
            messagebox.showwarning("Erreur", "Pas assez d'expérience !")

    tk.Label(upgrade_window, text="🛠️ Choisissez une amélioration :", font=("Verdana", 12, "bold"), bg="#f1f1f1").pack(pady=10)

    upgrades = [
        ("❤️ Santé Max +10 (XP Global)", "max_hp", "global", 100, 10),
        ("💪 Bonus Force +0.1 (XP Force)", "force_bonus", "force", 100, 0.1),
        ("⚡ Fatigue Max +10 (XP Force)", "max_fatigue", "force", 100, 10),
        ("🔮 Bonus Magie +0.1 (XP Magie)", "magic_bonus", "magic", 100, 0.1),
        ("🌀 Mana Max +10 (XP Magie)", "max_mana", "magic", 100, 10)
    ]

    for label, stat, xp_type, cost, amount in upgrades:
        tk.Button(
            upgrade_window,
            text=f"{label} ({cost} XP)",
            font=("Verdana", 10),
            width=35,
            bg="#dcecf5",
            command=lambda s=stat, x=xp_type, c=cost, a=amount, l=label: upgrade(s, x, c, a, l)
        ).pack(pady=5)

    tk.Button(
        upgrade_window,
        text="Fermer",
        font=("Verdana", 10),
        bg="lightgray",
        command=upgrade_window.destroy
    ).pack(pady=15)


def open_military_window():
    ShopWindow("Entra\u00eeneur militaire", ["Coup simple : 100", "Coup puissant : 250", "Parade : 250"])

def open_magic_window():
    ShopWindow("Ma\u00eetre magicien", ["Magie \u00e9l\u00e9mentaire Feu : 200", "Magie \u00e9l\u00e9mentaire Air : 200", "Magie \u00e9l\u00e9mentaire Eau : 200", "Magie \u00e9l\u00e9mentaire Terre : 200", "Magie d'illusion : 300", "Magie psychique : 300"])

def open_milishop_window():
    ShopWindow("Marchand militaire", ["\u00c9p\u00e9e courte : 200", "\u00c9p\u00e9e longue : 350", "Dague : 200", "Hache de guerre : 250", "Arc : 250", "Bouclier : 350"])

def open_itemshop_window():
    ShopWindow("Marchand d'objets", ["Potion de soin : 50", "Potion de poison : 50", "Potion de mana : 100", "Potion de repos : 100", "Bombe l\u00e9g\u00e8re : 100", "Bombe lourde : 250", "Bombe fumig\u00e8ne : 100", "Filet : 100"])


initialize_save()  # ensures money and stats exist

# Main window
window = tk.Tk()
window.title("Project RPG")
window.geometry(f"{WINDOW_WIDTH_MAIN}x{WINDOW_HEIGHT_MAIN}")
window.configure(bg=COLOR_BACKGROUND_DARK)

# ═════════════════════════════════════════════════════════════════════════════
# HEADER - Dramatic RPG Title with Visual Effects
# ═════════════════════════════════════════════════════════════════════════════
header_frame = tk.Frame(window, bg=COLOR_HEADER_BG, height=HEADER_HEIGHT)
header_frame.pack(fill=tk.X, padx=0, pady=0)
header_frame.pack_propagate(False)

# Decorative top border
top_border = tk.Frame(header_frame, bg=COLOR_HEADER_ACCENT, height=BORDER_HEIGHT)
top_border.pack(fill=tk.X)

# Main title with dramatic styling
title_frame = tk.Frame(header_frame, bg=COLOR_HEADER_BG)
title_frame.pack(fill=tk.BOTH, expand=True)

# Decorative shields and divider
title_label = tk.Label(title_frame, text=f"{DECORATIVE_SWORD}  {DECORATIVE_HORIZONTAL}  {DECORATIVE_SWORD}", 
                       font=FONT_TITLE_LARGE, fg=COLOR_HEADER_ACCENT, bg=COLOR_HEADER_BG)
title_label.pack(pady=5)

# Main title
main_label = tk.Label(title_frame, text="PROJECT RPG", 
                      font=FONT_TITLE_MAIN, 
                      fg=COLOR_TEXT_GOLD, bg=COLOR_HEADER_BG)
main_label.pack(pady=0)

# Subtitle
version_label = tk.Label(title_frame, text=f"[ Version {CURRENT_VERSION} - {VERSION_NAME} ]", 
                        font=FONT_VERSION, fg=COLOR_TEXT_DARK_GRAY, bg=COLOR_HEADER_BG)
version_label.pack(pady=2)

# Decorative bottom
bottom_divider = tk.Label(title_frame, text=f"{DECORATIVE_SWORD}  {DECORATIVE_HORIZONTAL}  {DECORATIVE_SWORD}", 
                          font=FONT_TITLE_LARGE, fg=COLOR_HEADER_ACCENT, bg=COLOR_HEADER_BG)
bottom_divider.pack(pady=5)

# ═════════════════════════════════════════════════════════════════════════════
# PLAYER STATS BAR
# ═════════════════════════════════════════════════════════════════════════════
stats_frame = tk.Frame(window, bg=COLOR_BACKGROUND_VERY_DARK, height=STATS_BAR_HEIGHT)
stats_frame.pack(fill=tk.X, padx=0, pady=0)
stats_frame.pack_propagate(False)

# Stats bar background with border
stats_container = tk.Frame(stats_frame, bg=COLOR_STATS_BG, relief=tk.RAISED, bd=2)
stats_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Left stats
left_stats = tk.Frame(stats_container, bg=COLOR_STATS_BG)
left_stats.pack(side=tk.LEFT, padx=15, fill=tk.Y, expand=True)

player_name_label = tk.Label(left_stats, text="", font=FONT_TITLE_LARGE, 
                            fg=COLOR_TEXT_GREEN, bg=COLOR_STATS_BG)
player_name_label.pack(side=tk.LEFT, padx=10)

# Center divider
divider = tk.Label(stats_container, text=DECORATIVE_DIVIDER, font=("Courier", 16), fg="#666666", bg=COLOR_STATS_BG)
divider.pack(side=tk.LEFT, padx=10)

# Right stats
right_stats = tk.Frame(stats_container, bg=COLOR_STATS_BG)
right_stats.pack(side=tk.RIGHT, padx=15, fill=tk.Y, expand=True)

main_money_label = tk.Label(right_stats, text=f"💰 {money} deullars", 
                           font=FONT_TITLE_LARGE, 
                           fg=COLOR_HEADER_ACCENT, bg=COLOR_STATS_BG)
main_money_label.pack(side=tk.RIGHT, padx=10)

# ═════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═════════════════════════════════════════════════════════════════════════════
content_frame = tk.Frame(window, bg=COLOR_BACKGROUND_DARK)
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Conteneur pour organiser les catégories en grille 2x2
buttons_frame = tk.Frame(content_frame, bg=COLOR_BACKGROUND_DARK)
buttons_frame.pack(fill=tk.BOTH, expand=True)

# Row 1
row1_frame = tk.Frame(buttons_frame, bg=COLOR_BACKGROUND_DARK)
row1_frame.pack(fill=tk.BOTH, expand=True)

# ----- Catégorie 1 : Marchands -----
merchants_frame = styled_frame(row1_frame, "🏪 MARCHANDS 🏪", "#1a1a1a", COLOR_BORDER_GOLD, "#daa520")
create_button(merchants_frame, "⚔️  Entraîneur militaire", open_military_window, "merchant")
create_button(merchants_frame, "🗡️  Marchand militaire", open_milishop_window, "merchant")
create_button(merchants_frame, "🔮  Maître magicien", open_magic_window, "magic")
create_button(merchants_frame, "🧪  Marchand d'objets", open_itemshop_window, "merchant")

# ----- Catégorie 2 : Joueur -----
player_frame = styled_frame(row1_frame, "👤 JOUEUR 👤", COLOR_PLAYER_SECTION_BG, COLOR_BORDER_BLUE, COLOR_PLAYER_ACCENT)
create_button(player_frame, "✨  Fusion de compétences", open_skills_creation_window, "magic")
create_button(player_frame, "📖  Inventaire", open_inventaire_window, "player")
create_button(player_frame, "📈  Améliorer les stats", open_upgrade_window, "player")
create_button(player_frame, "😴  Se reposer à l'auberge", inn_rest, "neutral")

# Row 2
row2_frame = tk.Frame(buttons_frame, bg=COLOR_BACKGROUND_DARK)
row2_frame.pack(fill=tk.BOTH, expand=True)

# ----- Catégorie 3 : Combat et Quêtes -----
combat_frame = styled_frame(row2_frame, "⚔️  AVENTURE  ⚔️", COLOR_COMBAT_SECTION_BG, COLOR_BORDER_DARK, COLOR_COMBAT_ACCENT)
create_button(combat_frame, "🗡️  Partir à l'attaque", open_rpg_ui_window, "combat")
create_button(combat_frame, "📜  Quêtes", open_rpg_quests_window, "combat")
create_button(combat_frame, "🗺️  Carte du monde (WIP)", open_rpg_ui_map_window, "neutral")

# ----- Catégorie 4 : Options -----
options_frame = styled_frame(row2_frame, "⚙️  OPTIONS  ⚙️", COLOR_OPTIONS_SECTION_BG, COLOR_BORDER_GRAY, COLOR_OPTIONS_ACCENT)
create_button(options_frame, "💾  Sauvegarder la partie", save_game, "neutral")
create_button(options_frame, "🔄  Réinitialiser le jeu", reset_game, "danger")

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
footer_frame = tk.Frame(window, bg=COLOR_BACKGROUND_VERY_DARK, height=FOOTER_HEIGHT)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=0, pady=0)
footer_frame.pack_propagate(False)

# Bottom border
bottom_border = tk.Frame(footer_frame, bg=COLOR_HEADER_ACCENT, height=BORDER_HEIGHT)
bottom_border.pack(fill=tk.X)

footer_label = tk.Label(footer_frame, text=f"{DECORATIVE_SWORD}  Un jeu par Eazeon  {DECORATIVE_SWORD}", 
                       font=FONT_DECORATIVE_SMALL, fg=COLOR_OPTIONS_ACCENT, bg=COLOR_BACKGROUND_VERY_DARK)
footer_label.pack(pady=3)

# ═════════════════════════════════════════════════════════════════════════════
# INITIALIZATION & MAIN LOOP
# ═════════════════════════════════════════════════════════════════════════════

# Initialize the game (load save or create new)
initialize_save()
update_main_window()

# Display the main window
player_name_label.config(text=f"👤 {player_name}")

# Start the main event loop
window.mainloop()

