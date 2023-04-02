import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


text="""In the early medieval era, Christianity, Islam, 
Judaism, and Zoroastrianism became established on India's southern and 
western coasts. Muslim armies from Central Asia intermittently 
overran India's northern plains,[43] eventually founding the Delhi 
Sultanate, and drawing northern India into the cosmopolitan networks of
medieval Islam. In the 15th century, the Vijayanagara Empire created a
long-lasting composite Hindu culture in south India. In the Punjab,
Sikhism emerged, rejecting institutionalised religion. The Mughal 
Empire, in 1526, ushered in two centuries of relative peace,
leaving a legacy of luminous architecture.Gradually expanding rule
of the British East India Company followed, turning India into a 
colonial economy, but also consolidating its sovereignty."""


def text_summarizer(raw_docx):
    #stopwords=list(STOP_WORDS)
    #print(stopwords)

    nlp=spacy.load("en_core_web_sm")
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    #doc=nlp(rawdocs)
    #print(doc)


    #tokens=[token.text for token in docx]
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]
    #print(tokens)
    word_frequencies={}
    for word in docx:
        if word.text.lower() not in stopwords and word.text.lower() in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text]=1
            else:
                word_frequencies[word.text]+=1

    #print(word_freq)

    max_freq=max(word_frequencies.values())
    #print(max_freq)

    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_freq

    #print(word_freq)

    sent_tokens=[sent for sent in docx.sents]
    #print(sent_tokens)

    # Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]


    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary