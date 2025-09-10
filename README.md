# 🛠️ Gadget Repair Cost Estimator


**Gadget Repair Cost Estimator** is a smart, user-friendly web application that predicts the repair cost of electronic gadgets. Built with **Python Flask**, it combines **data-driven insights**, **machine learning**, and a sleek **web interface** to provide instant repair cost estimates for various devices.

---

## 🌟 Features

- **Predictive Cost Estimation:**  
  Uses machine learning models to estimate repair costs based on gadget type, issue, and brand.

- **User-friendly Web Interface:**  
  Interactive web forms built with **HTML, CSS, and Bootstrap** for smooth user experience.

- **Database Integration:**  
  Stores gadget repair history using **SQLite**, enabling quick access and management of past records.

- **Secure User Sessions:**  
  Implements session management with Flask’s `secret_key` to keep user data safe.

- **Dynamic Data Handling:**  
  Supports uploading CSVs and displaying historical repair data using **Pandas**.

- **Easy Deployment:**  
  Runs on any local or cloud server with Python and Flask installed.

---

## 🛠️ Technologies Used

- **Backend:** Python 3, Flask  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite  
- **Data Processing:** Pandas, Pickle (for ML model serialization)  
- **Machine Learning:** Custom-trained ML models for cost prediction  
- **Version Control:** Git & GitHub  

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mandar353/Gadget-Repair-Cost-Estimator.git
   cd Gadget-Repair-Cost-Estimator
2. Create a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
3. Run the Application:
    ```bash
   python app.py


## Screenshots

**Home Page:**  

<img width="427" height="469" alt="image" src="https://github.com/user-attachments/assets/9ec13a23-d382-44f8-aa79-26e15a369289" />

 

**Cost Estimation Form:**  

<img width="395" height="371" alt="image" src="https://github.com/user-attachments/assets/72d217e7-0787-4044-9f45-3c094cae9af3" />


---

## 🧩 How It Works

1. **User Input:**  
   Users select their gadget type, brand, and issue from a clean form interface.

2. **Data Processing:**  
   Input data is processed using Pandas, cleaned, and transformed to feed into the ML model.

3. **Prediction:**  
   The pre-trained ML model (stored as `model.pkl`) predicts the repair cost.

4. **Database Update:**  
   The repair request is stored in SQLite for future reference.

5. **Result Display:**  
   Predicted cost and historical repairs are displayed dynamically.

---

## 💡 Why Use This App?

- Quick and accurate repair cost estimates.  
- Keeps track of previous repairs.  
- User-friendly and visually appealing interface.  
- Easy to extend with new gadgets or issues.  
- Fully built using Python, making it easy for developers to customize.

---

## 🚀 Future Enhancements

- Add user authentication for personalized dashboards.  
- Integrate payment gateway for direct booking of repairs.  
- Expand ML model to include more gadget types and complex issues.  
- Implement interactive visual analytics of repair trends.
