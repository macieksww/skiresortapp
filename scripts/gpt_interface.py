import openai
import os
import copy
from gpt_prompts import GPTPrompts
debug = False
openai.api_key = os.getenv('OPENAPI_KEY')
models = openai.Model.list()['data']
csv_path = os.path.basename('src/csv')

if debug:
    for model in models:
        print(model['id'])

def ask_chat(messages):
    max_attempts = 5
    current_attempt = 0
    response_received = False
    timeout_const = 30
    timeout = len(messages)*timeout_const
    while not response_received and current_attempt < max_attempts:
        print("Attempt to prompt GPT: " + str(current_attempt))
        try:
            response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',
                                                    messages=messages,
                                                    max_tokens = 1024,
                                                    temperature = 0.8)
        except openai.error.InvalidRequestError as e:
            print(e)
            current_attempt += 1
        except TimeoutError as e:
            print(e)
            current_attempt += 1
        else:
            response_received = True
            finish_reason = response['choices'][0]['finish_reason']
            return response.choices[0].message.content, messages
    return None, None


def ask_chat_one_by_one(messages):
    so_far_asked_questions_and_gpt_answers = []
    message_iterator = 0
    timeout_const = 30
    for message in messages:
        # if debug:
        #     print(so_far_asked_questions_and_gpt_answers)
        max_attempts = 5
        current_attempt = 0
        response_received = False
        while not response_received and current_attempt < max_attempts:
            print("Attempt to prompt GPT: " + str(current_attempt))
            print("MESSAGES")
            print(messages)
            try:
                response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',
                                                        messages=so_far_asked_questions_and_gpt_answers,
                                                        max_tokens=1024,
                                                        temperature=0.8)

            except openai.error.InvalidRequestError as e:
                print(e)
                current_attempt += 1
            except TimeoutError as e:
                print(e)
                current_attempt += 1
            else:
                response_received = True
                so_far_asked_questions_and_gpt_answers.append(
                    {
                        'role': 'assistant',
                        'content': response.choices[0].message.content
                    }
                )
                message_iterator += 1
                if message_iterator == len(messages):
                    final_response = response.choices[0].message.content
                    finish_reason = response['choices'][0]['finish_reason']
                    return response.choices[0].message.content, so_far_asked_questions_and_gpt_answers
    return None, None


def initial_conversation(args=[]):
    gpt_prompts = GPTPrompts(args)
    """
    Conducting initial conversation, including telling GPT
    what it will be working on, what the system is requested to do
    Making sure that GPT understands well what the requested task is
    It may be useful in the case of any mistakes in retrieving the
    request from the user (like spelling mistakes)
    """
    messages = gpt_prompts.create_initial_conversation_prompt(args)
    response, conversation_context = ask_chat(messages)
    if not response:
        return None, None
    return response, conversation_context


def ask_to_create_data(args, init_context):
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_ask_for_data_prompt(args)
    response, conversation_context = ask_chat_one_by_one(messages)
    if not response:
        return None, None
    return response, conversation_context


def ask_to_create_table_data(args, init_context):
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_ask_for_table_data_prompt(args, copy.deepcopy(init_context))
    response, conversation_context = ask_chat(messages)
    if not response:
        return None, None
    else:
        return response, conversation_context