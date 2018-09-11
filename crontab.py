#!/usr/bin/env python

import http.client
import json
import time
import datetime
import sys
import os


def gitCmd(date):
    gitAdd = 'git add .'
    gitCommit = 'git commit -m ' + date
    gitPush = 'git push -u origin master'

    os.system(gitAdd)
    os.system(gitCommit)
    os.system(gitPush)


def createMarkdown(date,filename,lang):
    with open(filename,'w') as f:
        f.write("## " + lang + "周报\n")

def writeMarkdown(data,filename):
    with open(filename,"a") as f:
        for value in data:
            description = value['description']
            url = value['url']
            title = value['reponame']
            username = value['username']
            starCount = value['starCount']
            forkCount = value['forkCount']
            avatar = value['owner']['avatar']
            
            content = '''
#### [{username} / {title}]({url})

> {description}

+ start: {starCount}
+ fork: {forkCount}

----

'''.format(title=title, url=url, description=description,username=username,starCount=starCount,forkCount=forkCount)

            f.write(content)


# @param lang
# @return json

def scrapy(lang):
    conn = http.client.HTTPSConnection("extension-ms.juejin.im")

    payload = {
        "category":"upcome",
        "period":"week",
        "lang":lang,
        "offset":0,
        "limit":10
    }

    payload = json.dumps(payload)

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    conn.request("POST", "/resources/github", payload, headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return data

def crontab():
    strdate = datetime.datetime.now()
    weekday = strdate.weekday()
    date = strdate.strftime('%Y-%m-%d')

    lang = ""

    if weekday == 1 :
        lang = "php"
    elif weekday == 2:
        lang = "javascript"
    elif weekday == 3:
        lang = "go"
    elif weekday == 4:
        lang = "python"
    elif weekday == 5:
        lang = "vue"
    else:
        lang = ""

    if lang == "":
        print("exit")
        sys.exit(0)

    filename = './{lang}/{date}.md'.format(lang=lang,date=date)
    createMarkdown(date,filename,lang)
    data = scrapy(lang)
    data = json.loads(data)
    if data['code'] == 200:
        writeMarkdown(data['data'],filename)
        gitCmd(date)

if __name__ == '__main__':
    crontab()
