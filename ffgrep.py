#ffgrep - A Python-based file search utility
import argparse
import sys
import os

#command to execute to open a text editor to the matching file and line
#param {0} is the full file path and {1} is the line number
TEXT_EDITOR_COMMAND = "\"C:\\Program Files (x86)\\Notepad++\\notepad++.exe\" {0} -n{1}"

#default values for numbered parameters. user can change via command line parameters
DEFAULT_ITEMS_PER_PAGE = 25
DEFAULT_LINE_LENGTH = 50

items_per_page = DEFAULT_ITEMS_PER_PAGE
line_length = DEFAULT_LINE_LENGTH

#set up command line parser using the argparse library
def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Search for a string in the specified file or path.")

    parser.add_argument('pattern', metavar='pattern', type=str,
                        help='search pattern')

    parser.add_argument('paths', default='.', nargs='*',
                        help='file(s) and/or path(s) to search (default is local directory)')

    parser.add_argument('-i','--ignore-case', action='store_const', const=True,
                        help='ignore case in the search term')

    parser.add_argument('-n','--no-subdir', action='store_const', const=True,
                        help='do not look in sub-directories of the search directories')

    parser.add_argument('-p', '--items_per_page', nargs='?', type=int,
                        default=DEFAULT_ITEMS_PER_PAGE, help='number of items to list per page')

    parser.add_argument('-l', '--line_length', nargs='?', type=int,
                        default=DEFAULT_LINE_LENGTH, help='length of each match result line')

    return parser

#retrieves a list of files for a given path
def get_files(path, include_subs=True):
    file_list = []

    #use os.walk if we are including subdirectories, otherwise just traverse the list of files
    if (include_subs):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root,file))
    else:
        for file in os.listdir(path):
            file_list.append(os.path.join(path,file))

    return file_list

#retrieves a list of lines that include the search term
#results are tuples containing (line number, line text, file path)
def find_matching_lines(filepath, search_term, ignore_case=False):
    f = open(filepath)
    data = f.readlines()

    #if we are ignoring case, cast the search term and line data into lower case before searching
    if (ignore_case):
        matches = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if
                    line.lower().find(search_term.lower()) >= 0]
    else:
        matches = [(num+1,line.strip(),filepath) for num,line in enumerate(data) if line.find(search_term) >= 0]

    f.close()
    return matches

#prints a set of results based on a set of tuple matches
def print_results(results, search_term, start_line=1, ignore_case=True):
    for (num,line_match) in enumerate(results,start_line):
        filename = line_match[2]

        #the filename is the data after the last "\" in the path
        if (os.sep in filename):
            filename = filename.split(os.sep)[-1]

        line_data = str(line_match[1]).strip()

        #find the location where the search term is first found to display the appropriate line subsection
        if (ignore_case):
            item_idx = line_data.lower().find(search_term.lower())
        else:
            item_idx = line_data.lower().find(search_term.lower())

        #slice the data so the search term is centered on the printed line
        start_idx = item_idx - (line_length - len(search_term))/2
        end_idx = item_idx + len(search_term) + (line_length - len(search_term))/2

        if (start_idx < 0):
            start_idx = 0
            end_idx = min(line_length, len(line_data))
        elif (end_idx > len(line_data)):
            start_idx -= max(0,(line_length - len(line_data)))
            end_idx = min(line_length, len(line_data))

        line_data = line_data[start_idx:end_idx]

        print "{3} : {0}[{1}]: {2}".format(filename, line_match[0], line_data, num)

#script is intended to be executed interactively from the command line
#basic usage: python ffgrep.py search_term file_path
if __name__ == '__main__':
    parser = setup_arg_parser()
    parser.set_defaults()
    args = parser.parse_args()

    items_per_page = int(args.items_per_page)
    line_length = int(args.line_length)

    search_matches = []

    for path in args.paths:
        if (os.path.isfile(path)):
            match_set = [find_matching_lines(path, args.pattern, True)]
        elif (os.path.isdir(path)):
            match_set = map(lambda x: find_matching_lines(x, args.pattern, True), get_files(path))
        else:
            match_set = []

        for match in match_set:
            map(lambda x: search_matches.append(x),match)

    if (len(search_matches) == 0):
        print "No matches found. Exiting..."
        exit()

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
                os.system(TEXT_EDITOR_COMMAND.format(
                    search_matches[viewLine-1][2],search_matches[viewLine-1][0]))
                exit()

