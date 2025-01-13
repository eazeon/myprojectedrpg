import tkinter as tk
from tkinter import messagebox

# Global variables
money = 1000
purchased_items = []
selected_items = []
fusion_results = []

fusion_recipes = {
    frozenset(["Coup simple", "\u00c9p\u00e9e courte"]): "Coup d'estoc a l'\u00e9p\u00e9e",
    frozenset(["Coup simple", "\u00c9p\u00e9e longue"]): "Long coup a l'\u00e9p\u00e9e longue",
    frozenset(["Coup simple", "Dague"]): "Coup de dague",
    frozenset(["Coup simple", "Hache de guerre"]): "Frappe simple de hache",
    frozenset(["Coup simple", "Arc"]): "Tir simple",
    frozenset(["Coup simple", "Bouclier"]): "Coup de bouclier",
    frozenset(["Coup puissant", "Épée courte"]): "Coup lourd à l'épée",
    frozenset(["Coup puissant", "Épée longue"]): "Abattage de l'épée longue",
    frozenset(["Coup puissant", "Dague"]): "Frappe reversé de dague",
    frozenset(["Coup puissant", "Hache de guerre"]): "Abattage de hache",
    frozenset(["Coup puissant", "Arc"]): "Tir violent",
    frozenset(["Coup puissant", "Bouclier"]): "Pillonage de bouclier",
    frozenset(["Parade", "Épée courte"]): "Parade simple d'épée",
    frozenset(["Parade", "Épée longue"]): "Parade lourde d'épée",
    frozenset(["Parade", "Dague"]): "Blocage à la dague",
    frozenset(["Parade", "Hache de guerre"]): "Blocage avec la hache",
    frozenset(["Parade", "Arc"]): "Blocage avec l'arc",
    frozenset(["Parade", "Bouclier"]): "Blocage au bouclier",
    frozenset(["Coup simple", "Magie élémentaire Feu"]): "Boule de feu simple",
    frozenset(["Coup simple", "Magie élémentaire Air"]): "Bourrasque d'air",
    frozenset(["Coup simple", "Magie élémentaire Eau"]): "Rafale d'eau",
    frozenset(["Coup simple", "Magie élémentaire Terre"]): "Jet de pierres",
    frozenset(["Coup simple", "Magie d'illusion"]): "Créer une illusion simple",
    frozenset(["Coup simple", "Magie psychique"]): "Décharge mentale",
    frozenset(["Coup puissant", "Magie élémentaire Feu"]): "Colonne de flammes",
    frozenset(["Coup puissant", "Magie élémentaire Air"]): "Tornade localisée",
    frozenset(["Coup puissant", "Magie élémentaire Eau"]): "Déversement torrentiel",
    frozenset(["Coup puissant", "Magie élémentaire Terre"]): "Séisme localisé",
    frozenset(["Coup puissant", "Magie d'illusion"]): "Créer une illusion simple",
    frozenset(["Coup puissant", "Magie psychique"]): "Emprise mentale",
    frozenset(["Parade", "Magie élémentaire Feu"]): "Bouclier de feu",
    frozenset(["Parade", "Magie élémentaire Air"]): "Bouclier d'air",
    frozenset(["Parade", "Magie élémentaire Eau"]): "Bouclier d'eau",
    frozenset(["Parade", "Magie élémentaire Terre"]): "Bouclier de terre",
    frozenset(["Parade", "Magie d'illusion"]): "Illusion de blocage par le bras",
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
    frozenset(["Magie élémentaire Terre", "Dague"]): "Dague des profondeurs",
    frozenset(["Magie élémentaire Terre", "Hache de guerre"]): "Hache des marées",
    frozenset(["Magie élémentaire Terre", "Arc"]): "Arc des courants",
    frozenset(["Magie élémentaire Terre", "Bouclier"]): "Bouclier alourdis par l'eau",
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
        result = fusion_recipes[selected_set]
        if result in fusion_results:
            result_label.config(
                text="\u00c9chec de la fusion : Cette fusion a d\u00e9j\u00e0 \u00e9t\u00e9 r\u00e9alis\u00e9e.", fg="red"
            )
        else:
            fusion_results.append(result)

            # Remove items used in the fusion if they are shop items
            for item in selected_set:
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
                text=f"Fusion r\u00e9ussie ! Vous avez cr\u00e9\u00e9 : {result}", fg="green"
            )
    else:
        result_label.config(
            text="\u00c9chec de la fusion : La combinaison actuelle ne donne aucun r\u00e9sultat.",
            fg="red",
        )

    # Clear the selected items
    selected_items.clear()
    display_label.config(text="Aucun \u00e9l\u00e9ment s\u00e9lectionn\u00e9")

def open_skills_creation_window():
    skills_window = tk.Toplevel(window)
    skills_window.title("Cr\u00e9ation des comp\u00e9tences")
    skills_window.geometry("600x400")

    tk.Label(skills_window, text="Cr\u00e9ation des comp\u00e9tences", font=("Verdana", 14)).pack(pady=20)

    display_label = tk.Label(skills_window, text="Aucun \u00e9l\u00e9ment s\u00e9lectionn\u00e9", font=("Verdana", 12), wraplength=500)
    display_label.pack(pady=10)

    items_frame = tk.Frame(skills_window)
    items_frame.pack(pady=10)

    if purchased_items:
        tk.Label(skills_window, text="Cliquez sur un \u00e9l\u00e9ment pour personnaliser :", font=("Verdana", 12)).pack(pady=10)
        for item in purchased_items:
            tk.Button(
                items_frame, 
                text=item, 
                font=("Verdana", 10), 
                command=lambda i=item: toggle_item_display(i, display_label)
            ).pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(skills_window, text="Aucun \u00e9l\u00e9ment achet\u00e9 pour le moment.", font=("Verdana", 12)).pack(pady=20)

    result_label = tk.Label(skills_window, text="", font=("Verdana", 12), wraplength=500)
    fusion_button = tk.Button(
        skills_window, 
        text="Fusion", 
        font=("Verdana", 12), 
        command=lambda: handle_fusion(display_label, result_label, items_frame)
    )
    fusion_button.pack(pady=20)
    result_label.pack(pady=10)

def open_rpg_ui_window():
    rpg_window = tk.Toplevel(window)
    rpg_window.title("RPG UI")
    rpg_window.geometry("800x600")
    tk.Label(rpg_window, text="Pr\u00e9parez-vous pour le combat !", font=("Verdana", 14)).pack(pady=20)
    tk.Label(rpg_window, text="Ajoutez ici votre interface utilisateur RPG pour le combat.", font=("Verdana", 12), wraplength=600).pack(pady=10)

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
