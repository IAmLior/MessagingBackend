# A messaging system backend in the cloud!
This project is an MVP for a cloud-based backend messaging system.  
It’s designed to handle user and group registrations, one-on-one and group messaging, groups management (users adding and removal),user blocking and also to support scaling from daily several users to thousands to millions of users.

## Technologies

The backend API is implemented using **Python FastAPI**.

### Databases

**MongoDB** Serves as the primary database for persisting user details, messages, and group information, chosen for its robust handling of large volumes of data, MongoDB facilitates easy horizontal scaling, which is critical when expanding to accommodate more users.

**Sharding** and **Indexing** was used as features of the MongoDB for scaling support using data distribution and faster queries.

Sharding was implemented over receiver_id property which related to unique groups and users (avoiding sharding over sender_id & receiver_id both for group sharding support). By sharding the database with the receiver_id, we ensure even distribution of data, which is crucial for maintaining performance as the user base grows.

```
cls._instance.mongo_client.admin.command('shardCollection', 'MessagingDB.messages', key={'reciever_id': ASCENDING})
```

Two indexes were created, one better fit to users chat and the other for groups chat.

```
messages_collection.create_index([('sender_id', ASCENDING), ('receiver_id', ASCENDING)]) # better for user's chat query
messages_collection.create_index([('receiver_id', ASCENDING)]) # better for group's chat
```

**Redis** Utilized for fast data caching and for avoid many frequent requests to the database.
It Reduces the load on the main database by caching frequently accessed data (such as group messages), and batching sent messages for batch database insertion.We have implemented a mechanism to send requests either every 3 seconds or after accumulating 50 messages, whichever occurs first.
This approach ensures efficient handling of message traffic and optimizes system performance for both individual and group messaging scenarios.
Redis usage significantly improving the system's responsiveness and ability to handle simultaneous requests.

### Deployment


The **deployment** process of the project uses **Pulumi** as infra-as-a-code tool. The code is packed as a Docker Image and uploaded to ECR. The created docker image is deployed as a serverless solution on AWS Lambda Function for scale support. The connection to the lambda function is using APIGateway.
The MongoDB and Redis Clusters are also deployed using pulumi and their connection properties are given to the docker image as an environment variables.

## Pricing
Estimating the cost differences for an AWS-powered messaging system serving different scales of users involves several factors, particularly due to the scalable nature of the services involved.

### Key AWS Services and Costs
**AWS Lambda**: Costs depend on the number of requests and the duration of each request. The cost increases linearly with the number of requests and the complexity (duration) of each execution.

**Amazon API Gateway**: This manages incoming requests. Costs are primarily based on the number of API calls received.

**Amazon Elastic Container Registry (ECR)**: Storage cost for Docker images and data transfer costs if the container is pulled frequently.

**Amazon MongoDB Atlas and Redis on AWS**: These are third-party managed services on AWS. Costs depend on instance size, data storage, data transfer, and operations performed (like read/write operations).

**Data transfer costs**: These can become significant at scale, especially when transferring large volumes of data in and out of AWS services.

### Cost Evaluation for Different User Tiers
#### **10 Users** 
Minimal resource usage. Costs are mostly flat fees for Lambda (given the free tier covers 1M requests per month and 400,000 GB-seconds of compute time), API Gateway (with 1 million API calls per month for free), and ECR (500MB of storage for free). MongoDB and Redis may stay within the free or lower-tier usage, leading to very low costs.

**Estimated Monthly Cost**: Minimal, possibly under $100 assuming low usage.

  
#### **1000 Users**

Increased API calls and more frequent Lambda invocations. Data storage and operations in MongoDB and Redis will increase. This moves beyond the free tiers for most services, introducing moderate costs, particularly for database operations and data storage.

**Estimated Monthly Cost**:
Lambda Approx. of 100 million requests per month, API Gateway Approx. of 50 million API calls per month, MongoDB: Medium instance and
Redis Small to medium instance.
Total: hundreds of dollars.

#### **10000 Users**

With ten times more users, the number of requests and API calls will increase substantially, pushing the use of AWS services well beyond free tiers and requiring more robust database solutions.

**Estimated Monthly Cost**:
Lambda Approx. of 10 million requests per month, API Gateway Approx. of 5 million API calls per month, MongoDB: Larger or multiple medium instances and
Redis Medium to large instance.
Total: thousands of dollars.

#### **1 Million Users**

Substantial costs due to high utilization of all services. Lambda and API Gateway costs will be driven by a significantly higher number of requests. MongoDB and Redis will require larger and possibly more instances to handle the increased load, significantly increasing costs. Data transfer costs also become a major factor due to the volume of data being moved.

**Estimated Monthly Cost**:
Lambda Approx. of 1 billion requests per month, API Gateway Approx. of 500 million API calls, MongoDB: Large configurations or multiple large instances, Redis: Larger or multiple instances.
Total: Anywhere from many thousands of dollars to tens of thousands of dollars, depending on specific usage and instance sizes.

#### Optimization of Lambda Functions, Effective Use of Caching, Database Optimization and Data Transfer Optimization can be good keys for cost reducing in large system scales.
