import sqlite3
import pandas as pd
from langchain.prompts import PromptTemplate
import os
import torch
import re
from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from sentence_transformers import SentenceTransformer, util
import openai
import json


pattern = r'\{.*?\}'

openai.api_type = "azure" 
openai.api_base =  os.environ["AZURE_OPENAI_ENDPOINT"] 
openai.api_version = os.environ["AZURE_OPENAI_API_VERSION"]
openai.api_key = os.environ["AZURE_OPENAI_API_KEY"]


class datachat():
    def __init__(self):
        load_dotenv()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.corpus = []
        self.vectorize()
        self.corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)

    def exe_sql(self,statement):
        conn = sqlite3.connect('dbs.db')
        df = pd.read_sql_query(statement, conn)
        conn.close()
        return df



    def extract_code(self,response):
        start = 0
        q = ""
        temp_block=""
        for line in response.splitlines(): 
            if '```sql' in line and start==0:
                start=1
            if '```' == line.strip() and start==1:
                start =0
                break
            if start ==1 and '```' not in line:
                q=q+'\n'+line

        return q


        
    def vectorize(self):
        statement = '''select sql from sqlite_master where type = 'table' ;'''
        df = self.exe_sql(statement)
        meta = df.to_dict(orient='records')

        for i, chunk in enumerate(meta):
            self.corpus.append(str(chunk))
        return

    def get_chatGPT(self, input):
        response = openai.Completion.create( 
           engine="gpt-35-instruct",
           prompt=input,
           temperature=1,
           max_tokens=2000,
           top_p=0.8,
           frequency_penalty=0, 
           presence_penalty=0,
           best_of=1,
           stop=None)
        return response

    def search_table(self, query, top_k=8, acc_range = 50):
        results = []
        acc = []
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k) 
        for score, idx in zip(top_results[0], top_results[1]):
           results.append([self.corpus[idx], float(score*100)])
           if  float(score*100) < acc_range - 10  :
               break
    
        return results

    def data_ops(self,query):
        x_axis = 'NA'
        y_axis = 'NA'
        instruction = """
        As a SQL developer generate SQL statement for the query with reference to the database objects in the database schema and source is SQLITE.
        Treat first name and last name  as Name by Concatenating

        Database schema: """

        schema = self.search_table(query, 8 , 10)
        meta = str(schema)
        prompt_template = str(instruction) + str(meta) + '\n question: '+ str(query) +'\n answer SQL Query alone to extract the data:'
        try:
           completion = self.get_chatGPT(prompt_template )
           data = ''
           for comp in completion['choices']:
               data = comp["text"]
           
           gen_sql = self.extract_code(data) #response['text'])
           if gen_sql  <= ' ':
              gen_sql = data
           
           df = self.exe_sql(gen_sql)
        except:                                                     
           df = ['Re pharase the query and try']
           return df, x_axis, y_axis
        try:
           
           cols = ''
           col = ''
           for cl in df:
               cols = cols + str( cl ) + ', '
               col = cl
           
           if len(df[col]) <= 1:
              return df, x_axis, y_axis
           graph_q = 'Share the column name for x axis and y axis for line chart using the below column name.Columns: '+ cols +' . Reply only "x axis" and "y axis" column in python dict format inside {}. Sample expected output is {"x axis": ">
           g_data = ''
           graph_completion = self.get_chatGPT(graph_q )
           
           for g_comp in graph_completion['choices'] :
               g_data = g_comp["text"].replace('\n',' ')
           
           
           g_dict = json.loads(g_data)
           x_axis = g_dict['x axis'] #.replace('"','')
           y_axis = g_dict['y axis'] #.replace('"','')
           
           
        except:
           a = 1
           
        return df, x_axis, y_axis

                                                                      
