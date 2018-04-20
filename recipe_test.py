import unittest
import json
import requests
import scrape_recipe as r_data
import sqlite3


class TestRecipe(unittest.TestCase):

    def test_get_recipe(self):
        pizza1 = r_data.get_recipes('pizza dinner')
        pasta1 = r_data.get_recipes('pasta dinner')
        self.assertEqual(type(pizza1), type({}))
        self.assertEqual(type(list(pasta1.keys())[0]), type(''))
        self.assertEqual(type(list(pasta1.values())[0]), type([]))

    def test_call_to_database(self):
        calories = r_data.call_to_database([1,1, 500, 0])
        cook_time = r_data.call_to_database([1,2,0,75])
        self.assertEqual(type(calories), type([]))
        self.assertEqual(len(calories), 2)
        self.assertEqual(len(cook_time), 2)

    def test_get_cal_cook_time(self):
        cupcake1 = r_data.get_cal_cook_time('cupcakes dessert')
        tiramisu1 = r_data.get_cal_cook_time('tiramisu dessert')
        self.assertEqual(type(float(list(cupcake1.values())[0][-1])), type(3.2)) #checks if the value in the dictionary can be turned into a float
        self.assertEqual(type(float(list(cupcake1.values())[0][-2])), type(3.2))
        self.assertEqual(type(int(list(tiramisu1.values())[0][-4])), type(3)) #checks if the value in the dictionary can be turned into an int

    def test_database(self):
        conn = sqlite3.connect('stuff.db')
        cur = conn.cursor()
        sql0 = 'SELECT COUNT (*) FROM details_table'
        results = cur.execute(sql0)
        count = results.fetchone()[0]
        self.assertTrue(count > 100)

        sql2 = 'SELECT COUNT (*) FROM ingredients_table'
        results1 = cur.execute(sql2)
        count1 = results1.fetchone()[0]
        self.assertTrue(count1 > 100)

        sql3 = 'SELECT Protein FROM details_table'
        results3 = cur.execute(sql3)
        first_protein = results3.fetchone()[0]
        self.assertEqual(type(first_protein), type(9.9))
        self.assertEqual(first_protein, 5.5)

        sql4 = 'SELECT Calories FROM details_table'
        results4 = cur.execute(sql4)
        first_cal = results4.fetchone()[0]
        self.assertEqual(type(first_cal), type(9))
        self.assertEqual(first_cal, 189)

        sql5 = 'SELECT Recipe FROM ingredients_table'
        results5 = cur.execute(sql5)
        recipe_1 = results5.fetchone()[0]
        self.assertEqual(type(recipe_1), type(''))
        self.assertTrue(len(recipe_1) > 1)

unittest.main()
