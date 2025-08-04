from config import watsonx_enabled
from langchain_ibm import ChatWatsonx
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenTextParams

model_id = "mistralai/mistral-medium-2505" #"meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
# Get the credentials
credentials = watsonx_enabled()
llm = ChatWatsonx(
    model_id=model_id,
    params={GenTextParams.MAX_NEW_TOKENS: 2000, GenTextParams.DECODING_METHOD: "sample", GenTextParams.TEMPERATURE: 0.7},
    **credentials,
)
def generate(prompt: str, context: str = "") -> str:
    if watsonx_enabled():
        # print(f"Using LLM with prompt: {prompt}\nContext:\n{context}")
        response = llm.invoke(f"{prompt}\nContext:\n{context}")
        # print(f"LLM response: {response}")
        return response.content.strip()

    # Local stub behavior
    if not context:
        return prompt
    return f"{prompt}\n\n(From your recent notes:) {context[:300]}..."
