import chainlit as cl
import base64
from groq import Groq

# Initialize Groq client once
client = Groq()

def encode_image(image_path):
    """Encode an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@cl.set_chat_profiles
async def chat_profiles():
    return [
        cl.ChatProfile(
            name="Llama3.2 Vision",
            markdown_description="The underlying LLM model is **Llama3.2 Vision**. Supports text and one image per request.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="deepseek-r1:8b",
            markdown_description="The underlying LLM model is **deepseek-r1:8b**. (Text-only)",
            icon="https://picsum.photos/250",
        ),
        cl.ChatProfile(
            name="gemma2-9b-it	",
            markdown_description="The underlying LLM model is **gemma2-9b-it**. (Text-only)",
            icon="https://picsum.photos/300",
        ),
        cl.ChatProfile(
            name="qwen-2.5-32b",
            markdown_description="The underlying LLM model is **qwen-2.5-32b**. (Text-only)",
            icon="https://picsum.photos/350",
        ),
    ]

@cl.on_chat_start
async def start_chat():
    # Initialize conversation context (system prompt will be used only for text models)
    cl.user_session.set("interaction", [
        {"role": "system", "content": "You are a helpful assistant."}
    ])

    msg = cl.Message(content="")
    selected_profile = cl.user_session.get("chat_profile")
    model_used = selected_profile or "Llama3.2 Vision"
    start_message = f"Hello, I'm your assistant running on {model_used}. How can I help you today?"
    for token in start_message:
        await msg.stream_token(token)
    await msg.send()

@cl.step(type="tool")
async def tool(input_message, image=None):
    interaction = cl.user_session.get("interaction")
    selected_profile = cl.user_session.get("chat_profile")

    # Map the selected profile to the corresponding model ID.
    if selected_profile == "deepseek-r1:8b":
        model_name = "deepseek-r1-distill-llama-70b"  # per documentation
    elif selected_profile == "gemma2-9b-it	":
        model_name = "gemma2-9b-it	"  # assuming this is the model ID
    elif selected_profile == "qwen-2.5-32b":
        model_name = "qwen-2.5-32b"
    else:
        # Default to vision model for Llama3.2 Vision
        model_name = "llama-3.2-11b-vision-preview"

    # Check if this is a vision request.
    if image and model_name == "llama-3.2-11b-vision-preview":
        # Only one image is allowed. Encode the first image.
        base64_image = encode_image(image[0])
        # Construct the vision message as a list of parts.
        vision_message = [
            {"type": "text", "text": input_message},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        # Do not include system messages when sending an image.
        messages = [{"role": "user", "content": vision_message}]
        stream_response = False  # Vision requests do not support streaming.
    else:
        # For text-only models, append the user message to the conversation history.
        interaction.append({"role": "user", "content": input_message})
        messages = interaction
        stream_response = True

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=stream_response
        )
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        await cl.Message(content=error_msg).send()
        return

    final_response = ""
    if stream_response:
        # For text-only models, accumulate the streamed response.
        for chunk in completion:
            token = chunk.choices[0].delta.content or ""
            final_response += token
        interaction.append({"role": "assistant", "content": final_response})
    else:
        # For vision requests, streaming is off.
        final_response = completion.choices[0].message.content

    # Mimic the previous response structure.
    class Response:
        pass
    response = Response()
    response.message = type("Message", (), {})()
    response.message.content = final_response
    return response

@cl.on_message
async def main(message: cl.Message):
    # Extract image files if any.
    images = [file for file in message.elements if "image" in file.mime]
    if images:
        # Pass the local image path(s) to the tool function.
        tool_res = await tool(message.content, [i.path for i in images])
    else:
        tool_res = await tool(message.content)

    msg = cl.Message(content="")
    for token in tool_res.message.content:
        await msg.stream_token(token)
    await msg.send()
