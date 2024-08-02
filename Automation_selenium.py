import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.1mg.com/")

try:
    update_modal = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='UpdateCityModal_update-btn_2qmN1 UpdateCityModalbtn__oMW5n']"))
    )
    update_modal.click()
    time.sleep(2)
except Exception as e:
    print("No update modal found:", e)

time.sleep(2)

search_bar = driver.find_element(By.XPATH, "//input[@id='srchBarShwInfo']")
search_bar.send_keys("Multivitamins")

search_button = driver.find_element(By.XPATH, "//div[@class='header_search_icon']")
search_button.click()

time.sleep(5)

with open('vitamins.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Brand', 'Cost', 'Rating', 'Final Rating', 'No of Tablets', 'No of Users', 'Product Highlights',
                     'Number of Product Highlights', 'Product Description', 'Number of Key Ingredients',
                     'Number of Key Benefits', 'Product Form'])

    while True:
        count = 0
        product_boxes = driver.find_elements(By.XPATH, "//div[@class='style__product-box___3oEU6']")
        for product_box in product_boxes:
            count += 1
            print(f"Processing product {count}")
            try:
                product_url = product_box.find_element(By.XPATH, ".//a").get_attribute("href")
                driver.execute_script("window.open(arguments[0], '_blank');", product_url)
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])

                brand_name = "Not available"
                cost = "Not available"
                rating = "Not available"
                final_rating = "Not available"
                tablet_count = "Not available"
                no_of_users = "Not available"
                product_highlights = "Not available"
                number_of_product_highlights = "Not available"
                product_description = "Not available"
                number_of_key_ingredients = "Not available"
                number_of_key_benefits = "Not available"
                product_form = "Not available"

                try:
                    brand_name = driver.find_element(By.XPATH, "//h1").text
                except Exception as e:
                    print("Brand name not found:", e)

                try:
                    cost = driver.find_element(By.XPATH,"//span[contains(@class, 'PriceBoxPlanOption__offer-price')]").text
                except Exception as e:
                    print("Cost not found:", e)

                try:
                    rating = driver.find_element(By.XPATH,"//span[contains(@class, 'RatingDisplay__ratings-header')]").text
                except Exception as e:
                    print("Rating not found:", e)

                try:
                    final_rating = driver.find_element(By.XPATH,
                                                       "//div[@class='RatingDisplay__ratings-container___3oUuo']").text
                except Exception as e:
                    print("Final rating not found:", e)

                try:
                    tablet_count = driver.find_element(By.XPATH,
                                                       "//span[contains(@class, 'PackSizeLabel__single-packsize')]").text
                except Exception as e:
                    print("Tablet count not found:", e)

                try:
                    no_of_users = driver.find_element(By.XPATH,
                                                      "//span[contains(@class, 'SocialCue__views-text')]").text
                except Exception as e:
                    print("Number of users not found:", e)

                try:
                    product_highlights = driver.find_element(By.XPATH,
                                                             "//div[contains(@class, 'ProductHighlights__highlights-text')]").text
                    highlights = product_highlights.split('\n')  # Assuming each highlight is on a new line
                    highlights = [highlight for highlight in highlights if
                                  highlight.strip()]  # Filter out any empty strings
                    number_of_product_highlights = len(highlights)
                except Exception as e:
                    print("Product highlights not found:", e)

                try:
                    product_description = driver.find_element(By.XPATH,
                                                              "//div[contains(@class, 'ProductDescription__product-description')]").text

                    if "Key Ingredients:" in product_description and "Key Benefits:" in product_description:
                        key_ingredients_text = product_description.split("Key Ingredients:")[1]
                        key_ingredients_section = key_ingredients_text.split("Key Benefits:")[0]
                        key_ingredients_list = key_ingredients_section.split(',')
                        number_of_key_ingredients = len([item for item in key_ingredients_list if item.strip()])

                        key_benefits_text = product_description.split("Key Benefits:")[1]
                        if "Directions for Use:" in key_benefits_text:
                            key_benefits_section = key_benefits_text.split("Directions for Use:")[0]
                        else:
                            key_benefits_section = key_benefits_text.split("Safety Information:")[0]

                        key_benefits_list = key_benefits_section.split('\n')
                        number_of_key_benefits = len([item for item in key_benefits_list if item.strip()])

                    if "Product Form:" in product_description:
                        product_form_text = product_description.split("Product Form:")[1]
                        product_form = product_form_text.split("\n")[0].strip()

                except Exception as e:
                    print("Product description or key ingredients/benefits/form not found:", e)

                writer.writerow([brand_name, cost, rating, final_rating, tablet_count, no_of_users, product_highlights,
                                 number_of_product_highlights, product_description, number_of_key_ingredients,
                                 number_of_key_benefits, product_form])

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print("Exception occurred:", e)

        try:
            next_button = driver.find_element(By.XPATH, "//span[contains(@class, 'style__next')]")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
        except Exception as e:
            print("No more pages or unable to find the next button:", e)
            break
driver.quit()
