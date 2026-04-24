// ── STATE ────────────────────────────────────────
const state = {
    isLoading: false,
    theme: localStorage.getItem('theme') || 'light',
};

// ── DOM ELEMENTS ─────────────────────────────────
const chatArea      = document.getElementById('chatArea');
const messages      = document.getElementById('messages');
const userInput     = document.getElementById('userInput');
const sendBtn       = document.getElementById('sendBtn');
const themeToggle   = document.getElementById('themeToggle');
const welcomeScreen = document.getElementById('welcomeScreen');
const newChatBtn    = document.getElementById('newChatBtn');
const clearBtn      = document.getElementById('clearBtn');

// ── INIT ─────────────────────────────────────────
document.documentElement.setAttribute('data-theme', state.theme);
updateThemeIcon();

// ── THEME ─────────────────────────────────────────
themeToggle.addEventListener('click', () => {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('theme', state.theme);
    updateThemeIcon();
});

function updateThemeIcon() {
    const icon = themeToggle.querySelector('.theme-icon');
    icon.textContent = state.theme === 'light' ? '☽' : '☀';
}

// ── INPUT AUTO RESIZE ────────────────────────────
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 200) + 'px';
});

// ── KEYBOARD SHORTCUTS ───────────────────────────
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// ── SEND BUTTON ──────────────────────────────────
sendBtn.addEventListener('click', sendMessage);

// ── NEW CHAT ─────────────────────────────────────
newChatBtn.addEventListener('click', clearChat);
clearBtn.addEventListener('click', clearChat);

function clearChat() {
    messages.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    userInput.value = '';
    userInput.style.height = 'auto';
}

// ── USE SUGGESTION ───────────────────────────────
function useSuggestion(btn) {
    const text = btn.querySelector('span:last-child').textContent;
    userInput.value = text;
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
    sendMessage();
}

// ── SEND MESSAGE ─────────────────────────────────
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || state.isLoading) return;

    // Hide welcome screen
    welcomeScreen.style.display = 'none';

    // Add user message
    appendUserMessage(message);

    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';

    // Show loading
    const loadingEl = appendLoading();
    state.isLoading = true;
    sendBtn.disabled = true;

    try {
        // Call API
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Remove loading
        loadingEl.remove();

        if (data.success) {
            appendAIMessage(data);
        } else {
            appendError(data.error || 'Something went wrong');
        }

    } catch (error) {
        loadingEl.remove();
        appendError('Network error. Please try again.');
    } finally {
        state.isLoading = false;
        sendBtn.disabled = false;
        scrollToBottom();
    }
}

// ── APPEND USER MESSAGE ──────────────────────────
function appendUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message-user';
    div.innerHTML = `
        <div class="user-bubble">${escapeHtml(text)}</div>
    `;
    messages.appendChild(div);
    scrollToBottom();
}

// ── APPEND LOADING ───────────────────────────────
function appendLoading() {
    const div = document.createElement('div');
    div.className = 'message-ai';
    div.innerHTML = `
        <div class="ai-header">
            <div class="ai-avatar">◆</div>
            <span class="ai-name">Smart AI</span>
        </div>
        <div class="ai-bubble">
            <div class="processing-steps">
                <div class="step active" id="step1">
                    <span class="step-icon">○</span>
                    <span>Detecting task type...</span>
                </div>
                <div class="step" id="step2">
                    <span class="step-icon">○</span>
                    <span>Calling best AI models in parallel...</span>
                </div>
                <div class="step" id="step3">
                    <span class="step-icon">○</span>
                    <span>Combining into expert answer...</span>
                </div>
            </div>
        </div>
    `;
    messages.appendChild(div);
    scrollToBottom();

    // Animate steps
    setTimeout(() => {
        const s1 = div.querySelector('#step1');
        if (s1) {
            s1.classList.add('done');
            s1.querySelector('.step-icon').textContent = '✓';
        }
        const s2 = div.querySelector('#step2');
        if (s2) s2.classList.add('active');
    }, 800);

    setTimeout(() => {
        const s2 = div.querySelector('#step2');
        if (s2) {
            s2.classList.add('done');
            s2.querySelector('.step-icon').textContent = '✓';
        }
        const s3 = div.querySelector('#step3');
        if (s3) s3.classList.add('active');
    }, 2000);

    return div;
}

// ── APPEND AI MESSAGE ────────────────────────────
function appendAIMessage(data) {
    const div = document.createElement('div');
    div.className = 'message-ai';

    // Build support answers HTML
    let supportHTML = '';
    if (data.support_answers &&
        Object.keys(data.support_answers).length > 0) {

        // Lead answer block
        supportHTML += `
            <div class="raw-model-block">
                <div class="raw-model-name">
                    ${data.lead_model}
                    <span class="lead-tag">lead</span>
                </div>
                <div class="raw-model-answer">${
                    escapeHtml(data.lead_answer || '')
                }</div>
            </div>
        `;

        // Support answers
        for (const [model, answer] of
            Object.entries(data.support_answers)) {
            if (!answer.includes('Error')) {
                supportHTML += `
                    <div class="raw-model-block">
                        <div class="raw-model-name">
                            ${model}
                            <span class="support-tag">support</span>
                        </div>
                        <div class="raw-model-answer">${
                            escapeHtml(answer)
                        }</div>
                    </div>
                `;
            }
        }
    }

    div.innerHTML = `
        <div class="ai-header">
            <div class="ai-avatar">◆</div>
            <span class="ai-name">Smart AI Expert</span>
        </div>

        <div class="ai-bubble">
            ${formatMarkdown(data.final_answer)}
        </div>

        <div class="answer-meta">
            <span class="meta-badge intent">
                ${getIntentIcon(data.intent)} ${data.intent}
            </span>
            <span class="meta-badge lead">
                ◆ ${data.lead_model}
            </span>
        </div>

        <div class="answer-actions">
            <button class="action-btn"
                onclick="copyAnswer(this, \`${
                    escapeTick(data.final_answer)
                }\`)">
                Copy answer
            </button>
            ${supportHTML ? `
            <button class="action-btn"
                onclick="toggleRaw(this)">
                Show model answers
            </button>
            ` : ''}
        </div>

        ${supportHTML ? `
        <div class="raw-answers" style="display:none">
            <button class="raw-answers-toggle"
                onclick="toggleRawContent(this)">
                <span>Individual model answers</span>
                <span>▾</span>
            </button>
            <div class="raw-answers-content">
                ${supportHTML}
            </div>
        </div>
        ` : ''}
    `;

    messages.appendChild(div);
    scrollToBottom();
}

// ── APPEND ERROR ─────────────────────────────────
function appendError(message) {
    const div = document.createElement('div');
    div.className = 'message-ai';
    div.innerHTML = `
        <div class="ai-header">
            <div class="ai-avatar">◆</div>
            <span class="ai-name">Smart AI Expert</span>
        </div>
        <div class="ai-bubble" style="color: #ef4444;">
            ⚠ ${escapeHtml(message)}
        </div>
    `;
    messages.appendChild(div);
}

// ── COPY ANSWER ──────────────────────────────────
function copyAnswer(btn, text) {
    navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = 'Copy answer';
            btn.classList.remove('copied');
        }, 2000);
    });
}

// ── TOGGLE RAW ANSWERS ───────────────────────────
function toggleRaw(btn) {
    const messageEl = btn.closest('.message-ai');
    const rawEl = messageEl.querySelector('.raw-answers');
    if (!rawEl) return;

    const isHidden = rawEl.style.display === 'none';
    rawEl.style.display = isHidden ? 'block' : 'none';
    btn.textContent = isHidden
        ? 'Hide model answers'
        : 'Show model answers';
}

function toggleRawContent(btn) {
    const content = btn.nextElementSibling;
    content.classList.toggle('open');
    const arrow = btn.querySelector('span:last-child');
    arrow.textContent = content.classList.contains('open') ? '▴' : '▾';
}

// ── HELPERS ──────────────────────────────────────
function scrollToBottom() {
    setTimeout(() => {
        chatArea.scrollTop = chatArea.scrollHeight;
    }, 50);
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function escapeTick(text) {
    return String(text).replace(/`/g, '\\`');
}

function getIntentIcon(intent) {
    const icons = {
        'CODING':           '{ }',
        'COMPLEX_LOGIC':    '∑',
        'CREATIVE_WRITING': '✦',
        'DATA_ANALYSIS':    '◎',
        'QUICK_ANSWER':     '⚡',
        'GENERAL':          '◈',
    };
    return icons[intent] || '◈';
}

function formatMarkdown(text) {
    return String(text)
        // Code blocks
        .replace(/```(\w+)?\n([\s\S]*?)```/g,
            '<pre><code>$2</code></pre>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Bold
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        // Headers
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
        .replace(/^# (.+)$/gm,   '<h1>$1</h1>')
        // Lists
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}