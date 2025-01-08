from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from contract_processor import read_contract, find_keywords, get_recommendations

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# הגדרת מילות מפתח לבדיקה
KEYWORDS = ['יתחייבו' ,'במקרה של הפרת החוזה' ,'שכר העבודה יינתן' ,'יתחייב לעבוד' ,
'ללא אפשרות לסיים את החוזה', 'ריבית', 'כפייה', 'חוזה', 'סנקציות',
 'בונוס', 'קנס', 'עיקול רכוש', 'גישור']

# משתמשים לדוגמה
USERS = {
    "admin": "Havachelet51",  # שם משתמש וסיסמה לדוגמה
    "user": "password"
}

@app.route('/')
def index():
    """
    עמוד הבית: טופס להעלאת קובץ חוזה.
    """
    if 'user' not in session:  # בדיקה אם המשתמש מחובר
        flash("עליך להתחבר כדי לגשת לעמוד זה", "error")
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    עמוד הכניסה ועיבוד פרטי ההתחברות.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            session['user'] = username  # שמירת המשתמש המחובר ב-session
            flash(f"ברוך הבא, {username}!", "success")
            return redirect(url_for('index'))  # מפנה לעמוד הבית
        else:
            flash("שם משתמש או סיסמה שגויים", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    התנתקות משתמש.
    """
    session.pop('user', None)  # הסרת נתוני המשתמש מה-session
    flash("התנתקת בהצלחה", "success")
    return redirect(url_for('login'))

@app.route('/analyze', methods=['POST'])
def analyze_contract():
    """
    ניתוח הקובץ שהועלה: חיפוש מילות מפתח והצעת המלצות.
    """
    if 'user' not in session:  # בדיקה אם המשתמש מחובר
        flash("עליך להתחבר כדי לגשת לעמוד זה", "error")
        return redirect(url_for('login'))

    file = request.files['contract']
    if file:
        # יצירת תיקיית static אם אינה קיימת
        os.makedirs('static', exist_ok=True)

        # שמירת הקובץ שהועלה
        file_path = f'static/{file.filename}'
        file.save(file_path)

        # קריאה וניתוח התוכן
        content = read_contract(file_path)
        found_keywords = find_keywords(content, KEYWORDS)
        recommendations = get_recommendations(found_keywords)

        # יצירת חוזה מתוקן
        updated_content = content + "\n\nמילים בעייתיות והמלצות:\n"
        for keyword, recommendation in zip(found_keywords, recommendations):
            updated_content += f"{keyword}: {recommendation}\n"

        # שמירת החוזה המתוקן
        updated_file_path = f'static/updated_{file.filename}'
        with open(updated_file_path, 'w', encoding='utf-8') as updated_file:
            updated_file.write(updated_content)

        # הצגת התוצאה בדף
        return render_template('index.html', content=content, keywords=found_keywords, 
                               recommendations=recommendations, updated_file=f'updated_{file.filename}')

    flash("לא נבחר קובץ לניתוח.", "error")
    return redirect(url_for('index'))

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    """
    הוספת מילת מפתח חדשה
    """
    if 'user' not in session:
        return jsonify({"success": False, "message": "יש להתחבר למערכת"})

    name = request.form.get('name')
    keyword = request.form.get('keyword')
    reason = request.form.get('reason')

    if not name or not keyword or not reason:
        return jsonify({"success": False, "message": "נא למלא את כל השדות"})

    # שמירת המידע בקובץ
    new_request = f"{name},{keyword},{reason}\n"
    try:
        with open('static/keywords_requests.csv', 'a', encoding='utf-8') as file:
            file.write(new_request)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)