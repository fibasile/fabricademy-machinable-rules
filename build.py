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
SOURCE_DIR = os.path.join(os.getcwd(), 'src')
JSON_DIR = os.path.join(os.getcwd(), 'json')
GITBOOK_DIR = os.path.join(os.getcwd(), 'gitbook')
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
    yaml_data = yaml.load(yaml_file.read())
    yaml_file.close()
    return yaml_data


def make_task(task):
    """ Create a Markdown fragment for a task """
    task_md = UTFWriter()
    print >> task_md, '## %s\n' % task['name']
    print >> task_md, task['description']
    print >> task_md, '### Learning outcomes\n'
    for task_outcome in task['outcomes']:
        print >> task_md, '* %s' % task_outcome
    print >> task_md, '\n### Have you?\n'
    for task_checklist in task['checklist']:
        print >> task_md, '* %s' % task_checklist
    return task_md.buffer.getvalue()


def make_book_page(unit_data):
    """ Create a Markdown version of a unit """
    md_buffer = UTFWriter()
    print >> md_buffer, '# %s\n' % unit_data['unit']
    for task in unit_data['tasks']:
        print >> md_buffer, make_task(task)
    print >> md_buffer, '## FAQ\n'
    print >> md_buffer, unit_data['faq']
    return md_buffer.buffer.getvalue()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: build.py [command]\n'
        print 'Available commands'
        print '   test: Check if file syntax is ok'
        print '   json: Export rules to nueval-app json'
        print '   gitbook: Build markdown pages from YAML source\n\n'
        sys.exit(-1)
    BUILD_CMD = sys.argv[1]
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
                jsonFile = os.path.basename(source).replace('.yaml', '.json')
                jsonData = json.dumps(data, indent=4)
                tmp_file = codecs.open(
                    os.path.join(JSON_DIR, jsonFile), 'w', encoding='utf-8')
                tmp_file.write(jsonData)
                tmp_file.close()
            except Exception, ex:
                print 'Syntax Error'
                traceback.print_exc()
        elif BUILD_CMD == 'gitbook':
            if not os.path.exists(GITBOOK_DIR):
                os.makedirs(GITBOOK_DIR)
            try:
                data = read_yaml(source)
                md_file = os.path.basename(source).replace('.yaml', '.md')
                md_data = make_book_page(data)
                tmp_file = codecs.open(
                    os.path.join(GITBOOK_DIR, md_file), 'w', encoding='utf-8')
                tmp_file.write(md_data)
                tmp_file.close()
            except Exception, ex:
                traceback.print_exc()
