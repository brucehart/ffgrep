#ffgrep - A Python-based file search utility
import argparse
import sys
import os
import subprocess

items_per_page = 10
line_length = 50

def setup_arg_parser():
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
        matches  = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if
                    line.lower().find(search_term.lower()) >= 0]
    else:
        matches  = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if line.find(search_term) >= 0]

    f.close()
    return matches

def print_results(results, search_term, start_line=1, ignore_case=True):
    for (num,line_match) in enumerate(results,start_line):
        filename = line_match[2]
        if ("\\" in filename):
            filename = filename.split("\\")[-1]

        line_data = str(line_match[1]).strip()

        if (ignore_case):
            item_idx = line_data.lower().find(search_term.lower())
        else:
            item_idx = line_data.lower().find(search_term.lower())

        start_idx = item_idx - (line_length - len(search_term))/2
        end_idx = item_idx + len(search_term) + (line_length - len(search_term))/2

        if (start_idx < 0):
            start_idx = 0
            end_idx = min(line_length, len(line_data))
        elif (end_idx > len(line_data)):
            start_idx -= (line_length - len(line_data))
            end_idx = min(line_length, len(line_data))

        if (start_idx < 0):
            start_idx = 0

        line_data = line_data[start_idx:end_idx]

        print "{3} : {0}[{1}]: {2}".format(filename, line_match[0], line_data, num)

if __name__ == '__main__':
    parser = setup_arg_parser()
    parser.set_defaults()
    args = parser.parse_args()

    search_matches = []

    for path in args.paths:
        print path
        if (os.path.isfile(path)):
            match_set = [find_matching_lines(path, args.pattern, True)]
        elif (os.path.isdir(path)):
            match_set = map(lambda x: find_matching_lines(x, args.pattern, True), get_files(path))
        else:
            match_set = []

        for match in match_set:
            map(lambda x: search_matches.append(x),match)

    current_page = 0
    print_results(search_matches[0:min(items_per_page, len(search_matches))], args.pattern, 1)

    while(True):
        print "Items [{0}:{1} of {2}]. Enter a match number, N for next page or X to exit"\
            .format(current_page*items_per_page+1,min((current_page+1)*items_per_page,
                    len(search_matches)),len(search_matches))

        openLine = sys.stdin.readline()

        if (openLine[0] == "n" or openLine[0] == "N"):
            current_page += 1
            if (len(search_matches) > current_page*items_per_page):
               print_results(search_matches[current_page*items_per_page:min((current_page+1)*items_per_page,
                             len(search_matches))], args.pattern, current_page*items_per_page+1)
            else:
                exit()
        elif (openLine[0] == "x" or openLine[0] == "X"):
            exit()
        else:
            try:
                viewLine = int(openLine)
            except:
                continue

            if (viewLine > 0 and viewLine <= len(search_matches)):
                os.system("\"C:\\Program Files (x86)\\Notepad++\\notepad++.exe\" {0} -n{1}".format(
                    search_matches[viewLine-1][2],search_matches[viewLine-1][0]))
                exit()

