import os
import json
import codecs

from datetime import datetime

ScriptName = "Keyword AutoReply"
Website = "http://www.dustydiamond.de/"
Description = "Auto Answer to given Keywords"
Creator = "DustyDiamond"
Version = "1.2.3"


settings = {}
keywords = []


def Init():
    global settings
    global keywords
    work_dir = os.path.dirname(__file__)

    with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
        settings = json.load(json_file, encoding='utf-8-sig')

    temp = str(settings["keywords"])
    keywords = temp.split(",")
    return


def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log(ScriptName, dt_string + ": " + message)
    return


def send_message(message):
    Parent.SendStreamMessage(message)
    log("Message Sent")
    return


def Execute(data):
    if data.GetParam(0) == "":
        return

    paramCount = int(data.GetParamCount())

    username = data.User

    for i in range(paramCount):
        for x in range(len(keywords)):
            if keywords[x] in data.GetParam(i):
                send_message(settings["bot_response"].format(username))
                continue
            else:
                # log(keywords[x])
                continue

        if settings["list"] in data.GetParam(i):   # Lists all Keywords
            msg = ""
            for x in range(len(keywords)):
                msg += str(keywords[x]) + ", "

            msg = msg[:len(msg) - 2]
            if settings["list_enable"]:
                send_message("Keywords are: " + msg)
                continue
            continue


def Tick():
    return


def ReloadSettings(jsonData):
    global settings
    global keywords
    work_dir = os.path.dirname(__file__)
    # Execute json reloading here
    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            json.dump(json.loads(jsonData), json_file, encoding='utf-8-sig')
            log("Settings Saved")
    except Exception, e:
        log("Saving Error")

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
            temp = str(settings["keywords"])
            keywords = temp.split(",")
            log("Settings Reloaded")
    except Exception, e:
        log(str(e))

    return


def Unload():
    return
