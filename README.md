# Hello there!
Welcome to this demo to consume data from a queue of SQS, AWS Service, also, a little demo to show the buckets from S3
## Getting started
First, configure your AWS credentials in your CLI or you can create a ".env" file and leave the credentials there, you can use "example.env" like a template, now let's start with this app!
1. First, create a venv with 
```python
python3 -m venv env
```

2. Activate your venv with 
```python
source env/bin/activate
```

3. Install the dependencies with 
```python
pip3 install requirements.txt -r
```

4. Finally, execute 
```python
python3 main.py
```
 and check the code, I recommend to first try with the option "Create the queue"

## Troubleshooting
Don't forget to check the credentials and the policies, if you don't have enough credentials you might found a **Credential Error**, in this case, check the IAM Service