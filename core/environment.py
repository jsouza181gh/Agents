from core.action import Action

import traceback
import time

class Environment:
    def execute_action(self, action: Action | None, args: dict):
        if action is None:
            return {
                "tool_executed": False,
                "error": "Unknown tool: no registered action matches this tool call."
            }

        try:
            result = action.execute(**args)
            return self.format_result(result)

        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }


    @staticmethod
    def format_result(result):
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }