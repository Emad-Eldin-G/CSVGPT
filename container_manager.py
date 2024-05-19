from CSVGPT import analyze_button_response, chat_response


class print_to_analyze_button_response:
    def markdown(message):
        analyze_button_response.markdown(message)
    
    def write(message):
        analyze_button_response.write(message)

    def table(data):
        analyze_button_response.table(data)

    def data_frame(data):
        analyze_button_response.data_frame(data)


class print_to_chat_response:
    def markdown(message):
        chat_response.markdown(message)
    
    def write(message):
        chat_response.write(message)

    def table(data):
        chat_response.table(data)

    def data_frame(data):
        chat_response.data_frame(data)

    def chat_message(message):
        chat_response.chat_message(message)

    def chat_response(message):
        chat_response.chat_r