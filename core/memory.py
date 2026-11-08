from dataclasses import dataclass, field

@dataclass
class Memory:
    items: list = field(default_factory=list)

    def add_memory(self, memory: dict):
        self.items.append(memory)


    def get_memories(self, limit: int | None = None):
        return self.items[:limit]


    def copy_without_system_memories(self):
        filterd_memories = [
            memory
            for memory in self.items
            if memory["role"] != "system"
        ]

        memory = Memory()
        memory.items = filterd_memories

        return memory