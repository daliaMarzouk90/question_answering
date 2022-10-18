from unicodedata import name
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader
from config.config import model_path
from sklearn.metrics import classification_report


class SemanticSimilarity():
    def __init__(self, model=None):
        if(model == None):
            self.model = SentenceTransformer('stsb-roberta-large')

    def train(self, data):
        #define the train dataset
        train_examples = [InputExample(texts=x[0], label=x[1]) for x in data]

        #the dataloader and the train loss
        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
        train_loss = losses.CosineSimilarityLoss(self.model)

        #tune the model
        self.model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100)

    def test(self, data):
        labels = [self.__get_prediction(x[1]) for x in data]
        preds = [self.measure_similarity(x[0][0], x[0][1]) for x in data]
        report = classification_report(labels, preds, output_dict=True)
        return report

    def measure_similarity(self, ref_answers, answer):
        #calculate embeddings
        ref_answers_embeddings = [self.model.encode(ref_answer) for ref_answer in ref_answers]
        answer_embeddings = self.model.encode(answer)

        #calculate cosine similarities
        cosine_scores = [util.pytorch_cos_sim(ref_answers_embedding, answer_embeddings).item() for ref_answers_embedding in ref_answers_embeddings]

        #return max similarity
        max_similarity = max(cosine_scores)

        return self.__get_prediction(max_similarity)
        
    def __get_prediction(self, similarity):
        answer = "correct"
        if similarity > 0.75:
            answer = "correct"
        elif 0.75 <= similarity < 0.5:
            answer = "correct"
        elif 0.5 <= similarity < 0.25:
            answer = "contradictory"
        else:
            answer = "incorrect"

        return answer

    def save(self, version=0):
        self.model.save(path=model_path, name="answer_assessment_model_v{}".format(version))
