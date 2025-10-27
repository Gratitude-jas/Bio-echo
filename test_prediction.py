from app.services.predict import train_model

report = train_model("data/features/features.csv")
print("✅ Model trained")
print("📊 Evaluation Report:")
for label, metrics in report.items():
    if isinstance(metrics, dict):
        print(f"{label}: {metrics}")