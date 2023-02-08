# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 16:03:11 2023

@author: Seldon
"""

from flask import Flask, render_template, request
import pandas as pd
import openai_simple


class website_posts:
    def __init__(self):
        self.index = 0
        self.forum_data = pd.DataFrame()
    def get_first_n_items(self,n):
        # retrieve the first n items from your dataset
        items = self.forum_data.iloc[0:n]
        self.index += n
        items = items.submission_permalink.tolist()
        return items
    
    def get_next_n_items(self,n):
        # retrieve the next n items starting from start index from your dataset
        items = self.forum_data.iloc[self.index:(self.index+n)]
        items = items.submission_permalink.tolist()
        self.index +=n
        return items
    
    def get_n_links(self,n):
        links = self.forum_data.submission_permalink.sample(n).tolist()
        return(links)
    
    def load_local_data(self,path):
        self.forum_data = pd.read_csv(path)


# loads data
wp = website_posts()
wp.load_local_data("../Data/reddit_uc_simple.csv")

app = Flask(__name__)

@app.route("/")
def index():
    items = [wp.get_first_n_items(n=1)]
    return render_template("index.html", items=items)

@app.route("/more/<int:start>")
def more(start):
    items = wp.get_next_n_items(n=3)
    return render_template("more.html", items=items)

@app.route('/', methods=['POST'])
def search():
    search_query = request.form['search_query']
    
    lst = openai_simple.semantic_search([search_query], wp.forum_data.submission_text.tolist())
    order = [item['order'] for item in lst]
    links = wp.forum_data.iloc[order].submission_permalink.tolist()[0:5]
    return render_template("index.html", items=links)




if __name__ == "__main__":
    app.run()