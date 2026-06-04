from google import genai


class QAAgent:

    def __init__(self, api_key, vector_store):

        self.client = genai.Client(
            api_key=api_key
        )

        self.vector_store = vector_store

    def answer(self, question):

        context = self.vector_store.get_context(
            query=question,
            top_k=3
        )

        prompt = f"""
        You are a contract analysis assistant.
        
        Answer the user's question using ONLY the
        contract context provided below. 
        When you answer, include the page number and/or
        section number to ensure that the answer is grounded in the context.
        
        If the answer cannot be found in the context,
        say so.
        
        Question:
        {question}
        
        Context:
        {context}
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text