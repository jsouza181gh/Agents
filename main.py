from agents.readme_agent import ReadmeAgent

import logging

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL + 1)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(asctime)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("logs/application.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    readme_agent = ReadmeAgent()
    readme_agent.run()