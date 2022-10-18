from config.config import data_path
import pandas as pd
import xmltodict
import numpy as np
import re

class DataBaseManager():
    def __init__(self, questions_file_name=None):
        #load data frame
        self.__load_data(data_path)

        #shuffle data
        self.__questions.iloc[np.random.permutation(len(self.__questions))]

        #split to train and test
        self.__train_frame = self.__questions.sample(frac = 0.8)
        self.__test_frame = self.__questions.drop(self.__train_frame.index)

    def __get_annotation(self, annotation):
        if("correct(1)" in annotation['@Label']):
            return "correct"
        elif("correct_but_incomplete(1)" in annotation['@Label']):
            return "incomplete"
        elif("contradictory(1)" in annotation['@Label']):
            return "contradictory"
        else:
            return "incorrect"

    def __map_object(self,object):
        object["Annotation"] = self.__get_annotation(object["Annotation"])

    def __load_data(self, data_path):
        with open(data_path, 'rb') as file:
            self.data_array = xmltodict.parse(file.read())["root"]["Instance"]

            for object in self.data_array:
                self.__map_object(object=object)

        self.__questions = pd.DataFrame(self.data_array).drop(["@ID", "MetaInfo"], axis=1)

    def split_ref_ans(self, ref_ans_group):
        questions = ref_ans_group.split("\n")
        questions = {re.sub("[0-9]:  *", "", x) for x in questions}
        return questions

    def __get_group_ref_answers(self, ref_ans_group):
        similar_answers = set()

        for item in ref_ans_group:
            similar_answers.update(self.__split_ref_ans(item))
        
        return similar_answers

    def __get_similar_groups(self, data_frame):
        #group by ProblemDescription and Question (Ref answers have similar semantic meaning)
        groups = data_frame.groupby(["ProblemDescription", "Question"])["ReferenceAnswers"].unique()
        
        #get unique answer sets between groups
        similar_groups = [self.__get_group_ref_answers(group) for group in groups]

        return similar_groups

    def __prepare_labeled_data(self, data_frame, label):
        return data_frame[data_frame["Annotation"] == label] 

    def get_data(self, category):
        current_data = None

        if(category == "training"):
            current_data = self.__train_frame
        else:
            current_data = self.__test_frame

        correct_data = self.__prepare_labeled_data(current_data, "correct")
        incomplete_data = self.__prepare_labeled_data(current_data, "incomplete")
        contradictory_data = self.__prepare_labeled_data(current_data, "contradictory")
        incorrect_data = self.__prepare_labeled_data(current_data, "incorrect")

        return {
            "correct_data": correct_data,
            "incomplete_data": incomplete_data,
            "contradictory_data": contradictory_data,
            "incorrect_data": incorrect_data
        }

    def get_training_combinations(self, df, label=0.0):
        combinations = []

        for index, row in df.iterrows():
            ref_answers = self.split_ref_ans(row["ReferenceAnswers"])
            answer = row["Answer"]

            for ref_answer in ref_answers:
                combinations.append([[ref_answer, answer], label])

        return combinations

    def get_testing_combinations(self, df, label=0.0):
        combinations = []

        for index, row in df.iterrows():
            ref_answers = self.split_ref_ans(row["ReferenceAnswers"])
            answer = row["Answer"]

            combinations.append([[ref_answers, answer], label])

        return combinations


    def prepare_training_combinations(self):
        category_data = self.get_data("training")

        data = []

        data += self.get_training_combinations(category_data["correct_data"], 0.9)
        data += self.get_training_combinations(category_data["incomplete_data"], 0.7)
        data += self.get_training_combinations(category_data["contradictory_data"], 0.4)
        data += self.get_training_combinations(category_data["incorrect_data"], 0.1)

        return data

    def prepare_test_combinations(self):
        category_data = self.get_data("testing")

        data = []

        data += self.get_testing_combinations(category_data["correct_data"], 0.9)
        data += self.get_testing_combinations(category_data["incomplete_data"], 0.7)
        data += self.get_testing_combinations(category_data["contradictory_data"], 0.4)
        data += self.get_testing_combinations(category_data["incorrect_data"], 0.1)

        return data