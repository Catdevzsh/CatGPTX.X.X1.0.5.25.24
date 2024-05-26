import openai
from openai import OpenAI

client = OpenAI(api_key="lm-studio")
import tkinter as tk
from tkinter import scrolledtext

# Configuration for the OpenAI API client
# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="http://localhost:1234/v1")'
# openai.api_base = "http://localhost:1234/v1"

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

class CatGPTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CatGPT M1 Mac Desktop App v0x.x")
        self.root.geometry("600x400")

        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 10))
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(root, font=("Arial", 12))
        self.user_input.pack(pady=10, padx=10, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self.append_to_chat("You: " + user_message)
        history.append({"role": "user", "content": user_message})
        self.user_input.delete(0, tk.END)

        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, "CatGPT is typing...\n")
        self.chat_history.configure(state='disabled')

        try:
            response = client.completions.create(engine="gpt-3.5-turbo",
            prompt=self.build_prompt(),
            temperature=0.7,
            max_tokens=150)

            assistant_message = response.choices[0].text.strip()
            self.append_to_chat("CatGPT: " + assistant_message)
            history.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            self.append_to_chat(f"Error: {e}")

    def build_prompt(self):
        prompt = ""
        for message in history:
            if message["role"] == "system":
                prompt += "System: " + message["content"] + "\n"
            elif message["role"] == "user":
                prompt += "You: " + message["content"] + "\n"
            elif message["role"] == "assistant":
                prompt += "CatGPT: " + message["content"] + "\n"
        return prompt

    def append_to_chat(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatGPTApp(root)
    root.mainloop()
