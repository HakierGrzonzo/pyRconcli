from prompt_toolkit import PromptSession, print_formatted_text, ANSI
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import argparse
import mcrcon

def minecraft_colors_to_ansi(text):
    color_dict = {
        "§0": "\u001b[30m",
        "§1": "\u001b[34m",
        "§2": "\u001b[32m",
        "§3": "\u001b[36m",
        "§4": "\u001b[31m",
        "§5": "\u001b[35m",
        "§6": "\u001b[33m",
        "§7": "\u001b[37m",
        "§8": "\u001b[30;1m",
        "§9": "\u001b[34;1m",
        "§a": "\u001b[32;1m",
        "§b": "\u001b[36;1m",
        "§c": "\u001b[31;1m",
        "§d": "\u001b[35;1m",
        "§e": "\u001b[33;1m",
        "§f": "\u001b[37;1m"
    }
    for key, value in color_dict.items():
        text = text.replace(key, value)
    return text.replace('\n', '\u001b[0m\n')


parser = argparse.ArgumentParser(prog="pyrconcli", description="a better terminal interface for minecraft rcon")
parser.add_argument('ip', type = str, help = "ip adresss of server")
parser.add_argument('password', type = str, help = "password for rcon protocol")
parser.add_argument('-P', type= int, help= "rcon port (default is 25575)", default=25575, dest="port")
args = parser.parse_args()
with mcrcon.MCRcon(args.ip, args.password, args.port) as rcon:
    session = PromptSession("rcon@{}> ".format(args.ip))
    try:
        print("type 'exit' or press crtl-d to exit")
        command = session.prompt()
        while command != "exit":
            resp = rcon.command(command)
            resptext = minecraft_colors_to_ansi(resp)
            print_formatted_text(ANSI(resptext))
            command = session.prompt(auto_suggest=AutoSuggestFromHistory())
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
        