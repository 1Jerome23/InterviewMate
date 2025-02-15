from gpt4all import GPT4All  

# Load the model only once at the start
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

def evaluate_answer(question, answer):
    """
    Uses GPT4All (Orca) to evaluate the interviewee's response in a structured and detailed way.
    """
    prompt = f"""
    You are an AI interviewer providing **detailed and structured feedback** on a candidate's interview response.
    
    Evaluate the candidate's answer based on the following criteria:

    **1. Strengths:** Identify positive aspects of the response. Highlight well-articulated points, strong reasoning, or relevant examples.  

    **2. Weaknesses:** Identify any gaps, missing details, or areas where the response could be stronger.  

    **3. Technical Accuracy:** Assess whether the response correctly addresses the question, and point out any factual inaccuracies or misunderstandings.  

    **4. Clarity & Communication:** Evaluate how clearly the response was conveyed. Was it concise yet informative? Was it structured logically?  

    **5. Suggestions for Improvement:** Provide actionable tips on how to enhance the response, such as adding examples, improving structure, or refining key points.  

    **Interview Question:**  
    {question}  

    **Candidate's Answer:**  
    {answer}  

    Provide a structured and constructive evaluation based on the points above.
    """

    try:
        response = model.generate(prompt, max_tokens=500)
        return response.strip()
    except Exception as e:
        return f"Error generating feedback: {e}"
