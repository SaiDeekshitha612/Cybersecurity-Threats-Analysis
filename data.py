import os
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
file_path = 'C:/Users/gudur/Desktop/Projects/Global_Cybersecurity_Threats_2015-2024.csv'

try:
    df = pd.read_csv(file_path)
    print("File loaded successfully")
except Exception as e:
    print(e)
print(df.info())
print(df.head())
# print(df.isnull().sum())
dataset_copy = df.copy()

def clean_dataset(df):
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True) 
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^\w\s]', '', regex=True)
    columns_to_clean = ['country','attack_type','target_industry','attack_source','security_vulnerability_type','defense_mechanism_used']

    for col in columns_to_clean:
        df[col] = df[col].str.strip().str.title()
    print(df.info())
    return df
df = clean_dataset(df)
print(df.head())
print("cleaning completed successfully")

connection = mysql.connector.connect(
    host='localhost',
    user='root',   
    password='Deekshu@06',  
    database='cybersecurity'  
)
cursor = connection.cursor()
print("Connection established")
def insert_data_to_mysql(df, cursor, connection):
    # Inserting
    insert_query = """
        INSERT INTO attacks (country, year, attack_type, target_industry, financial_loss_in_million,
                             number_of_affected_users, attack_source, security_vulnerability_type,
                             defense_mechanism_used, incident_resolution_time_in_hours)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for row in df.itertuples(index=False):
        cursor.execute(insert_query, row)
    connection.commit()
    print(f"{cursor.rowcount} rows inserted into the database!")
insert_data_to_mysql(df, cursor, connection)
cursor.close()

def perform_analysis(df):
    from tabulate import tabulate  
# Top countries affected by cyber attacks
    top_countries = df['country'].value_counts().head(10)
# Frequency of different types of threats
    threat_frequency = df['attack_type'].value_counts()
# Year over year trends
    yearly_trends = df.groupby('year').size()
# Impact by region 
    impact_by_region = df.groupby('country')['financial_loss_in_million_'].sum().sort_values(ascending=False).head(10)
# Correlation between attack type and sector
    attack_sector_correlation = df.groupby(['attack_type', 'target_industry']).size().unstack(fill_value=0)

def print_table(title, data):
    print(f"\n {title}")
    print(tabulate(data.items() if isinstance(data, pd.Series) else data, headers='keys', tablefmt='pretty'))
    print_table("Top 10 Countries Affected by Cyber Attacks", top_countries)
    print_table("Frequency of Threat Types", threat_frequency)
    print_table("Year-over-Year Incident Counts", yearly_trends)
    print_table("Top 10 Countries by Financial Impact", impact_by_region)
    print_table("Attack Type vs. Target Industry Matrix", attack_sector_correlation)
perform_analysis(df)

def plot_graphs(df):
    plt.figure(figsize=(10, 6))
    top_countries = df['country'].value_counts().head(10)
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
    plt.title("Top 10 Countries Affected by Cyber Attacks")
    plt.xlabel("Number of Incidents")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='attack_type', order=df['attack_type'].value_counts().index, palette='magma')
    plt.title("Frequency of Different Threat Types")
    plt.xlabel("Count")
    plt.ylabel("Attack Type")
    plt.tight_layout()
    plt.show()
perform_analysis(df)
plot_graphs(df)
connection.close()

