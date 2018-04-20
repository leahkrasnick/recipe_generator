from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import json
import os
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import random




CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print('fetching new data...')
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

food_list = ['pizza dinner', 'pasta dinner', 'burger dinner',
 'steak dinner', 'cupcake dessert', 'salmon dinner', 'tiramisu dessert']
foods_l = ["pizza","pasta","burger", "steak","salmon","cupcake","tiramisu"]

def get_recipes(string):
    baseurl = 'https://www.allrecipes.com/search/results/'
    x = string.split()[0]
    url_soup = baseurl + str(x)
    item = make_request_using_cache(url_soup)
    item_soup = BeautifulSoup(item, 'html.parser')
    list_links=[]
    searching_div = item_soup.find(class_='recipe-section fixed-grid')
    single_recipe = searching_div.find_all(class_='fixed-recipe-card')
    for x in single_recipe:
        divs = x.find(attrs={'class':"fixed-recipe-card__h3"})
        t = divs.find('a')
        u = t.get('href')
        list_links.append(u)
    recipe_dict = {}
    list_links = list_links[:15]

    for recipe in list_links:
        recipe1 = make_request_using_cache(str(recipe))
        recipe_soup = BeautifulSoup(recipe1, 'html.parser')
        search = recipe_soup.find(attrs={'class':'ar_recipe_index full-page'})
        list_ingred = search.find(id = 'lst_ingredients_1')
        labels = list_ingred.find_all('label')
        ingredients_item = []
        for x in labels:
            ingredients_item.append(x.text.strip())
        list_ingred2 = search.find(id = 'lst_ingredients_2')
        labels2 = list_ingred2.find_all('label')
        for x2 in labels2[:-1]:
            ingredients_item.append(x2.text.strip())
        r = ((recipe.split('/'))[-2]).split('-')
        e = ' '.join(r)
        recipe_dict[e] = ingredients_item

    return recipe_dict


def get_cal_cook_time(string):
    baseurl = 'https://www.allrecipes.com/search/results/'
    x = string.split()[0]
    url_soup = baseurl + str(x)
    item = make_request_using_cache(url_soup)
    item_soup = BeautifulSoup(item, 'html.parser')
    list_links=[]
    searching_div = item_soup.find(class_='recipe-section fixed-grid')
    single_recipe = searching_div.find_all(class_='fixed-recipe-card')
    for x in single_recipe:
        divs = x.find(attrs={'class':"fixed-recipe-card__h3"})
        t = divs.find('a')
        u = t.get('href')
        list_links.append(u)
    details_dict = {}
    list_links = list_links[:15]

    for recipe in list_links:
        list_per_recipe = []
        recipe1 = make_request_using_cache(str(recipe))
        recipe_soup = BeautifulSoup(recipe1, 'html.parser')
        search = recipe_soup.find(attrs={'class':'ar_recipe_index full-page'})
        ing_l=search.find(attrs={'class':'recipe-ingredients__header__toggles'})
        stuff = ing_l.find(attrs={'class':'calorie-count'})
        cals = stuff.find('span').string
        list_per_recipe.append(cals)
        time = ing_l.find(attrs={'class':'ready-in-time'}).string
        list_per_recipe.append(time)
        health=search.find(attrs={'class':'recipe-footnotes','itemprop':'nutrition'})
        next_find = health.find('div')
        protein = next_find.find(attrs={'itemprop':'proteinContent'}).string
        list_per_recipe.append(protein)
        fat = next_find.find(attrs={'itemprop':'fatContent'}).string
        list_per_recipe.append(fat)
        r = ((recipe.split('/'))[-2]).split('-')
        e = ' '.join(r)
        details_dict[e] = list_per_recipe

    return details_dict

def health_add_to_csv():
    csvfile1 = "time_cals.csv"
    csvfile = open(csvfile1, 'w')
    columnTitleRow = "type, food, calories, cook time, protein, fat\n"
    csvfile.write(columnTitleRow)

def add_to_csv():
    csvfile1 = "recipe.csv"
    csvfile = open(csvfile1, 'w')
    columnTitleRow = "type, food, recipe, meal\n"
    csvfile.write(columnTitleRow)

def health_add_more(details_dict, user_input):
    x = (user_input.split())[0]
    fd = open('time_cals.csv','a')
    for key in details_dict.keys():
        food = key
        cals = details_dict[key][0]
        hour_to_min = 0
        time_min = 0
        hour_min = (details_dict[key][1]).split(' ')
        if hour_min[-1] == 'h':
            time_min = int(hour_min[0]) * 60
        elif hour_min[1] == 'm':
            time_min = int(hour_min[0])
        if hour_min[1] == 'h' and hour_min[-1] == 'm':
            time_min = (int(hour_min[0]) * 60) + int(hour_min[2])
        protein = details_dict[key][2]
        fat = details_dict[key][3]
        row =str(x)+","+food+","+cals+","+str(time_min)+","+protein+","+fat+"\n"
        fd.write(row)


def ingred_add_more(recipe_dict, user_input):
    x = (user_input.split())[0]
    y = (user_input.split())[1]
    fd = open('recipe.csv','a')
    for key in recipe_dict.keys():
        foods = key
        ingred = recipe_dict[key]
        row = str(x) + ","+foods+","+"\""+','.join(ingred)+"\""+","+str(y)+"\n"
        fd.write(row)

def write_data_base(file):
    DBNAME = 'stuff.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    drop_ingred = 'DROP TABLE IF EXISTS "Ingredients_table"'
    cur.execute(drop_ingred)
    conn.commit()
    ingred_statement = ''' CREATE TABLE IF NOT EXISTS 'Ingredients_table' (
    Id INTEGER PRIMARY KEY,
    Type TEXT NOT NULL,
    Food TEXT NOT NULL,
    Recipe TEXT NOT NULL,
    Meal TEXT NOT NULL)
    '''
    cur.execute(ingred_statement)
    conn.commit()

    with open (file, 'r') as f:
        reader = csv.reader(f)
        columns = next(reader)
        cur = conn.cursor()
        query = '''INSERT INTO Ingredients_table ({0}) values ({1})'''
        query = query.format(','.join(columns), ','.join('?' * len(columns)))
        for data in reader:
            cur.execute(query, data)
        conn.commit()

def health_write_data_base(file):
    DBNAME = 'stuff.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    drop_table = 'DROP TABLE IF EXISTS "details_table"'
    cur.execute(drop_table)
    conn.commit()
    ingred_statement = ''' CREATE TABLE IF NOT EXISTS 'details_table' (
    Id INTEGER PRIMARY KEY,
    Type_food TEXT NOT NULL,
    Food TEXT NOT NULL,
    Calories INTEGER NOT NULL,
    Cook INTEGER NOT NULL,
    Protein REAL NOT NULL,
    Fat REAL NOT NULL)
    '''
    cur.execute(ingred_statement)
    conn.commit()

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        conn = sqlite3.connect('stuff.db')
        cur = conn.cursor()
        for x in reader:
            query = '''INSERT INTO "details_table"(Id, Type_food, Food,
             Calories, Cook, Protein, Fat)
             VALUES (?,?,?,?,?,?,?)'''
            cur.execute(query, (None, x['type'], x[' food'],
             int(x[' calories']), int(x[' cook time']), float(x[' protein']),
              float(x[' fat'])))
        conn.commit()


def call_to_database(list_num):
    x = ''
    conn = sqlite3.connect('stuff.db')
    cur = conn.cursor()
    if int(list_num[1]) == 1:
        statement = '''
        SELECT Ingredients_table.Food, Recipe
        FROM Ingredients_table
          JOIN details_table
          ON details_table.Food = Ingredients_table.Food
          WHERE details_table.Type_food = '{}' AND details_table.Calories < {}
          ORDER BY details_table.Calories ASC
        LIMIT 15
        '''.format(foods_l[int(list_num[0])-1], int(list_num[2]))
        cur.execute(statement)
        list_ = []
        for row in cur:
            list_.append(row)
        num = len(list_)
        num1 = random.randint(0, num-1)
    elif int(list_num[1]) == 2:
        statement2 = '''
        SELECT Ingredients_table.Food, Recipe
        FROM Ingredients_table
          JOIN details_table
          ON details_table.Food = Ingredients_table.Food
          WHERE details_table.Type_food = '{}' AND details_table.Cook < {}
          ORDER BY details_table.Cook ASC
         LIMIT 15
        '''.format(foods_l[int(list_num[0])-1], int(list_num[3]))
        cur.execute(statement2)
        list_ = []
        for row in cur:
            list_.append(row)
        num = len(list_)
        if num == 0:
            print ("No results for filter, sorry")
        num1 = random.randint(0, num-1)
    return [list_[num1][0], list_[num1][1]]

def plotly_plot(data_l):
    conn = sqlite3.connect('stuff.db')
    cur = conn.cursor()
    index_num = int(data_l[-3])
    list_select = ['Calories', 'Protein', 'Fat', 'Cook']
    graph_type = list_select[index_num -1]
    df = pd.read_sql_query('''
    SELECT details_table.Food as f, {} as m FROM details_table
    WHERE details_table.Type_food = '{}' AND details_table.Food != '{}'
    '''.format(graph_type, foods_l[int(data_l[0])-1], data_l[5]), conn)
    df2 = pd.read_sql_query('''
    SELECT details_table.Food as r, {} as y FROM details_table
    WHERE details_table.Type_food = '{}' AND details_table.Food = '{}'
    '''.format(graph_type, foods_l[int(data_l[0])-1], data_l[5]), conn)
    if index_num == 4:
        graph_type = 'Cooking time'

    data1 = go.Bar(
            x= df.f,
            y= df.m,
            name = 'Other Similar Recipes')

    data2 = go.Bar(
            x= df2.r,
            y= df2.y,
            name = 'Your recipe')
    layout = go.Layout(
        title='{} per recipe'.format(graph_type),
    )
    fig = go.Figure(data=[data1, data2], layout=layout)
    url_plot = py.plot(fig, filename='Compare recipe graph')
#-------------------------------------------------------#
    ingred1 = data_l[-1].split(',')
    new_list = '<br>'.join(ingred1)
    trace = go.Table(
    header=dict(values=['Food', 'Ingredients'],
                line = dict(color='#ffc66b'),
                fill = dict(color='#ffc66b'),
                font = dict(color = 'black', size = 30),
                height = 40),
    cells=dict(values=[['<br>' + data_l[5], ' '],
                       [new_list, '']],
                       line = dict(color='#ffffff'),
                       fill = dict(color='#ffffff'),
                       font = dict(color = 'black', size = 20),
                       height = 600))
    datar = [trace]
    layout2 = go.Layout(
        title='Food-Ingredients Result',
    )
    fig2 = go.Figure(data=datar, layout=layout2)
    py.plot(fig2, filename = 'ingredients_table')


def interactive_prompt():
    response = ''
    print (' - * - * - * - * - * - * - * - * - * - * -')
    print ("                  Hello!                  ")
    print (' - * - * - * - * - * - * - * - * - * - * -')
    while response != '2':
        print ("\n - Welcome to the Random Recipe Generator! - ")
        print ("\n     To begin, please select an option: ")
        print ('           1) Find a recipe\n           2) exit')
        response = input('Enter an option: ')

        while response not in ['1', '2']:
            response = input('Bad input. Enter an option: ')
        if int(response) == 1:
            cal_ = 0
            minit = 0
            print('''\nWe have recipes for: \n 1) pizza\n 2) pasta\n 3) burgers\n 4) steak\n 5) salmon\n 6) cupcakes\n 7) tiramisu\n 8) exit''')
            food_choice = input('''\nPlease enter a number corresponding to your choice ''')
            while food_choice not in ['1','2','3','4','5','6','7','8']:
                food_choice = input('''\nBad input! Please enter a number corresponding to your choice ''')
            if int(food_choice) == 8:
                break
            print('''\nFilter recipes based on:\n 1) Calories\n 2) cook time\n 3) exit''')
            filter_choice = input('''\nPlease enter a number corresponding to your choice ''')
            while filter_choice not in ['1','2','3']:
                filter_choice = input('''\nBad input! Please enter a number corresponding to your choice ''')
            if int(filter_choice) == 3:
                break
            if int(filter_choice) == 1:
                print("\nFind recipe with below ___ calories\n")
                cal_ = input('Please enter a number ')
                try:
                    cal_ = int(cal_)
                except:
                    cal_ = cal_
                while type(cal_) != type(1):
                    cal_ = int(input('''\nBad input! Please enter a number corresponding to your choice '''))
            elif int(filter_choice) == 2:
                print("\nFind recipe that takes under _____ minutes\n")
                minit = input('''Please enter a number of minutes (1.5 hours is 90 minutes) ''')
                try:
                    minit = int(minit)
                except:
                    minit = minit
                while type((minit)) != type(1):
                    minit = int(input('''\nBad input! Please enter a number of minutes '''))
            entry_list = [int(food_choice), filter_choice, cal_, minit]
            status = False
            while status == False:
                try:
                    data3 = (call_to_database(entry_list))
                    status = True
                except:
                    status = False
                    print("\nNo results for input, please try a larger entry\n")
                    if int(filter_choice) == 1:
                        cal_ = input('Please enter a number ')
                    elif int(filter_choice) == 2:
                        minit = input('''Please enter a time in minutes ''')
                    entry_list = [int(food_choice), filter_choice, cal_, minit]
            food_name = data3[0]
            recipe_stuff = data3[1]
            print('''\n\nCompare recipe to other {} recipes by:\n 1) Calories\n 2) Protein\n 3) Fat\n 4) Cook time\n
            '''.format(foods_l[int(food_choice)-1]))
            data_choice = input('''\nPlease enter a number corresponding to your choice ''')
            while data_choice not in ['1','2','3','4']:
                data_choice = input('''\nBad input! Please enter a number corresponding to your choice ''')
            entry_list.append(int(data_choice))
            entry_list.append(food_name)
            entry_list.append(recipe_stuff)
            plotly_plot(entry_list)
            continue
        elif int(response) == 2:
            print ("\nGoodbye")
            return
        else:
            print("Command not recognized: bad command ")

if __name__=="__main__":
    if os.stat("recipe.csv").st_size==0 and os.stat("time_cals.csv").st_size==0:
        add_to_csv()
        health_add_to_csv()
        for x in food_list:
            dict_recipe = get_recipes(x)
            detail = get_cal_cook_time(x)
            ingred_add_more(dict_recipe, x)
            health_add_more(detail,x)
        write_data_base('recipe.csv')
        health_write_data_base('time_cals.csv')
    interactive_prompt()
