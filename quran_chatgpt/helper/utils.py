from langchain.schema import HumanMessage, SystemMessage


def get_context(data: list) -> list:

    context = ''

    for i in range(len(data)):
        context += f'{data[i]["query"]}\n'
        context += f'{data[i]["response"]}\n'

    return context


def generate_messages(messages: list, query: str, name: str) -> list:
    formated_messages = [SystemMessage(
        content=f"""Consider yourself a highly conversational Muslim scholar and refer to Tafsir Ibn Kathir or the Quran in your answer and please go into detail and ask questions back given context. Refer to the user as {name} in the beggining of the answer.""")]
    for m in messages:
        formated_messages.append(
            HumanMessage(content=m['query'])
        )
        formated_messages.append(
            SystemMessage(content=m['response'])
        )
    formated_messages.append(HumanMessage(content=query))
    return formated_messages


def create_string_chunks(string, length):
    words = string.split()
    sentences = []
    temp_string = ''
    for w in words:
        if len(temp_string) > length:
            sentences.append(f'{temp_string}...')
            temp_string = ''
        temp_string += f'{w} '
    sentences.append(temp_string)
    return sentences
