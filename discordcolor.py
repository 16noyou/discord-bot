import requests
import threading
import time
import random
token = 'Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw'
headers = {"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw"}
defaultChannel = "1017186119252713523"
defaultGuild = "1017172184847884288"
defaultFile = "roles.colors"
prevID = "0"
colorConvertTable = [['RED', '#FF0000'],['ORANGE', '#FFA500'],['YELLOW', '#FFFF00'],['GREEN', '#00FF00'],['BLUE', '#0000FF'],['PURPLE', '#800080'],['BROWN', '#964B00'],['WHITE', '#FFFFFF'],['BLACK', '#000000']]
class help(object):

    default = {
        "type":"rich",
        "title":"Color Picker Bot Help",
        "description":"Commands for Color Picker Bot",
        "color":10,
        "fields":[
            {
                "name":"Colorset",
                "value":"`cp colorset <color>`\ngive yourself a color!",
                "inline":True
            },
            {
                "name":"Help",
                "value":"`cp help [command]`\ndisplay help for a command",
                "inline":True
            }
        ],
        "footer":{
            "text":"<- want this color? run `cp colorset #00ff00` to get it!"
        }
    }
    help = {
      "type": "rich",
      "title": "Help Command Help",
      "description": "The Help command gets help for a command",
      "color": 10,
      "fields": [
        {
          "name": "Syntax",
          "value": "`help [command]`\n​",
          "inline": True
        },
        {
          "name": "Arguments",
          "value": "`[command]`\nSpecifiys what command to get help for",
          "inline": True
        }
      ],
      "footer": {
        "text": "<- want this color? run \"cp colorset #00ff00\" to get it!"
      }
    }
    give = {
   "type":"rich",
   "title":"Colorset Command Help",
   "description":"The Colorset Command gives a color to the user executing it",
   "color":10,
   "fields":[
      {
         "name":"Syntax",
         "value":"`cp colorset <color>`"
      },
      {
         "name":"Arguments",
         "value":"`<color>`\nMay be one of :\n    `red, orange, yellow, green, blue, brown,` \n    `white, black, purple` \nMay also be any valid hex code (ex. `#af590d`)"
      },
      {
         "name":"Errors",
         "value":"will raise a `MISSING_PERMISSIONS ERROR` if the bot user does not have\nthe `MANAGE_ROLES` permission\n\nwill also raise a `INVALID_COLOR ERROR` if the color provided is invalid"
      }
   ],
   "footer":{
      "text":"<- want this color? run `cp colorset #00ff00` to get it!"
   }
}
def readRoleFile(filename, substr):
    file = open(filename, 'r', encoding='UTF-8')
    while (line := file.readline()):
        print(line)
        if substr in line:
            role = []
            temp_var = ''
            for i in range(len(line)):
                if line[i] == "=":
                    role.append(temp_var)
                    print(f"temp_var={temp_var}")
                    temp_var = ''
                else:
                    temp_var += line[i]
                    if i == len(line) - 1:
                        role.append(temp_var)
                        print(f"temp_var={temp_var}") 
            #role.append(line[len(line)-1])
            print(role)
            file.close()
            return role
        print(line)
    return "LINE_NOT_FOUND"
def writeRoleFile(filename, role_name, r_id, mode):
    if mode == 0:
        check = readRoleFile(filename, role_name)
        if check == "LINE_NOT_FOUND":
            f = open(filename, 'a')
            f.write(f"{role_name}={r_id}=1\n")
            f.close()
        else:
            role = check
            num = int(role[2])+1
            f = open(filename, 'r')
            file = f.read()
            f.close()
            file = file.replace(f"{role_name}={r_id}={role[2]}", f"{role_name}={r_id}={str(num)}\n")
            f = open(filename, 'w')
            f.write(file)
    else:
        role = readRoleFile(filename, r_id)
        #print(role)
        if role[2] == '1\n':
            f = open(filename, 'r')
            file = f.read()
            f.close()
            file = file.replace(f"{role[0]}={r_id}=1\n", '')
            f = open(filename, 'w')
            f.write(file)
            x = requests.delete(f"https://discord.com/api/v9/guilds/{defaultGuild}/roles/{role[1]}", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": f"Remove Unused Color Role"})
        else:
            f = open(filename, 'r')
            file = f.read()
            f.close()
            num = role[2].removesuffix('\n')
            file = file.replace(f"{role[0]}={r_id}={role[2]}", f"{role[0]}={r_id}={int(num)-1}\n")
            f = open(filename, 'w')
            f.write(file)
def sendMessage(c_id, content):
    x = requests.post(f"https://discord.com/api/v9/channels/{c_id}/messages", headers=headers, json={"content": content})
    responseJson = x.json()
    #print(responseJson)
    if x.status_code == 429:
        time.sleep(responseJson['retry_after'])
        sendMessage(c_id, content)
    return responseJson['id']
def sendEmbededMessage(c_id, embed: dict):
    col_hex = ''
    for i in range(6):
        col_hex += random.choice(['a','b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
    col_num = int(col_hex, 16)
    embed['color'] = col_num
    embed['footer']['text'] = f"<- want this color? run \"cp colorset #{col_hex}\" to get it!"
    x = requests.post(f"https://discord.com/api/v9/channels/{c_id}/messages", headers=headers, json={"content": "", "embeds":[embed]})
    responseJson = x.json()
    #print(responseJson)
    if x.status_code == 429:
        time.sleep(responseJson['retry_after'])
        sendEmbededMessage(c_id, embed)
    return responseJson['id']
def getLastMessage(c_id):
    x = requests.get(f"https://discord.com/api/v9/channels/{c_id}/messages?before=9223372036854775807&limit=1", headers=headers)
    responseJson = x.json()
    print(x.status_code)
    try:
        newmsg = responseJson[0]['content']
        newmsgid = responseJson[0]['author']['id']
        print(newmsg)
        return [newmsg, newmsgid]
    except Exception:
        time.sleep(responseJson['retry_after'])
        return getLastMessage(c_id)
def sendHelpGive(c_id):
    col_hex = ''
    for i in range(6):
        col_hex += random.choice(['a','b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
    col_num = int(col_hex, 16)
    help.give['color'] = col_num
    help.give['footer']['text'] = f"<- want this color? run \"cp colorset #{col_hex}\" to get it!"
    sendEmbededMessage(c_id, help.give)
def sendHelp(c_id):
    col_hex = ''
    for i in range(6):
        col_hex += random.choice(['a','b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
    col_num = int(col_hex, 16)
    help.default['color'] = col_num
    help.default['footer']['text'] = f"<- want this color? run \"cp colorset #{col_hex}\" to get it!"
    sendEmbededMessage(c_id, help.default)
def editMessage(c_id, content):
    global prevID
    x = requests.patch(f"https://discord.com/api/v9/channels/{c_id}/messages/{prevID}", headers=headers, json={"content":content})
    if x.status_code == 429:
        responsejson = x.json()
        time.sleep(responsejson['retry_after'])
        editMessage(c_id, content)
def newColorRole(g_id, color: str, u_id):
    global prevID
    color = color.upper()
    color_name = color.upper()
    for i in range(len(colorConvertTable)):
        if color == colorConvertTable[i][0] or color == colorConvertTable[i][1]:
            color = colorConvertTable[i][1]
            color_name = colorConvertTable[i][0].capitalize()
    if color[0] != '#' or len(color) != 7:
        editMessage(defaultChannel, f"`INVALID_COLOR ERROR, {color}` is not a valid color")
        return 0
    if color == '#000000':
        color = '#010101'
    try:
        role = {'name': color_name,
            'color': int(color.removeprefix('#'), 16)}
    except Exception:
        editMessage(defaultChannel, f"`INVALID_COLOR ERROR, {color}` is not a valid color")
        return 0
    x = requests.get(f"https://discord.com/api/v9/guilds/{g_id}/members/{u_id}", headers=headers)
    member_roles = x.json()
    member_roles = member_roles['roles']
    print(member_roles)
    found = 0
    for i in range(len(member_roles)):
        rolefile2 = readRoleFile(defaultFile, str(member_roles[i]))
        print(f"{rolefile2}{i}")
        if rolefile2 != "LINE_NOT_FOUND":
            found = 1
            break
    if found == 1:
        x = requests.delete(f"https://discord.com/api/v9/guilds/{g_id}/members/{u_id}/roles/{rolefile2[1]}", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": f"Remove Unused Color Role from User {u_id}"})
        writeRoleFile(defaultFile, None, rolefile2[1], 1)
    rolefile = readRoleFile(defaultFile, color)
    if rolefile != "LINE_NOT_FOUND":
        x = requests.put(f"https://discord.com/api/v9/guilds/{g_id}/members/{u_id}/roles/{rolefile[1]}", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": f"Add Color Role to User {u_id}"})
        writeRoleFile(defaultFile, color, rolefile[1], 0)
        editMessage(defaultChannel, f"Succesfully Assigned color `{color_name}` to <@{u_id}>")
    else:
        x = requests.post(f"https://discord.com/api/v9/guilds/{g_id}/roles", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": "Create Color Role"}, json=role)
        role = x.json()
        editMessage(defaultChannel, f"Succesfully Assigned color `{color_name}` to <@{u_id}>")
        x = requests.put(f"https://discord.com/api/v9/guilds/{g_id}/members/{u_id}/roles/{role['id']}", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": f"Add Color Role to User {u_id}"})
        x = requests.patch(f"https://discord.com/api/v9/guilds/{g_id}/roles", headers={"Authorization": "Bot OTg2NzgyNjU1NjExODA1NzM2.GMC-TY.U0eXPNf2dPvaclGMMEwdQZgRlhXrAdfy3WlOpw", "X-Audit-Log-Reason": "Move Color Role to showw on user"}, json=[{"id":f"{role['id']}", "position":23}])
        writeRoleFile(defaultFile, color, role['id'], 0)
    if x.status_code == 401:
        editMessage(defaultChannel, "`MISSING_PERMISSIONS ERROR` I am missing the `MANAGE_ROLES` premission(s)")
        return 0
    elif x.status_code == 429:
        response = x.json()
        time.sleep(response['retry_after'])
        newColorRole(g_id, color)
def main():
    global prevID
    while True:
        time.sleep(0.84)
        lastMessage = getLastMessage(defaultChannel)
        lastMessageid = lastMessage[1]
        lastMessage = lastMessage[0].lower()
        print(lastMessage)
        try:
            if lastMessage[0] + lastMessage[1] + lastMessage[2] == "cp ":
                lastMessage = lastMessage.removeprefix("cp ")
                if lastMessage == "test":
                    threading.Thread(target=lambda: sendMessage(defaultChannel, "test is here to help!")).start()
                elif lastMessage == "formattest":
                    threading.Thread(target=lambda: sendMessage(defaultChannel, "`test` *test* **test** __test__ ~~test~~ ||test|| \n > test \n >>> test \n testtttttttt")).start()
                elif lastMessage == "help":
                    threading.Thread(target=lambda: sendEmbededMessage(defaultChannel, help.default)).start()
                else:
                    try:
                        if lastMessage[0] + lastMessage[1] + lastMessage[2] + lastMessage[3] + lastMessage[4] == "copy ":
                            lastMessage = lastMessage.removeprefix("copy ")
                            threading.Thread(target=lambda: sendMessage(defaultChannel, lastMessage)).start()
                        elif lastMessage[0] + lastMessage[1] + lastMessage[2] + lastMessage[3] + lastMessage[4] + lastMessage[5] + lastMessage[6] + lastMessage[7] + lastMessage[8]== "colorset ":
                            lastMessage = lastMessage.removeprefix("colorset ")
                            prevID = sendMessage(defaultChannel, f"Attempting to change color of user <@{lastMessageid}>")
                            threading.Thread(target=lambda: newColorRole(defaultGuild, lastMessage, lastMessageid)).start()
                        elif lastMessage[0] + lastMessage[1] + lastMessage[2] + lastMessage[3] + lastMessage[4] == "help ":
                            lastMessage = lastMessage.removeprefix("help ")
                            if lastMessage == "help":
                                threading.Thread(target=lambda: sendEmbededMessage(defaultChannel, help.help)).start()
                            elif lastMessage == "colorset":
                                threading.Thread(target=lambda: sendEmbededMessage(defaultChannel, help.give)).start()
                            else:
                                threading.Thread(target=lambda: sendMessage(defaultChannel, f"`UNKNOWN_COMMAND ERROR` Command `{lastMessage}` not found")).start()
                    except Exception:
                        threading.Thread(target=lambda: sendMessage(defaultChannel, f"`UNKNOWN_COMMAND ERROR` Command `{lastMessage}` not found")).start()
        except Exception:
            pass
main()



