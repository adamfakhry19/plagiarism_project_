import pandas as pd
import numpy as np
import javalang
from scipy.sparse import hstack
import os
from joblib import load
from django.conf import settings

model_dir = os.path.join(settings.BASE_DIR, 'model_files')
calibrated_ensemble = load(os.path.join(model_dir, 'calibrated_ensemble_model.joblib'))
tfidf_vectorizer = load(os.path.join(model_dir, 'tfidf_vectorizer.joblib'))
scaler = load(os.path.join(model_dir, 'scaler.joblib'))

def read_java_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def extract_detailed_features(code):
    features = {}
    try:
        tree = javalang.parse.parse(code)
        features['node_count'] = len(list(tree))
        features['operators'] = len({token.value for token in tree if isinstance(token, javalang.tokenizer.Operator)})
        features['operands'] = len({token.value for token in tree if isinstance(token, javalang.tokenizer.Literal)})
        features['max_depth'] = max((node.position[0] for path, node in tree if node.position), default=0)
        features['method_count'] = sum(1 for _, node in tree if isinstance(node, javalang.tree.MethodDeclaration))
    except javalang.parser.JavaSyntaxError:
        features.update(dict.fromkeys(['node_count', 'operators', 'operands', 'max_depth', 'method_count'], 0))
    return features

def preprocess_new_data(file_path1, file_path2):
    content1 = read_java_file(file_path1)
    content2 = read_java_file(file_path2)
    combined_content = content1 + " " + content2

    ast_features = extract_detailed_features(combined_content)
    ast_features_df = pd.DataFrame([ast_features])

    tfidf_features = tfidf_vectorizer.transform([combined_content])
    ast_features_scaled = scaler.transform(ast_features_df)

    combined_features = hstack([tfidf_features, ast_features_scaled])
    return combined_features

def predict_plagiarism(file_path1, file_path2):
    features = preprocess_new_data(file_path1, file_path2)
    predicted_label = calibrated_ensemble.predict(features)
    prediction_probabilities = calibrated_ensemble.predict_proba(features)
    print("Prediction Probabilities:", prediction_probabilities)
    print("Predicted Label:", np.argmax(prediction_probabilities))

    return predicted_label[0]
