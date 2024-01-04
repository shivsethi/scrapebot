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

embed = DiscordEmbed(title="Forex Calendar News", description= ':red_circle:' " **High Impact News** - " + today_date, color="0080ff")
#embed.set_author(name="Shiv")
#embed.set_footer(text="Date:")
webhook.add_embed(embed)


driver = webdriver.Chrome()

try:
    driver.get("https://www.forexfactory.com/")
    # Get the table
    data_table = driver.find_element(By.CLASS_NAME, "calendar__table")
    value_list = []

    # loop each row in calendar table
    for row in data_table.find_elements(By.CSS_SELECTOR, "tr.calendar__row"):
        # Find the high impact red folder tag in row
        try:
            find_impact = row.find_element(By.XPATH, ".//span[@title='High Impact Expected']")
            #print("This is a high impact event")
            row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
            #add rows to list
            if row_data:
                value_list.append(row_data)

        except:
            ""
            #print("The div element does not exist in this row.")
        

    #print(value_list)

    for value in value_list:
        found = 0
        for i in value:
            if (i == 'USD') or (i == 'GBP'):
                found = 1
        
        if found == 1:
            embed.add_embed_field(name="Time" ':hourglass:' , value=f'{value[0]}', inline=True)
            embed.add_embed_field(name="Event", value=f'{value[2]}', inline=True)
            
            if(value[1] == 'USD'):
                embed.add_embed_field(name="Currency", value=f'{value[1]}' " :dollar:", inline=True)
            else:
                embed.add_embed_field(name="Currency", value=f'{value[1]}' " :pound:", inline=True)


finally:
    #embed.set_footer(text = today_date)
    driver.quit()

response = webhook.execute()