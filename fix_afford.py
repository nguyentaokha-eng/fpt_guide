import os

# Read the file
with open('templates/afford_new.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the first {% endblock %} and keep only up to that line
result = []
for line in lines:
    result.append(line)
    if '{% endblock %}' in line:
        break

# Write back
with open('templates/afford_new.html', 'w', encoding='utf-8') as f:
    f.writelines(result)

# Also fix afford.html
with open('templates/afford.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
for line in lines:
    result.append(line)
    if '{% endblock %}' in line:
        break

with open('templates/afford.html', 'w', encoding='utf-8') as f:
    f.writelines(result)
    f.write('\n')

print(f"Fixed afford.html: {len(result)} lines")

# Clean up
os.remove('templates/afford_new.html')
print("Removed afford_new.html")

# Read the file
with open('templates/afford_new.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the first {% endblock %} and keep only up to that line
result = []
for line in lines:
    result.append(line)
    if '{% endblock %}' in line:
        break

# Write back
with open('templates/afford_new.html', 'w', encoding='utf-8') as f:
    f.writelines(result)

# Also fix afford.html
with open('templates/afford.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
for line in lines:
    result.append(line)
    if '{% endblock %}' in line:
        break

with open('templates/afford.html', 'w', encoding='utf-8') as f:
    f.writelines(result)
    f.write('\n')

print(f"Fixed afford.html: {len(result)} lines")

# Clean up
os.remove('templates/afford_new.html')
print("Removed afford_new.html")

