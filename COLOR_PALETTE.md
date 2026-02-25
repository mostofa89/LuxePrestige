# Ethereal Store - New Color Palette

## Color Reference Guide

### Primary Colors

1. **Black** - `#0a0908`
   - Use: Primary dark color, text, borders, buttons
   - Replaces: `obsidian`, `black-pearl`
   - Tailwind: `bg-[#0a0908]`, `text-[#0a0908]`, `border-[#0a0908]`

2. **White Smoke** - `#f2f4f3`
   - Use: Primary light color, backgrounds, text (dark mode)
   - Replaces: `pearl`, `moon-white`
   - Tailwind: `bg-[#f2f4f3]`, `text-[#f2f4f3]`, `border-[#f2f4f3]`

3. **Rosy Taupe** - `#c09891`
   - Use: Primary accent color, highlights, hover states
   - Replaces: `mint` (#52B787)
   - Tailwind: `bg-[#c09891]`, `text-[#c09891]`, `border-[#c09891]`
   - Description: Primary accent for buttons, links, badges, focus states

### Secondary/Accent Colors

4. **Dusty Taupe** - `#a9927d`
   - Use: Secondary accent, gradients, decorative elements
   - Replaces: `sea-green`, secondary emerald tones
   - Tailwind: `bg-[#a9927d]`, `from-[#a9927d]`
   - Description: Earthy, warm neutral for depth and sophistication

5. **Soft Blush** - `#f4dbd8`
   - Use: Light accents, gradients, subtle backgrounds
   - Replaces: `emerald-50`, `mint-light`, `frosted-mint`
   - Tailwind: `bg-[#f4dbd8]`, `to-[#f4dbd8]`
   - Description: Feather-light pink for gentle, romantic touches

6. **Lilac Ash** - `#bea8a7`
   - Use: Secondary text, muted UI elements, subtle contrast
   - Replaces: `twilight`, `lavender-mist`
   - Tailwind: `text-[#bea8a7]`
   - Description: Subdued grey-purple for labels, descriptions, subtle text

## Usage Examples

### Buttons
```html
<!-- Primary Button -->
<button class="bg-[#0a0908] text-[#f2f4f3] dark:bg-[#f2f4f3] dark:text-[#0a0908] hover:bg-[#c09891]">
  Click Me
</button>

<!-- Secondary Button -->
<button class="border border-[#0a0908]/15 text-[#0a0908] dark:border-[#f2f4f3]/15 dark:text-[#f2f4f3] hover:border-[#c09891] hover:text-[#c09891]">
  Learn More
</button>
```

### Cards
```html
<div class="bg-[#f2f4f3]/85 dark:bg-[#0a0908]/70 border border-[#0a0908]/10 dark:border-[#f2f4f3]/10">
  <h3 class="text-[#0a0908] dark:text-[#f2f4f3]">Card Title</h3>
  <p class="text-[#bea8a7]">Card description text</p>
</div>
```

### Gradients
```html
<!-- Soft background gradient -->
<div class="bg-gradient-to-br from-[#f4dbd8]/60 via-[#f2f4f3]/70 to-[#a9927d]/20">
  <!-- Content -->
</div>

<!-- Accent gradient -->
<div class="bg-gradient-to-br from-[#c09891]/20 via-[#bea8a7]/10 to-[#f4dbd8]/30">
  <!-- Content -->
</div>
```

### Text Hierarchy
```html
<h1 class="text-[#0a0908] dark:text-[#f2f4f3]">Main Heading</h1>
<p class="text-[#bea8a7]">Body text or description</p>
<span class="text-[#c09891]">Accent or link</span>
```

### Form Inputs
```html
<input class="bg-[#f2f4f3]/70 dark:bg-[#0a0908]/40 
              border border-[#0a0908]/15 dark:border-[#f2f4f3]/15 
              text-[#0a0908] dark:text-[#f2f4f3]
              focus:border-[#c09891] focus:ring-[#c09891]/20" />
```

## Color Philosophy

**Sophistication & Romance**: The new palette shifts from the fresh, vibrant mint-green theme to a more sophisticated, romantic, and timeless aesthetic. The taupe and blush tones evoke:

- **Elegance**: Deep black paired with soft taupes creates luxury
- **Warmth**: Rosy and dusty browns add earthiness and comfort
- **Romance**: Soft blush brings delicate, feminine touches
- **Timelessness**: Neutral base ensures the design ages gracefully

## Files Updated
- ✅ templates/backends/register.html
- ✅ templates/backends/login.html  
- ⚠️ templates/home/index.html (partial)
- ⏳ templates/backends/memberships.html (pending)
- ⏳ templates/backends/product*.html (pending)
- ⏳ templates/backends/403.html, 404.html (pending)

## Migration Notes

When updating remaining templates:

1. Replace `mint` → `[#c09891]` (rosy taupe)
2. Replace `obsidian` → `[#0a0908]` (black)
3. Replace `pearl`/`moon-white` → `[#f2f4f3]` (white smoke)
4. Replace `twilight`/`lavender-mist` → `[#bea8a7]` (lilac ash)
5. Replace `emerald-*`/`mint-light` → `[#f4dbd8]` (soft blush) or `[#a9927d]` (dusty taupe)
6. Update shadow colors: `rgba(82,183,136,0.X)` → `rgba(192,152,145,0.X)`

