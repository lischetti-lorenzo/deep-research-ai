import gradio as gr
from dotenv import load_dotenv
from research_agents.research_manager import ResearchManager

load_dotenv(override=True)

async def run_research(query: str, recipient_email: str):
  async for chunk in ResearchManager().run(query, recipient_email):
    yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
  gr.Markdown("# Deep Research AI")
  query = gr.Textbox(label="What topic do you want to research?")
  recipient_email = gr.Textbox(label="What is the email address where you want to receive the report?")
  run_button = gr.Button("Run Research", variant="primary")
  report = gr.Markdown(label="Report")

  run_button.click(fn=run_research, inputs=[query, recipient_email], outputs=report)

  ui.launch()
