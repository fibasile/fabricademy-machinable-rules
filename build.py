"""Build script for machine-friendly eval rules"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import sys
import traceback
import os
import json
from cStringIO import StringIO
import codecs
import glob
import yaml
from datetime import datetime
import re
SOURCE_DIR = os.path.join(os.getcwd(), 'src')
JSON_DIR = os.path.join(os.getcwd(), 'public/json')
GITBOOK_DIR = os.path.join(os.getcwd(), 'public/gitbook')
SOURCE_FILES = glob.glob(os.path.join(SOURCE_DIR, '*.yaml'))

def UTFWriter():
    buffer = StringIO()
    wrapper = codecs.getwriter("utf8")(buffer)
    wrapper.buffer = buffer
    return wrapper


def read_yaml(yaml_src):
    """ Read a yamls file """
    print 'Reading %s' % yaml_src
    yaml_file = open(yaml_src, 'r')
    yaml_data = yaml.full_load(yaml_file.read())
    yaml_file.close()
    return yaml_data


def make_task(task):
    """ Create a Markdown fragment for a task """
    task_md = UTFWriter()
    # print >> task_md, '## %s\n' % task['name']
    if task['description']:
        print >> task_md, task['description']
    print >> task_md, '**Learning outcomes**\n'
    for task_outcome in task['outcomes']:
        print >> task_md, '- %s' % task_outcome
    print >> task_md, '\n**Student checklist**\n'
    for task_checklist in task['checklist']:
        print >> task_md, '- [x] %s' % task_checklist
    return task_md.buffer.getvalue()


def make_book_page(unit_data, loop_index):
    """ Create a Markdown version of a unit """
    md_buffer = UTFWriter()
    print >> md_buffer, '## %i. %s\n' % (loop_index, unit_data['unit'])
    for task in unit_data['tasks']:
        print >> md_buffer, make_task(task)
    if "None yet" not in unit_data['faq']:
        print >> md_buffer, '**FAQ**\n'
        # faq_md = unit_data['faq'].replace("Q: ", "!!! question \"") + "\""
        faq_md = re.sub(r"Q: (.*)$", "!!! question \"\\g<1>\"", unit_data['faq'], 0, re.MULTILINE)
        faq_md = re.sub(r"A:", "   ", faq_md)
        print >> md_buffer, faq_md
    return md_buffer.buffer.getvalue()

def add_to_book(tmp_file, md_data):
    tmp_file.write(md_data)

def selectionSort(List):
    for i in range(len(List) - 1):
        minimum = i
        for j in range( i + 1, len(List)):
            j_date = datetime.strptime(List[j]['date'], "%Y-%m-%d")
            min_date = datetime.strptime(List[minimum]['date'], "%Y-%m-%d")
            if(j_date < min_date):
                minimum = j
        if(minimum != i):
            List[i], List[minimum] = List[minimum], List[i]
    return List

# fn built by chatgpt
def extract_date_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        # Check if 'date' field exists in the JSON file
        if 'date' in data:
            return data['date'], file_path
        else:
            print("No 'date' field found in {}".format(file_path))
            return None, file_path

def writeRulesList(JsonList):
    """ write rules file """
    md_buffer = UTFWriter()
    print >> md_buffer, '['
    urlist_len = len(JsonList)-1
    index = 0

    date_list = []
    # Loop through the JSON files and extract the date field
    for file in JsonList:
        date_str, file_name = extract_date_from_json(os.path.join(JSON_DIR, file))
        
        if date_str:
            # Convert the date string to a datetime object for sorting
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_list.append((date_obj, file))

    # Sort the list of tuples by date (first element)
    sorted_files = sorted(date_list, key=lambda x: x[0])

    for date_obj, file in sorted_files:
        index += 1
        print >> md_buffer, '\t"{0}"{1}'.format(file, ("," if index <= urlist_len else ""))
    print >> md_buffer, ']'
    tmp_file = codecs.open(
        os.path.join(JSON_DIR, 'rules.json'), 'w', encoding='utf-8')
    tmp_file.write(md_buffer.getvalue())
    tmp_file.close()
    print('Wrote rules.json file with list')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: build.py [command]\n'
        print 'Available commands'
        print '   test: Check if file syntax is ok'
        print '   json: Export rules to nueval-app json'
        print '   gitbook: Build markdown pages from YAML source\n\n'
        sys.exit(-1)
    BUILD_CMD = sys.argv[1]

    if BUILD_CMD == 'gitbook':
        heading_index = 1
        if not os.path.exists(GITBOOK_DIR):
            os.makedirs(GITBOOK_DIR)
        yaml_list = []
        for source in SOURCE_FILES:
            yaml_list.append(read_yaml(source))
        orderedYamlList = selectionSort(yaml_list)
        try:
            gitbook_file = codecs.open(
                os.path.join(GITBOOK_DIR, 'criteria.md'), 'w', encoding='utf-8')
        except Exception, ex:
            traceback.print_exc()

        for data in orderedYamlList:
            try:
                md_data = make_book_page(data, heading_index)
                md_data = md_data + "---\n\n"
                add_to_book(gitbook_file, md_data)
                # tmp_file.close()
                heading_index += 1
            except Exception, ex:
                traceback.print_exc()

        print 'Saved to criteria.md'
        gitbook_file.close()

    RulesFileList = []
    for source in SOURCE_FILES:
        if BUILD_CMD == 'test':
            try:
                read_yaml(source)
                print 'Syntax OK'
            except Exception, ex:
                print 'Syntax Error'
                traceback.print_exc()
        elif BUILD_CMD == 'json':
            if not os.path.exists(JSON_DIR):
                os.makedirs(JSON_DIR)
            try:
                data = read_yaml(source)
                for t in data['tasks']:
                    if not t['description']:
                       t['description']=''
                data['faq'] = data['faq'].replace("Q: ", "### ")
                data['faq'] = data['faq'].replace("A: ", "> ")
                jsonFile = os.path.basename(source).replace('.yaml', '.json')
                jsonData = json.dumps(data, indent=4)
                print 'Save to %s' % jsonFile
                tmp_file = codecs.open(
                    os.path.join(JSON_DIR, jsonFile), 'w', encoding='utf-8')
                tmp_file.write(jsonData)
                tmp_file.close()
                RulesFileList.append(jsonFile)
            except Exception, ex:
                print 'Syntax Error'
                traceback.print_exc()
        # elif BUILD_CMD == 'gitbook':

    if BUILD_CMD == 'json':
        writeRulesList(RulesFileList)

