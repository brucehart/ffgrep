#ffgrep - A Python-based file search utility
import argparse
import os
import sys

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
        matches  = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if line.lower().find(search_term.lower()) >= 0]
    else:
        matches  = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if line.find(search_term) >= 0]

    f.close()
    return matches

def print_results(results, search_term, start_line=1):
    for (num,line_match) in enumerate(results,start_line):
        filename = line_match[2]
        if ("\\" in filename):
            filename = filename.split("\\")[-1]

        line_data = line_match[1][0:line_length]

        #print line_data
        #term_idx = line_data.index(search_term)

        #if (len(line_data) > line_length):
            #need more logic here to center the term
        #    line_data = line_data[0:line_length]

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
    print_results(search_matches[0:min(items_per_page, len(search_matches))], 1)

    while(True):
        openLine = sys.stdin.readline()

        if (openLine[0] == "n" or openLine[0] == "N"):
            current_page += 1
            if (len(search_matches) > current_page*items_per_page):
               print_results(search_matches[current_page*items_per_page:min((current_page+1)*items_per_page,len(search_matches))], args.pattern, current_page*items_per_page+1)
            else:
                exit()
        elif (openLine[0] == "x" or openLine[0] == "X"):
            exit()
        else:
            viewLine = int(openLine)

            if (viewLine > 0 and viewLine <= len(search_matches)):
                os.system("\"C:\\Program Files (x86)\\Notepad++\\notepad++.exe\" {0} -n{1}".format(search_matches[viewLine-1][2],search_matches[viewLine-1][0]))

