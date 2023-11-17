from bs4 import BeautifulSoup

import requests
import webbrowser
import re
import codecs # встроенная бибилотека по чтению фалов 
from selenium import webdriver
import traceback
import time
import pandas as pd

from selenium.webdriver.common.by import By
df= pd.DataFrame({'Название':[], 'Публикатор': [] })

list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_8, list_10, list_11, list_12 =[], [], [], [], [], [], [], [], [], [], [], []
big_list=[]

list_name =[]
list_name_publicator=[]
def list_append(name):

    pass

def test_div(temp):
    pass






def get_info(temp, inn):
    browser = webdriver.Chrome()
    df= pd.DataFrame({})
    time.sleep(3)
    # print('temp',temp)
    for a in temp.find_all('a', href=True):
        
        link='https://fedresurs.ru/'+a['href']

        browser.get(link)
        
        time.sleep(3)
        html = browser.page_source
        bs = BeautifulSoup(html, 'html.parser')

        ##### ищем название 
        name_tag= bs.find('div', {'class': 'subject'})
        for name_in_h2 in name_tag.find_all('h2'):
            list_name.append(name_in_h2.get_text())
            df['Название']=[name_in_h2.get_text()]
        tt =name_tag.find_all('span')
            
        df['Дата']=[ tt[-1].get_text()]
        df['Сообщение']= [tt[-2].get_text()]
        df['ГлавныйИНН']=[inn]
        #####
        ##### ищем публикатора
        publicator= bs.find('div', {'class' : ['card-section']}) # публикатор 
        temp_name=''
        
        for number ,i in enumerate( publicator.find_all('span') ):
        
                
                if temp_name!='' and temp_name=='ИНН:':
                    list_4.append(i.get_text())
                    df['ИНН']=[i.get_text()]
                elif temp_name!='' and temp_name=='ОГРН:': 
                    list_5.append(i.get_text())
                    df['ОГРН']=[i.get_text()]

                temp_name=i.get_text()
                if temp_name !='' and temp_name!='ИНН:' and temp_name!='ОГРН:' and  number==0:
                    list_name_publicator.append(temp_name)
                    df['Публикатор']=[i.get_text()]

                    
            
        #####
        ##### ищем сообщение
    

        


        name_data= bs.find_all('div', {'class': 'td_title field-text'}) # название даты
        data = bs.find_all('div', {'class': 'field-value'}) # дата



        for  i, j in zip(name_data , data):
            df[i.get_text()]=[j.get_text()]
            
    


        table_info= bs.find_all('table', {'class': 'info_table'})
        try:
            for number , name in enumerate(table_info):

                for n, nam in enumerate(name.find_all('thead')):
                    
                    for j, na in enumerate(nam.find_all('th')):
                        
                        df[na.get_text()]=['' for i in range(len(list(df['Название'])))]
                        for k, name_tbody in enumerate(name.find_all('tbody')):
                            for l , name_tr in enumerate(name_tbody.find_all('td')):
                                if l==j :
                                    
                                    if name_tr.get_text()=='':
                                        break
                                        df=pd.concat([df, pd.DataFrame({na.get_text():['']})])
                                        
                                    else:
                                        df=pd.concat([df, pd.DataFrame({na.get_text():[name_tr.get_text()]})])
                            break

            

        except Exception:
            print('сломался 2', traceback.print_exc())      
    
        last_tag= bs.find('div', {'class': 'info'})
        temp_teg=''
        
        for i , name in enumerate(last_tag.find_all('span')):
            if i == len(last_tag.find_all('span'))-1:
                tag=last_tag.find('div', {'class': 'message-text'})
                tag=tag.get_text()
                try:
                    # df['ебаный коммеент тупого пользователя']= [name.get_text()]
                    df=pd.concat([df, pd.DataFrame({'ебаный коммеент тупого пользователя':[name.get_text() for i in range(len(list(df['Название'])))]})])
                    break
                except:
                    # 
                    pass
            
            temp_teg= name.get_text()
        

        
        
        return df
 
        

                

def function(df):

    df=pd.DataFrame()
    temp_df= pd.read_csv('C:\\Users\\Admin\\Desktop\\VS_code\\new_pars\\pic.csv')

    list_inn=temp_df[' 101 001 787 '].to_list()
    # print(len(list_inn[0]))
    list_inn1= [ i[1:] for i in list_inn ]
   
    list_inn2=[]

    for i in list_inn1:
        if i[1]!=' ':
            list_inn2.append('0'+str(i))
        else:
            list_inn2.append(str(i))

    # list_inn= [ 0+i[1:] for i in list_inn]

    list_inn3= [ i.replace(' ','')  for i in list_inn2]

    list_i=[list_inn3[0]]
    
    new_list_in_last_number=[]
    tag = False

    for i in list_inn3:

        if i == 7810183813 or i ==str(7810183813):
            tag=True
        if tag:
            new_list_in_last_number.append(i)
    # print(new_list_in_last_number)

    
    for number ,i in enumerate(new_list_in_last_number):#, 7704221591, 2246000565]: # остановилась на 1020010520
        try:
            url=f'https://fedresurs.ru/search/encumbrances?offset=0&limit=15&searchString={i}&additionalSearchFnp=true'
            # response = requests.get(url , timeout=(2,10))
            browser = webdriver.Chrome()
            
            browser.get(url)
            
            time.sleep(3)

            

            try: 
                while True:
                    time.sleep(1)
                    element=browser.find_element(By.CLASS_NAME, 'btn_loadmore').click()
                    
            except:
                print('end')
            time.sleep(1)
            html = browser.page_source
            bs = BeautifulSoup(html, 'html.parser')
            temp= bs.find_all('div', {'class' : ['encumbrances-result__body']})
   

            
            for new_i in temp:

                temp_df=get_info(new_i, i)

                df=pd.concat([df,temp_df], ignore_index=True)
            df.to_csv('C:\\Users\\Admin\\Desktop\\VS_code\\new_parstest_upload.csv')
         
        except Exception:
            print(traceback.print_exc())   
            print('Не прошли->',number ,i)
        

    return df


df=function(df)
df.to_csv('C:\\Users\\Admin\\Desktop\\VS_code\\new_parstest.csv')
print(list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_8, list_10, list_11, list_12)

# нужен модуль для создания excel файла 
#df = pd.DataFrame({'ASK': ['test'], 'ANS': ['test']})



# driver = webdriver.Chrome('chromedriver.exe')



# def search(name_ask):
#     df = pd.DataFrame({'ASK': ['test'], 'ANS': ['test']})    
   
#     for i in range(len(name_ask)):
        
#         if re.search(r'\ ', name_ask[i]):

#             #webbrowser.open_new_tab('https://' + name_ask[0] )
#             driver.get("http://www.google.com"+'/search?q='+ name_ask[i] )
#             try:

#                 elem= driver.find_element(By.XPATH, '//*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[1]')
#                 print(elem.text)
#                 new_row = {'ASK':name_ask[i], 'ANS':elem.text }
#                 df = df.append(new_row, ignore_index=True)
                
                
#             except: #
#                 try:
#                     elem= driver.find_element(By.XPATH, '//*[@id="Odp5De"]/div[1]/div/div[1]/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/span/span')
#                     print(elem.text)
#                     new_row = {'ASK':name_ask[i], 'ANS':elem.text }
#                     df = df.append(new_row, ignore_index=True)
                    
                    
#                 except:
#                     new_row = {'ASK':name_ask[i], 'ANS':'Ищи сам епта' }
#                     df = df.append(new_row, ignore_index=True)
                    
#                 pass
#         time.sleep(6)
#     df.to_excel('ans_google.xlsx') # создание excel файла
            

# #//*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[1]    

# def open_file():

    

#     fileObj = codecs.open( "qwerst.txt", "r", "utf_8_sig" )#ваш файл с вопросами
#     text = fileObj.read() # или читайте по строке
#     fileObj.close()

   
#     new_text= text.split('\r\n')
#     print(new_text[0])
#     search(new_text)
    
#     pass



# open_file()
