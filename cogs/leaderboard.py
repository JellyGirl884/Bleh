import discord
from discord.ext import commands
from discord import app_commands
from database import add_or_update_points, get_leaderboard, reset_leaderboard

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="leaderboard", description="View the leaderboard")
    @app_commands.describe(limit="Number of top players to show (default: 10)")
    async def leaderboard(self, interaction: discord.Interaction, limit: int = 10):
        """Display the leaderboard"""
        try:
            # Fetch leaderboard data
            leaderboard_data = get_leaderboard(limit)
            
            if not leaderboard_data:
                embed = discord.Embed(
                    title="📊 Leaderboard",
                    description="No users on the leaderboard yet!",
                    color=discord.Color.gold()
                )
                await interaction.response.send_message(embed=embed)
                return
            
            # Create leaderboard embed
            embed = discord.Embed(
                title="📊 Leaderboard",
                description="Top players by points",
                color=discord.Color.gold()
            )
            
            for rank, (user_id, username, points) in enumerate(leaderboard_data, 1):
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                embed.add_field(
                    name=f"{medal} {username}",
                    value=f"**{points}** points",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error fetching leaderboard: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="give-points", description="Give points to a member (Admin only)")
    @app_commands.describe(
        member="The member to give points to",
        points="Number of points to give"
    )
    async def give_points(self, interaction: discord.Interaction, member: discord.Member, points: int):
        """Add points to a member (Admin only)"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command!",
                ephemeral=True
            )
            return
        
        if points <= 0:
            await interaction.response.send_message(
                "❌ Points must be greater than 0!",
                ephemeral=True
            )
            return
        
        try:
            add_or_update_points(member.id, member.name, points)
            embed = discord.Embed(
                title="✅ Points Added",
                description=f"Added **{points}** points to {member.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error adding points: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="remove-points", description="Remove points from a member (Admin only)")
    @app_commands.describe(
        member="The member to remove points from",
        points="Number of points to remove"
    )
    async def remove_points(self, interaction: discord.Interaction, member: discord.Member, points: int):
        """Remove points from a member (Admin only)"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command!",
                ephemeral=True
            )
            return
        
        if points <= 0:
            await interaction.response.send_message(
                "❌ Points must be greater than 0!",
                ephemeral=True
            )
            return
        
        try:
            add_or_update_points(member.id, member.name, -points)
            embed = discord.Embed(
                title="✅ Points Removed",
                description=f"Removed **{points}** points from {member.mention}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error removing points: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="reset-leaderboard", description="Reset the entire leaderboard (Admin only)")
    async def reset_leaderboard_cmd(self, interaction: discord.Interaction):
        """Reset all leaderboard data (Admin only)"""
        # Check if user is admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You must be an administrator to use this command!",
                ephemeral=True
            )
            return
        
        # Confirmation view
        class ConfirmView(discord.ui.View):
            def __init__(self, cog):
                super().__init__()
                self.cog = cog
                self.result = None
            
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
            async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                try:
                    reset_leaderboard()
                    embed = discord.Embed(
                        title="✅ Leaderboard Reset",
                        description="The entire leaderboard has been reset!",
                        color=discord.Color.green()
                    )
                    await button_interaction.response.send_message(embed=embed)
                    self.result = True
                    self.stop()
                except Exception as e:
                    await button_interaction.response.send_message(f"Error resetting leaderboard: {str(e)}", ephemeral=True)
            
            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
            async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                embed = discord.Embed(
                    title="❌ Cancelled",
                    description="Leaderboard reset cancelled.",
                    color=discord.Color.red()
                )
                await button_interaction.response.send_message(embed=embed, ephemeral=True)
                self.result = False
                self.stop()
        
        view = ConfirmView(self)
        embed = discord.Embed(
            title="⚠️ Confirm Reset",
            description="Are you sure you want to reset the entire leaderboard? This action cannot be undone!",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))
