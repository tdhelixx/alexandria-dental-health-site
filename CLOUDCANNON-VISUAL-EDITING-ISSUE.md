# CloudCannon Visual Editing Issue - Template Variables Showing 🔧

## 🚨 **Current Problem**

The Visual Editor is showing **template variables** (`{{ title }}`, `{{ subtitle }}`) instead of **rendered content**. This means CloudCannon is displaying the raw template files rather than the built HTML.

## 🔍 **What This Means**

- ❌ Visual Editor shows `{{ title }}` instead of "Dental Implants"
- ❌ Content appears as template code, not actual content
- ❌ Clicking on text doesn't work for editing
- ✅ Data Editor (sidebar) works correctly

## 🎯 **Root Cause**

CloudCannon's Visual Editor is pointing to the **source files** (`src/services/*.md`) instead of the **built HTML files** (`_site/dental-implants/index.html`).

## 🔧 **Fixes Applied**

### 1. **Updated CloudCannon Config**
Added proper build and preview settings:
```yaml
# Build settings for CloudCannon + 11ty
build:
  install_command: "npm install"
  build_command: "npm run build"
  output_dir: "_site"
  preview_command: "npm run build"

# CloudCannon preview configuration
preview:
  build: true
  output_dir: "_site"
  
# Source and output paths
paths:
  source: "src"
  output: "_site"
```

### 2. **Simplified Template Syntax**
- Removed complex CSS classes
- Added colored borders for better visibility
- Streamlined `data-cms-editable` attributes

### 3. **Collection Configuration**
Added `output: true` to collections for proper preview generation.

## 🚀 **Next Steps to Try**

### Option 1: **Force a Build**
1. In CloudCannon, go to **Site Settings**
2. Go to **Build** section
3. Click **"Trigger Build"** or **"Rebuild Site"**
4. Wait for build to complete
5. Try Visual Editor again

### Option 2: **Check Build Status**
1. Look for **build logs** in CloudCannon
2. Ensure 11ty build completed successfully
3. Verify `_site` directory was created
4. Check for any build errors

### Option 3: **Alternative Editor**
1. Try the **"Content Editor"** tab instead of Visual
2. This might show a hybrid view with better editing

### Option 4: **CloudCannon Support**
If the above doesn't work, this might be a CloudCannon + 11ty integration issue that requires support.

## 📋 **What Should Work After Fix**

When properly configured, you should see:
- ✅ **Actual page content** instead of template variables
- ✅ **"Dental Implants"** as the title (not `{{ title }}`)
- ✅ **Clickable text** that becomes editable
- ✅ **Visual editing indicators** on hover
- ✅ **Real-time preview** of changes

## 🎨 **Current Visual Indicators**

I've added colored borders to help identify editable regions:
- 🟢 **Green border** = Main content area
- 🔵 **Blue border** = Benefits section  
- 🟣 **Purple border** = Process steps
- 🟡 **Yellow border** = Investment info
- 🟢 **Green border** = FAQ section
- 🔵 **Cyan border** = Final CTA

## 💡 **Workaround**

While troubleshooting, you can still edit content using:
1. **Data Editor** (sidebar) - fully functional
2. **Content Editor** tab - might work better than Visual
3. **File editing** directly in CloudCannon

The issue is specifically with Visual Editor preview rendering, not the underlying editing functionality. 