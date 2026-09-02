from priority import calculate_recovery_priority


result = calculate_recovery_priority(
    amount=5000,
    severity="HIGH",
    recovery_likelihood=0.85,
    age_hours=12
)


print("\nRECOVERY PRIORITY")
print("=================")

print("Priority Score:", result["priority_score"])
print("Priority:", result["priority"])

print("\nScore Components:")

for key, value in result["components"].items():
    print(key, ":", value)