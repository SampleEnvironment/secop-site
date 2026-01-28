import pathlib
import sys

sourcedir = pathlib.Path(sys.argv[1])
destdir = pathlib.Path(sys.argv[2])

rfcs = []

for rfc in sourcedir.glob('RFC-*.rst'):
    if rfc.name.startswith(('RFC-000', 'RFC-template')):
        continue

    n = rfc.name.split('-')[1]

    with open(rfc, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert lines[0].startswith('- Feature: ')
    raw_title = lines[0][10:].strip()
    title = f'RFC {n}: {raw_title}'
    assert lines[1].startswith('- Status: ')
    status = lines[1][10:].strip()
    lines[:1] = [
        '.. _rfc-' + n + ':\n',
        '\n',
        title + '\n',
        '@' * len(title) + '\n',
        '\n',
    ]

    new_name = rfc.name.removeprefix('RFC-')

    dest_file = destdir / new_name
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    rfcs.append((new_name.removesuffix('.rst'), n, raw_title, status))

rfcs.sort()

with open(destdir / 'index.rst', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(destdir / 'index.rst', 'w', encoding='utf-8') as f:
    for line in lines:
        if line.strip() == '.. toctree::':
            f.write(line)
            f.write('   :maxdepth: 1\n')
            f.write('   :hidden:\n\n')
            for ref in rfcs:
                f.write(f'   {ref[0]}\n')

            f.write('\n')
            f.write('.. list-table::\n')
            f.write('   :widths: 10 70 20\n')
            f.write('   :header-rows: 1\n\n')
            f.write('   * - #\n')
            f.write('     - Title\n')
            f.write('     - Status\n')
            for ref, n, title, status in rfcs:
                f.write(f'   * - {n}\n')
                f.write(f'     - :ref:`{title} <rfc-{n}>`\n')
                f.write(f'     - {status}\n')

            break

        f.write(line)
