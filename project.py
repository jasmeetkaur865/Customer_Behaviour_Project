import pandas as pd
df=pd.read_csv("customerbehavior.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.describe(include="all"))
print(df.isnull().sum())
#df["Review Rating"]=df.groupby("Category")["Review Rating"].transform (lambda x: x.fillna(x.median()))
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
print(df.columns)
#df=df.rename(columns={"purchase_amount":"purchase_amount"})

#create a new column
labels=["young_adults","adult","middle_aged","senior"]
df["age_group"]=pd.qcut(df["age"],q=4,labels=labels)
print(df[["age","age_group"]])

#create column purchase frequency days
frequency_mapping={"Fortnightly":14,
                   "Weekly":7,
                   "Monthly":30,
                   "Quarterly":90,
                   "Bi-Weekly":14,
                   "Annually":365,
                   "Every 3 Months":90}
df["purchase_frequency_days"]=df["frequency_of_purchase"].map(frequency_mapping)
print(df[["purchase_frequency_days","frequency_of_purchase"]])
print(df[["discount","promo"]].head())
df=df.drop("promo",axis=1)
print(df.columns)

#step import dataset into mysql
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:qwerty%40123@localhost:3306/salesdb"
)

df.to_sql(
    name="customer_behavior",
    con=engine,
    if_exists="replace",   # Creates/Replaces the table
    index=False
)

