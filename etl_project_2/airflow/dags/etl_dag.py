from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine

# Database configuration
DATABASE_URL = 'postgresql://postgres:12345!@localhost:5432/music_db_2'

# Define the ETL functions
def extract_data():
    """Extract data from CSV."""
    df = pd.read_csv('data/cleaned_spotify_data.csv')
    return df

def transform_data(df):
    """Transform the data (cleaning, processing)."""
    df.dropna(inplace=True)  # Example: remove rows with missing values
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    return df

def load_data_to_db(df):
    """Load data into PostgreSQL database."""
    engine = create_engine(DATABASE_URL)
    df.to_sql('tracks', con=engine, if_exists='append', index=False)

# Define the DAG
with DAG(
    dag_id='etl_process',
    default_args={'owner': 'airflow', 'start_date': days_ago(1)},
    schedule_interval=None,  # Set to '0 0 * * *' for daily runs or adjust as needed
) as dag:

    # Define the tasks
    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_args=[extract.output],  # Pass the output of extract to transform
    )

    load = PythonOperator(
        task_id='load_data_to_db',
        python_callable=load_data_to_db,
        op_args=[transform.output],  # Pass the output of transform to load
    )

    # Set task dependencies
    extract >> transform >> load
