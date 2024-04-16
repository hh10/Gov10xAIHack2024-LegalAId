from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

from langchain.schema import HumanMessage

from langchain.chat_models import AzureChatOpenAI
import os


DEFAULT_SYSTEM_PROMPT = """
You are a legislative analyst working in the British civil service. Please answer analytically and carefully and avoid making any assumptions outside the provided bill and explanatory note.
"""

'''AZURE CREDS'''
os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://azureopenai-team22.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "7e6ee155fbeb4b0cab189e75c325be89"


class Pipeline:

    def __init__(self, name: str):
        self.name = name
        self.vector_store = None
        self.params = {
            "chunk_size": 1500,
            "chunk_overlap": 0,
            "llm": "gpt-4"
        }

    @staticmethod
    def _load(path: str):
        return PyPDFLoader(path).load()

    @staticmethod
    def split(docs,
              chunk_size: int = 1000,
              chunk_overlap: int = 1000):
        return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(docs)

    # def store(self) -> None:
    #     vector_db = FAISS.from_documents(documents=self.docs,
    #                                      embedding=OpenAIEmbeddings())
    #     vector_db.save_local('./db/' + self.name)

    @property
    def llm(self):
        return AzureChatOpenAI(deployment_name="team-22")

    # def preprocess(self,
    #                data_path: str) -> None:
    #     self.docs = self.split(docs=self._load(path=data_path,
    #                                            type=self.name.split("/")[-1].split('.')[-1]),
    #                            splitter=self.params["splitter"],
    #                            chunk_size=self.params["chunk_size"],
    #                            chunk_overlap=self.params["chunk_overlap"])
        # self.store()

    def ask(self,
            question: str,
            system_prompt: str = DEFAULT_SYSTEM_PROMPT,
            bills: str = None,
            xnotes: str = None):
        bill = "\n\n".join([d.page_content for d in bills])
        xnote = "\n\n".join([d.page_content for d in xnotes])
        enriched_prompt = f""" {system_prompt}
        The explanatory note is supposed to be the summary of the bill.

        Here is the bill: {bill}.

        Here is its explanatory note: {xnote}.

        Question: {question}
        Helpful Answer:"""
        answer = self.llm.invoke(input=[HumanMessage(content=enriched_prompt)]).content

        return answer  # , retrieved_docs


# if __name__ == '__main__':
#     chat_bot = Pipeline('current_chatbot')
#     document = chat_bot._load("../data/test_10.pdf")
#     answer = chat_bot.ask(question=input("Please ask a question:"), documents=document[5:7])
#     print(answer)
