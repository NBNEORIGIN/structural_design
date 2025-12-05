# Vercel Deployment Guide

## ✅ Step 1: GitHub Repository (COMPLETED)

Your code is now on GitHub:
- **Repository**: https://github.com/NBNEORIGIN/structural_design
- **Branch**: main
- **Files**: All calculator files pushed successfully

## 🚀 Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**: https://vercel.com

2. **Sign in with GitHub**:
   - Click "Sign Up" or "Log In"
   - Choose "Continue with GitHub"
   - Authorize Vercel to access your GitHub account

3. **Import Project**:
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Find and select: `NBNEORIGIN/structural_design`
   - Click "Import"

4. **Configure Project**:
   - **Project Name**: `wind-loading-calculator` (or your preferred name)
   - **Framework Preset**: Other (it will auto-detect static site)
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (static site)
   - **Output Directory**: `./` (leave as default)

5. **Deploy**:
   - Click "Deploy"
   - Wait 30-60 seconds for deployment
   - You'll get a URL like: `https://wind-loading-calculator.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project
cd "g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator"

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## 🌐 Step 3: Custom Domain (Optional)

If you want to use your own domain (e.g., `calculator.nbnesigns.com`):

1. **In Vercel Dashboard**:
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Add"
   - Enter your domain: `calculator.nbnesigns.com`

2. **In Your DNS Provider** (where you manage nbnesigns.com):
   - Add a CNAME record:
     - **Name**: `calculator`
     - **Value**: `cname.vercel-dns.com`
     - **TTL**: 3600 (or default)

3. **Wait for DNS Propagation** (5-30 minutes)

4. **Verify**: Visit `https://calculator.nbnesigns.com`

## 🔄 Automatic Updates

Every time you push to GitHub, Vercel will automatically:
1. Detect the changes
2. Build and deploy the new version
3. Update your live site (usually within 30 seconds)

### To Update the Calculator:

```bash
# Make your changes to files
# Then commit and push:

git add .
git commit -m "Description of changes"
git push
```

That's it! Vercel handles the rest automatically.

## 📊 Monitoring

### View Deployments:
- Go to: https://vercel.com/dashboard
- Select your project
- See all deployments, analytics, and logs

### View Live Site:
- Your Vercel URL: `https://[your-project-name].vercel.app`
- Or your custom domain (if configured)

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "name": "wind-loading-calculator",
  "builds": [
    {
      "src": "preview_3d.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/",
      "dest": "/preview_3d.html"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

This configuration:
- Sets the root URL (`/`) to show `preview_3d.html`
- Allows direct access to all other files
- Serves everything as static content (no server needed)

## 🎯 What Gets Deployed

All files in your repository, including:
- ✅ `preview_3d.html` - Main 3D calculator
- ✅ `preview.html` - Alternative 2D interface
- ✅ `index.html` - Landing page redirect
- ✅ All documentation (`.md` files)
- ✅ All Python files (for reference, not executed)

## 🔒 Environment Variables (If Needed)

If you need to add API keys or secrets later:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add variables:
   - **Name**: `API_KEY`
   - **Value**: `your-secret-key`
   - **Environments**: Production, Preview, Development

## 📱 Mobile Optimization

The calculator is already mobile-responsive and will work on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones
- ✅ All modern browsers (Chrome, Firefox, Safari, Edge)

## 🐛 Troubleshooting

### Issue: Deployment Failed
**Solution**: Check the build logs in Vercel dashboard for errors

### Issue: 404 Not Found
**Solution**: Ensure `index.html` and `preview_3d.html` are in the root directory

### Issue: Changes Not Showing
**Solution**: 
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Check deployment status in Vercel dashboard
3. Verify changes were pushed to GitHub

### Issue: Three.js Not Loading
**Solution**: Check browser console for errors. The CDN link should be:
```
https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js
```

## 📞 Support

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **GitHub Issues**: https://github.com/NBNEORIGIN/structural_design/issues

## ✅ Checklist

- [x] Code pushed to GitHub
- [x] Vercel configuration created (`vercel.json`)
- [x] Landing page created (`index.html`)
- [ ] Vercel account created/logged in
- [ ] Project imported to Vercel
- [ ] Deployment successful
- [ ] Live URL tested
- [ ] Custom domain configured (optional)
- [ ] Team notified of live URL

## 🎉 Next Steps

Once deployed:
1. Test all features on the live site
2. Share the URL with your team
3. Add the URL to your website
4. Monitor analytics in Vercel dashboard
5. Continue developing - all pushes auto-deploy!

---

**Your Repository**: https://github.com/NBNEORIGIN/structural_design
**Ready to Deploy**: ✅ Yes!
