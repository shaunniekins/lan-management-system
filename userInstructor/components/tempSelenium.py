from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_browser_content(link):
    # Set up the browser options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # To run the browser in the background
    
    # Create an instance of the Chrome browser
    browser = webdriver.Chrome(options=chrome_options)
    
    # Open the link in the browser
    browser.get(link)
    
    # Get the content of the browser
    content = browser.page_source
    
    # Close the browser
    browser.quit()
    
    # Return the content
    return content

# Create the GUI
root = Tk()

# Create a frame to display the browser content
browser_frame = Frame(root)
browser_frame.pack(fill=BOTH, expand=1)

# Create a button to get the content of the link
button = Button(root, text='Get Content', command=lambda: show_content(link_entry.get()))
button.pack()

# Create an entry to input the link
link_entry = Entry(root)
link_entry.pack()

# Function to show the content in the frame
def show_content(link):
    content = get_browser_content(link)
    browser_text = Text(browser_frame)
    browser_text.pack(fill=BOTH, expand=1)
    browser_text.insert(END, content)

# Run the GUI
root.mainloop()