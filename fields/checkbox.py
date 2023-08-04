from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


           # case AfterHandling.CHECKBOXES:
            #     inline_keyboard = callback.message.reply_markup.inline_keyboard

            #     for i in range(len(inline_keyboard)):
            #         for j in range(len(inline_keyboard[i])):
            #             if inline_keyboard[i][j].callback_data == callback.data:
            #                 if not "✅" in inline_keyboard[i][j].text:
            #                     inline_keyboard[i][j].text += " ✅"
            #                     await callback.message.edit_reply_markup(
            #                     reply_markup=InlineKeyboardBuilder(inline_keyboard).as_markup())
            #                     return

from constructor.blocks.handled import CallbackHandledBlock


class CheckboxBlock(CallbackHandledBlock):
    CONFIRM = 'confirm'
    OTHER = 'other'
    SELECTED = '✅'

    def __init__(self, name):
        super().__init__(name)

    async def apply_transformation(self, callback: CallbackQuery):
        if callback.data not in [self.CONFIRM, self.OTHER]:

            inline_keyboard = callback.message.reply_markup.inline_keyboard
        
            for i in range(len(inline_keyboard)):
                for j in range(len(inline_keyboard[i])):

                    if inline_keyboard[i][j].callback_data == callback.data:

                        if self.SELECTED in inline_keyboard[i][j].text:
                            inline_keyboard[i][j].text = inline_keyboard[i][j].text.replace(self.SELECTED, "")
                        else:
                            inline_keyboard[i][j].text += self.SELECTED

                        await callback.message.edit_reply_markup(
                            reply_markup=InlineKeyboardBuilder(inline_keyboard).as_markup())
                        return