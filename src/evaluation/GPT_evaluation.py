from openai import OpenAI
import os
from dotenv import load_dotenv

def G_retrieval_evaluate(query:str, retrieved_contexts:str):
    load_dotenv()
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": 
                """
                ### Instruction:
                You are tasked with evaluating a Retrieval-Augmented Generation (RAG) system. Your evaluation focuses on one components:

                1. **Retrieval Evaluation (20 points)**: Assess the relevance and quality of the retrieved contexts used to generate the final answer.

                evaluation criterion has a weight associated with it. Assign "Yes" (full points) or "No" (0 points) for each criterion and provide a short justification for your assessment.

                """
            },
            {
                "role": "user", 
                "content": f"""
                ### Input:
                **Query**: {query}

                **Retrieved Contexts**:
                {retrieved_contexts}

                ### Output:

                #### 1. Retrieval Evaluation (20 points):
                Evaluate the quality of the retrieved contexts based on the following criteria:

                1. **Do any of the retrieved contexts show strong similarity to the Ground Truth?** (5 points)  
                [Yes/No] - Justification:

                2. **Do the retrieved contexts collectively capture essential information from the Ground Truth?** (5 points)  
                [Yes/No] - Justification:

                3. **Do the retrieved contexts sufficiently address the user’s question?** (4 points)  
                [Yes/No] - Justification:

                4. **Are all retrieved contexts relevant to the Ground Truth or the user’s query?** (3 points)  
                [Yes/No] - Justification:

                5. **Does the combined length and number of retrieved contexts remain reasonable without overwhelming the user with excessive or irrelevant details?** (3 points)  
                [Yes/No] - Justification:

                **Total Retrieval Score**: [ / 20]

                """
            }
        ],
        temperature=0.0,
    )

    response_score = response.choices[0].message.content
    return response_score


def G_generation_evaluate(query:str, ground_truth_answer:str, generated_answer:str):
    load_dotenv()
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": 
                """
                ### Instruction:
                You are tasked with evaluating a Retrieval-Augmented Generation (RAG) system. Your evaluation focuses on one components:

                1. **Generation Evaluation (30 points)**: Assess the quality, accuracy, and presentation of the system-generated answer.

                evaluation criterion has a weight associated with it. Assign "Yes" (full points) or "No" (0 points) for each criterion and provide a short justification for your assessment.
                """
            },
            {
                "role": "user", 
                "content": f"""
                ### Input:
                **Query**: {query}

                **Ground Truth Answer**: {ground_truth_answer}

                **Generated Answer**:
                {generated_answer}

                ### Output:

                #### 2. Generation Evaluation (30 points):
                Evaluate the quality of the generated answer based on the following criteria:

                1. **Is the final answer clearly relevant to the question and reflective of the user’s intent?** (5 points)  
                [Yes/No] - Justification:

                2. **Is the answer factually correct and free from unsupported or inaccurate information?** (5 points)  
                [Yes/No] - Justification:

                3. **Does the answer include all essential points required by the question and the ground_truth_answer?** (5 points)  
                [Yes/No] - Justification:

                4. **Is the answer clear and concise, avoiding unnecessary repetition or ambiguity?** (5 points)  
                [Yes/No] - Justification:

                5. **Is the answer logically structured, consistent with the context, and free of contradictions?** (3 points)  
                [Yes/No] - Justification:

                6. **Does the answer provide sufficient detail for the question without being excessive?** (3 points)  
                [Yes/No] - Justification:

                7. **Does the answer provide proper citations or indications of the source when claims or data are referenced?** (2 points)  
                [Yes/No] - Justification:

                8. **Is the answer presented in a suitable format (list, table, short text, etc.) for the question?** (1 point)  
                [Yes/No] - Justification:

                9. **Does the answer offer any helpful extra insights or context that enrich the user’s understanding (without deviating from factual correctness)?** (1 point)  
                [Yes/No] - Justification:

                **Total Generation Score**: [ / 30]

                """
            }
        ],
        temperature=0.0,
    )

    response_score = response.choices[0].message.content
    return response_score




