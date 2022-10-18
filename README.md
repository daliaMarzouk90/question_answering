## Short Answers Assessment Model(SAAM)

### Proposal
The idea of SAAM is based on that the reference answers should have the same semantic meaning. And is we sucseeded in building a model that capture the semantic similarities between the reference answers then we will translate the completness of the students' answers into similarity with the reference answers.

### Training Process Steps
1. Run manual annotation process to set annotations to the answers to be on of the following values
    1.  correct
    2. incomplete
    3. contradictory
    4. incorrect

2. train the similarity model if two sentences is
    1. 1 <= similarity < .75, then correct answer
    2. .75 <= similarity < .5, then incomplete answer
    3. .5 <= similarity < .25, then contradictory answer
    4. .25 <= similarity, then incorrect answer

### Project Modules
#### 1. api
containes the api interface. The are REST apis

#### 2. config
containes all configurations related to the project

#### 3. controller
containes the main engine that manages all components

#### 4. datamanager
the module that manages the data (loading, splitting, aggregations and so on)

#### 5. test
containes any testing modules. Currently only the postman collection exists

### How Run the project
```shell
docker build -t question_answering .
docker run -d -p 5050:5050 question_answering
```

### How to use
1. Run the project
2. import the postman collection from the following <a href="https://www.getpostman.com/collections/7b8e486d2012466c7fea">link</a>
