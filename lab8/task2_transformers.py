from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import torch
import numpy as np


if __name__ == '__main__':
    torch.multiprocessing.freeze_support()
    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.WARNING)

    train_df = None
    test_df = None

    with open('task2/test_set_clean_only_tags.txt', 'r', encoding='utf-8') as test_tag, \
            open('task2/test_set_clean_only_text.txt', 'r', encoding='utf-8') as test_text, \
            open('task2/training_set_clean_only_tags.txt', 'r', encoding='utf-8') as training_tag, \
            open('task2/training_set_clean_only_text.txt', 'r', encoding='utf-8') as training_text:
        train_df = pd.DataFrame(data={'text': training_text.readlines(),
                                      'labels': np.array(list(map(lambda x: int(x[0]), training_tag.readlines())))})
        test_df = pd.DataFrame(data={'text': test_text.readlines(),
                                     'labels': np.array(list(map(lambda x: int(x[0]), test_tag.readlines())))})

    # Optional model configuration
    model_args = ClassificationArgs(num_train_epochs=5)

    # Create a ClassificationModel
    model = ClassificationModel(
        'bert',
        'bert-base-cased',
        num_labels=3,
        args=model_args
    )

    # Train the model
    model.train_model(train_df)

    with open('classifier_multiple_classes','wb') as f:
        torch.save(model,f)


    # Evaluate the model
    result, model_outputs, wrong_predictions = model.eval_model(test_df)

    # Make predictions with the model
    predictions, raw_outputs = model.predict(test_df['text'])
    with open('multi_class_simple_model_predictions','w') as f:
        for prediction in predictions:
            f.write(str(prediction)+'\n')
