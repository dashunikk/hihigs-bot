from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(command='start', description='Start'),
        BotCommand(command='status', description='User Information'),
        BotCommand(command='help', description='Help'),
        BotCommand(command='vmpath', description='Saving a VM'),
        BotCommand(command='check', description='Checking the connection'),
        BotCommand(command='ls', description='List directory contents'),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())