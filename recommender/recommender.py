# -*- coding: utf-8 -*-

# from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import numpy as np
import pandas as pd
# import spacy
import nltk
import requests
import json

# nlp = spacy.load('en_core_web_lg')


def recommender(id):

    # user_skills = ['Django','Python','PostgreSQL','Fullstack developer', 'React','Javascript']
    user_skills_url = "http://127.0.0.1:8000/api/skills/"

    user_skills_response = requests.request("GET", user_skills_url)
    user = json.loads(user_skills_response.text)
    # user = {
    #     "id": 5,
    #     "skills": ['java', 'sql', 'spring']
    #     # "skills":['Django','PostgreSQL', 'React','java','c','c++','sql','algorithms','html','css','javascript','python','web development','windows','linux']
    #     # "skills":['java','c','c++','sql','algorithms','html','css','javascript','python','web development','windows','linux']
    # }

    jobs_url = "http://127.0.0.1:8000/api/job-list"

    jobs_response = requests.request("GET", jobs_url)
    job_post = json.loads(jobs_response.text)

    df_job_post = pd.json_normalize(job_post)
    # print(df_job_post)

    df_user = pd.json_normalize(user)
    # print(df_user)

    nltk.download('omw-1.4')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

    # cleaning

    stop = stopwords.words('english')
    stop_words_ = set(stopwords.words('english'))
    wn = WordNetLemmatizer()

    def black_txt(token):
        return token not in stop_words_ and token not in list(string.punctuation) and len(token) > 2

    def clean_txt(text):
        clean_text = []
        clean_text2 = []
        text = re.sub("'", "", text)
        text = re.sub("(\\d|\\W)+", " ", text)
        text = text.replace("nbsp", "")
        clean_text = [wn.lemmatize(word, pos="v") for word in word_tokenize(
            text.lower()) if black_txt(word)]
        clean_text2 = [word for word in clean_text if black_txt(word)]
        return " ".join(clean_text2)

    # print(df_job_post)

    df_job_post['text'] = df_job_post['skills'].str.join(
        " ")+" "+df_job_post['job_description']+" "+df_job_post['roles_responsibilities']
    df_job_post['text'] = df_job_post['text'].apply(clean_txt)

    df_all_job = df_job_post[['id', 'text', 'job_title']]

    df_user['text'] = df_user['skills'].str.join(" ")

    u = id
    index = np.where(df_user['id'] == u)[0][0]
    user_q = df_user.iloc[[index]]
    user_q

    def get_recommendation(top, df_all_job, scores):
        recommendation = pd.DataFrame(columns=['JobID',  'JobTitle', 'score'])
        count = 0
        for i in top:
            recommendation.at[count, 'JobID'] = df_all_job['id'][i]
            recommendation.at[count, 'JobTitle'] = df_all_job['job_title'][i]
            recommendation.at[count, 'score'] = scores[count]
            count += 1
        return recommendation

    def get_recommended_json(top, df_all_job, scores):
        recommendation = pd.DataFrame(columns=[
            'id',  'job_title', 'job_location', 'company_name', 'min_salary', 'max_salary'])
        count = 0
        for i in top:
            recommendation.at[count, 'id'] = df_job_post['id'][i]
            recommendation.at[count, 'job_title'] = df_job_post['job_title'][i]
            recommendation.at[count,
                              'job_location'] = df_job_post['job_location'][i]
            recommendation.at[count,
                              'company_name'] = df_job_post['company_name'][i]
            recommendation.at[count,
                              'min_salary'] = df_job_post['min_salary'][i]
            recommendation.at[count,
                              'max_salary'] = df_job_post['max_salary'][i]
            count += 1
        result = recommendation.to_json(orient="records")
        parsed = json.loads(result)
        # return json.dumps(parsed, indent=4)
        return parsed

    # count Vector
    count_vectorizer = CountVectorizer()

    count_jobid = count_vectorizer.fit_transform(
        (df_all_job['text']))  # fitting and transforming the vector

    user_count = count_vectorizer.transform(user_q['text'])
    cos_similarity_countv = map(
        lambda x: cosine_similarity(user_count, x), count_jobid)

    output2 = list(cos_similarity_countv)

    # print("\nUsing Count Vector\n")

    top = sorted(range(len(output2)),
                 key=lambda i: output2[i], reverse=True)[:2]
    list_scores = [output2[i][0][0] for i in top]
    # print(get_recommended_json(top, df_all_job, list_scores))
    # print(get_recommendation(top, df_all_job, list_scores))

    return get_recommended_json(top, df_all_job, list_scores)

# job_post = [
#     {
#         "id": 1,
#         "job_title": "Full Stack Developer",
#         "job_description": "We are looking for a Full Stack Developer to produce scalable software solutions. You’ll be part of a cross-functional team that’s responsible for the full software development life cycle, from conception to deployment.\r\n\r\nAs a Full Stack Developer, you should be comfortable around both front-end and back-end coding languages, development frameworks and third-party libraries. You should also be a team player with a knack for visual design and utility.\r\n\r\nIf you’re also familiar with Agile methodologies, we’d like to meet you.",
#         "roles_responsibilities": "Work with development teams and product managers to ideate software solutions.\r\nDesign client-side and server-side architecture.\r\nBuild the front-end of applications through appealing visual design.\r\nDevelop and manage well-functioning databases and applications.\r\nWrite effective APIs.\r\nTest software to ensure responsiveness and efficiency.\r\nTroubleshoot, debug and upgrade software.\r\nCreate security and data protection settings.\r\nBuild features and applications with a mobile responsive design.\r\nWrite technical documentation.\r\nWork with data scientists and analysts to improve software.",
#         "education": [
#             "B.sc Computer Science",
#             "B.E Computer Science"
#         ],
#         "industry_type": "IT Services",
#         "job_location": [
#             "Coimbatore",
#             "Chennai"
#         ],
#         "employment_type": [
#             "Full-time"
#         ],
#         "min_experience": 1,
#         "min_salary": 300000,
#         "max_salary": 400000,
#         "skills": [
#             "HTML/ CSS",
#             "JavaScript",
#             "XML",
#             "jQuery",
#             "C#",
#             "Java",
#             "Python",
#             "Angular",
#             "React",
#             "Node.js",
#             "MySQL",
#             "MongoDB"
#         ],
#         "openings": 10,
#         "created_date": "2022-05-17",
#         "company_name": "Company1",
#         "user": 3
#     },
#     {
#         "id": 2,
#         "job_title": "Data Analyst",
#         "job_description": "We are looking for a passionate certified Data Analyst. The successful candidate will turn data into information, information into insight and insight into business decisions.",
#         "roles_responsibilities": "Interpret data, analyze results using statistical techniques and provide ongoing reports.\r\nDevelop and implement databases, data collection systems, data analytics and other strategies that optimize statistical efficiency and quality.\r\nAcquire data from primary or secondary data sources and maintain databases/data systems.\r\nIdentify, analyze, and interpret trends or patterns in complex data sets.\r\nFilter and “clean” data by reviewing computer reports, printouts, and performance indicators to locate and correct code problems.\r\nWork with management to prioritize business and information needs.\r\nLocate and define new process improvement opportunities.",
#         "education": [
#             "Any Degree"
#         ],
#         "industry_type": "IT Services",
#         "job_location": [
#             "Chennai",
#             "Pune",
#             "kolkata"
#         ],
#         "employment_type": [
#             "Part-time",
#             "Full-time"
#         ],
#         "min_experience": 1,
#         "min_salary": 400000,
#         "max_salary": 500000,
#         "skills": [
#             "SQL",
#             "Excel",
#             "SPSS",
#             "SAS",
#             "XML",
#             "Javascript",
#             "ETL"
#         ],
#         "openings": 5,
#         "created_date": "2022-05-17",
#         "company_name": "Company2",
#         "user": 4
#     },
#     {
#         "id": 3,
#         "job_title": "Java Developer",
#         "job_description": "We are looking for a Java Developer with experience in building high-performing, scalable, enterprise-grade applications.\r\n\r\nYou will be part of a talented software team that works on mission-critical applications. Java developer roles and responsibilities include managing Java/Java EE application development while providing expertise in the full software development lifecycle, from concept and design to testing.\r\n\r\nJava developer responsibilities include designing, developing and delivering high-volume, low-latency applications for mission-critical systems.",
#         "roles_responsibilities": "Contribute in all phases of the development lifecycle.\r\nWrite well designed, testable, efficient code.\r\nEnsure designs are in compliance with specifications.\r\nPrepare and produce releases of software components.\r\nSupport continuous improvement by investigating alternatives and technologies and presenting these for architectural review.",
#         "education": [
#             "Any Degree"
#         ],
#         "industry_type": "IT Services",
#         "job_location": [
#             "Chennai"
#         ],
#         "employment_type": [
#             "Full-time"
#         ],
#         "min_experience": 0,
#         "min_salary": 300000,
#         "max_salary": 450000,
#         "skills": [
#             "Java EE",
#             "SQL",
#             "ORM",
#             "JPA2",
#             "JSF",
#             "Wicket",
#             "GWT",
#             "Spring"
#         ],
#         "openings": 5,
#         "created_date": "2022-05-17",
#         "company_name": "Company1",
#         "user": 3
#     },
#     {
#         "id": 4,
#         "job_title": "UI/UX Designer",
#         "job_description": "We are looking for a UI/UX Designer to turn our software into easy-to-use products for our clients.\r\n\r\nUI/UX Designer responsibilities include gathering user requirements, designing graphic elements and building navigation components. To be successful in this role, you should have experience with design software and wireframe tools. If you also have a portfolio of professional design projects that includes work with web/mobile applications, we’d like to meet you.\r\n\r\nUltimately, you’ll create both functional and appealing features that address our clients’ needs and help us grow our customer base.",
#         "roles_responsibilities": "Gather and evaluate user requirements in collaboration with product managers and engineers.\r\nIllustrate design ideas using storyboards, process flows and sitemaps.\r\nDesign graphic user interface elements, like menus, tabs and widgets.\r\nBuild page navigation buttons and search fields.\r\nDevelop UI mockups and prototypes that clearly illustrate how sites function and look like.\r\nCreate original graphic designs (e.g. images, sketches and tables)\r\nPrepare and present rough drafts to internal teams and key stakeholders.\r\nIdentify and troubleshoot UX problems (e.g. responsiveness)\r\nConduct layout adjustments based on user feedback.\r\nAdhere to style standards on fonts, colors and images.",
#         "education": [
#             "Any Degree"
#         ],
#         "industry_type": "IT Services",
#         "job_location": [
#             "Chennai",
#             "Mumbai",
#             "Bangalore"
#         ],
#         "employment_type": [
#             "Full-time",
#             "Part-time"
#         ],
#         "min_experience": 1,
#         "min_salary": 400000,
#         "max_salary": 550000,
#         "skills": [
#             "Wireframe.cc",
#             "InVision",
#             "Time-management",
#             "Team spirit",
#             "Communication"
#         ],
#         "openings": 5,
#         "created_date": "2022-05-17",
#         "company_name": "Company2",
#         "user": 4
#     }
# ]


# tfidf_vectorizer = TfidfVectorizer(
#     analyzer='word',
#     min_df=0.0,
#     max_df=1.0,
#     strip_accents=None,
#     encoding='utf-8',
#     preprocessor=None,
#     token_pattern=r'(?u)\S\S+'
# )

# tfidf_jobid = tfidf_vectorizer.fit_transform(
#     (df_all_job['text']))  # fitting and transforming the vector

# user_tfidf = tfidf_vectorizer.transform(df_user['text'])
# cos_similarity_tfidf = map(
#     lambda x: cosine_similarity(user_tfidf, x), tfidf_jobid)

# output2 = list(cos_similarity_tfidf)

# top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
# list_scores = [output2[i][0][0] for i in top]
# print("\nUsing TFIDF\n")
# print(get_recommendation(top, df_all_job, list_scores))

# Spacy Starts
# list_docs = []
# for i in range(len(df_all_job)):
#     doc = nlp("u'" + df_all_job['text'][i] + "'")
#     list_docs.append((doc, i))
# # print(len(list_docs))


# def calculateSimWithSpaCy(nlp, df, user_text, n=6):
#     # Calculate similarity using spaCy
#     list_sim = []
#     doc1 = nlp("u'" + user_text + "'")
#     for i in df.index:
#         try:
#             doc2 = list_docs[i][0]
#             score = doc1.similarity(doc2)
#             list_sim.append((doc1, doc2, list_docs[i][1], score))
#         except:
#             continue

#     return list_sim


# print("\nUsing spacy\n")

# df3 = calculateSimWithSpaCy(nlp, df_all_job, user_q.text[0], n=15)

# df_recom_spacy = pd.DataFrame(df3).sort_values([3], ascending=False).head(10)

# df_recom_spacy.reset_index(inplace=True)

# index_spacy = df_recom_spacy[2]
# list_scores = df_recom_spacy[3]

# print(get_recommendation(index_spacy, df_all_job, list_scores))

# KNN

# KNN = NearestNeighbors(n_neighbors=4, p=1)
# KNN.fit(tfidf_jobid)
# NNs = KNN.kneighbors(user_tfidf, return_distance=True)

# NNs[0][0][1:]

# top = NNs[1][0][1:]
# index_score = NNs[0][0][1:]

# print("\nUsing KNN\n")

# print(get_recommendation(top, df_all_job, index_score))
