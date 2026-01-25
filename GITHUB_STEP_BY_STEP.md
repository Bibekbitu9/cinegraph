# 🚀 GitHub Token Creation & Push - Step-by-Step Guide

## Part 1: Create Personal Access Token on GitHub.com

### Step 1: Login to GitHub
1. Open your browser
2. Go to: **https://github.com/login**
3. Login with your credentials

---

### Step 2: Navigate to Token Settings
1. Click your **profile picture** (top-right corner)
2. Click **"Settings"**
3. Scroll down in left sidebar
4. Click **"Developer settings"** (near bottom)
5. Click **"Personal access tokens"**
6. Click **"Tokens (classic)"**

**Direct Link:** https://github.com/settings/tokens

---

### Step 3: Delete Old Token (If exists)
1. Look for token named similar to "CineGraph" or any recent token
2. Click **"Delete"** button next to it
3. Confirm deletion

---

### Step 4: Generate New Token
1. Click green button: **"Generate new token"**
2. Click **"Generate new token (classic)"**

---

### Step 5: Configure Token Settings

**Token Name:**
```
CineGraph-Full-Access
```

**Expiration:**
- Select: **90 days** (or "No expiration" if you prefer)

**Select Scopes - VERY IMPORTANT:**

Scroll down and check these boxes:

✅ **repo** (THIS IS THE MAIN ONE - check the parent checkbox)
   - This will auto-check all sub-items:
   - ✅ repo:status
   - ✅ repo_deployment
   - ✅ public_repo
   - ✅ repo:invite
   - ✅ security_events

✅ **workflow** (optional but recommended)

**Visual Guide:**
```
☐ repo                          ← CHECK THIS BOX!
  ☐ repo:status                 ← Will auto-check
  ☐ repo_deployment             ← Will auto-check
  ☐ public_repo                 ← Will auto-check
  ☐ repo:invite                 ← Will auto-check
  ☐ security_events             ← Will auto-check

☐ workflow                      ← Check this too
```

---

### Step 6: Generate Token
1. Scroll to bottom of page
2. Click green button: **"Generate token"**
3. **IMPORTANT:** You'll see your new token on next page

---

### Step 7: Copy Token Immediately
1. You'll see a green box with your token
2. Token starts with: `ghp_` or `github_pat_`
3. Click the **copy icon** (📋) next to the token
4. **SAVE IT SOMEWHERE** - you won't see it again!

Example token format:
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Part 2: Push Code Using Your Token

### Option A: Simple Copy-Paste Method

Once you have your token copied, paste it here and say **"Here's my new token: [paste]"**

I'll immediately run the push command for you!

---

### Option B: Manual Push (If you want to do it yourself)

Open terminal/command prompt and run these commands:

**Replace `YOUR_NEW_TOKEN` with the token you just copied:**

```bash
cd /app

git remote set-url origin https://YOUR_NEW_TOKEN@github.com/Bibekbitu9/cinegraph.git

git push -u origin main
```

---

## Expected Success Message

You should see output like this:

```
Enumerating objects: 542, done.
Counting objects: 100% (542/542), done.
Delta compression using up to 8 threads
Compressing objects: 100% (345/345), done.
Writing objects: 100% (542/542), 2.73 MiB | 1.45 MiB/s, done.
Total 542 (delta 178), reused 0 (delta 0)
remote: Resolving deltas: 100% (178/178), done.
To https://github.com/Bibekbitu9/cinegraph.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Part 3: Verify on GitHub.com

1. Go to: **https://github.com/Bibekbitu9/cinegraph**
2. You should see:
   - ✅ All your files (backend/, frontend/, etc.)
   - ✅ README.md with full documentation
   - ✅ Green "Code" button
   - ✅ Recent commit message

---

## 🎯 Quick Checklist

Before creating token:
- [ ] Logged into GitHub.com
- [ ] Navigated to Settings → Developer settings → Tokens (classic)

While creating token:
- [ ] Named it "CineGraph-Full-Access"
- [ ] **CHECKED the main "repo" checkbox** ← CRITICAL
- [ ] Copied token immediately

After creating token:
- [ ] Token saved somewhere safe
- [ ] Ready to paste token for push

---

## ⚠️ Common Mistakes to Avoid

1. **NOT checking "repo" checkbox**
   - This is the #1 reason for 403 errors
   - Make sure the PARENT "repo" checkbox is checked

2. **Using wrong token type**
   - Use "Tokens (classic)" NOT "Fine-grained tokens"

3. **Not copying token immediately**
   - GitHub only shows it once
   - If you miss it, delete and create new one

4. **Including spaces in token**
   - Copy the entire token
   - No spaces before or after

---

## 🆘 Still Having Issues?

**If push fails again:**

1. **Double-check token has "repo" scope:**
   - Go back to: https://github.com/settings/tokens
   - Click on your token name
   - Verify "repo" is listed under scopes

2. **Try regenerating:**
   - Click "Regenerate token" button
   - This keeps same permissions but creates new token

3. **Test token first:**
   ```bash
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   ```
   Should return your username without errors

---

## 📱 Screenshot Locations (For Reference)

If you're stuck, here's what each page should look like:

1. **Settings page:** Profile picture → Settings (top-right)
2. **Developer settings:** Left sidebar, scroll to bottom
3. **Tokens page:** "Personal access tokens" → "Tokens (classic)"
4. **Generate page:** Green "Generate new token" button
5. **Scopes page:** Long list of checkboxes (check "repo")
6. **Token page:** Green box with token string

---

## ✅ Success Criteria

You'll know it worked when:
- ✅ GitHub.com shows all your files
- ✅ README.md displays with formatting
- ✅ You can see commit history
- ✅ Repository has ~500+ files
- ✅ No error messages in terminal

---

## 🎉 After Successful Push

**Update your repository:**

1. Go to: https://github.com/Bibekbitu9/cinegraph
2. Click ⚙️ (Settings) at top
3. Under "About" section:
   - Description: `AI-Powered Movie Recommendation Platform with streaming availability`
   - Website: `https://screenscout-5.preview.emergentagent.com`
   - Topics: Add `movies`, `ai`, `recommendations`, `react`, `fastapi`, `streaming`

---

**Ready to start? Go to Step 1 and create your token!**

Once you have it, just paste it here and I'll push your code immediately! 🚀
