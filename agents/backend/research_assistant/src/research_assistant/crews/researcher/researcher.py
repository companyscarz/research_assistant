from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from research_assistant.src.research_assistant.config.llms import groq_llm, ollama_llm


@CrewBase
class Researcher_crew():
    """Researcher crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            # type: ignore[index]
            config=self.agents_config['researcher_agent'],
            verbose=False,
            llm=groq_llm,
            #tools=[web_search_tool]
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Researcher crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            verbose=False,
            #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
