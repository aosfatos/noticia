from noticia import prompts

DOCUMENT_SEPARATOR = "\n\n"


class ChatQA:
    def __init__(self, ir, qa):
        self.ir = ir
        self.qa = qa

    def follow_up_query(self, question):
        prompt = prompts.HISTORY_TEMPLATE.format(
            chat_history="/n".join(self.history), question=question
        )
        query = self.qa.completion(prompt)
        return query

    def __call__(self, query: str):
        documents = self.ir.search(query)

        contexts = [document["text"] for document in documents]
        context = DOCUMENT_SEPARATOR.join(contexts)
        prompt = prompts.QUESTION_TEMPLATE.format(context=context, question=query)

        answer = self.qa.completion(prompt)

        urls = [document["metadata"]["url"] for document in documents]
        urls = list(dict.fromkeys(urls))
        citation = [f"{i+1}. {url}" for i, url in enumerate(urls)]

        return "\n".join([answer, *citation])
