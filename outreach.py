import pyautogui
import time

init = [
    “Hey there! How are you doing today?”,
    “Hi! Hope you’re having a great day!”,
    “Hello! How’s it going?”,
    “Hi! How are things with you?”,
    “Hey! How’s your day been?”,
    “Good morning! How are you?”,
    “Hi there! How are things on your end?”,
    “Hello! What’s up?”,
    “Hey! How’s your day treating you?”,
    “Hi! How’s everything going?”,
    “Good afternoon! How have you been?”,
    “Hello! How’s it going for you today?”,
    “Hi! How’s your day shaping up?”,
    “Hey there! How’s your day been so far?”,
    “Hi! Hope your day is going well!”,
    “Hello! How’s everything with you?”,
    “Hi! How are you feeling today?”,
    “Hey! How have you been?”,
    “Hello! How’s your day progressing?”,
    “Hi! How’s it going for you?”
]


follow1 = [
    "Hi again! Just wanted to introduce myself properly. I’m Peyton Hassan, an indie artist, and I create unique die-cut stickers. Would you be interested in checking them out?",
    "Hey! Following up from yesterday. I wanted to share that I design fun and whimsical die-cut stickers. Let me know if you’d like to see them!",
    "Hello again! I realized I didn’t mention this yesterday—I’m an indie artist and I make custom die-cut stickers. Would you like to see some of my designs?",
    "Hi there! I forgot to tell you yesterday that I create unique die-cut stickers. Are you interested in seeing some of my work?",
    "Hey! Just wanted to let you know that I design original die-cut stickers. If you’re interested, I’d love to share some of my designs with you.",
]


follow2 = [
    "Hi again! Just checking in to see if you had a chance to look at my sticker designs. I'd love to hear your thoughts!",
    "Hey! Following up to see if you’ve had a moment to check out my die-cut stickers. Any feedback would be awesome!",
    "Hello! Did you get a chance to look at my art? I'd love to know what you think of the stickers.",
    "Hi there! Just a quick follow-up to see if my sticker collection caught your eye. Any thoughts?",
    "Hey! Just a reminder about my die-cut stickers. I'd love to hear your feedback if you had a chance to look at them.",
]



import json
import random
from datetime import datetime, timedelta
import schedule
import time

# Load slugs from JSON file
with open('slugs.json', 'r') as f:
    slugs = json.load(f)

# Select 20 slugs with the lowest contact values randomly
sorted_slugs = sorted(slugs.items(), key=lambda x: x[1])
lowest_20_slugs = sorted_slugs[:20]

# Randomize the selected 20 slugs
random.shuffle(lowest_20_slugs)

# Generate random time between 6 AM and 12 PM
def generate_random_time():
    start_time = datetime.strptime('06:00', '%H:%M')
    end_time = datetime.strptime('12:00', '%H:%M')
    delta = end_time - start_time
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start_time + timedelta(seconds=random_seconds)).time()

n = slugs[slug]
if n == 0:
    return random.choice(init)
elif n == 1:
    return random.choice(follow1)
elif n == 2:
    return random.choice(follow2)


# Schedule messages and increment contact count
def schedule_messages(slugs):
    for slug, _ in slugs:
        #message_time = generate_random_time()
        message = generate_contact_message(slug)
        
        # Schedule the message
        schedule_time = datetime.combine(datetime.today(), message_time)
        schedule.every().day.at(schedule_time.strftime('%H:%M')).do(send_message, slug, message)
        
        # Increment the contact count
        slugs[slug] += 1

        print(f"Scheduled message for {slug} at {message_time}: {message}")

# Update the JSON file with the new contact counts
def update_json_file(slugs):
    with open('slugs.json', 'w') as f:
        json.dump(slugs, f, indent=4)

# Schedule the messages
schedule_messages(dict(lowest_20_slugs))

# Update the JSON file with incremented contact counts
update_json_file(slugs)

# Keep the script running to process scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)




def automate_task(slug, msg):
    # Move to (300, 300) and click
    pyautogui.moveTo(300, 300, duration=0.5)
    pyautogui.click()
    
    # Move to (670, 130) and click
    pyautogui.moveTo(670, 130, duration=0.5)
    pyautogui.click()
    
    # Type the first string and press Enter
    pyautogui.typewrite(slug, interval=0.1)
    pyautogui.press('enter')
    
    # Type the second string and press Enter
    pyautogui.typewrite(msg, interval=0.1)
    pyautogui.press('enter')
    
    # Wait for 30 minutes (1800 seconds)
    time.sleep(1800)

# Main loop to repeat the task
while True:
    slug =  
    msg = 
    automate_task(slug, msg)