class Memory:

    def __init__(self):

        self.messages = []

    def add_message(self, role, content):

        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):

        return self.messages

    def clear_memory(self):

        self.messages = []

    def limit_memory(self, max_length=20):

        if len(self.messages) > max_length:

            self.messages = self.messages[-max_length:]