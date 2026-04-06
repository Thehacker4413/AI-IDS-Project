document.addEventListener('DOMContentLoaded', () => {
    // Basic Routing/Tabs
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Update active nav
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            
            // Update active content
            tabContents.forEach(tc => tc.classList.remove('active'));
            const targetId = item.getAttribute('data-target');
            const content = document.getElementById(targetId);
            if(content) content.classList.add('active');
            
            // Update Title
            const ts = {
                'overview': 'System Overview',
                'manual': 'Manual Intrusion Test',
                'batch': 'Batch CSV Evaluation',
                'realtime': 'Live Stream Traffic'
            };
            document.getElementById('page-title').innerText = ts[targetId];
        });
    });

    try {
        loadOverviewStats();
    } catch(e) {
        console.error('Stats loading failed:', e);
    }

    async function loadOverviewStats() {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();
            
            document.getElementById('overview-model-name').innerText = data.model_name;
            document.getElementById('overview-accuracy').innerText = data.accuracy;
            
            const labels = Object.keys(data.distribution);
            const values = Object.values(data.distribution);
            initChart(labels, values);
        } catch(e) {
            initChart(['Normal', 'DoS', 'Probe', 'R2L', 'U2R'], [67343, 45927, 11656, 995, 52]);
        }
    }

    // Manual Prediction
    document.getElementById('btn-manual-predict').addEventListener('click', async () => {
        const form = document.getElementById('manual-form');
        const inputs = form.querySelectorAll('input');
        const data = {};
        
        let hasData = false;
        inputs.forEach(i => {
            if(i.value.trim() !== '') {
                data[i.name] = i.value;
                hasData = true;
            }
        });
        
        if(!hasData) return alert('Please enter at least one value.');
        
        const btn = document.getElementById('btn-manual-predict');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing';
        btn.disabled = true;

        try {
            const res = await fetch('/predict/manual', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            
            const resDiv = document.getElementById('manual-result');
            resDiv.classList.remove('hidden');
            
            if(result.error) {
                resDiv.innerHTML = `<p class="text-red"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${result.error}</p>`;
            } else {
                let colorClass = result.attack_type === 'Normal' ? 'text-green' : 'text-red';
                let iconClass = result.attack_type === 'Normal' ? 'fa-check-circle' : 'fa-skull-crossbones';
                
                resDiv.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <h4 style="margin-bottom:8px; color: #94a3b8;">Evaluation Result</h4>
                            <div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;" class="${colorClass}">
                                <i class="fa-solid ${iconClass}"></i> ${result.attack_type}
                            </div>
                            <p style="font-size: 14px; opacity: 0.8;">Risk Level: ${result.risk_level}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-size: 12px; color: #94a3b8; margin-bottom: 4px;">Confidence Score</p>
                            <div style="font-size: 32px; font-weight: 800; font-family: monospace;">${result.confidence}</div>
                        </div>
                    </div>
                `;
            }
        } catch(err) {
            console.error(err);
        } finally {
            btn.innerHTML = originalHtml;
            btn.disabled = false;
        }
    });

    // File Upload Handler
    const fileInput = document.getElementById('batch-file');
    const uploaderBtn = document.getElementById('btn-batch-upload');
    const fileNameDiv = document.getElementById('file-name');

    fileInput.addEventListener('change', (e) => {
        if(e.target.files.length > 0) {
            fileNameDiv.innerText = e.target.files[0].name;
            uploaderBtn.disabled = false;
        } else {
            uploaderBtn.disabled = true;
        }
    });

    uploaderBtn.addEventListener('click', async () => {
        if(!fileInput.files.length) return;
        
        uploaderBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        uploaderBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const res = await fetch('/predict/batch', { method: 'POST', body: formData });
            const result = await res.json();
            
            document.getElementById('batch-results').classList.remove('hidden');
            if(result.error) {
                 document.getElementById('batch-results').innerHTML = `<p class="text-red">Error: ${result.error}</p>`;
                 return;
            }
            
            document.getElementById('batch-total').innerText = result.total;
            
            // Chips
            const chipsDiv = document.getElementById('batch-summary-chips');
            chipsDiv.innerHTML = '';
            for(let key in result.summary) {
                let cl = key === 'Normal' ? 'bad-normal' : `bad-${key.toLowerCase()}`;
                chipsDiv.innerHTML += `<span class="badge ${cl}">${key}: ${result.summary[key]}</span>`;
            }

            // Table
            const tbody = document.getElementById('batch-table-body');
            tbody.innerHTML = '';
            result.details.forEach(r => {
                let colorClass = r.type === 'Normal' ? 'text-green' : 'text-red';
                tbody.innerHTML += `
                    <tr>
                        <td>#${r.id}</td>
                        <td class="${colorClass}" style="font-weight: 600;">${r.type}</td>
                        <td>${r.risk}</td>
                    </tr>
                `;
            });
            
            if(result.details.length < result.total) {
                tbody.innerHTML += `<tr><td colspan="3" class="text-center text-gray">... showing first 100 rows ...</td></tr>`;
            }
            
        } catch (e) {
            alert('Upload failed.');
        } finally {
            uploaderBtn.innerHTML = '<i class="fa-solid fa-play"></i> Process Batch';
            uploaderBtn.disabled = false;
        }
    });

    // Real-time Stream Simulation
    let streamInterval = null;
    const btnStream = document.getElementById('btn-toggle-stream');
    const logWindow = document.getElementById('live-stream-log');

    function addLogLine(msg, isWarn, isSafe) {
        let cls = 'log-line';
        if(isWarn) cls += ' log-warn';
        if(isSafe) cls += ' log-safe';
        
        const line = document.createElement('div');
        line.className = cls;
        line.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
        logWindow.appendChild(line);
        logWindow.scrollTop = logWindow.scrollHeight; // auto-scroll
    }

    btnStream.addEventListener('click', () => {
        if(streamInterval) {
            clearInterval(streamInterval);
            streamInterval = null;
            btnStream.innerHTML = '<i class="fa-solid fa-play"></i> Start Stream';
            btnStream.className = 'btn-danger';
            addLogLine('> Stream paused.', false, false);
            document.querySelector('.status-dot').classList.remove('green-pulse');
            document.getElementById('status-text').innerText = 'System Paused';
        } else {
            addLogLine('> Initializing packet sniffer on port 21/80/443...', false, false);
            btnStream.innerHTML = '<i class="fa-solid fa-stop"></i> Stop Stream';
            btnStream.className = 'btn-secondary';
            document.querySelector('.status-dot').classList.add('green-pulse');
            document.getElementById('status-text').innerText = 'Live Feed Active';
            
            streamInterval = setInterval(async () => {
                try {
                    const res = await fetch('/simulate/stream');
                    const data = await res.json();
                    
                    if(data.error) {
                        addLogLine(`Error fetching stream: ${data.error}`, true, false);
                        clearInterval(streamInterval);
                        return;
                    }
                    
                    let msg = `Incoming: PROTO=${data.protocol} | SRC_BYTES=${data.source_bytes} | DST_BYTES=${data.destination_bytes} | PRED=${data.predicted_attack}`;
                    addLogLine(msg, data.predicted_attack !== 'Normal', data.predicted_attack === 'Normal');
                    
                    // Update header counters simulated
                    let tc = document.getElementById('traffic-count');
                    tc.innerText = (parseFloat(tc.innerText) + 0.1).toFixed(1) + 'K';
                    
                    if(data.predicted_attack !== 'Normal') {
                        let th = document.getElementById('threat-count');
                        th.innerText = parseInt(th.innerText.replace(',', '')) + 1;
                    }
                    
                } catch(e) {
                    console.log('Stream error', e);
                }
            }, 1000);
        }
    });

    // Pie chart mapping
    function initChart(labels_arr, data_arr) {
        const ctx = document.getElementById('attackPieChart').getContext('2d');
        
        // Match colors to exact labels
        const colorMap = {
            'Normal': '#10b981',
            'DoS': '#ef4444',
            'Probe': '#f59e0b',
            'R2L': '#ec4899',
            'U2R': '#8b5cf6'
        }
        
        const colors = labels_arr.map(L => colorMap[L] || '#64748b');

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels_arr,
                datasets: [{
                    data: data_arr,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#94a3b8', font: {family: 'Inter'} }
                    }
                },
                cutout: '75%'
            }
        });
    }
});
