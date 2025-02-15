import chainlit as cl
import ollama

@cl.set_chat_profiles
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Llama3.2 Vision",
            markdown_description="The underlying LLM model is **Llama3.2 Vision**. It supports both text and images.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="deepseek-r1:8b",
            markdown_description="The underlying LLM model is **deepseek-r1:8b**. Text-based model.",
            icon="https://picsum.photos/250",
        ),
        cl.ChatProfile(
            name="phi3",
            markdown_description="The underlying LLM model is **phi3**. Text-based model.",
            icon="https://picsum.photos/300",
        ),
        cl.ChatProfile(
            name="qwen2.5-coder:0.5b",
            markdown_description="The underlying LLM model is **qwen2.5-coder:0.5b**. Text-based model.",
            icon="https://picsum.photos/350",
        ),
    ]

@cl.on_chat_start
async def start_chat():
    # Initialize conversation context
    cl.user_session.set(
        "interaction",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ],
    )

    msg = cl.Message(content="")
    # Retrieve the selected profile; default to "Llama3.2 Vision" if none selected.
    selected_profile = cl.user_session.get("chat_profile")
    model_used = selected_profile or "Llama3.2 Vision"
    start_message = f"Hello, I'm your assistant running on {model_used}. How can I help you today?"

    for token in start_message:
        await msg.stream_token(token)
    await msg.send()

@cl.step(type="tool")
async def tool(input_message, image=None):
    interaction = cl.user_session.get("interaction")
    # Retrieve the selected chat profile.
    selected_profile = cl.user_session.get("chat_profile")
    
    # Map the selected profile to the correct model name.
    if selected_profile == "deepseek-r1:8b":
        model_name = "deepseek-r1:8b"
    elif selected_profile == "phi3":
        model_name = "phi3"
    elif selected_profile == "qwen2.5-coder:0.5b":
        model_name = "qwen2.5-coder:0.5b"
    else:
        # Default to Llama3.2 Vision if none is selected or for any other profile.
        model_name = "llama3.2-vision"

    # Only attach images if the model supports vision.
    if image and model_name == "llama3.2-vision":
        interaction.append({
            "role": "user",
            "content": input_message,
            "images": image
        })
    else:
        interaction.append({
            "role": "user",
            "content": input_message
        })

    try:
        response = ollama.chat(model=model_name, messages=interaction)
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        await cl.Message(content=error_msg).send()
        return

    interaction.append({
        "role": "assistant",
        "content": response.message.content
    })

    return response

@cl.on_message
async def main(message: cl.Message):
    # Check if the incoming message contains any image files.
    images = [file for file in message.elements if "image" in file.mime]

    if images:
        tool_res = await tool(message.content, [i.path for i in images])
    else:
        tool_res = await tool(message.content)

    msg = cl.Message(content="")
    for token in tool_res.message.content:
        await msg.stream_token(token)
    await msg.send()
