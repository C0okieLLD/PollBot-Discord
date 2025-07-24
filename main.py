import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


class PollView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.votes = {"Option 1": 0, "Option 2": 0, "Option 3": 0}
        self.ended = False

    @discord.ui.button(label="Option 1", style=discord.ButtonStyle.primary)
    async def option1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ended:
            await interaction.response.send_message("Poll has ended", ephemeral=True)
            return
        self.votes["Option 1"] += 1
        await interaction.response.send_message("Your vote has been counted for Option 1", ephemeral=True)

    @discord.ui.button(label="Option 2", style=discord.ButtonStyle.primary)
    async def option2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ended:
            await interaction.response.send_message("Poll has ended", ephemeral=True)
            return
        self.votes["Option 2"] += 1
        await interaction.response.send_message("Your vote has been counted for Option 2", ephemeral=True)

    @discord.ui.button(label="Option 3", style=discord.ButtonStyle.primary)
    async def option3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ended:
            await interaction.response.send_message("Poll has ended", ephemeral=True)
            return
        self.votes["Option 3"] += 1
        await interaction.response.send_message("Your vote has been counted for Option 3", ephemeral=True)

    @discord.ui.button(label="End Poll", style=discord.ButtonStyle.danger)
    async def end_poll(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Only moderators can end the poll.", ephemeral=True)
            return

        self.ended = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            f"**📊 Poll Ended! Results:**\n"
            f"Option 1: {self.votes['Option 1']} votes\n"
            f"Option 2: {self.votes['Option 2']} votes\n"
            f"Option 3: {self.votes['Option 3']} votes"
        )


@bot.tree.command(name="poll", description="Make a poll with 3 options")
async def poll_command(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str):
    embed = discord.Embed(title="📊 New Poll!", description=question, color=discord.Color.blurple())
    embed.add_field(name="Option 1", value=option1, inline=False)
    embed.add_field(name="Option 2", value=option2, inline=False)
    embed.add_field(name="Option 3", value=option3, inline=False)

    view = PollView()
    await interaction.response.send_message(embed=embed, view=view)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()


bot.run('YOUR_BOT_TOKEN_HERE')
