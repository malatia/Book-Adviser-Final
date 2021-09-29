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



