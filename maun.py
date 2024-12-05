from ollama import chat

# History of messages
messages = [
    {
        'role': 'user',
        'content': 'Explain the given code snippet.',
    },
    {
        'role': 'assistant',
        'content': "Sure! Please share the code snippet, and I will provide a detailed explanation.",
    },
]

while True:
    user_input = input('Provide a code snippet: ')
    
    # Send the user input to the chat model
    response = chat(
        'qwen2.5-coder:0.5b',
        messages= messages
        + [
            {'role': 'user', 'content': user_input},
        ],
    )
    
    # Add the conversation to the message history
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response.message.content},
    ]
    
    # Print the response
    print(response.message.content + '\n')
