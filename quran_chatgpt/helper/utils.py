def get_context(data: list) -> list:

    context = ''

    for i in range(len(data)):
        context += f'{data[i]["query"]}\n'
        context += f'{data[i]["response"]}\n'

    return context
