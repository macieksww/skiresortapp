class GPTPrompts:
    def __init__(self, args):
        self.initial_conversation_prompt = ''
        self.followup_conversation_prompt = ''
        self.args = args

    def create_initial_conversation_prompt(self, args):
        messages = [
        # description to the system, what it is gonna perform
        {
            'role': 'user',
            'content': f"""
                    You are a helpful system, that will help me generate data for my 
                    database. This is a database of a web app that stores info about ski resorts.
                    In the following messages I will give you the name of a table, column, datatype 
                    and how many rows of data i want you to generate. Be careful, when you generate data 
                    for a column that is a foreign key of a different columns primary key. Generate data 
                    that doesnt violate constraints.
                    """
        }]
        return messages

    def create_ask_for_table_data_prompt(self, args, context):
        messages = context
        messages.append(
            {
                'role': 'user',
                'content': f"""
                        There is a {args[0]} table, it has the following columns:
                        {args[1]}. The column records are of following types: {args[2]}
                        Generate {args[3]} records. As a return give me a python dict
                        where dict keys are the consecutive column names, and dict 
                        values are lists of generated records. 
                        Give me a python object declaration 
                        not a snippet of code. Name the output list as 'data'. Enclose strings
                        in double quotes.
                        """
            })
        return messages


    # def create_ask_for_data_prompt(self, args):
    #     messages = [
    #     # description to the system, what it is gonna perform
    #     {
    #         'role': 'user',
    #         'content': f"""
    #                 This is a {args[0]} table, {args[0]}-{args[1]} column.
    #                 Return a python list of {args[2]}-type values.
    #                 Generate {args[3]} records.
    #                 """
    #     }]
    #     return messages
