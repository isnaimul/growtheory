// // PART 4A: Configuration

// API Configuration - UPDATE THIS WHEN BACKEND IS READY
const API_CONFIG = {
    // Local development
    BASE_URL: '',  
    // Your backend will run here
    
    // Production (AWS API Gateway) - update later
    // BASE_URL: 'https://your-api-gateway-url.amazonaws.com/prod',
    
    ENDPOINTS: {
        ANALYZE: '/analyze',
        STATUS: '/status'
    }
};

// // PART 4B: DOM Elements

// Landing page elements
const companyInput = document.getElementById('companyInput');
const analyzeButton = document.getElementById('analyzeButton');
const loadingOverlay = document.getElementById('loadingOverlay');

// Report page elements  
const reportElements = {
    companyName: document.getElementById('companyName'),
    companyRole: document.getElementById('companyRole'),
    reportMeta: document.getElementById('reportMeta'),
    scoreNumber: document.getElementById('scoreNumber'),
    hiringVelocity: document.getElementById('hiringVelocity'),
    stabilityScore: document.getElementById('stabilityScore'),
    layoffRisk: document.getElementById('layoffRisk'),
    verdictText: document.getElementById('verdictText'),
    insightsList: document.getElementById('insightsList'),
    actionSteps: document.getElementById('actionSteps'),
    detailedAnalysis: document.getElementById('detailedAnalysis')
};

// // PART 4C: Event Listeners

if (analyzeButton) {
    analyzeButton.addEventListener('click', handleAnalyze);
    
    // Allow Enter key to trigger analysis
    companyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAnalyze();
        }
    });
}

// CTA buttons
document.querySelectorAll('.cta-button-large').forEach(button => {
    button.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        if (companyInput) companyInput.focus();
    });
});

// // PART 4D: Main Analysis Function

async function handleAnalyze() {
    const company = companyInput.value.trim();
    
    // Validation
    if (!company) {
        alert('Please enter a company name');
        return;
    }
    
    // Show loading
    showLoading();
    
    try {
        // Call backend API
        const result = await analyzeCompany(company);
        
        // Store result in sessionStorage
        sessionStorage.setItem('reportData', JSON.stringify(result));
        
        // Redirect to report page
        window.location.href = 'report.html';
        
    } catch (error) {
        hideLoading();
        alert('Error analyzing company. Please try again.');
        console.error('Analysis error:', error);
    }
}

// // PART 4E: API Communication

async function analyzeCompany(companyName) {
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company: companyName
        })
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// // PART 4F: Report Page Population

// Check if we're on the report page
if (window.location.pathname.includes('report.html')) {
    loadReport();
}

function loadReport() {
    // Get data from sessionStorage
    const reportData = sessionStorage.getItem('reportData');
    
    if (!reportData) {
        // No data, redirect back
        window.location.href = 'index.html';
        return;
    }
    
    const data = JSON.parse(reportData);
    populateReport(data);
}

function populateReport(data) {
    // Header
    reportElements.companyName.textContent = data.company;
    reportElements.companyRole.textContent = data.role || 'General Analysis';
    reportElements.reportMeta.textContent = `Generated ${new Date(data.timestamp).toLocaleString()}`;
    
    // Score
    reportElements.scoreNumber.textContent = `${data.score}%`;
    
    // Metrics
    reportElements.hiringVelocity.textContent = `${data.hiringVelocity}/10`;
    reportElements.stabilityScore.textContent = `${data.stabilityScore}/10`;
    reportElements.layoffRisk.textContent = `${data.layoffRisk}%`;
    
    // Verdict
    reportElements.verdictText.textContent = data.verdict;
    
    // Insights
    if (data.insights && data.insights.length > 0) {
        reportElements.insightsList.innerHTML = data.insights.map(insight => `
            <div class="insight-item ${insight.type}">
                <strong>${insight.title}</strong>
                <p>${insight.description}</p>
            </div>
        `).join('');
    }
    
    // Action Steps
    if (data.actionSteps && data.actionSteps.length > 0) {
        reportElements.actionSteps.innerHTML = data.actionSteps.map((step, index) => `
            <div class="action-step">
                <strong>Step ${index + 1}:</strong> ${step}
            </div>
        `).join('');
    }
    
    // Detailed Analysis
    if (data.detailedAnalysis) {
        reportElements.detailedAnalysis.innerHTML = data.detailedAnalysis;
    }
}

// // PART 4G: Utility Functions

function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    }
}

function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
}

// // PART 4H: Mock Data (for testing without backend)

// Uncomment this to test frontend without backend

// async function analyzeCompany(companyName) {
//     // Simulate API delay
//     await new Promise(resolve => setTimeout(resolve, 2000));
    
//     // Return mock data
//     return {
//         company: companyName,
//         role: 'Software Engineer',
//         timestamp: new Date().toISOString(),
//         score: 68,
//         hiringVelocity: 8.5,
//         stabilityScore: 9,
//         layoffRisk: 5,
//         verdict: `You're a strong candidate for ${companyName}. Your background aligns well with their hiring patterns.`,
//         insights: [
//             {
//                 type: 'positive',
//                 title: 'Strong Alumni Network',
//                 description: 'Multiple alumni from your school work here'
//             },
//             {
//                 type: 'positive',
//                 title: 'Fresh Posting',
//                 description: 'Job posted recently with high hiring velocity'
//             },
//             {
//                 type: 'neutral',
//                 title: '6-Week Timeline',
//                 description: 'Average interview process takes 42-49 days'
//             }
//         ],
//         actionSteps: [
//             'Apply on company careers page today',
//             'Reach out to alumni connections',
//             'Prepare for technical assessment',
//             'Attend upcoming networking events'
//         ],
//         detailedAnalysis: '<p>Detailed analysis will go here...</p>'
//     };
// }
