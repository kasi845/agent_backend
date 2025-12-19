// ============================================
// IMPORTS
// ============================================
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Load environment variables
dotenv.config();

// ============================================
// CONFIGURATION
// ============================================
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static('.'));

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// ============================================
// ROUTES
// ============================================

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        message: 'AI Image Analyzer API is running',
        timestamp: new Date().toISOString()
    });
});

// Image analysis endpoint
app.post('/analyze', async (req, res) => {
    try {
        const { image, mimeType } = req.body;

        if (!image) {
            return res.status(400).json({
                error: 'No image provided'
            });
        }

        if (!process.env.GEMINI_API_KEY || process.env.GEMINI_API_KEY === 'your_gemini_api_key_here') {
            return res.status(500).json({
                error: 'GEMINI_API_KEY not configured. Please add your API key to the .env file'
            });
        }

        console.log('📸 Analyzing image with Gemini AI...');

        // Get the generative model
        const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

        // Prepare the image data
        const imageParts = [
            {
                inlineData: {
                    data: image,
                    mimeType: mimeType || 'image/jpeg'
                }
            }
        ];

        // Create a detailed prompt for image analysis
        const prompt = `Analyze this image in detail and provide a comprehensive description. Include:

1. **Main Subject**: What is the primary focus of the image?
2. **Visual Elements**: Describe colors, composition, lighting, and style
3. **Context & Setting**: Where does this appear to be? What's the environment?
4. **Notable Details**: Any interesting or unique aspects worth mentioning
5. **Mood & Atmosphere**: What feeling or emotion does the image convey?

Please provide a well-structured, engaging description that captures all important aspects of the image.`;

        // Generate content
        const result = await model.generateContent([prompt, ...imageParts]);
        const response = await result.response;
        const description = response.text();

        console.log('✅ Analysis complete');

        res.json({
            success: true,
            description: description,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('❌ Error analyzing image:', error);

        let errorMessage = 'Failed to analyze image';

        if (error.message.includes('API key')) {
            errorMessage = 'Invalid API key. Please check your GEMINI_API_KEY in the .env file';
        } else if (error.message.includes('quota')) {
            errorMessage = 'API quota exceeded. Please check your Gemini API usage limits';
        } else if (error.message.includes('SAFETY')) {
            errorMessage = 'Image content was flagged by safety filters';
        }

        res.status(500).json({
            error: errorMessage,
            details: error.message
        });
    }
});

// ============================================
// SERVER STARTUP
// ============================================
app.listen(PORT, () => {
    console.log('');
    console.log('🚀 ============================================');
    console.log('   AI Image Analyzer Server');
    console.log('   ============================================');
    console.log(`   📡 Server running on: http://localhost:${PORT}`);
    console.log(`   🔑 API Key configured: ${process.env.GEMINI_API_KEY ? '✅ Yes' : '❌ No'}`);
    console.log('   ============================================');
    console.log('');

    if (!process.env.GEMINI_API_KEY || process.env.GEMINI_API_KEY === 'your_gemini_api_key_here') {
        console.log('⚠️  WARNING: GEMINI_API_KEY not configured!');
        console.log('   Please add your API key to the .env file');
        console.log('');
    }
});
