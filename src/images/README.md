# Alexandria Dental Health - Clean Asset Structure

This is the organized asset library for the Alexandria Dental Health website.

## 📁 Folder Structure:

```
src/images/
├── branding/              ← Logos, brand assets, favicons
├── hero/                  ← Hero/banner images for pages
├── gallery/               ← Before/after photos, smile gallery
├── cosmetic/              ← Cosmetic dentistry service images
├── family/                ← Family dentistry images  
├── restorative/           ← Restorative service images
├── services/              ← General service images
├── team/                  ← Team photos and professional shots
└── patients/              ← Patient education and information images
```

## 🎯 New vs Old Paths:

**NEW Clean Structure:**
- `/images/branding/header-logo.webp`
- `/images/hero/dental-implants-hero.webp`
- `/images/gallery/before-after/case-1-before.webp`

**OLD WordPress Structure (still works during transition):**
- `/wp-content/uploads/2025/01/Dentist-Alexandria-VA-...-Logo.webp`
- `/wp-content/uploads/2025/02/Dentist-Alexandria-VA-Case-Study-...`

## 🚀 Migration Priority:

1. **Branding** - Logo files (header, footer)
2. **Hero Images** - Page banners and service heroes  
3. **Gallery** - Before/after photos
4. **Service Images** - Treatment and procedure photos

## ✅ Benefits:

✅ **Clean URLs** - `/images/hero/` instead of `/wp-content/uploads/2025/01/`  
✅ **Organized** - Logical folder structure  
✅ **11ty Compatible** - Automatically copied to `_site/images/`  
✅ **Future Proof** - Easy to maintain and expand  
✅ **Performance** - Optimized file organization 