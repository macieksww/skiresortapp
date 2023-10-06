import re
import json
import os
import pandas as pd

from exceptions import AttributeErrorException, WrongPathException

def save_to_file(text, filepath):
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'w+') as file:
                file.write(text)
        else:
            raise WrongPathException()
    except WrongPathException as e:
        print('File doesnt exist')
        print(e)

def save_df_to_file(df, filepath):
    try:
        df.to_csv(filepath)
    except FileNotFoundError as e:
        print(filepath)
        print('File doesnt exist')
        raise

def read_df_from_file(filepath):
    try:
        if os.path.isfile(filepath):
            df = pd.read_csv(filepath)
        else:
            raise FileNotFoundError()
    # except WrongPathException as e:
    #     print('File doesnt exist')
    #     print(e)
    except FileNotFoundError as e:
        print(filepath)
        print('File doesnt exist')

def save_lines_to_file(lines, filepath):
    with open(filepath, 'w+') as file:
        file.writelines(lines)

def str_to_json(text):
    pattern = r'{(\n.*)*}'
    plan_lines = []
    matches = re.search(pattern, text)
    if matches:
        try:
            json_like_str = text[matches.span()[0]:matches.span()[1]]
            return json.loads(json_like_str)
        except AttributeErrorException() as e:
            print(e)
            return
    else:
        return
        
def write_file(filepath, text, mode='wl'):
    try:
        match mode:
            # write
            case 'w':
                with open(filepath, 'w+') as file:
                    file.write(text)
            # writelines
            case 'wl':
                with open(filepath, 'w+') as file:
                    file.writelines(text)
    except FileNotFoundError as e:
        print('File doesnt exist')
          
def read_file(filepath, mode='rl'):
    try:
        match mode:
            # read
            case 'r':
                with open(filepath, 'r') as file:
                    file = file.read()
            # readlines
            case 'rl':
                with open(filepath, 'r') as file:
                    file = file.readlines()
    except FileNotFoundError as e:
        print('File doesnt exist')
    else:  
        return file

def create_data_df(text, filepath):
    p_0 = r'\{[\s$]*\"'
    # p_0 = r'{'
    p_1 = r'\][\s$]*\}'
    matches_0 = re.search(p_0, text)
    matches_1 = re.search(p_1, text)
    print(text[int(matches_0.span()[0]):int(matches_1.span()[1])])
    data_dict = json.loads(text[int(matches_0.span()[0]):int(matches_1.span()[1])])
    data_df = pd.DataFrame(data_dict)
    save_df_to_file(data_df, filepath)
    print(data_df.head())


