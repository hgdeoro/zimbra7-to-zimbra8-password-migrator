import re
import sys

# $ zmmailbox -z -m username@domain.tld search -l 200 "in:/inbox (before:today)"
# num: 200, more: true
#
#         Id  Type   From                  Subject                                             Date
#    -------  ----   --------------------  --------------------------------------------------  --------------
# 1. -946182  conv   admin                 Daily mail report                                   09/24/15 23:57
# 2.  421345  conv   John                  Some great news for you                             09/24/15 23:57

REGEX_HEAD = re.compile(r'^Id')
REGEX_HEAD_SEP = re.compile(r'^---')

REGEX_DATA = re.compile(r'^(\d+)\.\s+\-?(\d+)\s+(\S+)')


def main():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]

    while True:
        line = lines.pop(0)
        if REGEX_HEAD.search(line):
            break

    line = lines.pop(0)
    assert REGEX_HEAD_SEP.search(line)

    ids = []

    for line in lines:
        matched = REGEX_DATA.match(line)
        if matched:
            ids.append(matched.group(2))
        else:
            sys.stderr.write("Couldn't parse line: {0}\n".format(line))
            sys.exit(1)

    for an_id in ids:
        print an_id

if __name__ == '__main__':
    main()