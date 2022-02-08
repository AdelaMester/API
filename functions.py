import sqlite3
import csv


# Connect to the database
conn = sqlite3.connect('files.db')

# Create a cursor object to execute queries on the database
cursor = conn.cursor()


# Open the csv file, read it and save the content in the adgroup variable
with open("adgroups.csv", "r") as data:
    adgroup = csv.reader(data)

    # SQL query to insert data into adgroup table
    insert_content = "INSERT INTO adgroup (ad_group,campaign_id,alias,status) VALUES(?,?,?,?)"

    # Import content of adgroups.csv into database
    cursor.executemany(insert_content, adgroup)

    #Commiting the changes
    conn.commit()

    #Closing the connection
    conn.close()

# Open the csv file, read it and save the content in the campaigns variable
with open("campaigns.csv", "r") as data:
    campaigns = csv.reader(data)

    # SQL query to insert data into campaigns table
    insert_content = "INSERT INTO campaigns (campaign_id,structure_value,status) VALUES(?,?,?)"

    # Import content of campaigns.csv into database
    cursor.executemany(insert_content, campaigns)

    #Commiting the changes
    conn.commit()

    #Closing the connection
    conn.close()

# Open the csv file, read it and save the content in the search_terms variable
with open("search_terms.csv", "r") as data:
    search_terms = csv.reader(data)

    # SQL query to insert data into search_terms table
    insert_content = "INSERT INTO search_terms (date,ad_group_id,campaign_id,clicks,cost,conversion_value,conversions,search_term) VALUES(?,?,?,?,?,?,?,?)"

    # Import content of search_terms.csv into database
    cursor.executemany(insert_content, search_terms)

    #Commiting the changes
    conn.commit()

    #Closing the connection
    conn.close()