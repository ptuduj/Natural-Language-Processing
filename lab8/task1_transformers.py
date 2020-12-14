from simpletransformers.classification import ClassificationModel
from simpletransformers.classification.transformer_models.bert_model import BertForSequenceClassification
from transformers import AutoTokenizer, AutoModel, AutoConfig
import pandas as pd
import numpy as np
import sklearn
import torch

if __name__ == '__main__':
    model: AutoModel  = AutoModel.from_pretrained("allegro/herbert-base-cased")
    tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained("allegro/herbert-base-cased")
    config: AutoConfig = AutoConfig.from_pretrained("allegro/herbert-base-cased")

    # to nie jest normalne użycie tego modelu - nie jest on obecnie jeszcze wspierany przez Simpletransformers
    cls_model = ClassificationModel("roberta", "allegro/herbert-base-cased", weight= [0.1, 0.9])
    bert_for_squence = BertForSequenceClassification(config)
    bert_for_squence.bert = model
    cls_model.model = bert_for_squence
    torch.multiprocessing.freeze_support()
    train_df = None
    test_df = None
    with open('task1/test_set_clean_only_tags.txt','r',encoding='utf-8') as test_tag,\
        open('task1/test_set_clean_only_text.txt', 'r', encoding='utf-8') as test_text,\
        open('task1/training_set_clean_only_tags.txt', 'r', encoding='utf-8') as training_tag,\
        open('task1/training_set_clean_only_text.txt', 'r', encoding='utf-8') as training_text:
        train_df = pd.DataFrame(data = {'text' : training_text.readlines(), 'labels': np.array(list(map(lambda x: int(x[0]),training_tag.readlines())))})
        test_df = pd.DataFrame(data={'text': test_text.readlines(),
                                      'labels': np.array(list(map(lambda x: int(x[0]), test_tag.readlines())))})

    cls_model.train_model(train_df, args={"num_train_epochs": 5 },overwrite_output_dir=True)
    with open('classifier','wb') as f:
        torch.save(cls_model,f)


    result, model_outputs, wrong_predictions = cls_model.eval_model(test_df, acc=sklearn.metrics.accuracy_score)
    print(result)
    print(model_outputs)
    print(wrong_predictions)

    predictions, raw_outputs = cls_model.predict(test_df['text'])
    with open('single_class_predictions.txt', 'w') as f:
        for prediction in predictions:
            f.write(str(prediction) + '\n')