
def spell_check(server_filename):
    """
    http://openbookproject.net/courses/python4fun/spellcheck.html
    :return:
    """
    correct_words = open("correct.words").readlines()
    correct_words = [word.strip() for word in correct_words]
    rcv_file = open(server_filename).readlines()
    modified_lines = []
    for i, line in enumerate(rcv_file):  # for each line
        line = line.strip()
        file_words = line.split()
        for j, txt_word in enumerate(file_words):  # for each word in a line
            if txt_word not in correct_words:
                file_words[j] = f"[{txt_word}]"
        modified_lines.append(' '.join(file_words) + '\n')
    f = open('modified.txt', 'a')
    f.writelines(modified_lines)
    f.close()

    return rcv_file


def main():
    server_filename = '../client/file1.txt'
    rcv_file = spell_check(server_filename)
    print(rcv_file)


if __name__ == '__main__':
    main()
