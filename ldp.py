from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import datetime
from mongodb_model import MongoDB  # Import the MongoDB model

# Encode the username and password
username = "cypsolabs"
password = "@testing01"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Construct the MongoDB URI
MONGO_URI = f"mongodb+srv://{encoded_username}:{encoded_password}@byner.vxp0o.mongodb.net/?retryWrites=true&w=majority&appName=byner"

# MongoDB configuration
DB_NAME = "testdb"
COLLECTION_NAME = "newdb"
COLLECTION_NAME2 = "last_index"
COLLECTION_NAME3 = "newinput"

def generate():
    try:
        # Initialize MongoDB connection
        db = MongoDB(MONGO_URI, DB_NAME, COLLECTION_NAME)
        db2 = MongoDB(MONGO_URI, DB_NAME, COLLECTION_NAME2)
        db3 = MongoDB(MONGO_URI, DB_NAME, COLLECTION_NAME3)

        last_entry = db2.fetch_data_by_query({"last_index": {"$exists": True}})
        last_index = last_entry[0]["last_index"] if last_entry else 0

        index_counter = last_index + 1

        # Configure Selenium driver
        driver_path = r"C:\www\geckodriver.exe"
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        service = Service(driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        # Target URL
        url = "https://binarybot.live/ldp/"
        driver.get(url)

        # Set the scraping time limit (2 hours)
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(minutes=120) 

        last_scraped_time = None  
        last_number = None

        while datetime.datetime.now() < end_time:
            try:
                digits_div = driver.find_element(By.ID, "digits")
                spans = digits_div.find_elements(By.TAG_NAME, "span")

                current_time = datetime.datetime.now()
                new_number = None
                number_class = ""

                # Get the last digit from the spans
                if spans:
                    last_span = spans[-1]  # Capture only the last updated number
                    new_number = last_span.text.strip()
                    number_class = last_span.get_attribute("class")

                if new_number and new_number.isdigit():  # Ensure it's a valid digit
                    new_number = int(new_number)  # Convert to integer

                    
                    if new_number != last_number:
                        trend = None
                        if last_number is not None:
                            trend = 1 if new_number > last_number else -1  # Increase or Decrease

                        market_indicator = None
                        if last_scraped_time is None or (current_time - last_scraped_time).total_seconds() >= 10:
                            try:
                                market_condition_element = driver.find_element(By.ID, "market_condition")
                                market_indicator = market_condition_element.text.strip()
                            except Exception:
                                market_indicator = "Unknown"

                            last_scraped_time = current_time  # Update last scraped time
                            

                        # Determine number type (good, bad, neutral)
                        indicator = "neutral"
                        if "digits_moved_up" in number_class:
                            indicator = "good"
                        elif "digits_moved_down" in number_class:
                            indicator = "bad"

                        # Populate good_number, bad_number, and neutral_number
                        good_number = new_number if indicator == "good" else None
                        bad_number = new_number if indicator == "bad" else None
                        neutral_number = new_number if indicator == "neutral" else None

                        # Populate digit_up and digit_down
                        digit_up = new_number if trend == 1 else None
                        digit_down = new_number if trend == -1 else None

                        # Extract digit colors from the class attribute
                        digit_colors = number_class  # Assuming class contains color info

                        # Prepare data for MongoDB
                        scraped_data = {
                            "timestamp": current_time.isoformat(),  # Store as a string for compatibility
                            "number": new_number,
                            "index": index_counter,
                            "trend": trend,
                            "market_indicator": market_indicator,
                            "indicator": indicator,  # Good, bad, or neutral
                            "good_number": good_number,  # Number if it is good
                            "bad_number": bad_number,  # Number if it is bad
                            "neutral_number": neutral_number,  # Number if it is neutral
                            "digit_up": digit_up,  # Digit if it moved up
                            "digit_down": digit_down,  # Digit if it moved down
                            "digit_colors": digit_colors  # Color associated with the digit
                        }

                        # Insert data into MongoDB
                        db.insert_data(scraped_data)
                        db3.insert_data(scraped_data)

                        # Print/log the data for debugging
                        yield f"Scraped at {current_time}: Number={new_number}, Index={index_counter}, Trend={trend}, Indicator={indicator}, Market={market_indicator}, Good={good_number}, Bad={bad_number}, Neutral={neutral_number}, Digit Colors={digit_colors}\n"

                        # Update last recorded number and index
                        last_number = new_number
                        index_counter += 1

                # Sleep for 1 second before checking again
                time.sleep(1)

            except Exception as e:
                yield f"Error during scraping: {e}\n"
                break

        driver.quit()
        db.close_connection()

        # Save last index and last number
        try:
            if last_number is not None:
                last_entry = {
                    "last_index": index_counter - 1,
                    "last_number": last_number
                }
                db2.collection.delete_many({"last_index": {"$exists": True}})
                db2.insert_data(last_entry)

        except Exception as e:
            yield f"Error saving last index and number: {e}\n"

    except Exception as e:
        yield f"Error occurred during initialization: {e}\n"


# Example usage
if __name__ == "__main__":
    for data in generate():
        print(data)