import discord
from discord.ext import commands
import json

# Crée une instance de bot avec les intents nécessaires
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Pour récupérer le contenu des messages
bot = commands.Bot(command_prefix="!", intents=intents)

# Fichier pour stocker les données des pays
data_file = "pays_stats.json"

# Fonction pour charger les données des pays
def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fonction pour sauvegarder les données des pays
def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

# Commande !bonus pour ajouter un bonus à un pays
@bot.command(name="bonus", help="Ajoute un bonus à un pays (Ex: !bonus France bonheur 5)")
async def bonus(ctx, pays: str, stat: str, valeur: int):
    # Charger les données
    data = load_data()

    # Si le pays n'est pas encore enregistré, l'ajouter avec des stats par défaut
    if pays not in data:
        data[pays] = {
            "Bonheur": 0,
            "Sécurité": 0,
            "Puissance Militaire": 0,
            "Influence": 0
        }

    # Appliquer le bonus à la stat spécifiée
    if stat.capitalize() in data[pays]:
        data[pays][stat.capitalize()] += valeur
        save_data(data)
        await ctx.send(f"**+{valeur} {stat.capitalize()}** pour **{pays}**.")
    else:
        await ctx.send(f"Statistique invalide pour {pays}. Les statistiques valides sont : Bonheur, Sécurité, Puissance Militaire, Influence.")

# Commande !malus pour ajouter un malus à un pays (correction)
@bot.command(name="malus", help="Ajoute un malus à un pays (Ex: !malus France bonheur -5)")
async def malus(ctx, pays: str, stat: str, valeur: int):
    # Charger les données
    data = load_data()

    # Si le pays n'est pas encore enregistré, l'ajouter avec des stats par défaut
    if pays not in data:
        data[pays] = {
            "Bonheur": 0,
            "Sécurité": 0,
            "Puissance Militaire": 0,
            "Influence": 0
        }

    # Appliquer le malus (soustraction de la valeur) à la stat spécifiée
    if stat.capitalize() in data[pays]:
        data[pays][stat.capitalize()] -= valeur  # Soustraction au lieu d'addition
        save_data(data)
        await ctx.send(f"**-{valeur} {stat.capitalize()}** pour **{pays}**.")
    else:
        await ctx.send(f"Statistique invalide pour {pays}. Les statistiques valides sont : Bonheur, Sécurité, Puissance Militaire, Influence.")

# Commande pour afficher les stats d'un pays
@bot.command(name="stats", help="Affiche les stats d'un pays (Ex: !stats France)")
async def stats(ctx, pays: str):
    # Charger les données
    data = load_data()

    if pays in data:
        stats = data[pays]
        await ctx.send(f"Stats de **{pays}** :\n"
                       f"Bonheur : {stats['Bonheur']}\n"
                       f"Sécurité : {stats['Sécurité']}\n"
                       f"Puissance Militaire : {stats['Puissance Militaire']}\n"
                       f"Influence : {stats['Influence']}")
    else:
        await ctx.send(f"Le pays **{pays}** n'est pas encore enregistré.")

# Lorsque le bot est prêt, il affiche un message dans la console
@bot.event
async def on_ready():
    print(f'{bot.user} est connecté(e) et prêt(e) à fonctionner !')

# Lancer le bot avec ton token
bot.run("MTM0Mzk3MjYzOTE2NDU5NjI0NA.GEPsF6.r4h5uPSG4mUth_f-aex8NdGze-0iw9UOb7tpC0")
