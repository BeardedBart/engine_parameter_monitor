import os, csv, re


def regex_func(basename):
    '''Modyfikuje nazwę pliku na "modded"'''

    regex1 = re.compile(r"(\.)|(\_{6}\.)")
    string = regex1.sub("_modded.", basename)

    return string


def mod(file, fout, dir, data_dir):
    os.chdir(data_dir)
    # sprawdź czy folder "Data_mod" istnieje
    if os.path.isdir(r"{}\DataMod".format(dir)) != True:
        os.mkdir(r"{}\DataMod".format(dir))

    # NOTE: najpierw część regexFunc.py
    temp_fin = os.path.abspath(file)
    basename = os.path.basename(regex_func(os.path.basename(temp_fin)))
    dirname = os.path.abspath(r"{}\DataMod".format(dir))
    # zmiana co do programu, bo musi zmienić on folder
    fout = os.path.join(dirname, basename)

    with open(file, "r") as fin, open(fout, "w", newline="") as fout:
        reader = csv.reader(fin, skipinitialspace=True)
        writer = csv.writer(fout)
        for index, row in enumerate(reader):
            if index > 0:
                writer.writerow(list(row))

    print("Edycja pliku zakończona")
