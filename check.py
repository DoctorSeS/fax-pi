from threading import Thread
from flask import Flask
import socket
from termcolor import cprint
import main
import server

def run_flask():
    server.run_site()

def run_discord_bot():
    # This starts your Discord bot
    main.run_bot()

if __name__ == "__main__":
    # Start both the Flask app and the bot in separate threads
    flask_thread = Thread(target=run_flask)
    bot_thread = Thread(target=run_discord_bot)

    # Start the threads
    flask_thread.start()
    bot_thread.start()

    # Join the threads to wait for their completion
    flask_thread.join()
    bot_thread.join()
