from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from research_assistant.src.research_assistant.crews.researcher.researcher import Researcher_crew
from research_assistant.src.research_assistant.crews.analyst.analyst import Analyst
from research_assistant.src.research_assistant.crews.writer.writer import Writer
from research_assistant.src.research_assistant.crews.presenter.presenter import Presenter


#------------------------------------------------------------------------------------------------
class ResearchAssistant_state(BaseModel):
    topic: str = ""
    research_results: str = ""
    analysed_results: str = ""
    long_essy: str = ""
    summarised_essy: str = ""


class Research_assistant(Flow[ResearchAssistant_state]):
    @start()
    def make_research(self):
        # get the topic to search about store in state and pass it as variable to agent
        # return list of facts about this topic
        crew = Researcher_crew().crew()
        inputs = {
            "topic": self.state.topic,  # save the topic in the general state storage
        }
        result = crew.kickoff(inputs=inputs)  # kick off this agent
        self.state.research_results = result.raw  # get the raw content from the agent
        return "research on topic is done"  # return to be listened by other agents

    @listen("research on topic is done")
    def analyse_research(self):
        # look after making research analyse the list of content returned from researcher agent
        # return analysed data about and save it in state
        crew = Analyst().crew()
        inputs = {
            "content_to_be_analysed": self.state.research_results,
        }
        result = crew.kickoff(inputs=inputs)
        self.state.analysed_results = result.raw
        return "researched results analysed"

    @listen("researched results analysed")
    def write_essy(self):
        # write an essy about the analysed content,
        crew = Writer().crew()
        inputs = {
            "essy_content": self.state.analysed_results,
            "topic": self.state.topic,
            "current_year": "2026"  # Pass the year here
        }
        result = crew.kickoff(inputs=inputs)
        self.state.long_essy = result.raw
        return "done writing essy"

    @listen("done writing essy")
    def summarise_essy(self):
        # summarise the content from writer agent correct any grammar or spelling mitakes
        crew = Presenter().crew()
        inputs = {
            "essy_content": self.state.long_essy,
        }
        short_essy = crew.kickoff(inputs=inputs)
        self.state.summarised_essy = short_essy.raw
        text_results = self.state.summarised_essy
        #return text_results


def research_on(topic):
    flow = Research_assistant()
    flow.state.topic = topic
    flow.kickoff()
    return flow.state.dict()

    
def plot():
    research_assistant_flow = Research_assistant()
    research_assistant_flow.plot()


#Research_assistant().plot()
#if __name__ == "__main__":
#    research_on("museveni")
