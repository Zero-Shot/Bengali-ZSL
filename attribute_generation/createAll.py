import sys
from createS import runS
from createS4Split import run

if __name__ == '__main__':
    if len(sys.argv) < 4:
        exit("Not enough arguments given, needs alphabet csv, label/word txt and output s matrix")

    prefix = ""
    if len(sys.argv) > 4:
        prefix = sys.argv[4]

    alphabet_csv = sys.argv[1]
    word_txt = sys.argv[2]
    s_matrix_csv = sys.argv[3]

    run(alphabet_csv, word_txt, s_matrix_csv, prefix=prefix)
    runS(alphabet_csv, word_txt, s_matrix_csv, prefix=prefix)
