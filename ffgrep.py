import argparse

def setup_parser():
    parser = argparse.ArgumentParser(description="Search for a string in the specified file or path.")

    parser.add_argument('pattern', metavar='S', type=str,
                        help='search pattern')

    parser.add_argument('paths', default='.', nargs='*',
                        help='file(s) and/or path(s) to search (default is local directory)')

    parser.add_argument('-i','--ignore-case', action='store_const', const=True,
                        help='ignore case in the search term')

    return parser



if __name__ == '__main__':
    parser = setup_parser()
    parser.set_defaults()
    args = parser.parse_args()


    print args.ignore_case