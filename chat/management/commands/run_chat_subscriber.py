import asyncio
from django.core.management.base import BaseCommand
from chat.service.subscriber import main

class Command(BaseCommand):
    help = 'Starts the whatsapp chat subsriber service'

    async def handle_async(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Starting websocket subscriber service...'
            ))

        await main()

    def handle(self, *args, **options):
        asyncio.run(self.handle_async(*args, **options))
