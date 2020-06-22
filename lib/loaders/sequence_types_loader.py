import csv


def load_sequence_types(path="../data/sequence_types.csv"):
    pos_sequences = {}
    neg_sequences = {}
    pass_sequences = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            if row[0] in pos_sequences.keys():
                pos_sequences[row[0]].append((row[1], None if row[2] == "" else row[2]))
                neg_sequences[row[0]].append((row[1], None if row[3] == "" else row[3]))
                pass_sequences[row[0]].append((row[1], None if row[4] == "" else row[4]))
            else:
                pos_sequences[row[0]] = [(row[1], None if row[2] == "" else row[2])]
                neg_sequences[row[0]] = [(row[1], None if row[3] == "" else row[3])]
                pass_sequences[row[0]] = [(row[1], None if row[4] == "" else row[4])]
    return pos_sequences, neg_sequences, pass_sequences

