import gradio as gr

from noticia import chat, embeddings, ir, llm

encoding_fnc = embeddings.OpenAIEmbedding()
index = ir.PineconeSearch(encoding_fnc)
qa = llm.ChatGPT()

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    chat = chat.ChatQA(index, qa)
    msg = gr.Textbox(
        placeholder="Enter text and press enter, or upload an image",
    )
    clear = gr.Button("Clear")

    def respond(question, chat_history):
        bot_message = chat(question)
        chat_history.append((question, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: "", None, chatbot, queue=False)

demo.launch()
