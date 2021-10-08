from src.utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import pandas as pd
import os
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
import json


def tune(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config["artifacts"]['artifacts_dir']
    raw_local_dir = config["artifacts"]['raw_local_dir']
    raw_local_file = config["artifacts"]['raw_local_file']

    raw_local_file_path = os.path.join(artifacts_dir, raw_local_dir, raw_local_file)

    print(raw_local_file_path)
    
    df = pd.read_csv(raw_local_file_path)
    X = df.drop('quality',axis=1)
    Y = df['quality']

    alpha = params["hyper_params"]["ElasticNet"]["alpha"]
    l1_ratio = params["hyper_params"]["ElasticNet"]["l1_ratio"]
    random_state = params["base"]["random_state"]

    parametersGrid = {"alpha":alpha,"l1_ratio":l1_ratio}

    eNet = ElasticNet()
    grid = GridSearchCV(eNet, parametersGrid, scoring='neg_mean_squared_error', cv=10)
    
    grid.fit(X,Y)
    print(grid.best_estimator_)

    model_dir = config["artifacts"]["hyperparam_dir"]
    model_filename = config["artifacts"]["hyperparam_filename"]

    model_dir = os.path.join(artifacts_dir, model_dir)

    create_directory([model_dir])

    file_path = os.path.join(model_dir, model_filename)


    with open(file_path,'w') as fout :
         json_dumps_str = json.dumps(grid.best_params_,indent=4)
         print(json_dumps_str,file=fout)

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    tune(config_path=parsed_args.config, params_path=parsed_args.params)