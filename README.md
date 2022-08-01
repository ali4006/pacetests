
# Serverless Framework AWS Lambda Function

This is an example assignment for RioTinto Data Engineer position.
The main goals of the assignment are:

1. Write a script (bash preferred) that uploads the local raw file into an S3 bucket.
2. Write a Lambda handler that triggers when a file that matches the filename lands in the bucket you created above.
        a) The first Lambda should extract the data from the CSV and store it in a new bucket keyed `Data/Raw/Input`.
3. Write a second Lambda handler that triggers when a file that matches the filename lands in the new bucket you just created `1`Data/Raw/Input`.
        a) The second Lambda should extract the data from the CSV and process the file.
        b) Normalize MovementDateTime to ISO format.
        c) For each ship grouped by `CallSign`, if the `MoveStatus` is `Under way using engine`, fill in any missing or zero `speeds` with the average of all speeds for that `CallSign`.
        d) Create a new feature called `BeamRatio` calculated as Beam / Length (Beam divided by Length).
        e) Programmatically store the cleaned data in a Postgres table on RDS.


## Usage

### Deployment

In order to deploy the example, you need to run the following command:

```
$ serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying pacetest to stage dev (us-east-1)

✔ Service deployed to stack pacetest-dev (103s)

functions:
  storecsv: pacetest-dev-storecsv (15 MB)
  processdb: pacetest-dev-processdb
```

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
sh bucket_opt.sh upload_file_to_bucket salarsourcebucket data/pace-data.txt pace-data.txt

```

Which should result in creating a postgres table called `shipping_info`
