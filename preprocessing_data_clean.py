import nltk
import MySQLdb
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.chunk import RegexpParser
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import config

def getid(num):
    
    if num<10:
        number = "0000000" + str(num)
    elif num<100:
        number = "000000" + str(num)
    elif num<1000:
        number = "00000" + str(num)
    elif num<10000:
        number = "0000" + str(num)
    elif num<100000:
        number = "000" + str(num)
    elif num<1000000:
        number = "00" + str(num)
    elif num<10000000:
        number = "0" + str(num)
    else:
        number = str(num)
        
    return str(number)


review_id = 'R.2016.05.27.00001'

conn = MySQLdb.connect(config.DB_HOST , config.DB_USER, config.DB_PASS , config.DB_NAME)

c = conn.cursor()

c.execute("DELETE FROM preprocessing_data WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM preprocessing_np WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM frequent_aspect WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM infrequent_aspect WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM ontology_aspect WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM opinion_mining_result WHERE review_id = %s",(review_id,))
conn.commit()
c.execute("DELETE FROM summary WHERE review_id = %s",(review_id,))
conn.commit()

no1 = 0
no3 = 0

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

c.execute("SELECT * FROM review_detail WHERE review_id = %s ORDER BY review_detail_id",(review_id,))
rows = c.fetchall()
for eachRow in rows:
    sentence = eachRow[2]
    sentence = sentence.replace("/"," or ")
    word_tokens = nltk.word_tokenize(sentence)


    tagged = nltk.pos_tag(word_tokens)

    patterns = """
            NP: {<NN>+<NN>}
            {<JJ>+<NN>}
            """
    NPChunker = nltk.RegexpParser(patterns) 
    result = NPChunker.parse(tagged) 
    no2 = 0
    for subtree in result.subtrees(filter=lambda t: t.label() == 'NP'):

        no3 += 1
        np_tag = str(subtree.leaves())
        np_tag = np_tag.replace("'","")
        np_tag = np_tag.replace(" ","")
        np_tag = np_tag.replace("[","")
        np_tag = np_tag.replace("]","")
        np_real = ""
        np_stem = ""
        no = 0
        for leave in subtree.leaves():
            no += 1
            if no == 1:
                np_real += leave[0]
                np_stem += ps.stem(leave[0])
            else:
                np_real += " "+leave[0]
                np_stem += " "+ps.stem(leave[0])

        np_stem = np_stem.replace(".","")
        np_stem = np_stem.replace(",","")
        np_stem = np_stem.replace("'","")
        np_stem = np_stem.replace("?","")
        np_stem = np_stem.replace("!","")
        preprocessing_np_id = review_id + ".PNP." + getid(no3)
        c.execute("INSERT INTO preprocessing_np (preprocessing_np_id, review_id, review_detail_id, preprocessing_np_detail, preprocessing_np_original, preprocessing_np_word) VALUES (%s,%s,%s,%s,%s,%s)"
                  ,(preprocessing_np_id, review_id, eachRow[0], np_tag, np_real, np_stem))
        conn.commit()
        


    no2 = 0
    for tag in tagged:
        no1 += 1
        preprocessing_data_id = review_id + ".PD." + getid(no1)
        no2 += 1
        preprocessing_data_word = tag[0]
        preprocessing_data_tag = tag[1]
        preprocessing_data_word_processed = ""
        if preprocessing_data_word not in stop_words:
            preprocessing_data_word_processed = ps.stem(preprocessing_data_word)
            preprocessing_data_word_processed = preprocessing_data_word_processed.replace(".","")
            preprocessing_data_word_processed = preprocessing_data_word_processed.replace(",","")
            preprocessing_data_word_processed = preprocessing_data_word_processed.replace("'","")
            preprocessing_data_word_processed = preprocessing_data_word_processed.replace("?","")
            preprocessing_data_word_processed = preprocessing_data_word_processed.replace("!","")
        c.execute("INSERT INTO preprocessing_data (preprocessing_data_id, review_id, review_detail_id, preprocessing_data_word_number, preprocessing_data_word, preprocessing_data_tag, preprocessing_data_word_processed, preprocessing_data_word_orientation, preprocessing_data_word_feature) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                  ,(preprocessing_data_id, review_id, eachRow[0], no2, preprocessing_data_word, preprocessing_data_tag, preprocessing_data_word_processed, "", ""))
        conn.commit()
    
