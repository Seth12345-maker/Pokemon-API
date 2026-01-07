import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO


class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Information Finder")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        
        title_label = tk.Label(
            self.root,
            text="Pokémon Information Finder",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.search_entry = tk.Entry(
            input_frame,
            width=25,
            font=("Arial", 12)
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(
            input_frame,
            text="Search",
            font=("Arial", 12),
            command=self.search_pokemon
        )
        search_button.pack(side=tk.LEFT)

        clear_button = tk.Button(
            self.root,
            text="Clear",
            font=("Arial", 10),
            command=self.clear_results
        )
        clear_button.pack(pady=5)

      
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        self.info_text = tk.Text(
            self.root,
            height=20,
            width=55,
            font=("Arial", 10)
        )
        self.info_text.pack(pady=10)
        self.info_text.config(state=tk.DISABLED)

    def search_pokemon(self):
        pokemon_name = self.search_entry.get().strip().lower()

        if not pokemon_name:
            messagebox.showwarning("Input Error", "Please enter a Pokémon name.")
            return

        try:
            data = self.fetch_pokemon_data(pokemon_name)
            self.display_pokemon(data)
        except Exception:
            messagebox.showerror(
                "Not Found",
                "Pokémon not found. Please check the spelling."
            )

    def fetch_pokemon_data(self, name):
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Pokemon not found")

        return response.json()

    def display_pokemon(self, data):
        self.clear_results()

        
        image_url = data["sprites"]["front_default"]
        if image_url:
            image_response = requests.get(image_url)
            image_data = image_response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((150, 150))
            self.pokemon_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.pokemon_image)

        
        name = data["name"].capitalize()
        height = data["height"]
        weight = data["weight"]

        types = ", ".join(
            [t["type"]["name"].capitalize() for t in data["types"]]
        )

        stats = ""
        for stat in data["stats"]:
            stats += f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}\n"

        info = (
            f"Name: {name}\n"
            f"Type(s): {types}\n"
            f"Height: {height}\n"
            f"Weight: {weight}\n\n"
            f"Base Stats:\n{stats}"
        )

        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

    def clear_results(self):
        self.image_label.config(image="")
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
