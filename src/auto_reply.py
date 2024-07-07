
import chromadb
import ollama

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class AutoReply:
    
    def __init__(self,  user_id: str):
        self.chroma_client = chromadb.Client()
        
        self.script = None
        self.script_chunks = None
        self.chromadb_collection = self.chroma_client.get_or_create_collection(name=user_id)
        self.llm = ChatOllama(model='llama3', temperature=0, format='json')
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful AI Assistant chatbot that replies to user queries from a livestream.
            
            Based on the following document:
            {document}, and
            
            User Message: {user_message}

            Determine if the User's Message is directly related to the document. If it is not relevant, return key value pair as Success: False, Message: None
            
            Else, if you are able to reply to the user's message given the document, return key value pair as Success: True, Message: <Your Response>
            Adopt a helpful tone and be concise in your answers.
            """
        )
        self.chain = self.prompt | self.llm | JsonOutputParser()
        
        
    # Read the script from an uploaded file
    def _read_script(self, file_path):
        with open(file_path, 'r') as file:
            script = file.read()
        self.script = script
        return script
    
    # Can look into other methods for splitting into chunks (this requires the user to split into paragraphs by 2 lines)
    def _split_script(self, script, split_by='paragraph'):
        if self.script is None:
            raise ValueError("Script has not been added.")
        if split_by == 'paragraph':
            # Split by double newline characters for paragraphs
            chunks = script.split('\n\n')
        elif split_by == 'sentence':
            # Split by periods for sentences
            chunks = script.split('. ')
        else:
            raise ValueError("Unsupported split_by value. Use 'paragraph' or 'sentence'.")
        
        self.script_chunks = chunks
        return chunks
    
    def _get_embedding(self, text):
        res = ollama.embeddings(model='nomic-embed-text', prompt=text)
        return res['embedding']
    
    def _store_script_chunks(self, chunks):
        embeddings = [self._get_embedding(chunk) for chunk in chunks]
        documents = chunks
        ids = list(str(x) for x in range(len(chunks)))
        self.chromadb_collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        
    # Main function to process the script
    def process_script(self, file_path):
        script = self._read_script(file_path)
        chunks = self._split_script(script, split_by='paragraph')
        self._store_script_chunks(chunks)
    
    def check_collection(self):
        return self.chromadb_collection.get()
    
    
    # retrieve specific parts from script to reply user's message
    def _get_relevant_document(self, message):
        res = self.chromadb_collection.query(query_embeddings=[self._get_embedding(message)], n_results=1)
        return res

    # generate auto reply from retrieved document, if no retrieved documents, return None
    def _get_auto_reply_json(self, message):
        document = self._get_relevant_document(message)
        if document:
            reply = self.chain.invoke({"document": document, "user_message": message})
            # Example of successful reply: {'Success': True, 'Message': 'The Slip-Ons come in versatile colors: grey, navy, and black.'}
            # Example of unsuccesful reply: {'Success': False, 'Message': "Hello! It seems like you're just saying hello. If you have any questions or need help with something specific, feel free to ask!"}
            return reply
        else:
            return None
    
    # To use to determine if a user's message can be replied by the bot
    def get_auto_response(self, message):
        reply = self._get_auto_reply_json(message)
        if reply['Success']:
            return reply['Message']
        else:
            return None

# Example Usage

auto_reply = AutoReply(user_id="User0")

# Uploading of user's script
file_path = "./data/scripts/example_script" 
auto_reply.process_script(file_path=file_path)




