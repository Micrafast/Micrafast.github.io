#!/usr/bin/python3
import sys
import os
import re
import shutil
import markdown
from datetime import date


argv = sys.argv
if len(argv) == 1:
    print("Wrong arguments!")
    exit()


if argv[1] == 'add':
    title = '';
    context = '';
    dt = date.today().strftime('%Y/%m/%d')
    filedt = date.today().strftime('%Y%m%d')
    argv = argv[2:]
    for i in range(len(argv)):
        arg = argv[i]
        if arg == '-t':
            title = argv[i+1]
        elif arg == '-c':
            context = '<p>'+argv[i+1]+'</p>';
        elif arg == '-f':
            ctxfile = open(argv[i+1], "r")
            context = markdown.markdown(ctxfile.read())
    def repprocess(match):
        src = match.group(1)
        return '<a href="' + src + '"><img src="' + src +'" /></a>'
    context = re.sub(r' img: *(.*?) ', repprocess, context)
    times = 1
    diaryfilename = 'diary/' + filedt + '-1.html'
    while os.path.exists(diaryfilename):
        times+=1
        diaryfilename = 'diary/' + filedt + '-' + str(times) + '.html'
    shutil.copyfile('diary/demo.html', diaryfilename)
    diaryfile = open(diaryfilename, 'r+')
    diary = diaryfile.read()
    diaryfile.seek(0)
    diary = diary.replace('<!-- CONTEXT -->', '<h3>'+title+'</h3>'+\
    '<h6>'+dt+'</h6>'+context)
    diaryfile.write(diary)
    diaryfile.flush()
    diaryfile.close()
    indexfile = open('index.html', 'r+')
    index = indexfile.read()
    indexfile.seek(0)
    index = index.replace('<!-- DIARYADD -->', '<!-- DIARYADD -->\n' + \
        '<div class="subblock"><h3>' + title + '</h3><p>'+context[:10].replace('<', '&lt;').replace('>', '&gt;')+'</p>...<a href="'+\
        diaryfilename+'" class="btn">查看详情</a></div>')
    indexfile.write(index)
    indexfile.flush()
    indexfile.close()
    
