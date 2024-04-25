#Check initilization.py for dependencies and file initilization

#Modal form creation to send to user for Voting Group Creation
class create_group(ui.Modal, title = 'Voting Group Creation'):
    def __init__(self,matches):
        super().__init__()
        self.matches = matches
        
    name = ui.TextInput(label='Voting Group name')
    creators = ui.TextInput(label='Creator wallet list:', style=discord.TextStyle.paragraph)
    excluded = ui.TextInput(label='Excluded ContractIds:', style=discord.TextStyle.paragraph)
    requirements = ui.TextInput(label='Proposal Requirements:', style=discord.TextStyle.paragraph)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral = True, thinking= True)
        result = str(interaction.user.id)
        user = str(interaction.user.name)
        try:
            name = str(self.name)
            creators = str(self.creators)
            creator_keys = json.loads(creators).keys()
            
            if set(creator_keys).issubset(self.matches):
                excluded = str(self.excluded)
                requirements = str(self.requirements)
                server_id = interaction.guild_id
                guild = bot.get_guild(server_id)
                server_name = guild.name
                result = str(interaction.user.id)
                
                mod = False
                reply = check_format(name, creators, excluded,requirements,server_id,server_name, user,mod)
                await interaction.followup.send(f"{reply}", ephemeral=True)
            
            else:
                await interaction.followup.send(f"All creator wallets inputted are not verified with {user} ", ephemeral=True)
        
        except Exception as e:
            traceback.print_exc()
            logger.error(f"create_group class: {e}")

#Buttons used to view instructions for creating the Voting Groups and proceeding with creation
class ynview(discord.ui.View):  
    def __init__(self,matches):
        super().__init__()
        self.matches = matches
    
    @discord.ui.button(label="Instructions",
                       style=discord.ButtonStyle.grey)
    
    async def ins(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        await interaction.response.defer(ephemeral = True, thinking= True)
        await interaction.followup.send(f"```{instructions}```")
        
    
    @discord.ui.button(label="Yes",
                        style=discord.ButtonStyle.success)
    
    async def yes(self,interaction:discord.Interaction, button:discord.ui.Button):
        self.clear_items()
        modal = create_group(self.matches)
        await interaction.response.send_modal(modal)
        
#Slash command users execute to start Voting Group creation
@tree.command(name='vb_create', description = 'Create a Voting Group, must have registered a creator wallet using /register')
async def group(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral = True, thinking= True)
        result = str(interaction.user.id)
        user = str(interaction.user.name)
        if result in user_database:
            addies = user_database[result]['address']
            matching_addresses = addies
          
            if matching_addresses:
                await interaction.followup.send(f"{user} can create Voting Groups with {matching_addresses}", ephemeral=True)
                view = ynview(matching_addresses)
                await interaction.followup.send("Do you want to proceed with Voting Group creation?", ephemeral=True, view=view)
            else:
                await interaction.followup.send("Something went wrong", ephemeral=True)
                
        else:
            await interaction.followup.send(f"{user} not in database, please run /register to get started", ephemeral=True)
            
    except Exception as e:
        traceback.print_exc()
        logger.error(f"create_group: {e}")
        await interaction.followup.send("An error occured please try again.", ephemeral=True)
