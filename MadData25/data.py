import pandas as pd
import openai

df = pd.read_csv("/Users/aashishmankala/Desktop/MadData25/All_Countries.csv")

print(df.head())

openai.api_key = "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"
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Welcome to the chatbot! Type 'quit', 'exit', or 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print("Chatbot:", response)