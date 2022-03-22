import win32com.client
import os
import json
import zipfile
from random import choice
import xml.etree.ElementTree as ET
import easygui
from pathlib import Path
import shutil


def disk_info():  # выводит информацию о дисках
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
    for objItem in colItems:
        print("\nName: ", objItem.Name)
        print("Description: ", objItem.Description)
        print("File System: ", objItem.FileSystem)
        print("Size: ", objItem.Size)
        print("Free Space: ", objItem.FreeSpace)
        print("Volume Name: ", objItem.VolumeName)


def file():  # работа с обычными файлами
    try:
        write_line = input('Введите строку для записи: ')
        with open('new_file.txt', 'w') as f:
            f.write(write_line)
            f.close()
        with open('new_file.txt', 'r') as f:
            print('\nПрочитано из файла: ', f.read())
            f.close()
    except:
        print('Error. Try again')


def gen_person():  # генерация json объектка
    name = ''
    tel = ''

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    nums = ['1', '2', '3', '4', '5', '6', '7']

    while len(name) != 5:
        name += choice(letters)

    while len(tel) != 7:
        tel += choice(nums)

    person = {
        'name': name,
        'tel': tel
    }

    print('\nСгенерирован json объект:', person)

    return person


def get_json():  # вывод json объекта в консоль
    with open('persons.json') as f:
        templates = json.load(f)

    print('\nПрочитано из json файла:', templates)


def xml_file():  # работа с xml файлами
    items = [
        {"first_name": "Ivan", "last_name": "Ivanov", "city": "Moscow"},
        {"first_name": "Sergey", "last_name": "Sidorov", "city": "Sochi"},
    ]

    root = ET.Element('root')

    for i, item in enumerate(items, 1):
        person = ET.SubElement(root, 'person' + str(i))
        ET.SubElement(person, 'first_name').text = item['first_name']
        ET.SubElement(person, 'last_name').text = item['last_name']
        ET.SubElement(person, 'city').text = item['city']

    tree = ET.ElementTree(root)
    tree.write('xmlf.xml')

    ET.dump(tree)


def zip(input_file):  # работа с архивами
    try:
        dir = os.path.abspath(os.curdir)
        filee = input_file
        file_cut = os.path.basename(filee)

        path = filee
        cut_path = path.replace(file_cut, '')
        file_source = cut_path
        file_destination = dir

        for file in Path(file_source).glob(file_cut):
            shutil.copy(os.path.join(file_source, file), file_destination)

        zname = 'zip_files.zip'
        newzip = zipfile.ZipFile(zname, 'w')
        newzip.write(file_cut)  # добавляем файл в архив
        file = os.path.basename(file_cut)
        zip_size = os.path.getsize(file)
        print('\nРазмер архива:', zip_size, 'байт')
        os.remove(file)
        newzip.extract(file)
        newzip.close()  # закрываем архив
    except:
        print('Error. Try again')


def delete():  # функция удаления
    try:
        if os.path.exists('persons.json'):
            os.remove('persons.json')
        if os.path.exists('new_file.txt'):
            os.remove('new_file.txt')
        if os.path.exists('xmlf.xml'):
            os.remove('xmlf.xml')
        if os.path.exists('zip_files.zip'):
            os.remove('zip_files.zip')
        print('Success')
    except:
        print('Error. Try again')


def main():  # главная функция
    while True:
        choic = str(input(
            '\n1 - информация о диске\n2 - создание файла\n3 - создание json файла\n4 - создание xml файла\n5 - создание архива\n6 - удаление файлов\n'))
        try:
            if choic == '1':
                disk_info()
            elif choic == '2':
                file()
            elif choic == '3':
                json_file()
                get_json()
            elif choic == '4':
                xml_file()
            elif choic == '5':
                input_file = easygui.fileopenbox()
                zip(input_file)
            elif choic == '6':
                delete()
        except:
            print('Error. Try again')


def json_file():
    persons = []

    for i in range(3):
        persons.append(gen_person())
    with open('persons.json', 'w') as f:
        json.dump(persons, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

input()