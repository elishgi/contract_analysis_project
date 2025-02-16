def read_contract(file_path):
    """
    קורא חוזה מקובץ טקסט.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: The file does not exist."
    except Exception as e:
        return f"Error: {str(e)}"


def find_keywords(content, keywords):
    """
    מחפש מילות מפתח בטקסט החוזה.
    """
    found = []
    for keyword in keywords:
        if keyword.lower() in content.lower():  # חיפוש בלתי תלוי באותיות רישיות
            found.append(keyword)
    return found


def get_recommendations(found_keywords):
    """
    מספק המלצות לתיקון על סמך מילות מפתח שנמצאו.
    """
    recommendations = {
        'ריבית': 'שקול להשתמש ב"היתר עסקה" כדי להימנע מאיסור ריבית.',
        'כפייה': 'ודא שהניסוח בחוזה מאפשר גמישות לשני הצדדים.',
        'חוזה': 'וודא שכל סעיף מוגדר היטב עם תנאים ברורים.',
        'סנקציות': 'בדוק אם הסנקציות מתאימות להלכה ולחוק.',
        'בונוס': 'ודא שהבונוס מבוסס על קריטריונים ברורים ולא שרירותיים.',
        'קנס': 'בדוק אם הקנס מידתי ומותאם לכללי ההלכה.',
        'עיקול רכוש': 'בדוק אם העיקול מתבצע בהתאם להלכה.',
        'גישור': 'וודא שהגישור מתבצע על ידי גורם מוסמך ותוך שקיפות מלאה.',
        'ללא אפשרות לסיים את החוזה': 'יש לשקול לכלול סעיף שמירת החוזה בתנאי אפשרות סיום.',
        'יתחייב לעבוד': 'אפשרות לדיון חוזר על תנאי העבודה.',
        'שכר העבודה יינתן': 'יש לפרט כיצד מחושב השכר ומה כולל (ברוטו/נטו).',
        'במקרה של הפרת החוזה': 'יש לפרט מה ייחשב כהפרה, באילו מסלול, ומה תוספת שיערך במקרה כזה (לדוגמה, שימוע או בירור).',
        'יתחייבו': 'כדאי להבהיר את התנאים והמסגרת שבה הגישור ייערך, וכן מה יקרה אם לא יושגו הסכמות בגישור.',
    }
    return [recommendations[keyword] for keyword in found_keywords if keyword in recommendations]

