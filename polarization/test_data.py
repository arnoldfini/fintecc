import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

sentence = "Trump did a terrible job"

# Data
tokens = nltk.word_tokenize(sentence)
#tagged = nltk.pos_tag(tokens)
#entities = nltk.chunk.ne_chunk(tagged)
sid = SentimentIntensityAnalyzer()

# Initialise arrays to classify its respective atribute
positive = []
negative = []
neutral = []

# Hardcode some words polarity
hardcode_pos = []
hardcode_neg = ['Trump']
hardcode_neut = []

'''for word in tokens:
    if (sid.polarity_scores(word)['compound']) >= 0.5:
        positive.append(word)
    elif (sid.polarity_scores(word)['compound']) <= -0.5:
        negative.append(word)
    else:
        neutral.append(word)

print(positive)
print(neutral)
print(negative)'''

for word in tokens:
    testimonial = TextBlob(word)
    if testimonial.sentiment.polarity >= 0.5 or word in hardcode_pos:
        positive.append(word)
    elif testimonial.sentiment.polarity <= -0.5 or word in hardcode_neg:
        negative.append(word)
    else:
        neutral.append(word)

print(positive)
print(neutral)
print(negative)