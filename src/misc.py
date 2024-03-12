from os import system

def logo(clear):
    if clear:
        system("cls")

    with open("src/logo.txt", "r", encoding="utf-8") as f:
        print(f.read())