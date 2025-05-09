# 📸 SmartCamera

Έξυπνη κάμερα παρακολούθησης με Raspberry Pi που ανιχνεύει αντικείμενα σε πραγματικό χρόνο και στέλνει ειδοποιήσεις.

## 🔍 Περιγραφή

Η SmartCamera χρησιμοποιεί το προεκπαιδευμένο μοντέλο **MobileNet-SSD v3** για **ανίχνευση αντικειμένων** σε πραγματικό χρόνο μέσω κάμερας συνδεδεμένης σε Raspberry Pi. Το σύστημα μπορεί να στείλει ειδοποιήσεις, στιγμιότυπα, και καταγεγραμμένα αρχεία τόσο μέσω email όσο και στο cloud (AWS).  

Το μοντέλο έχει εκπαιδευτεί με το dataset **[COCO](https://cocodataset.org/#overview)**.

## 📦 Τεχνολογίες / Εργαλεία

- [OpenCV TensorFlow Object Detection API](https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API)
- MobileNet-SSD v3
- COCO Dataset
- Raspberry Pi
- Python
- AWS (S3)
- Android (Kotlin/Android Studio)

## 🎛️ Δυνατότητες

1. 📡 Live Streaming
2. 🧠 Ανίχνευση αντικειμένων
3. 📧 Αποστολή ειδοποιήσεων με φωτογραφία του αντικειμένου μέσω email
4. ☁️ Αποθήκευση καταγεγραμμένων αρχείων στο cloud (AWS)
5. 📱 Ανάπτυξη Android εφαρμογής για ειδοποιήσεις
6. 🖼️ Αποστολή στιγμιότυπου με ανιχνευμένο άνθρωπο στο κινητό



