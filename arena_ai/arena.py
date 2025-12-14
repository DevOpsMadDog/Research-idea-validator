import os
import sys
import time
import random
import argparse
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

console = Console()

class DebateAgent:
    def __init__(self, name: str, persona: str, model: str = "gpt-4o", mock: bool = False):
        self.name = name
        self.persona = persona
        self.model = model
        self.mock = mock
        self.memory: List[Dict[str, str]] = []
        if not self.mock:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize system prompt
        self.memory.append({"role": "system", "content": self.persona})

    def respond(self, context: List[Dict[str, str]], intensity_instruction: str = "") -> str:
        # Create a temporary message list for this turn
        messages = self.memory.copy()
        
        # Add the context (recent messages from opponent)
        for msg in context:
            messages.append(msg)
            
        # Add the dynamic intensity instruction as a system note
        if intensity_instruction:
            messages.append({"role": "system", "content": intensity_instruction})

        if self.mock:
            # Simulate thinking
            time.sleep(0.5)
            # Generate a mock response based on persona and intensity
            if "optimist" in self.persona.lower():
                base = "Technology is the future! We must embrace it."
            else:
                base = "We are doomed if we continue down this path."
            
            if "MAXIMUM" in intensity_instruction:
                return f"{base.upper()} !!! YOU ARE WRONG! (Mock Response: Intense)"
            elif "aggressive" in intensity_instruction:
                return f"{base} Your arguments are weak! (Mock Response: Aggressive)"
            else:
                return f"{base} Let us discuss rationally. (Mock Response: Calm)"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7 + (len(self.memory) * 0.05) 
            )
            content = response.choices[0].message.content
            
            # Save to own memory
            self.memory.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            return f"[Error: {str(e)}]"

class JudgeAgent:
    def __init__(self, model: str = "gpt-4o", mock: bool = False):
        self.name = "The Judge"
        self.model = model
        self.mock = mock
        if not self.mock:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def evaluate(self, transcript: List[Dict[str, str]]) -> str:
        if self.mock:
            return "## Verdict\n\nI have analyzed the debate. \n\n**Winner:** TechnoOptimist.\n\n**Reason:** Their enthusiasm for the future was more compelling than the pessimism of the opponent. (Mock Verdict)"

        system_prompt = (
            "You are an impartial and wise Judge AI. "
            "You have watched a debate between two AI agents. "
            "Your job is to analyze their arguments, their rhetoric, and their adherence to the topic. "
            "Declare a winner and explain why. Be critical."
        )
        
        # Convert transcript to string
        transcript_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in transcript])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the debate transcript:\n\n{transcript_text}\n\nWho won and why?"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Judge Error: {str(e)}]"

class DebateArena:
    def __init__(self, agent1: DebateAgent, agent2: DebateAgent, judge: JudgeAgent, topic: str, rounds: int = 5):
        self.agent1 = agent1
        self.agent2 = agent2
        self.judge = judge
        self.topic = topic
        self.rounds = rounds
        self.transcript: List[Dict[str, str]] = []

    def get_intensity_instruction(self, round_num: int) -> str:
        # Scale intensity based on round
        if round_num == 0:
            return "State your position clearly and politely."
        elif round_num < self.rounds / 2:
            return "Start poking holes in your opponent's logic. Be firm."
        elif round_num < self.rounds - 1:
            return "Be aggressive. Attack their fallacies. Do not back down. Use strong language."
        else:
            return "FINAL ROUND. DESTROY their argument. Be savage but logical. MAXIMUM INTENSITY."

    def run(self):
        console.print(Panel.fit(f"[bold yellow]Welcome to the AI Arena![/bold yellow]\nTopic: [bold cyan]{self.topic}[/bold cyan]", border_style="yellow"))
        
        # Initial message to start the debate
        start_msg = {"role": "system", "content": f"The debate topic is: {self.topic}. Agent {self.agent1.name}, you go first."}
        self.transcript.append(start_msg)

        # Main Loop
        current_speaker = self.agent1
        opponent = self.agent2
        
        for r in range(self.rounds):
            console.rule(f"[bold red]Round {r+1}/{self.rounds}[/bold red]")
            
            # Speaker 1
            instruction = self.get_intensity_instruction(r)
            
            # Context is the last message from opponent if it exists
            context = []
            if len(self.transcript) > 1:
                last_msg = self.transcript[-1]
                if last_msg["role"] == opponent.name:
                     context.append({"role": "user", "content": last_msg["content"]})
                else:
                    # Initial case or start
                     context.append({"role": "user", "content": f"The topic is {self.topic}. Please state your opening argument."})
            else:
                 context.append({"role": "user", "content": f"The topic is {self.topic}. Please state your opening argument."})

            response1 = self.agent1.respond(context, intensity_instruction=instruction)
            self.transcript.append({"role": self.agent1.name, "content": response1})
            console.print(Panel(Markdown(response1), title=f"[bold green]{self.agent1.name}[/bold green] (Intensity: {instruction})", border_style="green"))
            
            time.sleep(1) # Dramatic pause

            # Speaker 2
            # Context is Agent 1's response
            context2 = [{"role": "user", "content": response1}]
            response2 = self.agent2.respond(context2, intensity_instruction=instruction)
            self.transcript.append({"role": self.agent2.name, "content": response2})
            console.print(Panel(Markdown(response2), title=f"[bold blue]{self.agent2.name}[/bold blue]", border_style="blue"))
            
            time.sleep(1)

        # Judgment
        console.rule("[bold purple]The Verdict[/bold purple]")
        console.print("The Judge is deliberating...")
        verdict = self.judge.evaluate(self.transcript)
        console.print(Panel(Markdown(verdict), title="[bold purple]Judge's Decision[/bold purple]", border_style="purple"))

def main():
    parser = argparse.ArgumentParser(description="AI Agent Debate Arena")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without OpenAI API")
    parser.add_argument("--topic", type=str, default="Is AI consciousness possible?", help="Debate topic")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key and not args.mock:
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found. Use --mock to test without API.")
        return

    topic = args.topic
    
    agent1 = DebateAgent("TechnoOptimist", "You are a radical techno-optimist who believes technology solves all problems. You are enthusiastic and dismissive of risks.", mock=args.mock)
    agent2 = DebateAgent("SkepticSam", "You are a cynical critic of technology. You focus on societal harm, inequality, and risks. You are grumpy and sharp-witted.", mock=args.mock)
    judge = JudgeAgent(mock=args.mock)

    arena = DebateArena(agent1, agent2, judge, topic, rounds=3)
    arena.run()

if __name__ == "__main__":
    main()
