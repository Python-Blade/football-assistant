import pandas as pd
import sqlite3
import os

DB_NAME = "football.db"
DATASET_DIR = "dataset"

def load_data():
    
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Removed existing {DB_NAME}")

    conn = sqlite3.connect(DB_NAME)

    csv_files = [
        "appearances.csv",
        "games.csv",
        "leagues.csv",
        "players.csv",
        "shots.csv",
        "teams.csv",
        "teamstats.csv"
    ]
    
    for file_name in csv_files:

        file_path = os.path.join(DATASET_DIR, file_name)


        if os.path.exists(file_path):
        
            try:
                df = pd.read_csv(file_path)
                
                table_name = file_name.replace(".csv", "")
                
                df.to_sql(table_name, conn, if_exists="replace", index=False)

            except Exception as e:
                print(f"Error loading {file_name}: {e}")


        else:
            print(f"Warning: {file_name} not found in {DATASET_DIR}")

    conn.close()

if __name__ == "__main__":
    load_data()
