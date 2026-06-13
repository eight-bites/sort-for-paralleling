import os
import sys


def slit_spiskov(list1, list2):
    result = []
    x = 0
    y = 0
    while x < len(list1) and y < len(list2):
        if list1[x] <= list2[y]:
            result.append(list1[x])
            x = x + 1
        else:
            result.append(list2[y])
            y = y + 1
    for i in range(x, len(list1)):
        result.append(list1[i])
    for j in range(y, len(list2)):
        result.append(list2[j])
    return result


def sort_slianiem(data):
    if len(data) <= 1:
        return data
    sered = len(data) // 2
    levo = sort_slianiem(data[:sered])
    pravo = sort_slianiem(data[sered:])
    return slit_spiskov(levo, pravo)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ispolzovanie: python3 sort_ne_tot.py <fayl> <pamyat>")
        sys.exit(1)

    file_name = sys.argv[1]
    pamyat = int(sys.argv[2])

    if pamyat < 1:
        print("pamyat dolzhna byt >= 1")
        sys.exit(1)

    file_name = os.path.abspath(file_name)
    if not os.path.isfile(file_name):
        print("fayl ne nayden:", file_name)
        sys.exit(1)

    print("nachinayu sortirovku...")
    print("fayl:", file_name)

    papka = os.path.dirname(file_name) or "."
    imya, rassh = os.path.splitext(file_name)
    vyhodnoy = imya + ".sorted" + rassh

    spisok_vremennyh = []
    pachka = []
    nomer_kuska = 1

    with open(file_name, "r", encoding="ascii") as f:
        for stroka in f:
            stroka = stroka.strip()
            if stroka == "":
                continue
            pachka.append(int(stroka))
            if len(pachka) >= pamyat:
                print("sortiruem kusek", nomer_kuska)
                otsort = sort_slianiem(pachka)
                tmp_name = os.path.join(papka, "tmp" + str(nomer_kuska) + ".txt")
                with open(tmp_name, "w", encoding="ascii") as tmp_f:
                    for elem in otsort:
                        tmp_f.write(str(elem) + "\n")
                spisok_vremennyh.append(tmp_name)
                pachka = []
                nomer_kuska = nomer_kuska + 1

    if len(pachka) > 0:
        print("sortiruem posledniy kusek")
        otsort = sort_slianiem(pachka)
        tmp_name = os.path.join(papka, "tmp" + str(nomer_kuska) + ".txt")
        with open(tmp_name, "w", encoding="ascii") as tmp_f:
            for elem in otsort:
                tmp_f.write(str(elem) + "\n")
        spisok_vremennyh.append(tmp_name)

    if len(spisok_vremennyh) == 0:
        open(vyhodnoy, "w").close()
        print("gotovo!!!")
        print("rezultat v fayle:", vyhodnoy)
        sys.exit(0)

    print("kuski gotovy, teper sliyayu...")

    fayly = spisok_vremennyh
    schetchik = 100
    while len(fayly) > 1:
        novie = []
        i = 0
        while i < len(fayly):
            if i + 1 < len(fayly):
                nov_imya = os.path.join(papka, "merge" + str(schetchik) + ".txt")
                schetchik = schetchik + 1

                with open(fayly[i], "r", encoding="ascii") as f1, \
                     open(fayly[i + 1], "r", encoding="ascii") as f2, \
                     open(nov_imya, "w", encoding="ascii") as fout:

                    s1 = f1.readline()
                    s2 = f2.readline()
                    while s1 and s2:
                        if int(s1) <= int(s2):
                            fout.write(s1)
                            s1 = f1.readline()
                        else:
                            fout.write(s2)
                            s2 = f2.readline()

                    if s1:
                        fout.write(s1)
                        fout.writelines(f1)
                    if s2:
                        fout.write(s2)
                        fout.writelines(f2)

                os.remove(fayly[i])
                os.remove(fayly[i + 1])
                novie.append(nov_imya)
                i = i + 2
            else:
                novie.append(fayly[i])
                i = i + 1
        fayly = novie

    if os.path.exists(vyhodnoy):
        os.remove(vyhodnoy)
    os.replace(fayly[0], vyhodnoy)

    print("gotovo!!!")
    print("rezultat v fayle:", vyhodnoy)
