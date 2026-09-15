import json
import random

quizes = [{"question": "What is the first month of the Islamic calendar?", "options": ["Muharram", "Safar", "Rabi' al-Awwal", "Ramadhan"], "answer": "Muharram"},
             {"question": "What is the name of the Islamic holy book?", "options": ["Quran", "Hadith", "Sunnah", "Tafsir"], "answer": "Quran"},
             {"question": "What is the name of the Islamic declaration of faith?", "options": ["Shahada", "Salat", "Zakat", "Sawm"], "answer": "Shahada"},
             {"question": "What is the name of the Islamic pilgrimage to Mecca?", "options": ["Hajj", "Umrah", "Zakat","Muharram"], "answer": "Hajj"},]

def take_quiz():
    score = 0
    
    quize_questions= quizes.copy()
    random.shuffle(quize_questions)
    for q in quize_questions:
        print(q["question"])
        for i, option in enumerate(q["options"], 1):
            print(f"{i}. {option}")
        answer = input("Enter the number of your answer: ")
        try:
            if int(answer) < 1 or int(answer) > len(q["options"]) :
                print("Invalid option. Please select a valid option.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if q["options"][int(answer) - 1] == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {q['answer']}.")
    print(f"You scored {score} out of {len(quizes)}.")
    percentage = (score / len(quizes)) * 100
    print(f"Your score percentage is: {percentage:.2f}%")
    return score



def save_quiz_results(filename, score):
    try:
        with open(filename, 'a') as file:
            file.write(f"Score: {score} out of {len(quizes)}\n")
    except Exception as e:
        print(f"Error saving quiz results: {e}")

def load_quiz_results(filename):
    try:
        with open(filename, 'r') as file:
            results = file.readlines()
            for result in results:
                print(result.strip())
    except Exception as e:
        print(f"Error loading quiz results: {e}")



score =None

while True:
    print("1. Take the Islamic quiz 2. Save results 3. Load results 4.   Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        score=take_quiz()
    elif choice == '2':
        if score is None:
            print("No quiz taken yet. Please take the quiz first.")
        else:   
            save_quiz_results("quiz_results.txt", score)
    elif choice == '3':
        load_quiz_results("quiz_results.txt")
    elif choice == '4':
        print("Exiting the Islamic quiz. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")
