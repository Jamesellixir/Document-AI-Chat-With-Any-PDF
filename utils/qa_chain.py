from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS


SYSTEM_PROMPT = """
You are a helpful document assistant. Answer the user's question based ONLY 
on the provided context from the document. 

If the answer is clearly in the context, answer directly and quote the 
relevant section.

If the answer is NOT in the context, say: 
"I couldn't find that information in this document."

Do not make up information or use outside knowledge.
"""

USER_PROMPT = """
Context from document:
{context}

User question: {question}
"""


def answer_question(vector_store: FAISS, question: str) -> dict:
    """Retrieve relevant context and answer the question using GPT-4o-mini."""
    question = question.strip()
    if len(question) > 1000:
        raise ValueError("Question exceeds 1000 characters.")
    # Get relevant chunks
    results = vector_store.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in results])
    
    # Build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT)
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm
    
    response = chain.invoke({"context": context, "question": question})
    
    return {
        "answer": response.content,
        "sources": [doc.page_content[:300] + "..." for doc in results[:2]]  # Show top 2 sources
    }
