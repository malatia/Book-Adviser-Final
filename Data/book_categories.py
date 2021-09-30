#%%
import requests

# %%
response = requests.get("https://openlibrary.org/api/books?bibkeys=ISBN:0201558025&jscmd=data&format=json")

# %%
response.text
# %%
json = response.json()
# %%
print(type(json))
# %%
print ("Dict key-value are : ")
for i in json :
    print(f"{i} ------------ {json[i]}")
# %%
print(type(json["ISBN:0201558025"]))

#%%
print(json["ISBN:0201558025"]["subjects"])

#%%
for i in json["ISBN:0201558025"]["subjects"]:
    print(i["name"])

#%%
def cat_retrieve(isbn):
    response = requests.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json")
    json = response.json()
    subjects_list = [subject["name"] for subject in json[f"ISBN:{isbn}"]["subjects"]]
    #return "//".join(subjects_list)
    return subjects_list


test = cat_retrieve(9781407109084)
print(test)



# %%
subjects = []
for livre in json :
    print(type(livre))

# %%
import pandas as pd
import numpy as np

# %%
books = pd.read_csv("books.csv")
books

# %%
print(str(int(books["isbn13"].iloc[0])))
# %%
books.dtypes
# %%
books.isna().sum()

#%%
books.insert(len(books.columns), "categories", "non")

# %%

for i in range(books.shape[0]):
    if not pd.isnull(books["isbn13"].iloc[i]):
        isbn = str(int(books["isbn13"].iloc[i]))
        print(isbn)
        books["categories"].iloc[i] = "oui"



# %%
books["categories"].value_counts()

# %%
print(books.shape)
# %%
book_tags = pd.read_csv("book_tags.csv")
book_tags
# %%
book_tags["count"].value_counts()
# %%
test = book_tags[book_tags["count"] > 100]
test
# %%
tags = pd.read_csv("tags.csv")
tags
# %%
merge = test.merge(tags, how="left", on="tag_id")
merge
# %%
len(merge["tag_id"].unique())
# %%
