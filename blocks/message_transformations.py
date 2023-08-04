from ..data import Data
from .serial import SerialBlock


class MessageTransformationBlock(SerialBlock):
    pass


class RIKBlock(MessageTransformationBlock):
    """
        Remove inline keyboard.
    """
    async def __call__(self, data: Data):
        await data.callback.message.edit_text(data.callback.message.text)
        await SerialBlock.__call__(self, data)


class RMBlock(MessageTransformationBlock):
    """
        Remove message.
    """
    async def __call__(self, data: Data):
        await data.callback.message.delete()
        await SerialBlock.__call__(self, data)


class RIKMBTBlock(MessageTransformationBlock):
    """
        Remove inline keyboard.
        Move pressed button text to the end of message.
    """
    async def __call__(self, data: Data):
        inline_keyboard = data.callback.message.reply_markup.inline_keyboard

        for i in range(len(inline_keyboard)):
            for j in range(len(inline_keyboard[i])):
                inline_keyboard_button = inline_keyboard[i][j]

                if inline_keyboard_button.callback_data == data.callback.data:
                    adding_text = inline_keyboard_button.text
                    text = data.callback.message.text + '\n' + adding_text
                    await data.callback.message.edit_text(text)
                    
                    await SerialBlock.__call__(self, data)
                    return
        
        await SerialBlock.__call__(self, data)
                

