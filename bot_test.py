import csv


def main():
    fnames = []
    lnames = []
    phones = []
    classes = []

    with open('fbot.csv', encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            fnames.append(row[1][::-1])
            lnames.append(row[2][::-1])
            phones.append(row[3])
            classes.append(row[4][::-1])

    print(fnames[1:])
    print(lnames[1:])
    print(phones[1:])
    print(classes[1:])


if __name__ == "__main__":
    main()