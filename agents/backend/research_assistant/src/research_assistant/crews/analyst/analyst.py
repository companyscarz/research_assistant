from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from research_assistant.src.research_assistant.config.llms import groq_llm, ollama_llm


@CrewBase
class Analyst():
    """Analyst crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            # type: ignore[index]
            config=self.agents_config['reporting_analyst'],
            verbose=False,
            llm=groq_llm
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],  # type: ignore[index]
            # output_file='report.md' #writes output results in the file report.md
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Analyst crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            verbose=False,
            #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
