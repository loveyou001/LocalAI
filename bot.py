import pyautogui
import time

# กำหนดค่าตัวแปร
ATTACK_BUTTON_IMAGE = 'images/attack_button.png'
END_BATTLE_IMAGE = 'images/end_battle.png'
CONFIDENCE = 0.8  # ค่าความแม่นยำในการค้นหารูปภาพ (ปรับได้ตามความเหมาะสม)
SEARCH_INTERVAL = 2  # วินาที: ความถี่ในการค้นหาปุ่มโจมตี
BATTLE_CHECK_INTERVAL = 3 # วินาที: ความถี่ในการค้นหาปุ่มจบการต่อสู้

def find_and_click(image_path, confidence=0.8):
    """
    ฟังก์ชันสำหรับค้นหารูปภาพบนหน้าจอและคลิก
    - image_path: ที่อยู่ของไฟล์รูปภาพที่ต้องการค้นหา
    - confidence: ค่าความแม่นยำในการค้นหา
    - คืนค่าเป็น True หากเจอและคลิกสำเร็จ, มิฉะนั้นคืนค่าเป็น False
    """
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            print(f"คลิกที่รูปภาพ '{image_path}' ณ ตำแหน่ง {location}")
            return True
    except pyautogui.ImageNotFoundException:
        # ไม่ต้องทำอะไรเมื่อไม่เจอรูป
        pass
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการค้นหาและคลิก: {e}")
    return False

def main_loop():
    """
    ลูปหลักของบอท
    """
    print("="*30)
    print("บอทเริ่มทำงานแล้ว...")
    print("กด Ctrl+C ในหน้าต่าง Terminal เพื่อหยุดการทำงาน")
    print("="*30)

    while True:
        try:
            # 1. ค้นหาปุ่มโจมตี
            print(f"กำลังค้นหาปุ่มโจมตี ('{ATTACK_BUTTON_IMAGE}')...")
            if find_and_click(ATTACK_BUTTON_IMAGE, confidence=CONFIDENCE):

                # 2. เมื่อเจอและคลิกปุ่มโจมตีแล้ว ให้เข้าสู่สถานะ "กำลังต่อสู้"
                print("\n--- เริ่มการต่อสู้! กำลังรอให้การต่อสู้จบ... ---")
                battle_start_time = time.time()

                while True:
                    # 3. ค้นหาปุ่มจบการต่อสู้
                    if find_and_click(END_BATTLE_IMAGE, confidence=CONFIDENCE):
                        print("--- การต่อสู้จบลงแล้ว! ---")
                        time.sleep(1) # รอสักครู่เพื่อให้เกมโหลด
                        break # ออกจากลูปการต่อสู้

                    # Timeout: หากการต่อสู้ใช้เวลานานเกินไป (เช่น 5 นาที) ให้กลับไปค้นหาปุ่มโจมตีใหม่
                    if time.time() - battle_start_time > 300:
                        print("การต่อสู้ใช้เวลานานเกินไป กลับไปค้นหาปุ่มโจมตีใหม่...")
                        break

                    time.sleep(BATTLE_CHECK_INTERVAL)

            # รอสักครู่ก่อนจะเริ่มค้นหาครั้งต่อไป
            time.sleep(SEARCH_INTERVAL)

        except KeyboardInterrupt:
            print("\nบอทหยุดทำงานแล้ว ขอบคุณที่ใช้บริการครับ!")
            break
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่ไม่คาดคิดในลูปหลัก: {e}")
            time.sleep(10) # หากเกิดข้อผิดพลาด ให้รอ 10 วินาทีก่อนลองใหม่

if __name__ == "__main__":
    main_loop()
