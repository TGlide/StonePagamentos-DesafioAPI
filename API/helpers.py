import platform
import os
import time


def clear_screen():
    if platform.system().lower() == "Windows":
        return "cls"
    return "clear"


def screen_prompt(message: str, options: dict):
    choice = None
    while choice not in options.keys() and choice not in options.values():
        if choice:  # Usuário colocou um digito inválido
            os.system(clear_screen())
            print("Valor invalido, tente novamente.\n")
            time.sleep(3)
            os.system(clear_screen())
        # Prompt
        print(message)
        for key, value in options.items():
            print("{} - {}".format(key, value))
        choice = input("\nDigite a opção correspondente:")

    if choice in options.keys():
        return options[choice]
    return choice
