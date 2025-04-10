import yaml
import configparser
import argparse
import os
import re


config = configparser.ConfigParser(interpolation=None, allow_no_value=True)

parser = argparse.ArgumentParser(prog='TabbyToMobaXTerm')
parser.add_argument("-i", "--input",
    default="config.yaml",
    help="Input file (default: config.yaml)")
parser.add_argument("-o", "--output",
    default="tabbytomobaxterm",
    help="Output file (default: tabbytomobaxterm)")

binds = {
    'ssh': '109',
    'local': '151',
    'serial': '131'
}
args = parser.parse_args()

data = {}
if not os.path.exists(args.input):
    print(f"{args.input} doesn't exist. Aborting!")
    raise SystemExit

with open(args.input) as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

items = {'ungrouped': []}
for profile in data['profiles']:
    ptype = profile['type']
    pname = profile['name']
    entry = {
        'type_translated': binds[ptype],
        'type': ptype,
        'name': pname
    }

    if ptype == 'ssh':
        entry['host'] = profile['options']['host'] if 'host' in profile['options'] else 'localhost'
        entry['user'] = profile['options']['user'] if 'user' in profile['options'] else 'root'
        entry['port'] = profile['options']['port'] if 'port' in profile['options'] else '22'

    if 'group' in profile:  # Grouped stuff
        if not profile['group'] in  items:
            items[profile['group']] = [entry]
        else:
            items[profile['group']].append(entry)
    else:  # Ungrouped stuff
        items['ungrouped'].append(entry)

sessions_file = 'MobaXterm Sessions.mxtsessions'
if os.path.exists(sessions_file):
    config.read(sessions_file)
else:
    print("MobaXterm Sessions.mxtsessions not found. Creating file from scratch.")

sections = config.sections()
sections.sort(reverse=True)
last_section = 1

try:
    last_section = int(re.sub(r'^.*_(\d+)$', r'\1', sections[0]))
except IndexError:
    last_section = 0

section_id = last_section + 1
config.add_section(f'Bookmarks_{section_id}')
config[f'Bookmarks_{section_id}']['SubRep'] = 'Tabby sessions'
config[f'Bookmarks_{section_id}']['ImgNum'] = '63'
last_section += 1

for idx, key in enumerate(items):
    section_id = last_section + idx + 1
    config.add_section(f'Bookmarks_{section_id}')
    config[f'Bookmarks_{section_id}']['SubRep'] = f'Tabby sessions\\{key}'
    config[f'Bookmarks_{section_id}']['ImgNum'] = '41'
    for item in  items[key]:
        if item['type'] == 'ssh':
            entry = f"#{item['type_translated']}#0%{item['host']}%{item['port']}%{item['user']}"
            entry += "% %-1%-1% %%22%%0%0%Interactive shell%"
            config[f'Bookmarks_{section_id}'][item['name']] = entry

outputfilename = args.output + (".mxtsessions" if not args.output.endswith(".mxtsessions") else "")
with open(outputfilename, 'w') as out:
    config.write(out)
    print(f"{outputfilename} written.")
