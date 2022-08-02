#!/usr/bin/env bash


##############################################################################
# This script includes functions that perform the following tasks:
#    (1) Creating a bucket and verifying that it exists
#    (2) Copying a file from the local computer to a bucket
###############################################################################

###############################################################################
# This function checks to see if the specified bucket already exists.
###############################################################################
function check_bucket() {
    if [ $# != 1 ]; then
        echo "Usage: $0 Bucket_Name"
        exit 1
    fi
    bucketname=$1

    aws s3api head-bucket --bucket $bucketname \
                          >/dev/null 2>&1

    if [[ ${?} -eq 0 ]]; then
        echo "ERROR: A bucket with that name already exists. Try again."
        return 0        # if the bucket already exists
    else
        echo "The Bucket '$bucketname' doesn't exist"
        return 1        # if the bucket doesn't exists
    fi
}

###############################################################################
# This function creates the specified bucket, unless it already exists.
###############################################################################
function create_bucket() {

    if [ $# != 1 ]; then
        echo "Usage: $0 Bucket_Name"
        exit 1
    fi
    bucketname=$1

    # If the bucket already exists, we don't want to try to create it.
    if (check_bucket $bucketname); then 
        exit 0
    fi

    # The bucket doesn't exist, so try to create it.
    aws s3api create-bucket --bucket $bucketname \
                            >/dev/null 2>&1

    if [[ ${?} -eq 0 ]]; then
        echo "AWS S3 bucket $bucketname created successfully."
        return 0        # if the bucket creation succeed
    else
        echo "ERROR: AWS reports bucket creation failed."
        return 1        # if the bucket creation failed
    fi
}

###############################################################################
# This function uploads a file in the specified bucket.
###############################################################################
function upload_file_to_bucket() {

    if [ $# != 3 ]; then
        echo "Usage: $0 Bucket_Name Source_File_path Destination_File_name"
        exit 1
    fi

    bucketname=$1  # The name of the bucket to copy the file to
    sourcefile=$2  # The path and file name of the local file to copy to the bucket
    destfile=$3  # The key (name) to call the copy of the file in the bucket

    aws s3api put-object --bucket $bucketname \
                         --body $sourcefile --key $destfile \
                         >/dev/null 2>&1

    if [[ ${?} -eq 0 ]]; then
        echo "The file is uploaded successfully in AWS S3 bucket $bucketname."
        return 0
    else
        echo "ERROR: AWS reports object uploading failed."
        return 1
    fi
}

###############################################################################
# Verify the function exists
###############################################################################
if declare -f "$1" > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi
