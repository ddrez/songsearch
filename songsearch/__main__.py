import argparse

if __name__ == '__main__':

    example_text = """example:
     python -m %(prog)s index "music/**/*.mp3"
     python -m %(prog)s search "some query"

     """
    
    parser = argparse.ArgumentParser(prog='songsearch',
                                     description='Search songs by lyrics',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter
                                     )

    parser.add_argument('cmd', help="Action to perform", choices=['index','search'])
    parser.add_argument('arg', help="Glob pattern for index of Query string for search")
    parser.add_argument('-l', '--language', help="Transcribe into specific language (e.g. fr, it)")

    args = parser.parse_args()

    from .songsearch import index, search

    if args.cmd == 'index':
        index(args.arg, args.language)

    elif args.cmd == 'search':
        search(args.arg)
