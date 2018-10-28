#!/usr/bin/env python3
"""
Консольная программа для изучения английских слов. Работает только под Linux.
Для работы нужно установить консольный mp3 проигрователь mpg321.
sudo apt-get install mpg321
"""

import asyncio
import time

from prompt_toolkit import prompt_async  # $ pip install prompt_toolkit
from prompt_toolkit.shortcuts import Keys, Registry

import os
import csv
import random


class color:
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    END = '\033[0m'

BACKWARDS, STOP, FORWARDS = 1, 0, -1


async def interactive_prompt(direction):
    registry = Registry()

    @registry.add_binding('q')
    def stop(event):
        direction[0] = STOP
        event.cli.set_return_value(False)  # exit

    @registry.add_binding(Keys.Up)
    def backwards(event):
        direction[0] = BACKWARDS

    await prompt_async('Нажмите "стрелка вверх" для повторения / "q" для остановки',
                       patch_stdout=True,  # show prompt
                       key_bindings_registry=registry)


async def print_chars(direction, read_csv, menu, i, speed):
    time_start = time.time()

    while i < len(read_csv):
        if i % 10 == 0:
            time_print = int(time.time() - time_start)
            print(color.Red + str(i) + '        ' + str(time_print) + color.END)
        if direction[0] == BACKWARDS:
            i -= 1
        if direction[0] == STOP:
            with open('index_start.txt', 'w') as fio:
                fio.write(str(i))
            break

        english_word = color.Green + read_csv[i][0] + color.END
        transcription = color.Yellow + read_csv[i][1] + color.END
        russian_word = color.Yellow + read_csv[i][2] + color.END

        if menu == 1:
            print(transcription, english_word, russian_word)
            pause = (len(read_csv[i][0]) + len(read_csv[i][1]) + len(read_csv[i][2])) * 0.05 / speed
            await asyncio.sleep(pause * 0.7)
            mp3_name = read_csv[i][0].replace(' ', '_')
            os.system("mpg321 " + "en_mp3/" + mp3_name + ".mp3" + " 2>mpg321.txt")
            i += 1
            direction[0] = FORWARDS
            await asyncio.sleep(pause * 2.0)

        elif menu == 2:
            print(transcription, english_word)
            pause = (len(read_csv[i][0]) + len(read_csv[i][1]) + len(read_csv[i][2])) * 0.05 / speed
            await asyncio.sleep(pause * 0.7)
            mp3_name = read_csv[i][0].replace(' ', '_')
            os.system("mpg321 " + "en_mp3/" + mp3_name + ".mp3" + " 2>mpg321.txt")
            i += 1
            direction[0] = FORWARDS
            await asyncio.sleep(pause * 2.0 + len(read_csv[i-1][2]) * 0.05)
            d = len(read_csv[i-1][0]) + len(read_csv[i-1][1])
            print(' ' * d, russian_word)

        elif menu == 3:
            print(transcription, english_word)
            pause = (len(read_csv[i][0]) + len(read_csv[i][1]) + len(read_csv[i][2])) * 0.05 / speed
            await asyncio.sleep(pause * 0.7)
            mp3_name = read_csv[i][0].replace(' ', '_')
            os.system("mpg321 " + "en_mp3/" + mp3_name + ".mp3" + " 2>mpg321.txt")
            i += 1
            direction[0] = FORWARDS
            await asyncio.sleep(pause * 2.0 + len(read_csv[i-1][2]) * 0.05)
            d = len(read_csv[i-1][0]) + len(read_csv[i-1][1])
            print(' ' * d, russian_word)

        elif menu == 4:
            print(russian_word)
            pause = (len(read_csv[i][0]) + len(read_csv[i][1]) + len(read_csv[i][2])) * 0.05 / speed
            await asyncio.sleep(pause * 2.0 + (len(read_csv[i-1][0]) + len(read_csv[i-1][1])) * 0.05)
            mp3_name = read_csv[i][0].replace(' ', '_')
            os.system("mpg321 " + "en_mp3/" + mp3_name + ".mp3" + " 2>mpg321.txt")
            i += 1
            direction[0] = FORWARDS
            await asyncio.sleep(pause * 0.05)
            d = len(read_csv[i-1][2])
            print(' ' * d, transcription, english_word)
        if i == len(read_csv):
            i = 0
            with open('index_start.txt', 'w') as fio:
                fio.write(str(i))


with open('index_start.txt', 'r') as fio:
    i_start = int(fio.read())


menu_str_0 = color.Green + "Выберите вариант работы программы:\n" + color.END
menu_str_1 = color.Yellow + "  транскрипция - английское слово - английская озвучка - русский перевод >> Нажмите цифру " + color.END + color.Red + "1\n" + color.END
menu_str_2 = color.Yellow + "  транскрипция - английское слово - английская озвучка - временная задержка 1 секунда - русский перевод >> Нажмите цифру " + color.END + color.Red + "2\n" + color.END
menu_str_3 = color.Yellow + "  транскрипция - английское слово - английская озвучка - временная задержка 1 секунда - русский перевод\n (при этом слова из списка выводятся в случайном порядке) >> Нажмите цифру "  + color.END + color.Red + "3\n" + color.END
menu_str_4 = color.Yellow + "  русский перевод  - временная задержка 1 секунда - транскрипция - английское слово - английская озвучка >> Нажмите цифру " + color.END + color.Red + "4\n" + color.END

menu_str = menu_str_0 + menu_str_1 + menu_str_2 + menu_str_3 + menu_str_4
menu = int(input(menu_str))

n = input(color.Yellow + "Введите номер строки с которой надо начать (0 чтобы начать с первой строки) или Enter чтобы начать с того места где завершили в прошлый раз: " + color.END)
speed = float(input(color.Yellow + "Введите коэфициент скорости, например 2 для двукратного уменьшения пауз: " + color.END))

if n.isdigit():
    n = int(n)
else:
    n = i_start


if menu == 3:
    name_file = "random_1000_en.csv"
else:
    name_file = "1000_en.csv"

with open(name_file, "r") as fio:
    read_csv = [row for row in csv.reader(fio)]


if menu == 3 and n == 0:
    random.shuffle(read_csv)
    with open("random_1000_en.csv", "w") as fio:
        writer = csv.writer(fio)
        for line in read_csv:
            writer.writerow(line)


loop = asyncio.get_event_loop()
direction = [FORWARDS]
input_task = loop.create_task(interactive_prompt(direction))
loop.run_until_complete(print_chars(direction, read_csv, menu, n, speed))