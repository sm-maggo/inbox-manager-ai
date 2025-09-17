import os
import json
import httpx
import certifi
from flask import Flask, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

# Using gpt-4o-mini for reliable JSON response support
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configure httpx client to fix connection issues in Replit environment
if OPENAI_API_KEY:
    transport = httpx.HTTPTransport(retries=3)
    http_client = httpx.Client(
        http2=False, 
        timeout=15.0, 
        trust_env=False, 
        verify=certifi.where(),
        transport=transport
    )
    openai_client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://api.openai.com/v1",
        http_client=http_client
    )
else:
    openai_client = None

# Mock email data for the inbox manager
EMAILS = [
    {
        "id": 1,
        "sender": "john.doe@company.com",
        "subject": "Website Login Issues",
        "body": "Hi, I'm having trouble logging into my account. The password reset isn't working and I keep getting error messages. This is urgent as I need to access my project files for a client presentation tomorrow. Can someone please help me resolve this quickly?",
        "timestamp": "2025-09-16 09:15:00"
    },
    {
        "id": 2,
        "sender": "billing@stripe.com",
        "subject": "Payment Confirmation - Order #12345",
        "body": "Thank you for your payment of $99.99 for your Pro subscription. Your payment has been successfully processed and your account has been upgraded. Transaction ID: txn_abc123. Your next billing date is October 16, 2025.",
        "timestamp": "2025-09-16 08:30:00"
    },
    {
        "id": 3,
        "sender": "sarah.wilson@marketing.com",
        "subject": "Collaboration Opportunity",
        "body": "Hi there! I hope this email finds you well. I'm reaching out regarding a potential partnership between our companies. We've been following your work and think there could be great synergy. Would you be interested in scheduling a call next week to discuss this further?",
        "timestamp": "2025-09-16 07:45:00"
    },
    {
        "id": 4,
        "sender": "security@bank.com",
        "subject": "Security Alert: Unusual Activity Detected",
        "body": "We've detected unusual login activity on your account from an unrecognized device. If this was you, please ignore this message. If not, please immediately change your password and contact our security team. Location: New York, NY. Time: 2025-09-16 06:30:00 UTC.",
        "timestamp": "2025-09-16 06:35:00"
    },
    {
        "id": 5,
        "sender": "newsletter@techblog.com",
        "subject": "Weekly Tech Roundup - AI Advances",
        "body": "This week in tech: Major breakthroughs in AI safety research, new framework releases from top companies, and insights into the future of machine learning. Click here to read about the latest developments in artificial intelligence and how they might impact your projects.",
        "timestamp": "2025-09-16 06:00:00"
    }
]

# HTML template with Bootstrap styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Inbox Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .email-row:hover {
            background-color: #f8f9fa;
        }
        .analysis-result {
            margin-top: 15px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.375rem;
        }
        .spinner-border-sm {
            width: 1rem;
            height: 1rem;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4">📧 Flask Inbox Manager</h1>
        <p class="text-muted">Manage your emails with AI-powered analysis</p>
        
        <div class="table-responsive">
            <table class="table table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Sender</th>
                        <th>Subject</th>
                        <th>Timestamp</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for email in emails %}
                    <tr class="email-row">
                        <td>{{ email.id }}</td>
                        <td>{{ email.sender }}</td>
                        <td>{{ email.subject }}</td>
                        <td>{{ email.timestamp }}</td>
                        <td>
                            <button 
                                class="btn btn-primary btn-sm" 
                                onclick="analyzeEmail({{ email.id }})"
                                id="btn-{{ email.id }}"
                            >
                                AI Analyze
                            </button>
                        </td>
                    </tr>
                    <tr id="analysis-{{ email.id }}" style="display: none;">
                        <td colspan="5">
                            <div class="analysis-result p-3">
                                <div class="card border-0 bg-light">
                                    <div class="card-body">
                                        <h6 class="card-title text-primary mb-3">🤖 AI Analysis</h6>
                                        
                                        <div class="row">
                                            <div class="col-md-12 mb-3">
                                                <div class="badge bg-info mb-2">Summary</div>
                                                <p id="summary-{{ email.id }}" class="card-text mb-0"></p>
                                            </div>
                                        </div>
                                        
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <div class="badge bg-success mb-2">Intent</div>
                                                <p id="intent-{{ email.id }}" class="card-text mb-0 fw-bold"></p>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <div class="badge bg-warning mb-2">Suggested Action</div>
                                                <p id="action-{{ email.id }}" class="card-text mb-0"></p>
                                            </div>
                                        </div>
                                        
                                        <div class="text-muted small mt-2">
                                            <em>Analysis powered by OpenAI GPT-5</em>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="mt-4">
            <h5>Email Details</h5>
            <div id="email-details" class="card" style="display: none;">
                <div class="card-body">
                    <h6 class="card-title" id="detail-subject"></h6>
                    <p class="card-text"><strong>From:</strong> <span id="detail-sender"></span></p>
                    <p class="card-text"><strong>Time:</strong> <span id="detail-timestamp"></span></p>
                    <p class="card-text"><strong>Body:</strong></p>
                    <p class="card-text" id="detail-body"></p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const emails = {{ emails | tojson }};
        
        async function analyzeEmail(emailId) {
            const button = document.getElementById(`btn-${emailId}`);
            const analysisRow = document.getElementById(`analysis-${emailId}`);
            const summaryEl = document.getElementById(`summary-${emailId}`);
            const intentEl = document.getElementById(`intent-${emailId}`);
            const actionEl = document.getElementById(`action-${emailId}`);
            
            // Show loading state
            button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Analyzing...';
            button.disabled = true;
            
            // Show email details
            const email = emails.find(e => e.id === emailId);
            if (email) {
                document.getElementById('detail-subject').textContent = email.subject;
                document.getElementById('detail-sender').textContent = email.sender;
                document.getElementById('detail-timestamp').textContent = email.timestamp;
                document.getElementById('detail-body').textContent = email.body;
                document.getElementById('email-details').style.display = 'block';
            }
            
            try {
                const response = await fetch(`/summary/${emailId}`);
                const data = await response.json();
                
                // Display the AI analysis in the card layout
                summaryEl.textContent = data.summary || 'No summary available';
                intentEl.textContent = data.intent || 'Unknown';
                actionEl.textContent = data.suggested_action || 'No action suggested';
                
                // Show the analysis row
                analysisRow.style.display = '';
                
                // Reset button
                button.innerHTML = 'AI Analyze';
                button.disabled = false;
                
            } catch (error) {
                console.error('Error:', error);
                
                // Display error in the card layout
                summaryEl.textContent = 'Failed to analyze email - please try again later';
                intentEl.textContent = 'Error';
                actionEl.textContent = 'Check your connection and try again';
                
                // Show the analysis row
                analysisRow.style.display = '';
                
                // Reset button
                button.innerHTML = 'AI Analyze';
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main inbox view with email list"""
    return render_template_string(HTML_TEMPLATE, emails=EMAILS)

@app.route('/summary/<int:email_id>')
def get_email_summary(email_id):
    """Get AI-powered summary of an email"""
    
    # Find the email by ID
    email = next((e for e in EMAILS if e['id'] == email_id), None)
    if not email:
        return jsonify({"error": "Email not found"}), 404
    
    # Check if OpenAI API key is available
    if not OPENAI_API_KEY or not openai_client:
        return jsonify({
            "summary": "AI not available",
            "intent": "N/A", 
            "suggested_action": "Add OPENAI_API_KEY secret in Replit"
        })
    
    try:
        # Debug: Log API key status (but not the key itself)
        print(f"API Key present: {bool(OPENAI_API_KEY)}")
        print(f"API Key length: {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}")
        
        # Prepare the prompt for OpenAI
        prompt = f"""
        Analyze the following email and provide a JSON response with exactly these keys:
        - summary: A 1-2 sentence summary of the email
        - intent: The purpose/type of the email (e.g., "support request", "payment confirmation", "collaboration inquiry", "security alert", "newsletter")
        - suggested_action: A short and practical next step
        
        Email details:
        Subject: {email['subject']}
        Sender: {email['sender']}
        Body: {email['body']}
        
        Respond only with valid JSON in the requested format.
        """
        
        # Call OpenAI API with supported model
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Reliable model with JSON support
            messages=[
                {"role": "system", "content": "You are an email analysis assistant. Always respond with valid JSON in the exact format requested."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI API")
        analysis = json.loads(content)
        
        # Ensure all required keys are present
        result = {
            "summary": analysis.get("summary", "Unable to generate summary"),
            "intent": analysis.get("intent", "Unknown"),
            "suggested_action": analysis.get("suggested_action", "Review email manually")
        }
        
        return jsonify(result)
        
    except Exception as e:
        # Log detailed error for debugging
        print(f"OpenAI API Error: {type(e).__name__}: {str(e)}")
        # Return user-friendly error message
        return jsonify({
            "summary": "AI analysis temporarily unavailable",
            "intent": "Service Error",
            "suggested_action": "Please try again in a moment"
        }), 500

if __name__ == '__main__':
    # Configure Flask to allow all hosts for Replit environment
    app.run(host='0.0.0.0', port=5000, debug=True)