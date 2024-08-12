## Intro
The test is completed with Python + Selenium

## Tested Environment
1. 

## Local Environment Setup (On Mac)
1. Please have Google Chrome installed on your laptop
2. Create an python virtual environment with `python -m venv venv` 
3. Prepare the working environment with 
   1. `source venv/bin/activate`
   2. `pip install -r requirements.txt`

## Local Run
- Jupyter Notebook
  1.  Create a kernel with venv you created above
  2.  Locate the notbook I've prepared [app/scraper.ipynb](app/scraper.ipynb) and Run ALL
  3.  You will get the result dataframe in the last cell


## Docker deployment
- The scraper is packed into the container as well as to ease deployment process
- Always deploy or test on x86 CPU architecture because of limitation on runing chrome in container environment under ARM CPU architecture

**Script testing in docker**
- Here's docker deployment steps:
  1. Build the container `docker build -t mk-bags .`
  2. Run the docker

## Proposed AWS deployment
**Architecture**
![alt text](<src/NF Test.drawio.svg>)

**1/ ECR Push**

Pre-requisite:
- IAM user account with permission to upload docker layers
- An new ECR repository called `mk-bags`

Steps:

1. Logon the ECR repo with command provided on AWS portal `aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin {account}.dkr.ecr.ap-southeast-1.amazonaws.com`
2. Tag the image `docker tag mk-bags:latest {account}.dkr.ecr.ap-southeast-1.amazonaws.com/mk-bags:latest`
3. Push to ECR `docker push {account}.dkr.ecr.ap-southeast-1.amazonaws.com/mk-bags:latest`

**2/ Lambda Setup**

1. Create Function > Container Image > Pick image from ECR "mk-bags"
![alt text](src/lambda-setup-1.png)
2. No overriding needed

