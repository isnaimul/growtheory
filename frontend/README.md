# GrowTheory Frontend

AI-powered job search intelligence platform built with React + Vite.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- Backend API running (or use mock data)

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your backend URL:
```
VITE_API_BASE_URL=http://localhost:5000/api
VITE_API_ANALYZE_ENDPOINT=/analyze
VITE_API_STATUS_ENDPOINT=/status
```

3. **Start development server:**
```bash
npm run dev
```

The app will open at `http://localhost:3000`

## 📦 Build for Production

```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## 🌐 Deploy to Vercel

### Option 1: Vercel CLI
```bash
npm i -g vercel
vercel
```

### Option 2: GitHub Integration
1. Push code to GitHub
2. Import project in Vercel dashboard
3. Add environment variables in Vercel settings:
   - `VITE_API_BASE_URL` = your production API URL

## 🧪 Testing Without Backend

The app includes mock data by default. In `src/services/api.js`, the `Hero` component uses:

```javascript
// Mock data (current)
const result = await apiService.getMockData(company);

// Real API (uncomment when ready)
// const result = await apiService.analyzeCompany(company);
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/         # Navbar, Footer, Loading
│   │   ├── landing/        # Hero, Features, CTA
│   │   └── report/         # Report page components
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   └── ReportPage.jsx
│   ├── services/
│   │   └── api.js          # API service layer
│   ├── context/
│   │   └── ReportContext.jsx  # Global state
│   └── styles/             # Component styles
├── public/
└── index.html
```

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔐 Environment Variables

### Development (`.env.local`)
```
VITE_API_BASE_URL=http://localhost:5000/api
```

### Production (Vercel)
Set in Vercel dashboard under Project Settings → Environment Variables:
```
VITE_API_BASE_URL=https://your-production-api.com/api
```

## 🛠️ Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **React Router v6** - Client-side routing
- **Context API** - State management
- **CSS Modules** - Styling

## 📝 Notes

- All environment variables must be prefixed with `VITE_`
- Access them using `import.meta.env.VITE_*`
- The app uses React Context instead of sessionStorage for state management
- Responsive design included (mobile-friendly)

## 🐛 Troubleshooting

**Port already in use?**
```bash
PORT=3001 npm run dev
```

**Dependencies issues?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Environment variables not working?**
- Restart dev server after changing `.env.local`
- Ensure variables start with `VITE_`

## 📧 Support

For issues or questions, please open an issue in the repository.
