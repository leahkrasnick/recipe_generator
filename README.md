 finalproject
final project for si206
- Data sources used:
To gather my data I crawled through and scraped the allrecipes.com website. I stored the scraped data from this website in two CSV files.
recipe.CSV holds all the data for the ingredients in each recipe and time_cals.CSV holds all the nutrition facts for each recipe. To access
the data sources, a user would have to run scrape_recipes.py and the two functions, get_recipe_data and get_cal_cook_time both scrape
allrecipes.com and gather the data needed for the database. Once the scraped data is loaded into the CSV files, the data is then transfered
from the CSVs to a database called stuff.db. 
- Structure:
The code begins with the caching function that holds all the data for the recipes scraped from allrecipes.com. After the caching,
get_recipes and get_cal_cook_time scrape the website allrecipes.com and load all the data into dictionaries. The dictionary from get_recipes
contains the food name as a key and the ingredients needed for that recipe as the value, the dictionary from get_cal_cook_time contains the food name as a key and
a list with the calories, cook time, protein and fat. These dictionaries are then used to create the two CSV files for ingredient data and
nutrition data. The CSV files are then loaded into two separate tables in the database. After all data is stored in the database, 
an interactive_prompt function is run. This function asks the user for their input and saves the user's input in a list. This list 
of numbers (user choices) will then be used to grab select data from the database as well as create graphs and ingredient lists in plotly. 

- User guide:, including how to run the program and how to choose presentation options.
To run this program, first pull all data from github. Once the data is pulled, create a virtual environment. Because the home directory
on my computer has a space in it, I use /tmp in my virtualenv path. So to begin after the files are pulled from github, create a virtual 
environment and install the requirements.txt to be able to use all the modules I have included. Once all the modules are installed, the user
will then run "python3 scrape.py" in their terminal and a user guide will pop up. The first prompt will ask if you want to start the program
and the user can type 1 (enter) to begin and 2 (enter) to exit. Once started the user will be prompted with a choice of foods, the user will
then choose which food they want to find a recipe for. They will enter the number corresponding to the food and enter it. Then the user will 
be prompted to choose a filter to find a recipe for them. They can filter based on calories or the time it takes to cook the recipe. To filter
the recipes based on calories/cook time the user will enter 1 (enter) or 2 (enter), (or 3 to exit). If the user chooses calories, they will
be asked what number of calories they want their recipe to be below and if they choose cook time they will enter what number of minutes they want 
their recipe to be done under. Then the program will choose a recipe and ask the user how they want to compare this recipe to other recipes
that are similar to it. The 4 different data presentations are for the user tp compare their recipe to other recipes based on calories, protein,
fat, or cook time. Once a user enters a number corresponding to their choice, two tabs will open up in their browser. One tab will contain 
a graph comparing their recipe to other similar recipes based on their choice. The second tab will have a table showing the random recipe 
chosen for them based on their criteria as well as the ingredients needed for the recipe. The program will automatically re-route to the 
welcome page and run again for the user and the user can quit or run the program again for a new recipe. 
