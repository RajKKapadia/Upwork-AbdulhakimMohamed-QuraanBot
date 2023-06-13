def get_context(data: list) -> list:

    context = ''

    for i in range(len(data)):
        context += f'User - {data[i]["query"]}\n'
        context += f'AI - {data[i]["response"]}\n'

    return context
