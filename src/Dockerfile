FROM public.ecr.aws/lambda/python:3.8

# copy and install python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# copy lambda function code
COPY lambda_process.py ${LAMBDA_TASK_ROOT}

# set the CMD to handler
CMD ["lambda_process.process"]
