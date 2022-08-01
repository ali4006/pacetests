import json
import pandas as pd
import boto3
import psycopg2
import numpy as np
from sqlalchemy import create_engine


def get_credentials():
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        get_secret = client.get_secret_value(
            SecretId="pacetest/postgres"
        )
        secret_dict = json.loads(get_secret['SecretString'])
        username = secret_dict['username']
        passw = secret_dict['password']
        return username, passw

    except Exception as e:
        print(e)
        raise e


def process(event, context):

    bucketname = event['Records'][0]['s3']['bucket']['name']
    csvFile = event['Records'][0]['s3']['object']['key']
    print('Reading object {} from bucket {}.'.format(csvFile, bucketname))

    try:
        # Create connection string to postgres db
        username, passw = get_credentials()
        conn_string = "postgresql+psycopg2://{uid}:{pwd}@{host}:5432/{db}".format(
                            uid=username,
                            pwd=passw,
                            host='pacetest-db-id.cvov6hk03pgj.us-east-1.rds.amazonaws.com',
                            db='pacetest1_db')
        engine = create_engine(conn_string)

        # Read CSV file in chunks of 5000
        i = 0
        for df in pd.read_csv(f's3://{bucketname}/{csvFile}', sep=',', chunksize=5000):
            i +=1
            # DateTime to ISO format
            df['MovementDateTime'] = df['MovementDateTime'].map(lambda x: pd.to_datetime(x).isoformat()) #, format='%Y-%m-%s %h:%m:%s'
            # Fill missing or zero speed values
            df['Speed'] = np.where(np.logical_and(df.MoveStatus == 'Under way using engine',
                                np.logical_or(df.Speed.isnull(), df.Speed == 0)), 
                                df.groupby('CallSign').Speed.transform('mean'), df.Speed)
            # Create BeamRatio column
            df['BeamRatio'] = df['Beam'] / df['Length']
            # print (df.head())

            # transfer data from DataFrame to PostgreSQL table
            df.to_sql('shipping_info', con=engine, index=False, if_exists="append") #, chunksize=5000, method='multi'
            print('Chunk {} is stored.'.format(i))


        return {
            'statusCode': 200,
            'body': json.dumps('Store File Successfully!')
        }

    except Exception as e:
        print(e)
        print('Error processing object {} from bucket {}.'.format(csvFile, bucketname))
        raise e
