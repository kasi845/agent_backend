// ============================================
// STATE MANAGEMENT
// ============================================
let selectedImage = null;
let selectedImageFile = null;

// ============================================
// DOM ELEMENTS
// ============================================
const uploadSection = document.getElementById('uploadSection');
const previewSection = document.getElementById('previewSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

const imageInput = document.getElementById('imageInput');
const uploadBtn = document.getElementById('uploadBtn');
const changeBtn = document.getElementById('changeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const copyBtn = document.getElementById('copyBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const retryBtn = document.getElementById('retryBtn');

const previewImage = document.getElementById('previewImage');
const descriptionContent = document.getElementById('descriptionContent');
const errorMessage = document.getElementById('errorMessage');

// ============================================
// EVENT LISTENERS
// ============================================
uploadBtn.addEventListener('click', () => imageInput.click());
changeBtn.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', handleImageSelect);
analyzeBtn.addEventListener('click', analyzeImage);
copyBtn.addEventListener('click', copyDescription);
newAnalysisBtn.addEventListener('click', resetApp);
retryBtn.addEventListener('click', () => {
    hideError();
    showPreview();
});

// Drag and drop functionality
const uploadCard = document.querySelector('.upload-card');
uploadCard.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadCard.style.borderColor = 'rgba(102, 126, 234, 0.8)';
    uploadCard.style.background = 'rgba(102, 126, 234, 0.1)';
});

uploadCard.addEventListener('dragleave', () => {
    uploadCard.style.borderColor = '';
    uploadCard.style.background = '';
});

uploadCard.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadCard.style.borderColor = '';
    uploadCard.style.background = '';

    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        handleImageFile(files[0]);
    }
});

// ============================================
// IMAGE HANDLING
// ============================================
function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        handleImageFile(file);
    }
}

function handleImageFile(file) {
    selectedImageFile = file;
    const reader = new FileReader();

    reader.onload = (e) => {
        selectedImage = e.target.result;
        previewImage.src = selectedImage;
        showPreview();
    };

    reader.readAsDataURL(file);
}

// ============================================
// IMAGE ANALYSIS
// ============================================
async function analyzeImage() {
    if (!selectedImageFile) return;

    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('.btn-text').classList.add('hidden');
    analyzeBtn.querySelector('.btn-loader').classList.remove('hidden');

    try {
        // Convert image to base64
        const base64Image = await fileToBase64(selectedImageFile);

        // Send to FastAPI backend
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: base64Image,
                mime_type: selectedImageFile.type
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze image');
        }

        const data = await response.json();

        // Display results
        displayResults(data.description, data.agent_used);

    } catch (error) {
        console.error('Error analyzing image:', error);
        showError(error.message || 'Failed to analyze the image. Please make sure the server is running and try again.');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').classList.remove('hidden');
        analyzeBtn.querySelector('.btn-loader').classList.add('hidden');
    }
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            // Remove the data URL prefix (e.g., "data:image/jpeg;base64,")
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// ============================================
// UI STATE MANAGEMENT
// ============================================
function showPreview() {
    uploadSection.classList.add('hidden');
    previewSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

function showResults() {
    uploadSection.classList.add('hidden');
    previewSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    errorSection.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    uploadSection.classList.add('hidden');
    previewSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.remove('hidden');
}

function hideError() {
    errorSection.classList.add('hidden');
}

function resetApp() {
    selectedImage = null;
    selectedImageFile = null;
    imageInput.value = '';
    uploadSection.classList.remove('hidden');
    previewSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

// ============================================
// RESULTS DISPLAY
// ============================================
function displayResults(description, agentUsed = 'LangChain + Gemini') {
    // Format the description with nice typography
    const formattedDescription = formatDescription(description);

    // Add agent info at the top
    const agentBadge = `<div style="display: inline-block; padding: 0.5rem 1rem; background: var(--success-gradient); border-radius: 20px; font-size: 0.875rem; font-weight: 600; margin-bottom: 1rem;">🤖 ${agentUsed}</div>`;

    descriptionContent.innerHTML = agentBadge + formattedDescription;
    showResults();
}

function formatDescription(text) {
    // Split into paragraphs and add styling
    const paragraphs = text.split('\n').filter(p => p.trim());
    return paragraphs.map(p => {
        // Check if it's a heading (starts with # or **)
        if (p.trim().startsWith('#')) {
            const heading = p.replace(/^#+\s*/, '');
            return `<h4 style="color: var(--text-primary); margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 600;">${heading}</h4>`;
        }
        if (p.includes('**')) {
            // Handle bold text
            const formatted = p.replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--text-primary);">$1</strong>');
            return `<p style="margin-bottom: 1rem;">${formatted}</p>`;
        }
        // Check if it's a list item
        if (p.trim().startsWith('-') || p.trim().startsWith('*') || p.trim().match(/^\d+\./)) {
            const item = p.replace(/^[-*]\s*/, '').replace(/^\d+\.\s*/, '');
            return `<li style="margin-left: 1.5rem; margin-bottom: 0.5rem;">${item}</li>`;
        }
        // Regular paragraph
        return `<p style="margin-bottom: 1rem;">${p}</p>`;
    }).join('');
}

// ============================================
// COPY FUNCTIONALITY
// ============================================
async function copyDescription() {
    const text = descriptionContent.innerText;

    try {
        await navigator.clipboard.writeText(text);

        // Show success feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9L7 13L15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Copied!
        `;
        copyBtn.style.background = 'var(--success-gradient)';
        copyBtn.style.color = 'white';

        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
            copyBtn.style.color = '';
        }, 2000);

    } catch (error) {
        console.error('Failed to copy:', error);
        alert('Failed to copy to clipboard');
    }
}

// ============================================
// INITIALIZATION
// ============================================
console.log('🚀 AI Image Analyzer initialized');
console.log('🐍 Backend: FastAPI + LangChain + Gemini');
console.log('📸 Ready to analyze images!');
