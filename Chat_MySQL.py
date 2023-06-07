# -*- coding: utf-8 -*-
"""
Created on Sat May  6 16:29:29 2023

@author: yonadab
"""


###################################################
##      CONNECT CHAT-GTP WITH MYSQL DATABASE     ##
###################################################


import openai
import pymysql as PSQL


def connect_openai(api):
    
    API_KEY = openai.api_key = api
    
    return



def clean_code(response):
    
    import regex as re

    pattern = '(?<=```).*?(?=\;)'
    
    rplc = response.replace('\n\n', '').replace('\n',' ').strip()
    
    find_pat = re.findall(pattern, rplc)
    
    sql_query = []
    
    for i in find_pat:
        if 'sql' in i or 'myslq' in i:
            temp = i.replace('sql','').replace('my','').replace('mysql','').strip()
            sql_query.append(temp)
        else:
            sql_query.append(i)
            
    return sql_query


def sql_connect(host, user, pswd, db_name, port):
    

    conn = PSQL.connect(host=host,
                         user=user,
                         password=pswd,
                         db=db_name,
                         port=port)
    
    Cursor = conn.cursor()
    
    return Cursor
    
    


while True:
    try:
        Q_host = input('Please enter your host to connect: ')
        Q_user = input('Please the user: ')
        Q_pass = input('Please enter you DB password: ')
        Q_name = input('Please enter the name of DB to connect: ')
        Q_port = int(input('Please enter the port number: '))
        
        
        conn = PSQL.connect(host=Q_host,
                        user=Q_user,
                        password=Q_pass,
                        db=Q_name,
                        port=Q_port)
        
        Cursor = conn.cursor()
        
        break

    except:
        print('\n')
        print('-----### Incorrect connect to your DB. Check your data ###------')
        print('\n')
        continue

     
    
Q_api = input('Please enter your API-KEY')
connect_openai(Q_api)

print('------------------------------------------------')
print('------------ Connected succesfully -------------')
print('------------------------------------------------')
print('\n')
print('Note: If you want to exit just enter the word "Done"')

while True:
    
    init_context = [{'role':'system',
                    'content': 'You are an assistant to generate MySQL code'}]
    
    
    
    question = input("What's your query? ")
    
    
    if question == 'Done':
        conn.close()
        print('See you :)')
        break
    
        
    
    ##Add the question to a context
    init_context.append({'role':'user', 'content': question})
    
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=init_context)
    
    ##Add the response to a context
    init_context.append({'role':'assistant', 'content':response})
    
    
    
    consult = clean_code(response.choices[0].message.content)
    
    
    
    try:
        Cursor.execute(consult[0])
        result = Cursor.fetchall()
        col_names = [column[0] for column in Cursor.description]
        print('\n')
        print('COLUMN NAMES:')
        print(col_names)
        print('\n')
        print(result)
        print('\n')

    except:
        print('\n')
        print('An error has ocurred. Try with other question')
        print("###### Hint: It's important indicate correctly the params like table name and columns")
    