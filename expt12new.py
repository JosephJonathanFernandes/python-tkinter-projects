import tkinter as tk
from tkinter import messagebox

# Disease data: symptoms with weights and advice
DISEASE_DATABASE = {
    "Flu": {
        "symptoms": {"fever": 2, "cough": 2, "sore throat": 1, "body aches": 2, "runny nose": 1, "fatigue": 1},
        "advice": "Get rest, stay hydrated. Antiviral meds may help if prescribed."
    },
    "COVID-19": {
        "symptoms": {"fever": 2, "cough": 2, "shortness of breath": 3, "loss of taste": 3, "headache": 1, "fatigue": 2},
        "advice": "Consider getting a COVID test. Isolate and monitor oxygen."
    },
    "Measles": {
        "symptoms": {"fever": 2, "rash": 3, "runny nose": 1, "cough": 1},
        "advice": "Avoid contact with others. Consult doctor immediately."
    },
    "Common Cold": {
        "symptoms": {"cough": 1, "sore throat": 1, "runny nose": 2, "headache": 1},
        "advice": "Rest and drink warm fluids. Usually self-resolves in a few days."
    },
    "Dengue": {
        "symptoms": {"fever": 3, "rash": 2, "headache": 2, "body aches": 2},
        "advice": "Check platelet count. Visit hospital if bleeding or high fever."
    },
    "Malaria": {
        "symptoms": {"fever": 3, "headache": 2, "body aches": 2, "chills": 3},
        "advice": "Needs blood test. Go to nearest clinic for malaria screening."
    }
}

SYMPTOMS_LIST = [
    "fever", "cough", "sore throat", "body aches",
    "rash", "headache", "runny nose", "shortness of breath",
    "loss of taste", "fatigue", "chills"
]

class MedicalExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Expert System")
        self.symptom_vars = {}

        title = tk.Label(root, text="🩺 Medical Expert System", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        instructions = tk.Label(root, text="Select the symptoms you are experiencing:", font=("Arial", 12))
        instructions.pack()

        self.symptom_frame = tk.Frame(root)
        self.symptom_frame.pack(pady=5)

        for i, symptom in enumerate(SYMPTOMS_LIST):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.symptom_frame, text=symptom.capitalize(), variable=var, font=("Arial", 10))
            cb.grid(row=i // 2, column=i % 2, sticky='w', padx=10, pady=2)
            self.symptom_vars[symptom] = var

        diagnose_button = tk.Button(root, text="Diagnose", command=self.diagnose, font=("Arial", 12), bg="lightblue")
        diagnose_button.pack(pady=10)

        self.result_text = tk.Text(root, height=15, width=80, font=("Courier", 10))
        self.result_text.pack(padx=10, pady=10)

    def diagnose(self):
        symptoms = {symptom: var.get() for symptom, var in self.symptom_vars.items()}
        diagnosis = self.get_diagnosis(symptoms)

        if not diagnosis:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\nNo clear diagnosis. Please consult a doctor.")
            return

        result = self.generate_result(diagnosis)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def get_diagnosis(self, symptoms):
        result = {}

        for disease, data in DISEASE_DATABASE.items():
            disease_symptoms = data["symptoms"]
            match_score = 0
            total_score = sum(disease_symptoms.values())

            for symptom, weight in disease_symptoms.items():
                if symptoms.get(symptom, False):
                    match_score += weight

            confidence = (match_score / total_score) * 100
            if confidence > 0:
                result[disease] = round(confidence, 2)

        return result

    def generate_result(self, diagnosis):
        sorted_diag = sorted(diagnosis.items(), key=lambda x: x[1], reverse=True)
        result_text = ""

        # Conflict detection
        if len(sorted_diag) > 1 and abs(sorted_diag[0][1] - sorted_diag[1][1]) <= 15:
            result_text += f"⚠️ Conflict: Symptoms match both {sorted_diag[0][0]} and {sorted_diag[1][0]}\n\n"

        result_text += "Possible Diagnoses:\n\n"
        for disease, score in sorted_diag:
            advice = DISEASE_DATABASE[disease]["advice"]
            result_text += f"{disease} ({score}%)\n  → {advice}\n\n"

        result_text += "\n⚠️ This is not medical advice. Always consult a qualified doctor!"
        return result_text

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalExpertSystemGUI(root)
    root.mainloop()
