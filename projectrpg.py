import tkinter as tk
from tkinter import messagebox
import random
import os
import csv

from fusion_recipes_lists import fusion_recipes
from enemy_types_lists import enemy_types
from quests_list import quests

CURRENT_VERSION = "0.1.8"
VERSION_NAME = "Pre-Alpha - Quests update"

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

player_current_hp = player_stats["max_hp"]

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

            player_stats["max_hp"] = 1000
            player_stats["max_mana"] = 1000
            player_stats["max_fatigue"] = 1000
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
        
        player_current_hp = player_stats["max_hp"]
        
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

            player_current_hp = player_stats["max_hp"]

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
    global money, player_hp, player_mana, player_fatigue
    if money < 25:
        messagebox.showwarning("Pas assez d'argent", "Vous n'avez pas assez de deullars pour vous reposer à l'auberge.")
        return

    answer = messagebox.askyesno("Auberge", "Souhaitez-vous vous reposer à l'auberge pour 25 deullars ?")
    if answer:
        money -= 25
        player_hp["value"] = player_stats["max_hp"]
        player_mana["value"] = player_stats["max_mana"]
        player_fatigue["value"] = 0
        messagebox.showinfo("Repos", "Vous vous sentez reposé ! PV, Mana et Fatigue ont été restaurés.")
        update_main_window()


    
def open_inventaire_window():
    inventaire_window = tk.Toplevel(window)
    inventaire_window.title("Inventaire")
    inventaire_window.geometry("900x800")
    inventaire_window.transient(window)
    inventaire_window.grab_set()
    inventaire_window.focus_set()

    inventaire_window.configure(bg="#fff9ec")
    tk.Label(inventaire_window, text="📖 Fusions Réalisées", font=("Verdana", 14, "bold"), bg="#fff9ec").pack(pady=10)

    scroll_canvas = tk.Canvas(inventaire_window, bg="#fff9ec", highlightthickness=0)
    scroll_frame = tk.Frame(scroll_canvas, bg="#fff9ec")
    scrollbar = tk.Scrollbar(inventaire_window, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)
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



class ShopWindow:
    def __init__(self, title, button_texts):
        self.window = tk.Toplevel(window)
        self.window.title(title)
        self.window.geometry("600x500")

        # Display money
        self.window.configure(bg="#f9f5ec")

        self.money_label = tk.Label(self.window, text=f"💰 Argent : {money} deullars", font=("Verdana", 12), bg="#f9f5ec")
        self.money_label.pack(pady=10)

        tk.Label(self.window, text=f"🏪 Bienvenue chez le {title}", font=("Verdana", 14, "bold"), bg="#f9f5ec").pack(pady=10)

        frame = tk.Frame(self.window, bg="#f9f5ec")
        frame.pack(pady=5)

        for text in button_texts:
            item_name, cost = text.split(" : ")
            cost = int(cost)
            btn = tk.Button(
                frame,
                text=f"{item_name} - {cost} 💰",
                font=("Verdana", 10),
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

    # Effacer de la sélection les éléments
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
    skills_window.transient(window)
    skills_window.grab_set()
    skills_window.focus_set()

    skills_window.configure(bg="#eef7ff")
    tk.Label(skills_window, text="🔮 Création des compétences", font=("Verdana", 14, "bold"), bg="#eef7ff").pack(pady=20)

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
        font=("Verdana", 16, "bold"),
        command=lambda: handle_fusion(display_label, result_label, scrollable_frame)
    )
    fusion_button.pack(pady=5)

def open_rpg_wip_window():
    wip_window = tk.Toplevel(window)
    wip_window.title("Work in Progress")
    wip_window.geometry("500x500")
    wip_window.transient(window)
    wip_window.grab_set()
    wip_window.focus_set()

    tk.Label(wip_window, text="Work In Progress - A venir", font=("Verdana", 16, "bold")).pack(pady=10)

def open_rpg_quests_window():
    quests_window = tk.Toplevel(window)
    quests_window.title("📜 Quêtes")
    quests_window.geometry("800x600")
    quests_window.configure(bg="#fffaf0")
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

def complete_quest_choice(quest, choice, window):
    global money

    # Apply rewards
    if "reward" in choice:
        reward = choice["reward"]
        money += reward.get("money", 0)
        player_xp["global"] += reward.get("xp", 0)

    # Apply penalties
    if "penalty" in choice:
        penalty = choice["penalty"]
        money -= penalty.get("money", 0)
        player_xp["global"] -= penalty.get("xp", 0)

    # Mark quest as completed
    quest["completed"] = True

    # Show dialogues depending on outcome
    if "result_dialogues" in choice:
        msg = "\n".join(choice["result_dialogues"])
    else:
        # default summary
        rewards_text = ""
        if "reward" in choice:
            rewards_text += f"+{choice['reward'].get('money',0)}💰, +{choice['reward'].get('xp',0)} XP\n"
        if "penalty" in choice:
            rewards_text += f"-{choice['penalty'].get('money',0)}💰, -{choice['penalty'].get('xp',0)} XP\n"
        msg = f"Vous avez choisi : {choice['text']}\n\n{rewards_text.strip()}"

    messagebox.showinfo("📜 Résultat de la quête", msg)

    update_main_window()
    window.destroy()
    save_game()  # ensure persistence



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

            if can_do:
                has_option = True
                tk.Button(
                    dialogue_win,
                    text=choice["text"],
                    font=("Verdana", 11),
                    wraplength=500,
                    command=lambda c=choice, q=quest, w=dialogue_win: complete_quest_choice(q, c, w)
                ).pack(pady=5, fill="x", padx=20)

        if not has_option:
            tk.Label(dialogue_win, text="❌ Vous n'avez pas encore les compétences ou objets requis.", font=("Verdana", 10, "italic"), bg="#fffaf0").pack(pady=10)

    next_button.config(command=show_next)
    show_next()  # show first dialogue


def open_rpg_ui_window():
    rpg_window = tk.Toplevel(window)
    rpg_window.title("RPG Combat")
    rpg_window.geometry("1200x900")
    rpg_window.transient(window)
    rpg_window.grab_set()
    rpg_window.focus_set()

    main_frame = tk.Frame(rpg_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    right_container = tk.Frame(main_frame)
    right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

    right_canvas = tk.Canvas(right_container)
    right_scrollbar = tk.Scrollbar(right_container, orient="vertical", command=right_canvas.yview)
    right_frame = tk.Frame(right_canvas)  # <- keep using right_frame everywhere else

    right_frame.bind(
        "<Configure>",
        lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
    )

    right_canvas.create_window((0, 0), window=right_frame, anchor="nw")
    right_canvas.configure(yscrollcommand=right_scrollbar.set)

    right_canvas.pack(side=tk.LEFT, fill="y", expand=True)
    right_scrollbar.pack(side=tk.RIGHT, fill="y")


    tk.Label(left_frame, text="⚔️ Combat RPG", font=("Verdana", 16, "bold")).pack(pady=10)

    combat_frame = tk.Frame(left_frame)
    combat_frame.pack(pady=10)

    bars_frame = tk.Frame(left_frame)
    bars_frame.pack(pady=10)

    status_frame = tk.Frame(left_frame)
    status_frame.pack(pady=5)

    player_status_text = None
    enemy_status_text = None


    def update_status_display():
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
        player_status_text.config(text=format_status(player_status_effects))
        enemy_status_text.config(text=format_status(enemy_status_effects))

    status_frame = tk.Frame(left_frame)
    status_frame.pack(pady=5)

    tk.Label(status_frame, text="🧍 Statuts joueur : ", font=("Verdana", 10, "bold"), anchor="w", justify="left").pack(fill="x", padx=10)
    player_status_text = tk.Label(status_frame, text="", font=("Verdana", 9), anchor="w", justify="left")
    player_status_text.pack(fill="x", padx=20)

    tk.Label(status_frame, text="👹 Statuts ennemi : ", font=("Verdana", 10, "bold"), anchor="w", justify="left").pack(fill="x", padx=10)
    enemy_status_text = tk.Label(status_frame, text="", font=("Verdana", 9), anchor="w", justify="left")
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

    def update_skills_display():
        for widget in right_frame.winfo_children():
            widget.destroy()

        tk.Label(right_frame, text="Compétences disponibles", font=("Verdana", 12, "bold")).pack(pady=5)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("enchanted", False):
                        continue
                    if val.get("consumable", False):
                        break
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
            if "damage_per_turn" in data:
                enemy_hp["value"] -= data["damage_per_turn"]
                log_message(f"🔥 {current_enemy['name']} subit {data['damage_per_turn']} dégâts de {effect}.")
                show_floating_text(rpg_window, data["damage_per_turn"], "orange")
        
            data["duration"] -= 1
            if data["duration"] <= 0:
                to_remove.append(effect)

        for effect in to_remove:
            del enemy_status_effects[effect]


    def start_next_fight():
        if fight_counter["count"] >= 5:
            log_message("🎉 Vous avez remporté les 5 combats !")
            return
        if fight_counter["count"] == 0:
            fight_counter["count"] += 1
        else:
            fight_counter["count"] += 1
            xp_gain = 50
            player_xp["global"] += xp_gain
            log_message(f"🏆 Vous gagnez {xp_gain} points d'expérience globale !")

        enemy_type = random.choices(enemy_types, weights=[e['weight'] for e in enemy_types])[0]
        current_enemy.update(enemy_type)
        enemy_hp["value"] = enemy_type["hp"]
        enemy_status_effects.clear()

        update_bars()
        update_status_display()
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
        set_bar(player_hp_canvas, player_hp_bar, player_hp_label,
                player_hp["value"], player_stats["max_hp"])
        set_bar(enemy_hp_canvas, enemy_hp_bar, enemy_hp_label,
                enemy_hp["value"], current_enemy.get("hp", 100))
        set_bar(mana_canvas, mana_bar, mana_label,
                player_mana["value"], player_stats["max_mana"])
        set_bar(fatigue_canvas, fatigue_bar, fatigue_label,
                player_fatigue["value"], player_stats["max_fatigue"])

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
        set_state_all_buttons_in(right_frame, "disabled")

    def enable_all_actions():
        attack_button.config(state="normal")
        set_state_all_buttons_in(right_frame, "normal")


    def enemy_attack():
        def check_player_defeat(fight_window):
            global player_current_hp
            if player_current_hp <= 0:
                player_current_hp = 0
                messagebox.showinfo("💀 Défaite", "Vous vous évanouissez au milieu du donjon...")
                fight_window.destroy()
                return True
            return False

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
        player_current_hp -= damage
        if check_player_defeat(open_rpg_ui_window):
            return


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

        all_items = list(purchased_items)

        for fusion in fusion_results:
            for key, val in fusion_recipes.items():
                if isinstance(val, dict) and val.get("result") == fusion:
                    if val.get("enchanted", False):
                        continue
                    if val.get("consumable", False):
                        if fusion not in all_items:
                            all_items.append(fusion)

        for item in all_items:
            if item in itemshop_items or item in fusion_results:
                frame = tk.Frame(right_frame, bd=1, relief=tk.SOLID)
                frame.pack(pady=3, fill=tk.X)
                item_frames.append(frame)
                tk.Label(frame, text=item, font=("Verdana", 10)).pack(anchor="w")
                tk.Button(
                    frame,
                    text="Utiliser sur soi",
                    font=("Verdana", 9),
                    command=lambda i=item: use_item(i, target="self")
                ).pack(pady=2, side=tk.LEFT)
                tk.Button(
                    frame,
                    text="Jeter sur l'ennemi",
                    font=("Verdana", 9),
                    command=lambda i=item: use_item(i, target="enemy")
                ).pack(pady=2, side=tk.LEFT)

    def use_item(item, target="self"):
        disable_all_actions()

        # Check if item is a consumable fusion (from fusion_recipes_lists)
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
                        player_current_hp = min(player_current_hp + heal_value, player_stats["max_hp"])
                        log_message(f"🧪 Vous récupérez {heal_value} PV.")
                    else:
                        enemy_hp["value"] = min(current_enemy.get("hp", 100), enemy_hp["value"] + heal_value)
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
                enemy_hp["value"] = min(current_enemy.get("hp", 100), enemy_hp["value"] + 25)
                log_message(f"Vous lancez une potion de soin sur {current_enemy['name']} et il récupère 25 PV.")
        elif item == "Potion de soin supérieure":
            if target == "self":
                player_hp["value"] = min(player_stats["max_hp"], player_hp["value"] + 50)
                log_message("🧪 Vous buvez une potion de soin supérieure et récupérez 50 PV.")
            else:
                enemy_hp["value"] = min(current_enemy.get("hp", 100), enemy_hp["value"] + 50)
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
        else:
            log_message(f"❓ {item} n'a pas encore d'effet implémenté.")

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
            player_mana["value"] -= 10
            player_fatigue["value"] += 15
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

    attack_button = tk.Button(combat_frame, text="Attaque basique", font=("Verdana", 12), command=attack)
    attack_button.pack(pady=5)

    update_skills_display()
    tk.Label(right_frame, text="Objets disponibles", font=("Verdana", 12, "bold")).pack(pady=5)
    update_item_display()

    start_next_fight()

def open_upgrade_window():
    upgrade_window = tk.Toplevel(window)
    upgrade_window.title("📈 Améliorations")
    upgrade_window.geometry("420x500")
    upgrade_window.configure(bg="#f1f1f1")
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
window.geometry("800x700")

# Titre principal
main_label = tk.Label(window, text=" Project RPG - Menu Principal", font=("Verdana", 18, "bold"))
main_label.pack(pady=15)

# Label du nom du joueur en haut à droite
player_name_label = tk.Label(window, text="", font=("Verdana", 10), anchor="e", justify="right")
player_name_label.place(relx=1.0, x=-10, y=10, anchor="ne")

# Labels d'information
main_money_label = tk.Label(window, text=f"💰 Argent : {money} deullars", font=("Verdana", 12))
main_money_label.pack(pady=5)

# Conteneur pour organiser les catégories
buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=20, expand=True)

def styled_frame(parent, bg_color):
    return tk.Frame(parent, bd=3, relief=tk.RIDGE, bg=bg_color, padx=10, pady=10)

# ----- Catégorie 1 : Marchands -----
frame_top_left = styled_frame(buttons_frame, "#f9f1e7")
frame_top_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

tk.Label(frame_top_left, text="Marchands", font=("Verdana", 14, "bold")).pack()
tk.Button(frame_top_left, text="Entraîneur militaire", font=("Verdana", 12), command=open_military_window).pack(pady=5)
tk.Button(frame_top_left, text="Marchand militaire", font=("Verdana", 12), command=open_milishop_window).pack(pady=5)
tk.Button(frame_top_left, text="Maître magicien", font=("Verdana", 12), command=open_magic_window).pack(pady=5)
tk.Button(frame_top_left, text="Marchand d'objets", font=("Verdana", 12), command=open_itemshop_window).pack(pady=5)

# ----- Catégorie 2 : Joueur -----
frame_top_right = styled_frame(buttons_frame, "#eef5fc")
frame_top_right.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

tk.Label(frame_top_right, text="Joueur", font=("Verdana", 14, "bold")).pack()
tk.Button(frame_top_right, text="Fusion !", font=("Verdana", 12), command=open_skills_creation_window).pack(pady=5)
tk.Button(frame_top_right, text="Inventaire", font=("Verdana", 12), command=open_inventaire_window).pack(pady=5)
tk.Button(frame_top_right, text="Améliorer les stats", font=("Verdana", 12), command=open_upgrade_window).pack(pady=5)
tk.Button(frame_top_right, text="Se reposer à l'auberge", font=("Verdana", 12), command=inn_rest).pack(pady=5)

# ----- Catégorie 3 : Combat et Quêtes -----
frame_bottom_left = styled_frame(buttons_frame, "#f3f7e9")
frame_bottom_left.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

tk.Label(frame_bottom_left, text="Combat et Quêtes", font=("Verdana", 14, "bold")).pack()
tk.Button(frame_bottom_left, text="Partir à l'attaque", font=("Verdana", 12), command=open_rpg_ui_window).pack(pady=5)
tk.Button(frame_bottom_left, text="Quêtes", font=("Verdana", 12), command=open_rpg_quests_window).pack(pady=5)
tk.Button(frame_bottom_left, text="Carte du monde (WIP)", font=("Verdana", 12), command=open_rpg_wip_window).pack(pady=5)


# ----- Catégorie 4 : Options -----
frame_bottom_right = styled_frame(buttons_frame, "#f7e9f5")
frame_bottom_right.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

tk.Label(frame_bottom_right, text="Options", font=("Verdana", 14, "bold")).pack()
tk.Button(frame_bottom_right, text="💾 Sauvegarder la partie", font=("Verdana", 12), command=save_game).pack(pady=5)
tk.Button(frame_bottom_right, text="Réinitialiser le jeu", font=("Verdana", 12), bg="red", fg="white", command=reset_game).pack(pady=5)

buttons_frame.grid_rowconfigure(0, weight=1)
buttons_frame.grid_rowconfigure(1, weight=1)
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)

# Initialisation sauvegarde après création des labels et boutons
initialize_save()
update_main_window()

# Sauvegarde auto à la fermeture
def on_close():
    save_game()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()

window.mainloop()

