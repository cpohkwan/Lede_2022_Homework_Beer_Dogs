#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx")
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[3]:


df.shape
# 81,937 rows


# In[4]:


df.dtypes


# In[5]:


df.columns = df.columns.str.lower().str.replace(" ", "_")


# In[6]:


df.head(5)


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[7]:


# Each row is a pet dog that is issued a license. "Vaccinated" shows its vaccination status. "Spayed or Neut" shows whether it's sterilised.


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[8]:


# Is sterilisation more common among female dogs?
# What's the most common / popular breed of pet dogs over the years?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[9]:


df.primary_breed.value_counts().sort_values(ascending=False).head(10).sort_values().plot(kind="barh", title="Most Popular Breeds")


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[10]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values="Unknown")
df[df == "primary_breed"].shape


# In[11]:


df.columns = df.columns.str.lower().str.replace(" ", "_")


# In[12]:


df.primary_breed.value_counts().sort_values(ascending=False).head(10).sort_values().plot(kind="barh", title="Most Popular Breeds (Excluding Unknown)")


# ## What are the most popular dog names?

# In[13]:


df.animal_name.value_counts()


# In[14]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values="UNKNOWN")
df.columns = df.columns.str.lower().str.replace(" ", "_")


# In[15]:


df.animal_name.value_counts().sort_values(ascending=False).head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[16]:


df.query("animal_name == 'Poh'")


# In[17]:


df.query("animal_name == 'Max'").shape
# 515 dogs are named "Max".


# In[18]:


df.query("animal_name == 'Maxwell'").shape
# 30 dogs are named "Maxwell"


# ## What percentage of dogs are guard dogs?

# In[19]:


# Assuming that 'yes' - guard dogs
df["guard_or_trained"].value_counts(normalize=True, dropna=False)*100
# 0.06% are guard dogs


# ## What are the actual numbers?

# In[20]:


df["guard_or_trained"].value_counts(dropna=False)


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[21]:


df.shape


# In[22]:


df["guard_or_trained"].value_counts(dropna=False)


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[23]:


# Assuming that empty cells are "NaN"
import numpy as np

df.guard_or_trained.replace(" ", np.nan)
df.guard_or_trained.value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[24]:


df[df.guard_or_trained == 'Yes'].primary_breed.value_counts()
# Top dog breeds for guard dogs are German Shepherd, Chihuahua, Labrodor Retriever, Rottweiler, and American Pit Bull Mix.


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[25]:


year = df["animal_birth"].apply(lambda birth:birth.year)
year


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[26]:


age = 2022 - year
age.mean()


# In[27]:


age.median()


# # Joining data together

# In[28]:


neighborhood = pd.read_csv("zipcodes-neighborhoods.csv")
neighborhood.head(5)


# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[29]:


merged = df.merge(neighborhood, left_on="owner_zip_code", right_on="zip")
merged.head(5)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[30]:


merged.query("borough == 'Bronx'").animal_name.value_counts().head(10)
# Rocky is the most popular name


# In[31]:


merged.query("borough == 'Brooklyn'").animal_name.value_counts().head(10)

# Max is the most popular name.


# In[32]:


merged.query("neighborhood == 'Upper East Side'").animal_name.value_counts().head(10)
# Lucy is the most popular name 


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[33]:


merged["primary_breed"] = merged.primary_breed.replace("Unknown", np.nan)
merged.head(5)


# In[34]:


pd.set_option("display.max_rows", None)
merged.groupby("neighborhood").primary_breed.value_counts().sort_values(ascending=False)


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[35]:


merged.groupby("animal_gender").spayed_or_neut.value_counts(dropna=False)
# 8 missing values in gender
merged["animal_gender"] = merged.animal_gender.replace(" ", np.nan)


# In[36]:


merged[merged.spayed_or_neut == "No"].primary_breed.value_counts().head()
# Yorkshire Terrier are least likely to be neutered. 


# In[37]:


merged.query('spayed_or_neut == "No" & primary_breed == "Yorkshire Terrier"').animal_gender.value_counts(normalize=True)*100

# Male Yorkshire Terriers are least likely to be neutered. 


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[38]:


# convert all text to lower case first
merged["animal_dominant_color"] = merged["animal_dominant_color"].str.lower()


# In[39]:


# Including both "gray" and "grey"

monochrome = ["black", "white", "gray", "grey"]
merged.animal_dominant_color.isin(monochrome).value_counts()


# In[40]:


merged["monochrome"] = merged.animal_dominant_color.isin(monochrome) & merged.animal_secondary_color.isna() & merged.animal_third_color.isna()


# In[41]:


merged.monochrome.value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[42]:


merged.groupby("borough").size().sort_values().plot(kind="barh",title="Number of dogs with licence in NYC")


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[43]:


population = pd.read_csv("boro_population.csv")
population.head()


# In[44]:


dog = pd.DataFrame(merged.groupby("borough").size())
dog


# In[45]:


combined = dog.merge(population, left_on="borough", right_on="borough")
combined.head()


# In[46]:


combined["dog"] = combined[0]
combined


# In[47]:


dog_per_capita = combined.dog / combined.population * 1000000
dog_per_capita
# Manhattan has the highest dog_per_capita. 


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[89]:


merged.groupby("borough").primary_breed.value_counts()


# In[99]:


top_breed = pd.crosstab(merged.primary_breed, merged.borough)


# In[108]:


top_breed["Bronx"].sort_values(ascending=False).head(5).sort_values().plot(kind="barh", title="Top 5 breeds in Bronx")


# In[109]:


top_breed["Brooklyn"].sort_values(ascending=False).head(5).sort_values().plot(kind="barh", title="Top 5 breeds in Brooklyn")


# In[110]:


top_breed["Manhattan"].sort_values(ascending=False).head(5).sort_values().plot(kind="barh", title="Top 5 breeds in Manhattan")


# In[111]:


top_breed["Queens"].sort_values(ascending=False).head(5).sort_values().plot(kind="barh", title="Top 5 breeds in Queens")


# In[112]:


top_breed["Staten Island"].sort_values(ascending=False).head(5).sort_values().plot(kind="barh", title="Top 5 breeds in Staten Island")


# In[ ]:


# Really can't do this in one chart

