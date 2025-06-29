import gradio as gr
from agents import Runner, trace, gen_trace_id
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from research_agents.research_manager import research_manager_agent

load_dotenv(override=True)

async def run_research(query: str, recipient_email: str):
  trace_id = gen_trace_id()
  with trace("Research trace", trace_id=trace_id):
    print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
    yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
    
    # Run the research manager agent
    result = Runner.run_streamed(research_manager_agent, f"Query: {query}\nRecipient email: {recipient_email}")

    # Accumulate the full text and yield it each time
    full_text = ""
    
    # Yield the final output
    async for event in result.stream_events():
      if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        full_text += event.data.delta
        yield full_text

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
  gr.Markdown("# Deep Research AI")
  query = gr.Textbox(label="What topic do you want to research?")
  recipient_email = gr.Textbox(label="What is the email address where you want to receive the report?")
  run_button = gr.Button("Run Research", variant="primary")
  report = gr.Markdown(label="Report")

  run_button.click(fn=run_research, inputs=[query, recipient_email], outputs=report)

  ui.launch()
