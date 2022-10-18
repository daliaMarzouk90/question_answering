from semantic_similarity import SemanticSimilarity
from datamanager.data_manager import DataBaseManager



class ShortAnswersAssement():
    def __init__(self):
        self.similarity_model = SemanticSimilarity()
        self.dbmanager = DataBaseManager()

    def assess(self, ref_answers, answer):
        similarity = self.similarity_model.measure_similarity(ref_answers=ref_answers, answer=answer)
        answer = None
        
            
        return answer

    def train(self):
        training_combinations = self.dbmanager.prepare_training_combinations()
        self.similarity_model.train(training_combinations)
        return 

    def test(self):
        testing_combinations = self.dbmanager.prepare_test_combinations()
        return self.similarity_model.test(testing_combinations)