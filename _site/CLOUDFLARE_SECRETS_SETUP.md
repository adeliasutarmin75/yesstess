# Cloudflare Workers Secrets Setup Guide

## ✅ Ya, Cloudflare Worker BISA menulis ke GitHub!

Cloudflare Worker dapat menulis ke GitHub repository melalui GitHub API, tetapi memerlukan konfigurasi secrets yang benar.

## 🔑 Required Secrets untuk Cloudflare Workers

### 1. Setup WAJIB - Secrets yang dibutuhkan:

```bash
# 1. GEMINI API KEYS (WAJIB)
wrangler secret put GEMINI_API_KEYS
# Enter: key1,key2,key3

# 2. GITHUB TOKEN (WAJIB untuk menulis ke repo)
wrangler secret put GITHUB_TOKEN  
# Enter: ghp_xxxxxxxxxxxxxxxxxxxx
```

### 2. Membuat GitHub Personal Access Token

1. **Buka GitHub Settings**:
   - Pergi ke GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Buat Token Baru**:
   - Klik "Generate new token (classic)"
   - Pilih scopes berikut:
     - ✅ **repo** (Full repository access) - WAJIB
     - ✅ **workflow** (Update GitHub Actions) - WAJIB  
     - ✅ **write:packages** (jika diperlukan)

3. **Copy Token**:
   - Copy token yang dihasilkan (dimulai dengan `ghp_`)
   - Simpan dengan aman, tidak bisa dilihat lagi

### 3. Konfigurasi Wrangler.toml

Update file `wrangler.toml`:

```toml
[vars]
GITHUB_REPO = "username/repository-name"  # Ganti dengan repo Anda
GITHUB_BRANCH = "main"
```

### 4. Deploy ke Cloudflare

```bash
# Deploy worker ke Cloudflare
wrangler deploy

# Check status
wrangler tail
```

## 🔄 Cara Kerja Cloudflare Worker dengan GitHub

1. **Scheduled Trigger**: Worker runs daily at 6 AM UTC
2. **GitHub API Call**: Worker triggers GitHub Actions workflow 
3. **Python Execution**: GitHub Actions runs UpdateArticle.py
4. **Direct Commit**: Script commits article directly to repository
5. **Auto Deploy**: Jekyll rebuilds site automatically

## 📋 Permissions yang Dibutuhkan

GitHub Token harus memiliki permissions:

| Permission | Untuk Apa |
|-----------|------------|
| `repo` | Read/write access ke repository |
| `workflow` | Trigger GitHub Actions |
| `contents:write` | Commit files ke repository |

## 🧪 Testing Setup

1. **Test Manual Generation**:
```bash
curl -X POST https://your-worker.your-subdomain.workers.dev/generate \
  -H "Authorization: Bearer your-api-secret"
```

2. **Check Logs**:
```bash
wrangler tail
```

3. **Verify GitHub**:
   - Check GitHub Actions tab untuk workflow runs
   - Check `_posts/` directory untuk artikel baru

## ⚙️ Optional Secrets

```bash
# Image APIs (optional)
wrangler secret put UNSPLASH_ACCESS_KEY

# Manual generation security
wrangler secret put API_SECRET

# Webhook verification  
wrangler secret put GITHUB_WEBHOOK_SECRET
```

## 🚨 Troubleshooting

### "GITHUB_TOKEN secret not configured"
- Pastikan token sudah di-set: `wrangler secret put GITHUB_TOKEN`
- Verify dengan: `wrangler secret list`

### "Permission denied" saat commit
- Check GitHub token permissions
- Pastikan token memiliki `repo` access
- Test token di GitHub API explorer

### "Repository not found"
- Update `GITHUB_REPO` di `wrangler.toml`
- Format: `username/repository-name`
- Pastikan repository exists dan accessible

## ✅ Verification Checklist

- [ ] GitHub token created dengan repo permissions
- [ ] `wrangler secret put GITHUB_TOKEN` berhasil
- [ ] `wrangler secret put GEMINI_API_KEYS` berhasil  
- [ ] `GITHUB_REPO` di wrangler.toml sudah benar
- [ ] Worker deployed: `wrangler deploy`
- [ ] Test generation berhasil
- [ ] Artikel muncul di `_posts/`
- [ ] Jekyll site rebuild otomatis

## 🎯 Summary

**Ya, Cloudflare Worker DAPAT menulis ke GitHub** dengan setup yang benar:

1. ✅ GitHub Personal Access Token dengan repo permissions
2. ✅ Secrets di-configure di Cloudflare
3. ✅ Repository path di-set dengan benar
4. ✅ Worker memiliki akses ke GitHub API

Sistem akan:
- ✅ Baca keywords dari `_Article/keyword.txt`
- ✅ Generate artikel professional
- ✅ Upload images ke GitHub
- ✅ Commit artikel langsung ke repository
- ✅ Trigger Jekyll rebuild otomatis