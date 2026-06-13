import os
import sys
import uuid
from multiprocessing import Pool, cpu_count


def slit(a, b):
    otvet = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            otvet.append(a[i])
            i += 1
        else:
            otvet.append(b[j])
            j += 1
    otvet.extend(a[i:])
    otvet.extend(b[j:])
    return otvet


def sort_slianiem(massiv):
    if len(massiv) <= 1:
        return massiv
    seredina = len(massiv) // 2
    return slit(sort_slianiem(massiv[:seredina]), sort_slianiem(massiv[seredina:]))


def sort_kuska(dannie):
    chisla, put_kuska = dannie
    sort_chisla = sort_slianiem(chisla)
    with open(put_kuska, "w", encoding="ascii") as fayl:
        for chislo in sort_chisla:
            fayl.write(f"{chislo}\n")
    return put_kuska


if __name__ == "__main__":
    vhod = os.path.abspath(sys.argv[1])
    pamyat = int(sys.argv[2])
    papka = os.path.dirname(vhod)
    imya, rassh = os.path.splitext(vhod)
    vyhod = imya + ".sorted" + rassh

    potoki = cpu_count()
    razmer_kuska = pamyat // potoki

    spisok_kuskov = []
    pachka = []
    nomer = 0

    with open(vhod, "r", encoding="ascii") as f_vhod:
        for stroka in f_vhod:
            pachka.append(int(stroka.strip()))
            if len(pachka) >= razmer_kuska:
                tmp_fayl = os.path.join(papka, f".chunk_{nomer}.tmp")
                spisok_kuskov.append((pachka, tmp_fayl))
                pachka = []
                nomer += 1

    tmp_fayl = os.path.join(papka, f".chunk_{nomer}.tmp")
    spisok_kuskov.append((pachka, tmp_fayl))

    with Pool(potoki) as pool:
        sort_kuski = pool.map(sort_kuska, spisok_kuskov)

    uroven = sort_kuski
    while len(uroven) > 1:
        nov_uroven = []
        i = 0
        pary = []

        while i < len(uroven):
            if i + 1 < len(uroven):
                nov_fayl = os.path.join(papka, f".merged_{uuid.uuid4().hex}.tmp")
                pary.append((uroven[i], uroven[i + 1], nov_fayl))
                i += 2
            else:
                nov_uroven.append(uroven[i])
                i += 1

        for fayl_a, fayl_b, nov_fayl in pary:
            with open(fayl_a, "r", encoding="ascii") as f1, \
                 open(fayl_b, "r", encoding="ascii") as f2, \
                 open(nov_fayl, "w", encoding="ascii") as f_itog:

                stroka1 = f1.readline()
                stroka2 = f2.readline()

                while stroka1 and stroka2:
                    if int(stroka1) <= int(stroka2):
                        f_itog.write(stroka1)
                        stroka1 = f1.readline()
                    else:
                        f_itog.write(stroka2)
                        stroka2 = f2.readline()

                if stroka1:
                    f_itog.write(stroka1)
                    f_itog.writelines(f1)
                if stroka2:
                    f_itog.write(stroka2)
                    f_itog.writelines(f2)

            os.remove(fayl_a)
            os.remove(fayl_b)
            nov_uroven.append(nov_fayl)

        uroven = nov_uroven

    os.replace(uroven[0], vyhod)
