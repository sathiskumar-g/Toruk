let keywords = [];
let currentResults = null;

// Load existing keywords and latest results on page load
window.addEventListener('DOMContentLoaded', () => {
    loadKeywords();
    loadLatestResults();
});

async function loadKeywords() {
    try {
        const response = await fetch('/api/keywords');
        const data = await response.json();
        keywords = data.keywords || [];
        renderKeywords();
    } catch (error) {
        console.error('Failed to load keywords:', error);
    }
}

async function loadLatestResults() {
    try {
        const response = await fetch('/api/results');
        if (response.ok) {
            const data = await response.json();
            currentResults = data;
            displayResults(data);
        } else {
            // No results yet - that's okay
            console.log('No previous results found');
        }
    } catch (error) {
        console.error('Failed to load latest results:', error);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        addKeyword();
    }
}

function addKeyword() {
    const input = document.getElementById('keywordInput');
    const keyword = input.value.trim();
    
    if (keyword && !keywords.includes(keyword)) {
        keywords.push(keyword);
        input.value = '';
        renderKeywords();
        saveKeywords();
    }
}

function removeKeyword(keyword) {
    keywords = keywords.filter(k => k !== keyword);
    renderKeywords();
    saveKeywords();
}

function clearAllKeywords() {
    if (confirm('Remove all keywords?')) {
        keywords = [];
        renderKeywords();
        saveKeywords();
    }
}

function renderKeywords() {
    const list = document.getElementById('keywordsList');
    const count = document.getElementById('keywordCount');
    
    count.textContent = keywords.length;
    
    if (keywords.length === 0) {
        list.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No keywords added yet. Add some above!</p>';
        return;
    }
    
    list.innerHTML = keywords.map(keyword => `
        <div class="keyword-tag">
            <span>${keyword}</span>
            <span class="remove" onclick="removeKeyword('${keyword.replace(/'/g, "\\'")}')">×</span>
        </div>
    `).join('');
}

async function saveKeywords() {
    try {
        await fetch('/api/keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords })
        });
    } catch (error) {
        console.error('Failed to save keywords:', error);
    }
}

async function runResearch() {
    if (keywords.length === 0) {
        alert('Please add at least one keyword first!');
        return;
    }
    
    const limit = parseInt(document.getElementById('limitInput').value) || 5;
    const source = document.getElementById('sourceSelect')?.value || 'reddit';
    const btn = document.getElementById('researchBtn');
    
    // Show loading
    btn.disabled = true;
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    try {
        // Update loading status
        updateLoadingStatus(`Searching ${keywords.length} keywords on ${source}...`);
        
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords, limit, source })
        });
        
        if (!response.ok) {
            throw new Error('Research failed');
        }
        
        const data = await response.json();
        currentResults = data.results;
        
        // Hide loading, show results
        document.getElementById('loadingSection').style.display = 'none';
        displayResults(currentResults);
        
    } catch (error) {
        console.error('Research failed:', error);
        alert('Research failed: ' + error.message);
        document.getElementById('loadingSection').style.display = 'none';
    } finally {
        btn.disabled = false;
    }
}

function updateLoadingStatus(message) {
    document.getElementById('loadingDetail').textContent = message;
}

function displayResults(results) {
    // Update summary cards
    document.getElementById('totalKeywords').textContent = results.total_keywords;
    document.getElementById('totalOpportunities').textContent = results.total_opportunities;
    document.getElementById('allCount').textContent = results.total_opportunities;
    
    const topScore = results.top_10_opportunities.length > 0 
        ? results.top_10_opportunities[0].opportunity_score.total.toFixed(1)
        : '0';
    document.getElementById('topScore').textContent = topScore;
    
    // Render keyword summary table
    renderKeywordSummaryTable(results.keyword_summary);
    
    // Render top opportunities by default
    renderOpportunities(results.top_10_opportunities);
    
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function showTopOpportunities() {
    document.getElementById('topBtn').classList.add('active');
    document.getElementById('allBtn').classList.remove('active');
    renderOpportunities(currentResults.top_10_opportunities);
}

function showAllOpportunities() {
    document.getElementById('allBtn').classList.add('active');
    document.getElementById('topBtn').classList.remove('active');
    renderOpportunities(currentResults.all_opportunities);
}

function renderKeywordSummaryTable(summary) {
    const container = document.getElementById('keywordSummaryTable');
    
    const tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Keyword</th>
                    <th>Posts</th>
                    <th>Problems</th>
                    <th>Opportunities</th>
                    <th>Top Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                ${Object.entries(summary).map(([keyword, data]) => {
                    const hasError = data.error;
                    const statusIcon = hasError ? '⚠️' : (data.opportunities_found > 0 ? '✅' : '⚪');
                    const statusText = hasError ? 'Error' : (data.opportunities_found > 0 ? 'Success' : 'No results');
                    
                    return `
                    <tr ${hasError ? 'style="background: #fff3e0;"' : ''}>
                        <td><strong>${keyword}</strong></td>
                        <td>${data.total_posts}</td>
                        <td>${data.problems_found}</td>
                        <td>${data.opportunities_found}</td>
                        <td><strong>${data.top_opportunity_score.toFixed(1)}</strong></td>
                        <td>${statusIcon} ${statusText}</td>
                    </tr>
                    ${hasError ? `<tr><td colspan="6" style="color: #e65100; font-size: 12px; padding-left: 30px;">Error: ${data.error}</td></tr>` : ''}
                `}).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = tableHTML;
}

function renderOpportunities(opportunities) {
    const container = document.getElementById('opportunitiesList');
    
    if (opportunities.length === 0) {
        container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No opportunities found</p>';
        return;
    }
    
    // Helper function to format text content
    function formatPostContent(text) {
        if (!text) return 'No content available';
        
        // Convert escaped newlines to actual line breaks
        text = text.replace(/\\n/g, '\n');
        
        // Convert markdown bold to HTML
        text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Convert markdown italic to HTML
        text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // Convert newlines to <br> tags
        text = text.replace(/\n/g, '<br>');
        
        // Convert markdown headers to HTML
        text = text.replace(/^# (.+?)(<br>|$)/gm, '<strong style="font-size: 1.2em; display: block; margin: 10px 0 5px 0;">$1</strong>$2');
        text = text.replace(/^## (.+?)(<br>|$)/gm, '<strong style="font-size: 1.1em; display: block; margin: 8px 0 4px 0;">$1</strong>$2');
        text = text.replace(/^### (.+?)(<br>|$)/gm, '<strong style="display: block; margin: 6px 0 3px 0;">$1</strong>$2');
        
        return text;
    }
    
    container.innerHTML = opportunities.map((opp, index) => `
        <div class="opportunity-card">
            <div class="opportunity-rank">#${index + 1}</div>
            <div class="opportunity-header">
                <div class="opportunity-title">
                    <a href="${opp.url}" target="_blank" class="opportunity-link">${opp.original_title}</a>
                </div>
                <div class="opportunity-score">${opp.opportunity_score.total.toFixed(1)}</div>
            </div>
            
            <div class="opportunity-keyword">🔑 ${opp.research_keyword}</div>
            
            <div class="opportunity-problem">
                "${opp.problem_statement}"
            </div>
            
            <div class="post-content-section">
                <h4 style="color: #ffffff; margin: 15px 0 8px 0; font-size: 13px; font-weight: 600;">📄 Post Content:</h4>
                <div class="scrollable-content">${formatPostContent(opp.full_text || opp.problem_statement)}</div>
            </div>
            
            <div class="opportunity-meta">
                <span>👤 u/${opp.author}</span>
                <span>⬆️ ${opp.engagement.reactions} upvotes</span>
                <span>💬 ${opp.engagement.comments} comments</span>
                <span>📂 ${opp.category}</span>
            </div>
            
            <div class="score-breakdown">
                <div class="score-item">
                    <span class="score-label">Pain</span>
                    <span class="score-value">${opp.opportunity_score.pain}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Pervasiveness</span>
                    <span class="score-value">${opp.opportunity_score.pervasiveness}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Proximity</span>
                    <span class="score-value">${opp.opportunity_score.proximity}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Payment</span>
                    <span class="score-value">${opp.opportunity_score.payment}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Plausibility</span>
                    <span class="score-value">${opp.opportunity_score.plausibility}</span>
                </div>
            </div>
            
            ${opp.recommendation ? `
                <div class="opportunity-recommendation">
                    ${opp.recommendation}
                </div>
            ` : ''}
            
            ${opp.solution ? `
                <div class="solution-section">
                    <h3>💡 Proposed Solution</h3>
                    <p class="solution-statement">${opp.solution.statement}</p>
                    
                    <div class="features-grid">
                        <div class="feature-column">
                            <h4>🚀 MVP Features (Start Here)</h4>
                            <ul>
                                ${opp.solution.mvp_features.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="feature-column">
                            <h4>📈 Growth Features (Later)</h4>
                            <ul>
                                ${opp.solution.growth_features.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    
                    <div class="value-proposition">
                        <h4>💰 Value Proposition</h4>
                        <div class="value-grid">
                            <div class="value-item">
                                <span class="value-icon">⏰</span>
                                <span class="value-text">${opp.solution.value_proposition.time}</span>
                            </div>
                            <div class="value-item">
                                <span class="value-icon">💵</span>
                                <span class="value-text">${opp.solution.value_proposition.money}</span>
                            </div>
                            <div class="value-item">
                                <span class="value-icon">⚡</span>
                                <span class="value-text">${opp.solution.value_proposition.effort}</span>
                            </div>
                        </div>
                    </div>
                </div>
            ` : ''}
            
            ${opp.validation && opp.business ? `
                <div class="validation-section">
                    <h3>✅ Validation & Business Viability</h3>
                    
                    <div class="validation-grid">
                        <div class="validation-item">
                            <strong>🎯 Market Size:</strong> ${opp.validation.market_size}
                        </div>
                        <div class="validation-item">
                            <strong>🏆 Competition:</strong> ${opp.validation.competition}
                        </div>
                        <div class="validation-item">
                            <strong>⏱️ Time to Market:</strong> ${opp.validation.time_to_market}
                        </div>
                        <div class="validation-item">
                            <strong>💸 Pricing Model:</strong> ${opp.business.pricing_model}
                        </div>
                    </div>
                    
                    <div class="revenue-section">
                        <h4>💰 Revenue Potential</h4>
                        <div class="revenue-grid">
                            <div class="revenue-item">
                                <span class="revenue-label">Monthly</span>
                                <span class="revenue-value">${opp.business.monthly_revenue}</span>
                            </div>
                            <div class="revenue-item">
                                <span class="revenue-label">Annual</span>
                                <span class="revenue-value">${opp.business.annual_revenue}</span>
                            </div>
                            <div class="revenue-item">
                                <span class="revenue-label">LTV:CAC Ratio</span>
                                <span class="revenue-value">${opp.business.unit_economics.ltv_cac_ratio}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="customers-section">
                        <h4>🎯 Target Customers</h4>
                        <div class="customer-tags">
                            ${opp.business.target_customers.map(c => `<span class="customer-tag">${c}</span>`).join('')}
                        </div>
                    </div>
                    
                    <div class="gtm-section">
                        <h4>🚀 Go-to-Market Strategy</h4>
                        <p>${opp.business.go_to_market}</p>
                    </div>
                    
                    ${opp.validation.risk_factors && opp.validation.risk_factors.length > 0 ? `
                        <div class="risks-section">
                            <h4>⚠️ Risk Factors</h4>
                            <ul>
                                ${opp.validation.risk_factors.map(r => `<li>${r}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            ` : ''}
            
            ${opp.roadmap ? `
                <div class="roadmap-section">
                    <h3>🗺️ Product Roadmap</h3>
                    <div class="phase-grid">
                        <div class="phase-card">
                            <div class="phase-header phase-1">
                                <h4>Phase 1: ${opp.roadmap.phase_1.name}</h4>
                                <span class="phase-timeline">${opp.roadmap.phase_1.timeline}</span>
                            </div>
                            <p class="phase-goal"><strong>Goal:</strong> ${opp.roadmap.phase_1.goal}</p>
                            <ul class="phase-features">
                                ${opp.roadmap.phase_1.features.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                            <p class="phase-metrics"><strong>Metrics:</strong> ${opp.roadmap.phase_1.metrics}</p>
                        </div>
                        <div class="phase-card">
                            <div class="phase-header phase-2">
                                <h4>Phase 2: ${opp.roadmap.phase_2.name}</h4>
                                <span class="phase-timeline">${opp.roadmap.phase_2.timeline}</span>
                            </div>
                            <p class="phase-goal"><strong>Goal:</strong> ${opp.roadmap.phase_2.goal}</p>
                            <ul class="phase-features">
                                ${opp.roadmap.phase_2.features.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                            <p class="phase-metrics"><strong>Metrics:</strong> ${opp.roadmap.phase_2.metrics}</p>
                        </div>
                        <div class="phase-card">
                            <div class="phase-header phase-3">
                                <h4>Phase 3: ${opp.roadmap.phase_3.name}</h4>
                                <span class="phase-timeline">${opp.roadmap.phase_3.timeline}</span>
                            </div>
                            <p class="phase-goal"><strong>Goal:</strong> ${opp.roadmap.phase_3.goal}</p>
                            <ul class="phase-features">
                                ${opp.roadmap.phase_3.features.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                            <p class="phase-metrics"><strong>Metrics:</strong> ${opp.roadmap.phase_3.metrics}</p>
                        </div>
                    </div>
                </div>
            ` : ''}

           
        </div>
    `).join('');
}

//  ${(opp.competitors && opp.competitors.length > 0) ? `
//                 <div class="competitors-section">
//                     <h3>🔎 Competitors / Existing Products</h3>
//                     <ul class="competitors-list">
//                         ${opp.competitors.map(c => `<li><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></li>`).join('')}
//                     </ul>
//                 </div>
//             ` : ''}

function exportResults() {
    if (!currentResults) {
        alert('No results to export');
        return;
    }
    
    const dataStr = JSON.stringify(currentResults, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reddit_research_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
}
