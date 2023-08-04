class MessageTemplateError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path


class NotDefinedKeyboardType(MessageTemplateError):
    pass


class NotDefinedTemplate(MessageTemplateError):
    pass
