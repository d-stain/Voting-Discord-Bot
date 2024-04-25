#Check initilization.py for dependencies and file initilization

#Function to count and record votes per proposal number for selected voting group
def voting(voted, user, holdings, group_pick, pname):
    try:
        if voted != 'Abstain':
            des = active_proposals[group_pick][pname][voted]
        else:
            des = voted
            
        addresses = user_database[user]['address']
        apcopy = active_proposals[group_pick][pname]['results'].copy()
        s_des = active_proposals[group_pick][pname]['Proposal Description']
        
        #Skip creator wallets
        for address in addresses:
            if address in creator_database:
                continue

            merged_dict={}
            for key in group_database[group_pick]:
                if holder_database[user][address].get(key):
                    if key not in apcopy:
                        apcopy[key] = {}
                    
                    
                    for asset in holder_database[user][address][key]:
                        asset = str(asset)
                        
                        if creator_database.get(key) and creator_database[key].get(asset):
                            if creator_database[key][asset]['total_supply'] > 1:
                                if not apcopy.get(key):
                                    apcopy[key] = {}
                                if not apcopy[key].get(asset):                                   
                                    apcopy[key][asset] = {'user': [], 'voted': [], 'total': []}
                                
                                if not isinstance(apcopy[key][asset]['user'], list):
                                    apcopy[key][asset]['user'] = []
                                if not isinstance(apcopy[key][asset]['voted'], list):
                                    apcopy[key][asset]['voted'] = []
                                if not isinstance(apcopy[key][asset]['total'], list):
                                    apcopy[key][asset]['total'] = []
                                
                                if user in apcopy[key][asset]['user']:
                                    index = apcopy[key][asset]["user"].index(user)
                                    apcopy[key][asset]["voted"][index] = voted
                                    
                                else:
                                    amount = holder_database[user][address][key][asset]
                                    apcopy[key][asset]['user'].append(user)
                                    apcopy[key][asset]['voted'].append(voted)
                                    apcopy[key][asset]['total'].append(amount)
                            
                            else:
                                #need to add handling here for a single asset (WIP)
                                print("voting function: single mint/asset")

        #Combine dicts                        
        dict1 = active_proposals[group_pick][pname]['results']
        dict2 = apcopy
        merged_dict = {**dict1, **dict2}
        active_proposals[group_pick][pname]['results'].update(merged_dict)
        #save to database
        save_data_to_json(active_proposals, path_ap)
        
        return f"Voted **{des}** on **{pname}: {s_des}** of **{group_pick}** with Raw Voting Power: {holdings[group_pick]['power']} = {holdings[group_pick]['percent']}% ownership"
    
    except Exception as e:
        traceback.print_exc()
        logger.error(f"voting ({user}): {e}")

#Discord handling for selected voting group and proposal to vote on from dropdown menus
def propchoice(prop,choice,propnum, holds, og):
    try:
        now = time.time()
        timer = active_proposals[choice][propnum]['timestamp']
        days_to_add = float(active_proposals[choice][propnum]['Days'])
        future_timestamp = timer + days_to_add * 86400
        delta = abs(future_timestamp - now)
        rem = seconds_to_duration(delta)
        prop['Time remaining to vote'] = rem
        clean = convert_to_day_and_timestamp(time.time())
        clean = "_" + clean + "_"
        prop_string = '\n'.join([f"**{key}**: {value}" for key, value in prop.items() if key not in ['timestamp','Days','results']])
        prop_string += '\n\n' + clean
    
    except Exception as e:
        traceback.print_exc()
        logger.error(f"propchoice: {e}")
    
    class Vbutton(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.choice = choice
            self.embed= discord.Embed(
                title= f"**{propnum}**",
                description=f"{prop_string}",
                color=discord.Color.blue()
                )
        
        async def disable_buttons(self):
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
            
        @discord.ui.button(label="Option 1",
                            style=discord.ButtonStyle.primary)
        async def opt1(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.defer(ephemeral = True, thinking= True)
            result = str(interaction.user.id)
            await self.disable_buttons()
            value = 'Voting Option 1'
            text = voting(value, result, holds, choice, propnum)
            await og.edit(embed = self.embed, view = self)
            await interaction.followup.send(text, ephemeral=True)
            
        @discord.ui.button(label="Option 2",
                            style=discord.ButtonStyle.success)
        async def opt2(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.defer(ephemeral = True, thinking= True)
            result = str(interaction.user.id)
            await self.disable_buttons()
            value = 'Voting Option 2'
            text = voting(value, result, holds, choice, propnum)
            await og.edit(embed = self.embed, view = self)
            await interaction.followup.send(text, ephemeral=True)
            
        @discord.ui.button(label="Abstain",
                            style=discord.ButtonStyle.grey)
        async def opt4(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.defer(ephemeral = True, thinking= True)
            result = str(interaction.user.id)
            await self.disable_buttons()
            value = 'Abstain'
            text = voting(value, result, holds, choice, propnum)
            await og.edit(embed = self.embed, view = self)
            await interaction.followup.send(text, ephemeral=True)

    return Vbutton()

#Slash comamnd users execute 
@tree.command(name='vb_vote', description= 'Vote on proposals of Voting Group membership')
async def vote(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    og = await interaction.original_response()
    result = str(interaction.user.id)
    user = str(interaction.user.name)
    
    try:
        if result not in user_database:
            await interaction.response.send_message(f"**{user}** not in database, please run /register to get started",ephemeral=True)
        
        else:
            #on-chain check of users holdings
            reply, holds, votes = await check_holdings(result,user, og)
            
            await og.edit(content = "Checking holdings...")
            
            if not holds:
                await og.edit(content= f"{reply}")
        
            else:
                #cross-checks for eligible groups with Active voting proposals
                power = {}
                for keys in holds:
                    if keys in active_proposals and active_proposals[keys]:
                        power[keys] = holds[keys]
    
                if not power:
                    await og.edit(content= "No active proposals for Voting Groups you are a member in")
                
                #If active proposals exist, generate dropdown menus
                else:
                    logic = "active"
                    view = Groupchoice(power, 0, og, logic)
                    await og.edit(content= f"{truncated_reply}", view=view, embed = view.embed)
                    await view.wait()
    
    except Exception as e:
        traceback.print_exc()
        logger.error(f"vb_vote ({result}): {e}")
        await og.edit(content = "An error occured please try again.") 
        

