import binascii  #преобразования между двоичной и ASCII
import hashlib
import itertools  #повышает эффективность работы с циклами и генераторами последовательностей объектов
import multiprocessing  #параллельная обработка
import string
from datetime import datetime
from functools import partial  #работа с функциями высшего порядка

hsh = '1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad', '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b', '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f'






alphabet = string.ascii_lowercase.encode() #инициализированная строка,
#используемая в качестве строковой константы. Cтрока
#ascii_lowercase будет содержать строчные буквы «abcdefghijklmnopqrstuvwxyz»


def sha256(data):
    return hashlib.sha256(data).digest() #Эта функция используется для создания хэш-объекта SHA-256


def check_sha256(repls_parent, bytes_format, n, target_sha256):
    for repls in itertools.product(alphabet, repeat=n): #Возвращает генератор, выдающий «декартово произведение» для элементов указанных объектов
        data = bytes_format % (repls_parent + repls)
        if sha256(data) == target_sha256: #установка доп.констант
            return data


def brute_force2(mask, target_sha256, n_cutoff=4): #Подбор части пароля перебором
    bytes_format = mask.replace(b'%', b'%%').replace(b'*', b'%c')
    mp_check = partial(check_sha256,
                       bytes_format=bytes_format,
                       n=min(n_cutoff, mask.count(b'*')),
                       target_sha256=target_sha256)
    n = max(0, mask.count(b'*') - n_cutoff)
    all_repls_parent = itertools.product(alphabet, repeat=n) #возвращает кол-во символов
    with multiprocessing.Pool() as pool:
        for data in pool.imap_unordered(mp_check, all_repls_parent):
            if data is not None:
                return data

if __name__ == '__main__':
    print('ХЭШ:\n1 - ',hsh[0],'\n2 - ',hsh[1],'\n3 - ',hsh[2])
    A = int(input('Выберете ХЭШ\n>>  '))
    n = int(input('Введите количество потоков\n>>  '))

    start_time = datetime.now() #идет отсчет времени
    passw_bytes = brute_force2(b'*****', binascii.unhexlify(hsh[A - 1]), n)#вызывается функция подбора пароля
    print('пароль = ', passw_bytes.decode())
    print('Время обработки = ', datetime.now() - start_time)



