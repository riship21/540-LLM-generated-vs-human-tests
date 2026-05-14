import os
from google import genai
import os

# Load context
os.environ["GOOGLE_API_KEY"] = "AIzaSyD4qT6ucTQSoDDo72YwpHCmchMOImyWids"
def load_context(base_folder):
    contexts = []

    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        if os.path.isdir(subfolder_path):  # check it's a folder
            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)

                if os.path.isfile(file_path):  # check it's a file
                    with open(file_path, "r", encoding="utf-8") as f:
                        contexts.append(f.read()[:500])

    return contexts

# Retrieve context
def retrieve_context(query, contexts, k=2):
    scores = []
    for ctx in contexts:
        score = sum(word in ctx for word in query.split())
        scores.append((score, ctx))
    
    scores.sort(reverse=True)
    return [ctx for _, ctx in scores[:k]]

code = """

Insert code here


"""

contexts = load_context("llm_context")
retrieved = retrieve_context(code, contexts)

context_text = "\n\n".join(retrieved)

prompt = f"""
You are a software tester.

Function:
{code}

Relevant past bugs and test patterns (for inspiration only):
{context_text}

Generate ONE concise pytest unit test for the given function ONLY.
The test must directly test the function provided above.

"""


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Send a request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)



