# ----------------------------------------------
# PowerShell script – commit & push src updates
# ----------------------------------------------

# 1️⃣ Change to the repository folder
Set-Location "C:\Users\dance\FOTEI"

# 2️⃣ Stage every change (including the new src files)
git add .

# 3️⃣ Commit with a descriptive message
git commit -m "Update src files for Colab integration (semantic tagging & batch driver)"

# 4️⃣ Push to the remote feature branch
git push origin feature/colab-integration