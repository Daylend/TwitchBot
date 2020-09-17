from random import random
import datetime
import twitch
import gpt_2_simple as gpt2
import time
import re
import queue

#textchannels = ["dougdougw","summit1g","jericho","morrolantv","macilus","n0thing","loltyler1"]
textchannels = ["imaqtpie"]
bots = ["Nightbot"]
run_name = 'master'
chats = {}
logs = {}
global lastmsg
global msg

# Strips links so the bot doesn't advertise
strip_links = re.compile(r'^.*((http)s?|www\.\w+\.(com|org|net|ca|me|co)|[\d\w]+\.(com|org|net|ca|me|co)).*$', flags=re.MULTILINE|re.IGNORECASE)
# Strips mentions to prevent harassment
strip_ats = re.compile(r'^.*@[\d\w_]+.*$', flags=re.MULTILINE)
# Strip out all the bad words chat says
strip_profanity = re.compile(r'^.*(bad words).*$'
                             , flags=re.MULTILINE|re.IGNORECASE)

def handle_message(message: twitch.chat.Message) -> None:
    # if not isLink(message.text) and not isBot(message.sender):
    #     with open(message.channel+".txt","a+", encoding='utf-8') as log:
    #         log.write(message.text+"\n")
    #     print("[{}] {}: {}".format(message.channel, message.sender, message.text))
    global lastmsg, msg
    if not msg.empty():
        roll = random()
        print("Rolled {} ({})".format(roll, msg.full()))
        if random() <= 1/5:
            now = datetime.datetime.now()
            if lastmsg < now:
                text = msg.get(block=False)
                message.chat.send(text + "\r\n")
                print(text)
                lastmsg = datetime.datetime.now() + datetime.timedelta(0,10)


    if "WoodenLongboard" in message.text:
        print("{}: {}".format(message.sender, message.text))

def isLink(str):
    return "http://" in str or "https://" in str

def isBot(user):
    return user in bots

def close_logs():
    for log in logs:
        log.close()

def sanitize_message(txt):
    txt = txt.replace("<|startoftext|>", "")
    txt = txt.replace("<|endoftext|>", "")
    txt = strip_links.sub("", txt)
    txt = strip_profanity.sub("", txt)
    txt = strip_ats.sub("", txt)
    return txt

def genmsg(sess):
    while True:
        msg = gpt2.generate(sess, run_name=run_name,
                        length=100,
                        temperature=0.8,
                        prefix="<|startoftext|>",
                        truncate="<|endoftext|>",
                        include_prefix=False,
                        return_as_list=True)[0]
        msg = sanitize_message(msg)
        if msg != "":
            break
    return msg

def main():
    helix = twitch.Helix('***REMOVED***', use_cache=True)
    global lastmsg, msg
    lastmsg = datetime.datetime.now()
    msg = queue.Queue(10)
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=run_name)

    while not msg.full():
        msg.put(genmsg(sess))

    for channel in textchannels:
        chat = twitch.Chat(channel="#"+channel, nickname='WoodenLongboard', oauth="***REMOVED***",
                       helix=helix)
        chats[channel] = chat
        chats[channel].subscribe(handle_message)

    print("Finished init")

    while True:
        if not msg.full():
            msg.put(genmsg(sess))



if __name__ == '__main__':
    main()