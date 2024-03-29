# /usr/bin/env python3
# Between 2 PO files, copy the header (and only the header) from one to the other.
import sys


def find_po_header(lines):
    """Find the po header, starting from 'msgid ""' to the next empty line."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == 'msgid ""':
            start = i
        if start is not None and line.strip() == '':
            return (start, i + 1)
    return None


if __name__ == '__main__':
    with open(sys.argv[1]) as src_file:
        src = src_file.read().split('\n')
    with open(sys.argv[2]) as dst_file:
        dst = dst_file.read().split('\n')

    src_header = find_po_header(src)
    dst_header = find_po_header(dst)

    if src_header and dst_header:
        dst[dst_header[0]:dst_header[1]] = src[src_header[0]:src_header[1]]

        # Apart from the header, we also mimic the trailing newline style of the source file
        src_trailing = src[-1] == ''
        dst_trailing = dst[-1] == ''

        if src_trailing and not dst_trailing:
            dst.append('')
        if not src_trailing and dst_trailing:
            dst.pop()

        with open(sys.argv[2], 'w') as dst_file:
            dst_file.write('\n'.join(dst))
