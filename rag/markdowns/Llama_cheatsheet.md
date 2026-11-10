# ChatOllama Cheatsheet — LangChain

## 1. Initialization

`ChatOllama(model="llama3.2:3b")`

Creates a connection to your local Ollama model. The model generates text based on the messages you send.

## 2. Model Configuration

### General

| Parameter | Example value | Description |
|---|---|---|
| `model` | `"llama3.2:3b"` | Model to use. |
| `base_url` | `"http://localhost:11434"` | Ollama server address. |
| `validate_model_on_init` | `True` | Check that the model exists locally. |
| `reasoning` | `False` | Disable reasoning mode (for supported models). |
| `format` | `"json"` | Request JSON output. |

### Text Generation

| Parameter | Example value | Description |
|---|---|---|
| `temperature` | `0.2` | Low randomness, useful for factual RAG answers. |
| `num_predict` | `512` | Generate up to 512 tokens. |
| `num_ctx` | `4096` | Context window of 4096 tokens. |
| `top_k` | `40` | Consider up to 40 likely tokens at each generation step. |
| `top_p` | `0.9` | Sample from tokens covering 90% cumulative probability. |
| `seed` | `42` | Set a seed for more reproducible results. |
| `stop` | `["END"]` | Stop generating when `END` appears. |
| `repeat_penalty` | `1.1` | Slightly discourage repeated tokens. |
| `repeat_last_n` | `64` | Check the previous 64 tokens for repetition. |
| `tfs_z` | `1.0` | Disable tail-free sampling. |

### Performance

| Parameter | Example value | Description |
|---|---|---|
| `num_gpu` | `1` | GPU count setting, where supported. |
| `num_thread` | `8` | Use 8 CPU threads. |
| `keep_alive` | `"5m"` | Keep the model loaded for 5 minutes after use. |

### Advanced

| Parameter | Example value | Description |
|---|---|---|
| `mirostat` | `0` | Disable Mirostat sampling. |
| `mirostat_eta` | `0.1` | Mirostat adjustment speed. |
| `mirostat_tau` | `5.0` | Target perplexity for Mirostat. |
| `logprobs` | `True` | Include generated token probabilities. |
| `top_logprobs` | `5` | Return up to 5 alternative token probabilities. |
| `client_kwargs` | `{"timeout": 120}` | Set HTTP timeout to 120 seconds. |
| `sync_client_kwargs` | `{"headers": {"X-App": "rag"}}` | Extra HTTP settings for synchronous calls. |
| `async_client_kwargs` | `{"timeout": 60}` | Extra HTTP settings for asynchronous calls. |

### Example Configuration for RAG

    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0.2,
        num_ctx=4096,
        num_predict=512,
        top_k=40,
        top_p=0.9,
        repeat_penalty=1.1,
        keep_alive="5m",
        validate_model_on_init=True
    )


## 3. Main Methods and Return Values

### `invoke(input)`

- **Does:** Sends a prompt or list of messages to the LLM and generates a complete answer.
- **Input:** String, messages, or another supported prompt representation.
- **Returns:** `AIMessage` containing the generated answer.
- **Use:** Standard RAG answer generation.

### `ainvoke(input)`

- **Does:** Same as `invoke()`, but asynchronously. Allows other asynchronous tasks to run while awaiting the result.
- **Input:** Same as `invoke()`.
- **Returns:** `AIMessage` when awaited.
- **Use:** Asynchronous applications.

### `stream(input)`

- **Does:** Generates the answer incrementally instead of returning everything at once.
- **Input:** Prompt or messages.
- **Returns:** Iterator of `AIMessageChunk` objects.
- **Use:** Displaying answers as they are generated.

### `astream(input)`

- **Does:** Asynchronous version of `stream()`.
- **Input:** Prompt or messages.
- **Returns:** Async iterator of `AIMessageChunk` objects.
- **Use:** Streaming in asynchronous applications.

### `batch(inputs)`

- **Does:** Processes multiple independent prompts.
- **Input:** List of prompts or message lists.
- **Returns:** List of `AIMessage` objects, following input order.
- **Use:** Answering multiple questions in one workflow.

### `abatch(inputs)`

- **Does:** Asynchronous version of `batch()`.
- **Input:** List of prompts.
- **Returns:** List of `AIMessage` objects when awaited.

### `batch_as_completed(inputs)`

- **Does:** Processes multiple prompts and yields results as individual calls finish.
- **Input:** List of prompts.
- **Returns:** Iterator of `(input_index, result)` tuples. Results can be messages or exceptions when exception-returning behavior is enabled.

### `generate(messages)`

- **Does:** Generates responses for multiple conversations, supporting additional generation information.
- **Input:** List of message lists.
- **Returns:** `LLMResult`, containing generated messages and additional information.

### `agenerate(messages)`

- **Does:** Asynchronous version of `generate()`.
- **Returns:** `LLMResult` when awaited.

### `bind(**kwargs)`

- **Does:** Creates a model wrapper with predefined options reused for later calls.
- **Returns:** A new `Runnable` object.
- **Use:** Reusing generation configurations.

### `bind_tools(tools)`

- **Does:** Makes tools available for the model to request during generation, if supported.
- **Returns:** A configured `Runnable`.
- **Important:** It does not automatically execute requested tools.

### `with_structured_output(schema)`

- **Does:** Configures the model to produce output following a specified structure.
- **Input:** Schema such as a Pydantic model or JSON schema.
- **Returns:** A `Runnable` that produces structured data when invoked.
- **Use:** Responses requiring predictable fields.

### `with_retry()`

- **Does:** Creates a wrapper that automatically retries failed model calls.
- **Returns:** A `Runnable` with retry behavior.

### `get_num_tokens(text)`

- **Does:** Estimates token usage for a given string using the configured tokenizer.
- **Returns:** Integer token count.
- **Note:** The estimate may differ from Ollama's actual tokenizer count.

## 4. Message Types

Messages tell the LLM **who is providing the information**.

They are normally created before calling `invoke()` and passed together as a list.

| Message | Purpose | When to use |
|---|---|---|
| `SystemMessage` | Defines instructions, rules, and expected behavior. | Telling your RAG to answer using retrieved context. |
| `HumanMessage` | Represents information submitted by the user. | Passing the user question and relevant document chunks. |
| `AIMessage` | Represents a response produced by the model. | Reading responses or providing previous assistant replies in conversation history. |
| `ToolMessage` | Contains the result of an executed tool call. | When implementing tool-calling workflows. |

### How to use them

**Before calling the model:**

- `SystemMessage`: Explains the assistant's role and rules.
- `HumanMessage`: Contains the user's question and retrieved context.

**After calling the model:**

- `AIMessage`: Contains Llama's generated answer.

### Example

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(
        content="Answer using only the provided context."
    ),
    HumanMessage(
        content=f"Context:\n{context}\n\nQuestion:\n{user_prompt}"
    )
]

response = llm.invoke(messages)
```

## 5. Response Attributes

The `invoke()` method returns an `AIMessage`, not a plain string.

| Attribute | Returns | Description |
|---|---|---|
| `.content` | String or content blocks | The generated response. |
| `.response_metadata` | Dictionary | Model information, timing, token counts, and other Ollama response details. |
| `.usage_metadata` | Dictionary or `None` | Standardized token counts when available. |
| `.tool_calls` | List | Tools requested by the model, if any. |
| `.id` | String or `None` | Identifier associated with the response. |
| `.additional_kwargs` | Dictionary | Additional provider-specific response information. |

To retrieve the generated text:

```python
response = llm.invoke(messages)
answer = response.content
```

## 6. Documentation

**ChatOllama API Reference:**

https://reference.langchain.com/python/langchain-ollama/chat_models/ChatOllama

**ChatOllama Integration Guide:**

https://docs.langchain.com/oss/python/integrations/chat/ollama

**LangChain Message Concepts:**

https://docs.langchain.com/oss/python/langchain/messages
