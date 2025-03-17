import fitz, re

# Path to your transcript of records (with .pdf extension)
file_path = "przebieg.pdf"

# Your current semester, example: "Semestr letni 2024/2025" or "Summer semester 2024/2025" (depends on the language of your transcript)
current_semester = "Semestr letni 2024/2025"

if not file_path.strip():
    print("Error: You must specify the file path in 'file_path' variable.")
    quit()
if not current_semester.strip():
    print("Error: You must specify the current semester in 'current_semester' variable.")
    quit()


def extract_from_pdf(file_path, semester):
    text = ""
    with fitz.open(file_path) as file:
        for page in file:
            text += page.get_text("text")
    if semester not in text:
        raise ValueError(f"The specified semester \"{semester}\" was not found in the file. Correct the entry.")
    text = text.split(semester)[0]
    grades_regex = re.findall(r"\xa0(\d{1,2},\d{1,2})", text)
    ects_regex = re.findall(r"\xa0(\d+)\xa0", text)
    grades = [float(grades_regex[i].replace(",", ".")) for i in range(len(grades_regex))]
    ects = [float(ects_regex[i]) for i in range(len(grades_regex))]
    return grades, ects

def calculate_weighted_average(grades, ects):
    ects_sum = 0
    grades_ects = 0
    for i in range(len(grades)):
        ects_sum+=ects[i]
        grades_ects+=grades[i]*ects[i]
    return grades_ects / ects_sum


try:
    grades, ects = extract_from_pdf(file_path, current_semester)
    weighted_average = calculate_weighted_average(grades, ects)
    print(f"Extracted grades: \n{grades}")
    print(f"\nExtracted ECTS points: \n{ects}")
    print(f"\nECTS weighted average grade: {weighted_average:.2f}\n")
except Exception:
    print(f"Error: {Exception}")