import re
from pathlib import Path
import os

# Folder that contains VOD chat logs
folderpath = Path("~/vods")
# Don't include usernames or timestamps
strip_timestamp_username = re.compile(r'\[.+\]\s\<.+\>\s')
# Removes the majority of sub emotes (which the bot can't use)
strip_camel_emotes = re.compile(r'(\s[a-z]+[A-Z\d]+[a-z\d]*)|[\W\D]([a-z]+[A-Z\d]+[a-z\d]*\s)')
# Remove links to prevent the bot from inadvertently advertising
strip_links = re.compile(r'^.*((http)s?|www\.\w+\.(com|org|net|ca|me|co)|[\d\w]+\.(com|org|net|ca|me|co)).*$', flags=re.MULTILINE|re.IGNORECASE)
# Attempts to remove common bot messages
strip_sub_notifs = re.compile(r'^.*(subscribed\s(at|to|for|with)|has\sbeen\slive\sfor|subscribed\sfor\d+)\s.*$', flags=re.MULTILINE|re.IGNORECASE)
# Removes any messages by these bots
strip_bots = re.compile(r'^.*<.(Nightbot|StreamElements|CluntBotStovens|LacariBot)>.*$', flags=re.MULTILINE|re.IGNORECASE)
# Removes extra newlines left over from above strips
strip_extra_newlines = re.compile('\n\n+', flags=re.MULTILINE|re.IGNORECASE)
# Removes common bot commands
strip_commands = re.compile(r'^!.+$', flags=re.MULTILINE)
# Remove mentions so the bot doesn't harass people
strip_ats = re.compile(r'^.*@[\d\w_]+.*$', flags=re.MULTILINE)
# Strip out all the bad words chat says
strip_profanity = re.compile(r'^.*.*$'
                             , flags=re.MULTILINE|re.IGNORECASE)
# Removes any number of repeated phrases so "TEST TEST TEST TEST TEST" -> "TEST"
strip_repeated_phrases = re.compile(r'(\W|^)(.+)\s\2|\w\w{30,}', flags=re.MULTILINE|re.IGNORECASE)

text = ""

# Read in every log file in directory
for file in os.listdir(folderpath):
    print("Opened {}".format(file))

    if file.endswith(".log"):
        filepath = folderpath.joinpath(file)
        with open(filepath, "r", encoding='utf-8') as txt:
            text += txt.read()

    if os.path.isdir(folderpath.joinpath(file)):
        for file2 in os.listdir(folderpath.joinpath(file)):
            if file2.endswith(".log"):
                print("Opened {}/{}".format(file,file2))
                filepath = folderpath.joinpath(file).joinpath(file2)
                with open(filepath, "r", encoding='utf-8') as txt:
                    text += txt.read()

print("Removing extra info...")
# Strip out bots first
text = strip_bots.sub('', text)
# Remove time and username information
text = strip_timestamp_username.sub('', text)
print("Removing links, commands, bot sayings, @mentions, profanity")
# Remove links
text = strip_links.sub('', text)
# Remove sub emotes
text = strip_camel_emotes.sub('', text)
# Remove commands
text = strip_commands.sub('', text)
# Remove extra common bot stuff
text = strip_sub_notifs.sub('', text)
# Remove @mentions, bot is too dumb
text = strip_ats.sub('', text)
# Remove profanity
text = strip_profanity.sub('', text)
# Remove duplicate phrases
print("Stripping most repeated phrases... takes awhile.")
text = strip_repeated_phrases.sub('', text)
print("Cleaning up and converting to CSV")
# No blank lines
text = strip_extra_newlines.sub('\n', text)
# Convert to csv
text = text.replace('\n',',\n')

# Save logs to master csv after formatting
with open("master.csv", "w+", encoding='utf-8') as newlog:
    newlog.write(text)
    print("done")