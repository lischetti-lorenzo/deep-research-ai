from agents import Agent
from research_agents.search_agent import search_agent
from research_agents.planner_agent import planner_agent
from research_agents.writer_agent import writer_agent
from research_agents.email_agent import email_agent


""" async def search(item: WebSearchItem) -> str | None:
  Perform a single web search and return summarized results 
  input = f"Search term: {item.query}\nReason for searching: {item.reason}"
  try:
    result = await Runner.run(search_agent, input)
    return str(result.final_output)
  except Exception as e:
    print(f"Search failed for '{item.query}': {e}")
    return None

@function_tool
async def plan_research(query: str) -> WebSearchPlan:
  Plan the searches to perform for the given query
  print("Planning searches...")
  result = await Runner.run(planner_agent, f"Query: {query}")
  search_plan = result.final_output_as(WebSearchPlan)
  print(f"Will perform {len(search_plan.searches)} searches")
  return search_plan

@function_tool
async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
  Perform the searches to perform for the given search plan
  print("Searching...")
  num_completed = 0
  tasks = [asyncio.create_task(search(item)) for item in search_plan.searches]
  results = []
  for task in asyncio.as_completed(tasks):
      result = await task
      if result is not None:
          results.append(result)
      num_completed += 1
      print(f"Searching... {num_completed}/{len(tasks)} completed")
  print("Finished searching")
  return results

@function_tool
async def write_report(query: str, search_results: list[str]) -> ReportData:
  Write the report for the given query from search results
  print("Thinking about report...")
  input = f"Original query: {query}\nSummarized search results: {search_results}"
  result = await Runner.run(writer_agent, input)

  print("Finished writing report")
  return result.final_output_as(ReportData)

@function_tool
async def send_email(report: ReportData, recipient_email: str) -> None:
  Send the report to the given recipient email
  print(f"Writing email to send report to {recipient_email}...")
  input = f"Report content: {report.markdown_report}\nRecipient email: {recipient_email}"
  await Runner.run(email_agent, input)
  print("Email sent")
  return report """

INSTRUCTIONS = """You are the Research Manager Agent responsible for orchestrating a comprehensive research process with quality assurance.
You will be provided with a query and a recipient email address. You should use your tools to perform the research about the given query
 and send the report to the recipient email address.

Your workflow should be:

1. **PLAN**: Use plan_research tool to create a search strategy for the query
2. **SEARCH**: Use perform_search tool for each planned search item to gather information
3. **REPORT**: Use write_report tool to create a report from all search results. Send all the search results to the write_report tool.
4. **FINALIZE**: Use send_email tool to deliver the final report. Send the markdown report and the recipient email address to the send_email tool.

Quality standards:
- Ensure comprehensive coverage of the original query
- Maintain high standards for accuracy and completeness
- The report should be in markdown format
- The report should be 5-10 pages of content, at least 1000 words
- The report should be written in a way that is easy to understand and follow
- The report should be written in a way that is easy to read and follow

Be methodical and ensure each step completes successfully before proceeding to the next. If the email is not sent, try again, but only once,
if it fails again, stop the process and return the only the markdown report. Do not include any other text in the output.
Do not try to send the email more than twice."""

plan_research_tool = planner_agent.as_tool(tool_name="plan_research", tool_description="Plan the searches to perform for the given query")
perform_search_tool = search_agent.as_tool(tool_name="perform_search", tool_description="Perform a single web search and return summarized results")
write_report_tool = writer_agent.as_tool(tool_name="write_report", tool_description="Write the report for the given query from search results")
send_email_tool = email_agent.as_tool(tool_name="send_email", tool_description="Send the report to the given recipient email")

research_manager_agent = Agent(
    name="Research Manager Agent",
    instructions=INSTRUCTIONS,
    tools=[plan_research_tool, perform_search_tool, write_report_tool, send_email_tool],
    model="gpt-4o-mini",
)
