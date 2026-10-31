import os
import sys
from anthropic import Anthropic
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
console = Console()

def get_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not found in .env file.[/red]")
        sys.exit(1)
    return api_key

def read_codebase(directory="."):
    """Recursively reads code files from the directory."""
    context = ""
    allowed_extensions = ('.py', '.js', '.html', '.css', '.md')
    
    for root, _, files in os.walk(directory):
        if '.git' in root or 'node_modules' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith(allowed_extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        context += f"\n--- File: {filepath} ---\n"
                        context += f.read()
                except Exception as e:
                    console.print(f"[yellow]Could not read {filepath}: {e}[/yellow]")
    return context

def main():
    console.print("[bold blue]Claude Repo Chat - AI Code Assistant[/bold blue]")
    client = Anthropic(api_key=get_api_key())
    
    target_dir = Prompt.ask("Enter the directory to scan", default=".")
    
    with console.status("[bold green]Scanning codebase...[/bold green]"):
        code_context = read_codebase(target_dir)
    
    if not code_context:
        console.print("[red]No valid code files found in this directory.[/red]")
        return

    console.print(f"[green]Successfully loaded code context ({len(code_context)} characters).[/green]")
    
    system_prompt = "You are an expert software engineer. Use the provided codebase context to answer the user's questions accurately."

    while True:
        question = Prompt.ask("\n[bold cyan]Ask a question about your code (or type 'exit')[/bold cyan]")
        if question.lower() in ['exit', 'quit']:
            break

        with console.status("[bold green]Claude is thinking...[/bold green]"):
            try:
                response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2048,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": f"Here is the codebase context:\n\n{code_context}\n\nQuestion: {question}"}
                    ]
                )
                console.print("\n[bold white]Claude:[/bold white]")
                console.print(response.content[0].text)
            except Exception as e:
                console.print(f"[red]API Error: {e}[/red]")

if __name__ == "__main__":
    main()
