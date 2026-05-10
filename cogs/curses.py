import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
from database import add_curse, get_active_curses, expire_curses, remove_all_curses
from curses import CURSE_TYPES, apply_curse, generate_math_problem, get_curse_description

class CursesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.math_curse_problems = {}  # {user_id: (problem, answer)}
        self.expire_curses_loop.start()
    
    @tasks.loop(minutes=1)
    async def expire_curses_loop(self):
        """Periodically check for expired curses"""
        pass  # Database handles expiration with timestamp
    
    @expire_curses_loop.before_loop
    async def before_expire_curses_loop(self):
        await self.bot.wait_until_ready()
    
    @app_commands.command(name="curse", description="Apply a curse to a member (Admin only)")
    @app_commands.describe(
        member="The member to curse",
        curse_type="Type of curse to apply",
        hours="Duration in hours"
    )
    async def curse(self, interaction: discord.Interaction, member: discord.Member, curse_type: str, hours: int):
        """Apply a curse to a member (Admin only)"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command!",
                ephemeral=True
            )
            return
        
        # Validate curse type
        if curse_type not in CURSE_TYPES:
            curse_list = ", ".join(CURSE_TYPES)
            await interaction.response.send_message(
                f"❌ Invalid curse type! Available curses:\n{curse_list}",
                ephemeral=True
            )
            return
        
        if hours <= 0:
            await interaction.response.send_message(
                "❌ Hours must be greater than 0!",
                ephemeral=True
            )
            return
        
        try:
            # Calculate expiration time
            expires_at = datetime.utcnow() + timedelta(hours=hours)
            
            # Add curse to database
            add_curse(member.id, curse_type, expires_at.isoformat())
            
            # If math curse, generate first problem
            if curse_type == "math_curse":
                problem, answer = generate_math_problem()
                self.math_curse_problems[member.id] = (problem, answer)
                # Send initial problem
                await interaction.response.send_message(
                    f"🔥 Curse applied! {member.mention}, your first problem: **{problem}**",
                    ephemeral=False
                )
            else:
                embed = discord.Embed(
                    title="🔥 Curse Applied",
                    description=f"Applied **{curse_type}** to {member.mention} for **{hours}** hours",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="Effect",
                    value=get_curse_description(curse_type),
                    inline=False
                )
                embed.set_footer(text=f"Expires at {expires_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error applying curse: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="curses", description="View active curses on a member")
    @app_commands.describe(member="The member to check")
    async def curses(self, interaction: discord.Interaction, member: discord.Member):
        """View active curses on a member"""
        try:
            expire_curses(member.id)
            active_curses = get_active_curses(member.id)
            
            if not active_curses:
                embed = discord.Embed(
                    title="✨ No Active Curses",
                    description=f"{member.mention} is curse-free!",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = discord.Embed(
                title="🔥 Active Curses",
                description=f"Curses affecting {member.mention}",
                color=discord.Color.red()
            )
            
            for curse_id, curse_type, expires_at in active_curses:
                expires_dt = datetime.fromisoformat(expires_at)
                time_remaining = (expires_dt - datetime.utcnow()).total_seconds() / 3600
                
                embed.add_field(
                    name=f"🔗 {curse_type}",
                    value=f"Expires in {time_remaining:.1f} hours\n{get_curse_description(curse_type)}",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error fetching curses: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="lift-curse", description="Remove all curses from a member (Admin only)")
    @app_commands.describe(member="The member to remove curses from")
    async def lift_curse(self, interaction: discord.Interaction, member: discord.Member):
        """Remove all curses from a member (Admin only)"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command!",
                ephemeral=True
            )
            return
        
        try:
            remove_all_curses(member.id)
            
            # Remove math curse problem if exists
            if member.id in self.math_curse_problems:
                del self.math_curse_problems[member.id]
            
            embed = discord.Embed(
                title="✨ Curses Lifted",
                description=f"All curses have been lifted from {member.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error lifting curses: {str(e)}", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Intercept messages to apply curse effects"""
        if message.author.bot:
            return
        
        try:
            # Check for active curses
            expire_curses(message.author.id)
            active_curses = get_active_curses(message.author.id)
            
            if not active_curses:
                return
            
            # Apply curse effects
            for curse_id, curse_type, expires_at in active_curses:
                if curse_type == "math_curse":
                    # Generate new problem if doesn't exist
                    if message.author.id not in self.math_curse_problems:
                        problem, answer = generate_math_problem()
                        self.math_curse_problems[message.author.id] = (problem, answer)
                    
                    problem, answer = self.math_curse_problems[message.author.id]
                    
                    # Check if message is an answer
                    try:
                        user_answer = int(message.content.strip())
                        if user_answer == answer:
                            # Correct answer - delete message and send success
                            await message.delete()
                            await message.channel.send(
                                f"✅ {message.author.mention} got it right! Answer was {answer}."
                            )
                            
                            # Generate new problem
                            problem, answer = generate_math_problem()
                            self.math_curse_problems[message.author.id] = (problem, answer)
                            
                            # Ask new problem
                            await message.channel.send(
                                f"🔢 {message.author.mention}, next problem: **{problem}**"
                            )
                            return
                        else:
                            # Wrong answer - delete and ask again
                            await message.delete()
                            await message.channel.send(
                                f"❌ {message.author.mention} got it wrong! Try again: **{problem}**"
                            )
                            return
                    except ValueError:
                        # Not a number - delete and ask for answer
                        await message.delete()
                        await message.channel.send(
                            f"❓ {message.author.mention}, solve this: **{problem}**"
                        )
                        return
                else:
                    # Apply curse effect to message
                    cursed_text = apply_curse(message.content, curse_type)
                    
                    # Delete original message
                    await message.delete()
                    
                    # Send cursed message
                    await message.channel.send(
                        f"**{message.author.name}**: {cursed_text}"
                    )
                    return
        
        except Exception as e:
            print(f"Error in curse message handler: {str(e)}")

async def setup(bot):
    await bot.add_cog(CursesCog(bot))
