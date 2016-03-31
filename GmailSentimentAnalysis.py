import pandas as pd
import nltk
from mailbox import mbox

# read in messages
def store_content(message, body=None):
    if not body:
        body = message.get_payload(decode=True)
    if len(message):
        contents = {
            "subject" : message['subject'] or "",
            "body": body,
            "from": message['from'],
            "to": message['to'],
            "date": message['date'],
            "labels": message['X-Gmail-Labels'],
            "epilogue": message.epilogue
        }
    return df.append(contents, ignore_index=True)

# empty dataframe with categories
df = pd.DataFrame(
    columns = ("subject", "body", "from", "to", "date", "labels", "epilogue")
)

# import mailbox
box = mbox('All mail Including Spam and Trash.mbox')

fails = []
for message in box:
    try:
        if message.get_content_type() == 'text/plain':
            df = store_content(message)
        elif message.is_multipart():
            for part in message.get_payload():
                if part.get_content_type() == 'text/plain':
                    df = store_content(message, part.get_payload(decode=True))
                    break
    except:
        fails.append(message)

from collections import Counter

subject_word_bag = df.subject.apply(lambda t: t.lower() + " ").sum()

most_common = Counter(subject_word_bag.split()).most_common()[:10]

print(most_common)

from textblob import TextBlob
df['sentiment'] = df.subject.apply(lambda s: TextBlob(unicode(s, errors='ignore')).sentiment.polarity)

print(df[['subject', 'sentiment']])

