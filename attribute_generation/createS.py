import csv
import sys
import warnings
import io
import os

import numpy as np


def get_number_of_words(txt_file):
    with io.open(txt_file, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def get_number_of_columns(alphabet_csv):
    with io.open(alphabet_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', skipinitialspace=True)
        return len(next(reader))


def create_alphabet_dictionary(alphabet_csv):
    alphabet_dict = dict()

    with io.open(alphabet_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', skipinitialspace=True)

        for index, line in enumerate(reader):
            alphabet_dict[line[0]] = index

    return alphabet_dict


def write_s_file(write_file, matrix, words):
    with io.open(write_file, "w+", encoding="utf-8") as file:
        for row_number, row in enumerate(matrix):
            file.write(words[row_number] + "," + ",".join(np.char.mod('%f', row)) + "\n")

def create_s(alphabet_csv, word_txt, s_matrix_csv):
    number_of_words = get_number_of_words(word_txt)
    alphabet_dict = create_alphabet_dictionary(alphabet_csv)
    csv_num_cols = get_number_of_columns(alphabet_csv)
    numpy_csv = np.genfromtxt(alphabet_csv, dtype=float, delimiter=",", filling_values=1, encoding="utf-8")
    s_matrix = np.zeros((number_of_words, csv_num_cols))

    word_list = []

    with io.open(word_txt, "r", encoding="utf-8") as file:
        for word_index, line in enumerate(file):
            word = line.rstrip()
            word_list.append(word)
            numpy_word = None

            for letter in word:
                if letter is '\n':
                    continue

                try:
                    letter_index = alphabet_dict[letter]
                    s_matrix[word_index] += numpy_csv[letter_index]
                except KeyError:
                    warnings.warn("Key '%s' not found in dictionary" % (letter))

            divider = s_matrix[word_index][0]
            s_matrix[word_index][0] = 1 / divider

            for col_index in range(1, csv_num_cols):
                s_matrix[word_index][col_index] = s_matrix[word_index][col_index] / divider

    write_s_file(s_matrix_csv, s_matrix, word_list)

def runS(alphabet_csv, word_txt, s_matrix_csv, out_dir="out", prefix=""):
    if os.path.isdir(word_txt):
        outpath = os.path.join(word_txt, out_dir)
        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        for file in os.listdir(word_txt):
            file_path = os.path.join(word_txt, file)
            if os.path.isfile(file_path) and file.endswith(".txt"):
                create_s(alphabet_csv, file_path, os.path.join(outpath, prefix + "Smatrix_" + os.path.basename(file)))
    else:
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        create_s(alphabet_csv, word_txt, os.path.join(out_dir, s_matrix_csv))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        exit("Not enough arguments given, needs alphabet csv, label/word txt and output s matrix")

    alphabet_csv = sys.argv[1]
    word_txt = sys.argv[2]
    s_matrix_csv = sys.argv[3]

    runS(alphabet_csv, word_txt, s_matrix_csv)
