import argparse
import os

def setup_parser():
    parser = argparse.ArgumentParser(description="Search for a string in the specified file or path.")

    parser.add_argument('pattern', metavar='S', type=str,
                        help='search pattern')

    parser.add_argument('paths', default='.', nargs='*',
                        help='file(s) and/or path(s) to search (default is local directory)')

    parser.add_argument('-i','--ignore-case', action='store_const', const=True,
                        help='ignore case in the search term')

    parser.add_argument('-n','--no-subdir', action='store_const', const=True,
                        help='do not look in sub-directories of the search directories')
    return parser

def get_files(path, include_subs=True):
    file_list = []

    if (include_subs):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root,file))
    else:
        for file in os.listdir(path):
            file_list.append(os.path.join(path,file))

    return file_list

def find_matching_lines(filepath, search_term, ignore_case=False):
    f = open(filepath)
    data = f.readlines()

    if (ignore_case):
        matches  = [(num+1,line) for num,line in enumerate(data) if line.lower().find(search_term.lower()) >= 0]
    else:
        matches  = [(num+1,line) for num,line in enumerate(data) if line.find(search_term) >= 0]

    f.close()
    return matches


if __name__ == '__main__':
    parser = setup_parser()
    parser.set_defaults()
    args = parser.parse_args()

    print find_matching_lines("ffgrep.py", args.pattern, True)