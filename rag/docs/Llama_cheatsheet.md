
# ChatOllama Cheatsheet

## 1. Initialization

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b")
```

## 2. Model Configuration

### General

| Parameter | Description |
|---|---|
| `model` | Name of the Ollama model. |
| `base_url` | Ollama server address. |
| `validate_model_on_init` | Check if the model exists locally. |
| `reasoning` | Enable reasoning on supported models. |
| `format` | Output format, such as JSON. |

### Generation

| Parameter | Description |
|---|---|
| `temperature` | Controls randomness. |
| `num_predict` | Maximum generated tokens. |
| `num_ctx` | Context window size in tokens. |
| `top_k` | Limits token candidates. |
| `top_p` | Controls token probability threshold. |
| `seed` | Random seed for reproducibility. |
| `stop` | Sequences that stop generation. |
| `repeat_penalty` | Penalizes repeated tokens. |
| `repeat_last_n` | Number of previous tokens checked. |
| `tfs_z` | Tail-free sampling control. |

### Performance

| Parameter | Description |
|---|---|
| `num_gpu` | Number of GPUs to use. |
| `num_thread` | Number of CPU threads. |
| `keep_alive` | Time the model remains loaded in memory. |

### Advanced

| Parameter | Description |
|---|---|
| `mirostat` | Enable adaptive sampling. |
| `mirostat_eta` | Mirostat adjustment speed. |
| `mirostat_tau` | Target perplexity. |
| `logprobs` | Return token log probabilities. |
| `top_logprobs` | Number of alternative token log probabilities. |
| `client_kwargs` | Shared HTTP client options. |
| `sync_client_kwargs` | Synchronous HTTP client options. |
| `async_client_kwargs` | Asynchronous HTTP client options. |

## 3. Main Methods

| Method | Description |
|---|---|
| `invoke(input)` | Generate a complete response. |
| `ainvoke(input)` | Asynchronous response generation. |
| `stream(input)` | Generate response token chunks progressively. |
| `astream(input)` | Asynchronous streaming. |
| `batch(inputs)` | Process multiple prompts. |
| `abatch(inputs)` | Asynchronous batch processing. |
| `batch_as_completed(inputs)` | Return batch results as they complete. |
| `generate(messages)` | Generate responses for batches of chat messages. |
| `agenerate(messages)` | Asynchronous version of `generate()`. |
| `bind(**kwargs)` | Set reusable invocation arguments. |
| `bind_tools(tools)` | Bind tools for model tool calling. |
| `with_structured_output(schema)` | Request structured output matching a schema. |
| `with_retry()` | Retry failed invocations. |
| `get_num_tokens(text)` | Estimate the number of tokens in text. |

## 4. Message Types

| Type | Purpose |
|---|---|
| `SystemMessage` | Define instructions and model behavior. |
| `HumanMessage` | Provide the user's question and context. |
| `AIMessage` | Represent an assistant response. |
| `ToolMessage` | Provide results returned by tools. |

## 5. Response Attributes

| Attribute | Description |
|---|---|
| `.content` | Generated response content. |
| `.response_metadata` | Model and execution information. |
| `.usage_metadata` | Token usage statistics, when available. |
| `.tool_calls` | Tool calls requested by the model. |
| `.id` | Response identifier. |

## 6. Documentation

ChatOllama API Reference:
https://reference.langchain.com/python/langchain-ollama/langchain_ollama/chat_models/ChatOllama

ChatOllama Integration:
https://docs.langchain.com/oss/python/integrations/chat/ollama
