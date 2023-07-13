from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from config import config

chat = ChatOpenAI(temperature=0.0, openai_api_key=config.OPENAI_API_KEY)


def create_conversation(question: str, context: str, name: str) -> str:
    template_string = '''Consider yourself a highly conversational Muslim scholar \
        and refer to Tafsir Ibn Kathir or the Quran in your answer and please go into detail and ask questions back given context. \
        refer to the user as {name} in the beggining of the answer. \
        {context} \
        Question: {question} \
    '''
    prompt_template = ChatPromptTemplate.from_template(
        template=template_string
    )
    prompt_messages = prompt_template.format_messages(
        context=context, question=question, name=name)
    try:
        response = chat(prompt_messages)
        return response.content
    except:
        return config.ERROR_MESSAGE


def get_email(query: str) -> str:
    response_schemas = [
        ResponseSchema(
            name="email", description="it is an email address of a user")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract an email address from the question, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['email'] == -1:
            response = chat.predict('Politely ask email of a person.')
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output['email']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }


def get_name(query: str) -> dict:
    response_schemas = [
        ResponseSchema(name="name", description="it is a name of a person")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract name of a person from the question, if found then capitalize the name, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['name'] == -1:
            response = chat.predict('Politely ask name of a person.')
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output['name']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }


def get_consent(query: str) -> str:
    response_schemas = [
        ResponseSchema(name="consent", description="it is a consent of a user")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract a consent of user from the question, if found then return either Yes or No, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['consent'] == -1:
            return {
                'status': 0,
                'output': config.CONSENT_MESSAGE
            }
        return {
            'status': 1,
            'output': output['consent']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }

def get_general_response(query: str) -> str:
    try:
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
        response = chat.predict(query)
        return response
    except:
        return config.ERROR_MESSAGE
    
def chat_completion(messages: list) -> str:
    try:
        chat = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY)
        result = chat(messages)
        return result.content
    except:
        return config.ERROR_MESSAGE
