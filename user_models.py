class User(object):
    def __init__(self, chat_id, group, view_type, message_id):
        self.chat_id: int = chat_id
        self.group: str = group
        self.view_type: str = view_type
        self.message_id: int = message_id

