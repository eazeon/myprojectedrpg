import tkinter as tk
from tkinter import messagebox

# Global variables
money = 1000
purchased_items = []
selected_items = []
fusion_results = []

fusion_recipes = {
    frozenset(["Coup simple", "Épée courte"]): "Coup d'estoc a l'épée",
    frozenset(["Coup simple", "Épée longue"]): "Coup droit a l'épée",
    frozenset(["Coup simple", "Dague"]): "Frappe de dague",
    frozenset(["Coup simple", "Hache de guerre"]): "Frappe simple de hache",
    frozenset(["Coup simple", "Arc"]): "Tir simple",
    frozenset(["Coup simple", "Bouclier"]): "Coup de bouclier",
    frozenset(["Coup puissant", "Épée courte"]): "Coup lourd à l'épée",
    frozenset(["Coup puissant", "Épée longue"]): "Frappe lourde à l'épée",
    frozenset(["Coup puissant", "Dague"]): "Frappe reversé de dague",
    frozenset(["Coup puissant", "Hache de guerre"]): "Abattage de hache",
    frozenset(["Coup puissant", "Arc"]): "Tir violent",
    frozenset(["Coup puissant", "Bouclier"]): "Charge de bouclier",
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
}

itemshop_items = ["Potion de soin", "Potion de poison", "Bombe légère", "Bombe lourde", "Bombe fumigène", "Filet"]

# Function to update the main window with purchased items and fusion results
def update_main_window():
    purchases_label.config(text=f"Items achetés : {', '.join(purchased_items)}")
    fusions_label.config(text=f"Fusions réalisées : {', '.join(fusion_results)}" if fusion_results else "Fusions réalisées : Aucun")
    main_money_label.config(text=f"Argent : {money} deullars")

class ShopWindow:
    def __init__(self, title, button_texts):
        self.window = tk.Toplevel(window)
        self.window.title(title)
        self.window.geometry("600x500")

        # Display money
        self.money_label = tk.Label(self.window, text=f"Argent: {money} deullars", font=("Verdana", 12))
        self.money_label.pack(pady=10)

        # Title label
        tk.Label(self.window, text=f"Bienvenue à {title}", font=("Verdana", 14)).pack(pady=20)

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
    display_label.config(text=", ".join(selected_items) if selected_items else "Aucun élément sélectionné")

def handle_fusion(display_label, result_label, items_frame):
    global fusion_results
    selected_set = frozenset(selected_items)
    if selected_set in fusion_recipes:
        result = fusion_recipes[selected_set]
        if result in fusion_results:
            result_label.config(
                text="Échec de la fusion : Cette fusion a déjà été réalisée.", fg="red"
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
                text=f"Fusion réussie ! Vous avez créé : {result}", fg="green"
            )
    else:
        result_label.config(
            text="Échec de la fusion : La combinaison actuelle ne donne aucun résultat.",
            fg="red",
        )

    # Clear the selected items
    selected_items.clear()
    display_label.config(text="Aucun élément sélectionné")


def open_skills_creation_window():
    skills_window = tk.Toplevel(window)
    skills_window.title("Création des compétences")
    skills_window.geometry("600x400")

    tk.Label(skills_window, text="Création des compétences", font=("Verdana", 14)).pack(pady=20)

    display_label = tk.Label(skills_window, text="Aucun élément sélectionné", font=("Verdana", 12), wraplength=500)
    display_label.pack(pady=10)

    items_frame = tk.Frame(skills_window)
    items_frame.pack(pady=10)

    if purchased_items:
        tk.Label(skills_window, text="Cliquez sur un élément pour personnaliser :", font=("Verdana", 12)).pack(pady=10)
        for item in purchased_items:
            tk.Button(
                items_frame, 
                text=item, 
                font=("Verdana", 10), 
                command=lambda i=item: toggle_item_display(i, display_label)
            ).pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(skills_window, text="Aucun élément acheté pour le moment.", font=("Verdana", 12)).pack(pady=20)

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
    tk.Label(rpg_window, text="Préparez-vous pour le combat !", font=("Verdana", 14)).pack(pady=20)
    tk.Label(rpg_window, text="Ajoutez ici votre interface utilisateur RPG pour le combat.", font=("Verdana", 12), wraplength=600).pack(pady=10)

def open_military_window():
    ShopWindow("Entraîneur militaire", ["Coup simple : 100", "Coup puissant : 250", "Parade : 250"])

def open_magic_window():
    ShopWindow("Maître magicien", ["Magie élémentaire Feu : 200", "Magie élémentaire Air : 200", "Magie élémentaire Eau : 200", "Magie élémentaire Terre : 200", "Magie d'illusion : 300", "Magie psychique : 300"])

def open_milishop_window():
    ShopWindow("Marchand militaire", ["Épée courte : 200", "Épée longue : 350", "Dague : 200", "Hache de guerre : 250", "Arc : 250", "Bouclier : 350"])

def open_itemshop_window():
    ShopWindow("Marchand d'objets", ["Potion de soin : 50", "Potion de poison : 50", "Bombe légère : 100", "Bombe lourde : 250", "Bombe fumigène : 100", "Filet : 100"])

# Main window
window = tk.Tk()
window.title("Project RPG")
window.geometry("800x700")

main_label = tk.Label(window, text="Création des compétences", font=("Verdana", 18))
main_label.pack(pady=20)

main_money_label = tk.Label(window, text=f"Argent : {money} deullars", font=("Verdana", 12))
main_money_label.pack(pady=10)

purchases_label = tk.Label(window, text="Items achetés : ", font=("Verdana", 12), wraplength=600, justify="center")
purchases_label.pack(pady=10)

fusions_label = tk.Label(window, text="Fusions réalisées : Aucun", font=("Verdana", 12), wraplength=600, justify="center")
fusions_label.pack(pady=10)

military_button = tk.Button(window, text="Entraîneur militaire", font=("Verdana", 12), command=open_military_window)
military_button.pack(pady=5)

magician_button = tk.Button(window, text="Maître magicien", font=("Verdana", 12), command=open_magic_window)
magician_button.pack(pady=5)

milishop_button = tk.Button(window, text="Marchand militaire (une arme par personne)", font=("Verdana", 12), command=open_milishop_window)
milishop_button.pack(pady=5)

itemshop_button = tk.Button(window, text="Marchand d'objets", font=("Verdana", 12), command=open_itemshop_window)
itemshop_button.pack(pady=5)

skills_button = tk.Button(window, text="Création des compétences", font=("Verdana", 12), command=open_skills_creation_window)
skills_button.pack(pady=20)

rpg_button = tk.Button(window, text="Partir à l'attaque", font=("Verdana", 12), command=open_rpg_ui_window)
rpg_button.pack(pady=10)

window.mainloop()
