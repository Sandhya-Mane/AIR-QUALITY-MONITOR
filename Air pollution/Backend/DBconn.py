import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mini_project_db"
DB_USER = "postgres"
DB_PASSWORD = "root"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
'''
# Load SO2 data
so2_df = pd.read_csv(r"D:\Project\Mini project\Air pollution\Datasets\SO2_2011_plus.csv")
so2_df['measurement_datetime'] = pd.to_datetime(so2_df['Date'])
so2_df = so2_df.rename(columns={'Aveg.': 'so2_concentration'})
so2_df = so2_df[['measurement_datetime', 'location', 'so2_concentration']]

# Remove duplicates if any in SO2
so2_df = so2_df.drop_duplicates(subset=['measurement_datetime', 'location'])

# Load NOx data
nox_df = pd.read_csv(r"D:/Project/Mini project/Air pollution/Datasets/NOx/Nox_2011_plus.csv")
nox_df['measurement_datetime'] = pd.to_datetime(nox_df['Date'])
nox_df = nox_df.rename(columns={'Average': 'nox_concentration'})
nox_df = nox_df[['measurement_datetime', 'location', 'nox_concentration']]

# Remove duplicates if any in NOx
nox_df = nox_df.drop_duplicates(subset=['measurement_datetime', 'location'])
merged_df = pd.merge(
    so2_df,
    nox_df,
    on=['measurement_datetime', 'location'],
    how='outer'  # keeps all rows from both datasets
)

# Add AQI status
merged_df['aqi_status'] = 'Moderate'
merged_df.to_sql('air_quality_data', engine, if_exists='append', index=False)
print("Data inserted successfully!")

'''
def create_users_table():
    with engine.begin() as conn:  # begin() ensures commit after execution
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user'
            )
        """))
    print("table created successfully in DB")
create_users_table()


