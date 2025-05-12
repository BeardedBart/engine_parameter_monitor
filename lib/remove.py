def remove_empty(data_dir):
    import os, csv, send2trash

    filesToRemove = []

    os.chdir(data_dir)

    for file in os.listdir(data_dir):
        with open(file, "r") as f:
            csv_dict = [row for row in csv.DictReader(f)]
            if len(csv_dict) == 0:
                print(file)
                filesToRemove.append(
                    file
                )  # trzeba tak zrobić, bo to pętla otwierająca program
                # nie można z tego poziomu usunąć pliku

    counter = len(filesToRemove)

    for i in filesToRemove:
        send2trash.send2trash(i)

    if counter == 0:
        print("Nie ma pustych plików.")
        return False
    else:
        print(f"Usunięto {counter} pustych plików!")
        return True
