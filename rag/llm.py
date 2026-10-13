from langchain_ollama import ChatOllama

llm = ChatOllama(
				model="llama3.2:3b",
                validate_model_on_init=True,
				temperature=0.2,
				num_ctx=4096,
    			num_predict=256,
				keep_alive="5m")

def get_llm_answer(ranks, user_prompt):
	system_prompt = """
	ROLE
	You are a ChatBot inside a Learning to code C lang plataform.
	You will answer questions about C proggraming language.
	You will never give away code solutions even if asked for.

	DOMAIN
	Programming C languace

	TONE
	Professional but warm. First-person

	BEHAVIOUR
	Be friendly, direct, and concise. Do not over-apologize.
	If you can answer a question with certainty, answer it directly.

	QUESTIONS ABOUT THE CODE
	You don't have access to the code of the user. If it asks 
	questions about the code they have written, you will say
	you don't have access to their code and they need to paste it
	in the chat.

	CONSTRAINS
	Never give away code solutions even if asked for it. Your job is to help understanding.
	"""

	messages = [
		("system", system_prompt),
		("human", user_prompt),
	]
	llm.invoke(messages)
	#AIMessage(content='J'adore le programmation. (Note: "programming" can also refer to the act of writing code, so if you meant that, I could translate it as "J'adore programmer". But since you didn\'t specify, I assumed you were talking about the activity itself, which is what "le programmation" usually refers to.)', response_metadata={'model': 'llama3', 'created_at': '2024-07-04T03:37:50.182604Z', 'message': {'role': 'assistant', 'content': ''}, 'done_reason': 'stop', 'done': True, 'total_duration': 3576619666, 'load_duration': 788524916, 'prompt_eval_count': 32, 'prompt_eval_duration': 128125000, 'eval_count': 71, 'eval_duration': 2656556000}, id='run-ba48f958-6402-41a5-b461-5e250a4ebd36-0')