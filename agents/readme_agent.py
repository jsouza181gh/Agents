from core.language import GAMEFrameworkLanguage
from core.action import ActionRegistry
from core.environment import Environment
from services.llm.service import LLMService
from core.memory import Memory
from core.agent import Agent
from core.goal import Goal
from agents import tools

from dataclasses import dataclass, field, replace
import logging
import os

@dataclass
class ReadmeAgent:
    llm: LLMService = field(default_factory=LLMService)
    agent_language: GAMEFrameworkLanguage = field(default_factory=GAMEFrameworkLanguage)
    environment: Environment = field(default_factory=Environment)
    listed_files: set[str] = field(default_factory=set, init=False)
    read_files: set[str] = field(default_factory=set, init=False)
    logger = logging.getLogger(__name__)

    def tracked_list_project_files(self) -> list[str]:
        files = tools.list_project_files()
        self.listed_files = set(files)

        return files


    def tracked_read_project_file(self, name: str) -> str:
        content = tools.read_project_file(name)
        self.read_files.add(os.path.normpath(name))

        return content


    def guarded_write_project_file(self, name: str, content: str) -> str:
        if not self.listed_files:
            raise RuntimeError("Cannot write yet: call list_project_files first.")

        pending = sorted(self.listed_files - self.read_files)
        if pending:
            raise RuntimeError(f"Cannot write yet: these files have not been read: {pending}")

        return tools.write_project_file(name, content)


    def build_goals(self) -> list[Goal]:
        return [
            Goal(priority=1, name="Gather Information", description="Call list_project_files, then read EVERY file it returns, "
                                                                    "one by one, using read_project_file. Do not skip any file"),
            Goal(priority=1, name="Write README", description="Only after you have read all the files, write the content of the README "
                                                              "to a file named README.md using the write_project_file tool. "
                                                              "The write is refused while any listed file is still unread"),
            Goal(priority=1, name="Terminate", description="Call the terminate call after README.md has been written "
                                                            "and provide a short confirmation in the terminate message")
        ]


    def build_actions(self) -> ActionRegistry:
        action_registry = ActionRegistry(tags=["file_operations", "system"])

        for name, function in {
            "list_project_files": self.tracked_list_project_files,
            "read_project_file": self.tracked_read_project_file,
            "write_project_file": self.guarded_write_project_file,
        }.items():
            action_registry.register(replace(action_registry.actions[name], function=function))

        return action_registry


    def build_agent(self) -> Agent:
        return Agent(
            goals=self.build_goals(),
            agent_language=self.agent_language,
            actions=self.build_actions(),
            generate_response=self.llm.generate_response,
            environment=self.environment
        )


    def run(self, user_input: str = "Write a README for this project.") -> Memory:
        self.listed_files = set()
        self.read_files = set()

        agent = self.build_agent()
        final_memory = agent.run(user_input)

        self.logger.debug("Final memory: %s", final_memory.get_memories())

        return final_memory
