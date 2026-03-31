from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from research_assistant.src.research_assistant.config.llms import groq_llm, ollama_llm


@CrewBase
class Presenter():
    """Presenter crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def presenter(self) -> Agent:
        return Agent(
            config=self.agents_config['presenter'],  # type: ignore[index]
            verbose=False,
            llm=groq_llm
        )

    @task
    def present_task(self) -> Task:
        return Task(
            config=self.tasks_config['present_task'],  # type: ignore[index]
            # output_file='report.md' #writes output results in the file report.md
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Presenter crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            verbose=False,
            #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
