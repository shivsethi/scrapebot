from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1144998338102558841/wm0ou_l3XNoS6lzWElMiaQn_s8dI1MqDSv9VBR7U7q7mJ_MT97LYAQBZZIHqa4gUvfnT"
webhook = DiscordWebhook(url=WEBHOOK_URL)

# get current date
now = datetime.now()
today_date = now.strftime("%d/%m/%Y")

embed = DiscordEmbed(title="**Forex Calendar News**", description= ':red_circle:' " **High Impact News** - " + today_date, color="0080ff")
#embed.set_author(name="Shiv")
#embed.set_footer(text="Date:")
webhook.add_embed(embed)

def check_time(s):
    return any(i == ":" for i in s)

driver = webdriver.Chrome()
first = 0

try:
    driver.get("https://www.forexfactory.com/")
    # Get the table
    data_table = driver.find_element(By.CLASS_NAME, "calendar__table")
    value_list = []

    # loop each row in calendar table
    for row in data_table.find_elements(By.CSS_SELECTOR, "tr.calendar__row"):
        #print (first)
        # Find the prev time element
        find_time = row.find_element(By.XPATH, "//td[@class='calendar__cell calendar__time']/div/span[not(@class)]")
        time_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
        first += 1
        # find time in row
        for i in time_data:
                if ":" in i:
                    #print (i)
                    # save time to variable
                    prev_time = i


        
        # Find the high impact red folder tag in row
        try:
            find_impact = row.find_element(By.XPATH, ".//span[@title='High Impact Expected']")
            #print("This is a high impact event")
            row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
            #print(row_data)
            print(first)
            #add rows to list
            if row_data:
                for i in row_data:
                    if (i == 'USD'):
                        if (check_time(row_data[0])):
                            embed.add_embed_field(name="\a" , value=f'**Time: **{row_data[0]} \n**Event: **{row_data[2]} \n**Currency: **{row_data[1]}' " :dollar:", inline=False)
                        else:
                            embed.add_embed_field(name="\a" , value=f'**Time: ** {prev_time} \n**Event: **{row_data[1]} \n**Currency: **{row_data[0]}' " :dollar:", inline=False)                
            
                    elif (i == 'GBP'):
                        if (check_time(row_data[0])):
                            embed.add_embed_field(name="\a" , value=f'**Time: **{row_data[0]} \n**Event: **{row_data[2]} \n**Currency: **{row_data[1]}' " :pound:", inline=False)
                        else:
                            if (first == 1):
                                embed.add_embed_field(name="\a" , value=f'**Time: ** {row_data[1]} \n**Event: **{row_data[3]} \n**Currency: **{row_data[2]}' " :pound:", inline=False)
                            else:
                                embed.add_embed_field(name="\a" , value=f'**Time: ** {prev_time} \n**Event: **{row_data[1]} \n**Currency: **{row_data[0]}' " :pound:", inline=False)                

            else:
                ""

        except:
            ""
            #print("The div element does not exist in this row.")
        




finally:
    embed.set_footer(text = "Timezone: GMT(+0) | EST(-5)")
    driver.quit()

response = webhook.execute()