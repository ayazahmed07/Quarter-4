#!/usr/bin/env python3
import os
import google.generativeai as genai
from colorama import Fore, Style, init
from PIL import Image
import readline

# 🔧 Initialize
init(autoreset=True)

# 🔑 Your API key
API_KEY = "AIzaSyCAvugosuJWS7-8ffUemAiR5qGfPCtCBqg"
genai.configure(api_key=API_KEY)

# 🧠 Memory setup
conversation = []

# Choose your model
model = genai.GenerativeModel("models/gemini-2.5-flash")

print(Fore.GREEN + "\n🤖 Gemini CLI Chat (Memory + Files + Images)")
print(Fore.CYAN + "Type your message, or use:")
print(Fore.YELLOW + " - /clear         → clear chat memory")
print(Fore.YELLOW + " - exit / quit / bye → to end chat\n")

# 💬 Chat Loop
while True:
    try:
        user_input = input(Fore.BLUE + "👤 You: " + Style.RESET_ALL).strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print(Fore.MAGENTA + "👋 Goodbye! See you soon!\n")
            break

        elif user_input.lower() == "/clear":
            conversation.clear()
            print(Fore.CYAN + "🧹 Memory cleared!\n")
            continue

        elif user_input.startswith("/file "):
            file_path = user_input.split("/file ", 1)[1].strip()
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_text = f.read()
                print(Fore.YELLOW + "📄 File uploaded! Gemini is reading it...\n")
                prompt = f"Analyze or summarize this file:\n\n{file_text[:5000]}"
            else:
                print(Fore.RED + "❌ File not found.\n")
                continue

        elif user_input.startswith("/image "):
            image_path = user_input.split("/image ", 1)[1].strip()
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    print(Fore.YELLOW + "🖼️  Image uploaded! Gemini is analyzing...\n")
                    response = model.generate_content(
                        [user_input, img]
                    )
                    print(Fore.GREEN + "💬 Gemini: " + Style.RESET_ALL + response.text + "\n")
                    continue
                except Exception as e:
                    print(Fore.RED + f"❌ Error reading image: {e}\n")
                    continue
            else:
                print(Fore.RED + "❌ Image file not found.\n")
                continue

        else:
            prompt = user_input

        # Add memory
        conversation.append({"role": "user", "content": prompt})

        print(Fore.YELLOW + "🤖 Gemini is thinking...\n")
        chat = model.generate_content(
            [c["content"] for c in conversation]
        )

        reply = chat.text.strip()
        print(Fore.GREEN + "💬 Gemini: " + Style.RESET_ALL + reply + "\n")

        # Save model’s response to memory
        conversation.append({"role": "assistant", "content": reply})

    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\n👋 Chat ended by user.\n")
        break
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}\n")

