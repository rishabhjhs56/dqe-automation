import os
import csv
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# ==================================================
# CONFIG
# ==================================================

HTML_FILE = "facility_type_dashboard.html"

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "outputs"
CSV_DIR = OUTPUT_DIR / "csv"
SHOT_DIR = OUTPUT_DIR / "screenshots"

CSV_DIR.mkdir(parents=True, exist_ok=True)
SHOT_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# BROWSER CONTEXT MANAGER
# ==================================================

class Browser:
    def __enter__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")  # Remove if you want to see browser
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.driver.implicitly_wait(10)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

# ==================================================
# CSV SAVE
# ==================================================

def save_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# ==================================================
# TABLE EXTRACTION
# ==================================================

def extract_table(driver):
    print("Extracting table...")

    try:
        # Wait for table to be fully loaded
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        # Additional wait for all table rows to load
        time.sleep(2)

        # Get table heading
        table_heading = ""
        try:
            # Try multiple selectors for heading
            heading_selectors = [
                "//h2[contains(text(), 'Facility Data')]",
                "//h2",
                "//h3[contains(text(), 'Facility')]"
            ]
            
            for selector in heading_selectors:
                try:
                    table_heading_elem = driver.find_element(By.XPATH, selector)
                    table_heading = table_heading_elem.text.strip()
                    break
                except:
                    continue
                    
            if not table_heading:
                table_heading = "Last 7 Days Facility Data"
                
        except Exception:
            table_heading = "Facility Data Table"

        # Find table
        table = driver.find_element(By.TAG_NAME, "table")
        
        # Extract headers
        headers = []
        header_row = table.find_element(By.TAG_NAME, "tr")
        for th in header_row.find_elements(By.TAG_NAME, "th"):
            headers.append(th.text.strip())

        # Extract all data rows
        rows = []
        all_rows = table.find_elements(By.TAG_NAME, "tr")
        
        for i, tr in enumerate(all_rows):
            if i == 0:  # Skip header row
                continue
                
            cells = tr.find_elements(By.TAG_NAME, "td")
            if cells:
                row_data = []
                for td in cells:
                    row_data.append(td.text.strip())
                rows.append(row_data)

        print(f"Extracted {len(rows)} data rows from table")

        # CSV: heading row, header row, then data rows
        csv_rows = [[table_heading], headers] + rows

        save_csv(CSV_DIR / "table.csv", csv_rows)
        print("table.csv created successfully")

    except Exception as e:
        print(f"Table extraction error: {e}")

# ==================================================
# TABLE SCREENSHOT (COMPLETE TABLE)
# ==================================================

def table_screenshot(driver):
    print("Taking table screenshot...")
    try:
        # Wait for table to be visible
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))
        )
        
        # Scroll to table to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView(true);", table)
        time.sleep(1)
        
        # Get the complete table dimensions
        table_location = table.location
        table_size = table.size
        
        # Get current window size
        window_size = driver.get_window_size()
        
        # Calculate required window size to fit complete table
        required_width = max(table_size['width'] + 200, 1200)  # Add padding
        required_height = max(table_size['height'] + 300, 800)  # Add padding
        
        # Set window size to accommodate full table
        driver.set_window_size(required_width, required_height)
        time.sleep(2)
        
        # Scroll to top to ensure table is fully visible
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Take screenshot of the table element
        path = SHOT_DIR / "table_screenshot.png"
        table.screenshot(str(path))
        print("Table screenshot saved as table_screenshot.png")
        
    except Exception as e:
        print(f"Table screenshot error: {e}")

# ==================================================
# CHART SCREENSHOT (COMPLETE CHART)
# ==================================================

def chart_screenshot(driver):
    print("Taking chart screenshot...")
    try:
        # Wait for chart to be loaded
        chart_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "svg-container"))
        )
        
        # Scroll to chart
        driver.execute_script("arguments[0].scrollIntoView(true);", chart_container)
        time.sleep(2)
        
        # Get chart dimensions and position
        chart_location = chart_container.location
        chart_size = chart_container.size
        
        # Ensure window is large enough for complete chart
        required_width = max(chart_size['width'] + 100, 800)
        required_height = max(chart_size['height'] + 200, 600)
        
        driver.set_window_size(required_width, required_height)
        time.sleep(1)
        
        # Center the chart in view
        driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'center'
            });
        """, chart_container)
        time.sleep(2)
        
        path = SHOT_DIR / "doughnut_screenshot.png"
        chart_container.screenshot(str(path))
        print("Doughnut chart screenshot saved")
        
    except Exception as e:
        print(f"Chart screenshot error: {e}")

# ==================================================
# EXTRACT CHART CSV
# ==================================================

def extract_chart_csv(driver):
    print("Extracting chart data...")
    try:
        # Get chart heading
        chart_heading = ""
        try:
            heading_selectors = [
                "//h3[contains(text(), 'Average Time')]",
                "//h3",
                "//*[contains(text(), 'Average Time Spent')]"
            ]
            
            for selector in heading_selectors:
                try:
                    chart_heading_elem = driver.find_element(By.XPATH, selector)
                    chart_heading = chart_heading_elem.text.strip()
                    break
                except:
                    continue
                    
            if not chart_heading:
                chart_heading = "Average Time Spent by Facility Type"
                
        except Exception:
            chart_heading = "Doughnut Chart Data"

        # Wait for chart to be loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
        )
        
        pie = driver.find_element(By.CLASS_NAME, "pielayer")
        
        # Find all text elements in the pie chart
        labels = pie.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")

        rows = []
        for label in labels:
            try:
                tspans = label.find_elements(By.TAG_NAME, "tspan")
                if len(tspans) >= 2:
                    category = tspans[0].text.strip()  # Fixed: was tspans[1]
                    value = tspans[1].text.strip()     # Fixed: was tspans[2]
                    if category and value:
                        rows.append([category, value])
            except Exception as e:
                print(f"Error processing label: {e}")
                continue

        print(f"Extracted {len(rows)} chart data points")

        # CSV: heading row, header row, then data rows
        csv_rows = [[chart_heading], ["Facility Type", "Percentage"]] + rows

        if rows:
            save_csv(CSV_DIR / "doughnut.csv", csv_rows)
            print("doughnut.csv created successfully")
        else:
            print("No chart data found")

    except Exception as e:
        print(f"Chart csv extraction error: {e}")

# ==================================================
# MAIN
# ==================================================

def main():
    html_path = Path(HTML_FILE).resolve()
    
    if not html_path.exists():
        print(f"HTML file not found: {html_path}")
        return
        
    url = f"file://{html_path}"
    print(f"Loading: {url}")

    with Browser() as driver:
        try:
            driver.get(url)
            print("Page loaded, waiting for content...")
            
            # Wait for page to fully load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)  # Additional wait for dynamic content
            
            # Extract data and take screenshots
            extract_table(driver)
            table_screenshot(driver)
            extract_chart_csv(driver)
            chart_screenshot(driver)
            
        except Exception as e:
            print(f"Main execution error: {e}")

    print("Process completed!")

if __name__ == "__main__":
    main()
