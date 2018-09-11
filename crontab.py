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

    # 执行shell
    os.system(gitAdd)
    os.system(gitCommit)
    os.system(gitPush)


def createMarkdown(date,filename,lang):
    with open(filename,'w') as f:
        f.write("## " + lang + "周报\n")

def writeMarkdown(data,filename):
    with open(filename,"a") as f:
        for value in data:
            #项目描述
            description = value['description']
            #仓库链接
            url = value['url']
            #项目名称
            title = value['reponame']
            #作者名字
            username = value['username']
            #start数
            starCount = value['starCount']
            #fork数
            forkCount = value['forkCount']
            #头像
            avatar = value['owner']['avatar']
            
            content = '''
#### [{username} / {title}]({url})

> {description}

+ start: {starCount}
+ fork: {forkCount}

----

'''.format(title=title, url=url, description=description,username=username,starCount=starCount,forkCount=forkCount)

            #写入文件
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
    # 获取星期数
    weekday = strdate.weekday()
    date = strdate.strftime('%Y-%m-%d')

    #根据星期来获取语言
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

    # 创建markdown文件
    createMarkdown(date,filename,lang)
    # 获取trending
    data = scrapy(lang)
    # 写入markdown文件
    data = json.loads(data)
    if data['code'] == 200:
        writeMarkdown(data['data'],filename)
        # git提交
        gitCmd(date)

if __name__ == '__main__':
    crontab()
