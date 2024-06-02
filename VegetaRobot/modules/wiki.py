from VegetaRobot import pgram as bot
from pyrogram import filters, types
from bs4 import BeautifulSoup
import requests
import json
import random
import string

# Dictionary to store search results
search_results_dict = {}

# Function to fetch Wikipedia search results
def fetch_wikipedia_search_results(query, limit=8):
    url = f"https://en.m.wikipedia.org/w/index.php?search={query}&title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for invalid response status
    except requests.RequestException as e:
        print("Error fetching the page:", e)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []

    # Extract the search results
    search_results = soup.find_all('div', class_='mw-search-result-heading')
    descriptions = soup.find_all('div', class_='searchresult')

    for i in range(min(limit, len(search_results))):
        title_tag = search_results[i].find('a')
        if title_tag:
            title = title_tag.get('title')
            url = "https://en.wikipedia.org" + title_tag.get('href')
            description = descriptions[i].get_text(strip=True) if i < len(descriptions) else ""
            # Generate unique identifier for the search result
            identifier = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            # Store search result in dictionary
            search_results_dict[identifier] = {
                'title': title,
                'description': description,
                'url': url
            }
            results.append((title, identifier))

    return results

# Command handler for /wiki
@bot.on_message(filters.command("wiki"))
async def wiki(client, message):
    if len(message.command) == 1:
        await message.reply("Please provide a search query.")
        return

    query = ' '.join(message.command[1:])
    search_results = fetch_wikipedia_search_results(query)
    if not search_results:
        await message.reply_text("No results found.")
        return

    buttons = [
        [types.InlineKeyboardButton(title, callback_data=f"wiki:{identifier}")] for title, identifier in search_results
    ]
    reply_markup = types.InlineKeyboardMarkup(buttons)
    await message.reply_text("Choose a result:", reply_markup=reply_markup)

# Callback handler for wiki
@bot.on_callback_query(filters.regex('^wiki:'))
async def button(client, query):
    identifier = query.data.split(":", 1)[1]
    result = search_results_dict.get(identifier)

    if result:
        message = f"{result['title']}\n\n{result['description']}\n\nURL: {result['url']}"
        await query.edit_message_text(text=message)
    else:
        await query.answer("Invalid selection")
