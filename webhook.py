import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

pYsson_img = "https://avatars.githubusercontent.com/u/97378861?v=4"

def main(site, result, imgLink, prdt_name, price_t, prdt_size, email):
    webhook_url = ""

    with open('setting.json', 'r') as f:
        wb = json.load(f)
        webhook_url = wb['webhook']

    webhook = DiscordWebhook(url=webhook_url)
    title = "Success - " + str(site)
    embed = DiscordEmbed(title=title, url=result.url, color='A6A6C3')
    embed.set_thumbnail(url=imgLink)
    embed.add_embed_field(name='Product', value=prdt_name, inline=False)
    embed.add_embed_field(name='Price', value=price_t)
    embed.add_embed_field(name='Size', value=prdt_size)
    embed.add_embed_field(name='Profile', value="||"+email+"||", inline=False)
    embed.set_footer(text='Powered by pYsson#3604', icon_url=pYsson_img)
    embed.set_timestamp()
    
    webhook.add_embed(embed)
    response = webhook.execute()

def test():
    webhook_url = ""
    with open('setting.json', 'r') as f:
        wb = json.load(f)
        webhook_url = str(wb['webhook'])

    webhook = DiscordWebhook(url=webhook_url, username="pYsson")
    title = "Test Success"
    embed = DiscordEmbed(title=title, color='A6A6C3')
    embed.set_thumbnail(url=pYsson_img)
    embed.add_embed_field(name='Product', value="TEST", inline=False)
    embed.add_embed_field(name='Price', value="$999")
    embed.add_embed_field(name='Size', value="OS")
    embed.add_embed_field(name='Profile', value="||test@gmail.com||", inline=False)
    embed.set_footer(text='Powered by pYsson#3604', icon_url=pYsson_img)
    embed.set_timestamp()
    
    webhook.add_embed(embed)
    response = webhook.execute()


