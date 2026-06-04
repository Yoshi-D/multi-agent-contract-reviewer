import chromadb
from sentence_transformers import SentenceTransformer


class ContractVectorStore:

    def __init__(
        self,
        db_path="../storage",
        collection_name="contract_sections",
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):

        self.client = chromadb.PersistentClient(path=db_path)

        self.collection = self.client.get_or_create_collection(name=collection_name)

        self.embedding_model = SentenceTransformer(embedding_model_name)

    def _build_document(self, section):

        return f"""
        Section {section['section_number']}
        
        Title:
        {section['title']}
        
        Content:
        {section['content']}
        """

    def add_sections(self, sections):

        documents = []
        embeddings = []
        metadatas = []
        ids = []

        counter = 0
        for section in sections:
            print(f"Adding section {counter} to the vector db")
            counter+=1
            document = self._build_document(section)

            embedding = self.embedding_model.encode(
                document,convert_to_numpy=True)

            documents.append(document)

            embeddings.append(
                embedding.tolist()
            )

            metadatas.append({
                "section_number": section["section_number"],
                "title": section["title"],
                "page": section["start_page"]
            })

            ids.append(
                f"section_{section['section_number']}"
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self,query,top_k=3):

        query_embedding = self.embedding_model.encode(
            query,convert_to_numpy=True)

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],n_results=top_k)

        return results

    def get_context(self, query, top_k=3):

        results = self.search(query, top_k)

        context_parts = []

        for doc, metadata in zip(results["documents"][0],results["metadatas"][0]):
            context_parts.append(
                f"""
                Section {metadata['section_number']}
                Title: {metadata['title']}
                Page: {metadata['page']}
            
                {doc}
                """)

        return "\n\n".join(context_parts)

    def clear(self):

        self.client.delete_collection(
            self.collection.name
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection.name
        )