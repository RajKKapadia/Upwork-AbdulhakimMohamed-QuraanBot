# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate

# from config import config


# prompt_template = '''Followings are the conversation between AI and User.\
#     Use the conversation as context and try to give accurate answer to the Question in the end.\
#     Finally,. if you don't know the answer, just say that I am sorry, I don't have a answer to your question...\
# Context: {context}
# Question: {question}'''


# def create_conversation() -> RetrievalQA:

#     persist_directory = config.DB_DIR

#     embeddings = OpenAIEmbeddings(
#         openai_api_key=config.OPENAI_API_KEY
#     )

#     db = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embeddings
#     )

#     PROMPT = PromptTemplate(
#         template=prompt_template, input_variables=['context', 'question']
#     )

#     chain_type_kwargs = {'prompt': PROMPT}

#     qa = RetrievalQA.from_chain_type(
#         llm=ChatOpenAI(temperature=0.0),
#         chain_type="stuff",
#         retriever=db.as_retriever(),
#         verbose=True,
#         chain_type_kwargs=chain_type_kwargs
#     )

#     return qa

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from config import config

chat = ChatOpenAI(temperature=0.0, openai_api_key=config.OPENAI_API_KEY)

def create_conversation(question: str, context: str) -> str:
    template_string = '''Consider yourself a highly conversational Muslim scholar \
        and refer to Tafsir Ibn Kathir or the Quran in your answer and please go into detail and ask questions back given context. \
        {context} \
        Question: {question} \
    '''

    prompt_template = ChatPromptTemplate.from_template(
        template=template_string
    )

    prompt_messages = prompt_template.format_messages(context=context, question=question)

    try:
        response = chat(prompt_messages)
        return response.content
    except:
        return 'We are facing technical issue at this moment.'

