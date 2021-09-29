#%%
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate, GridSearchCV


# %%
ratings = pd.read_csv("ratings.csv")
ratings

# %%
reader = Reader(rating_scale=(1,5))
data = Dataset.load_from_df(ratings[["user_id", "book_id", "rating"]], reader)

# %%
algo = SVD()

cross_validate(algo, data, measures=["RMSE", "MAE"], cv =5, n_jobs=-1, verbose=True)

# %%
param_grid = {'n_epochs': [30], 'lr_all': [0.01, 0.005], 'reg_all': [0.1], "n_factors" : [100,150,200]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)

# %%
gs.fit(data)
# %%
print(gs.best_score["rmse"])
print(gs.best_score["mae"])
# %%
print(gs.best_params)
# %%
algo = gs.best_estimator
# %%

from surprise import dump
dump.dump("SVD1", algo=algo)
# %%
