from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import os

YOU_API_KEY = os.getenv("YOU_API_KEY", "ydc-sk-fef5ec29a1fdd9b1-pxy1kM4juRSUqSTirF7ng7fh12hxp2G1-e467f801<__>1SNetLETU8N2v5f4Zab03FiX")
YOU_API_URL = "https://api.you.com/v1/agents/runs"

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AutoBrand Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
        .pulse { animation: pulse 2s infinite; }
    </style>
</head>
<body class="gradient-bg min-h-screen p-8">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-6xl font-bold text-white mb-4">✨ AutoBrand Studio</h1>
            <p class="text-2xl text-blue-100">AI Marketing Pipeline • You.com Powered</p>
        </div>

        <div id="input" class="card rounded-3xl p-8 border border-white/20 mb-8">
            <h2 class="text-3xl font-bold text-white mb-6">Tell us about your brand</h2>
            <input id="brand" placeholder="Brand Name (e.g., Tesla)" 
                class="w-full px-6 py-4 rounded-xl bg-white/20 text-white text-lg placeholder-white/50 border-2 border-white/30 mb-4">
            <textarea id="desc" rows="4" placeholder="Brand description, audience, values..." 
                class="w-full px-6 py-4 rounded-xl bg-white/20 text-white text-lg placeholder-white/50 border-2 border-white/30 mb-4"></textarea>
            <button onclick="run()" id="btn"
                class="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white py-5 rounded-xl font-bold text-xl hover:from-pink-600 hover:to-purple-700">
                🎬 Run Pipeline
            </button>
        </div>

        <div id="progress" class="hidden card rounded-3xl p-8 border border-white/20 mb-8">
            <h2 class="text-2xl font-bold text-white mb-4">Processing...</h2>
            <div id="status" class="text-white text-lg"></div>
        </div>

        <div id="results" class="hidden space-y-4"></div>
    </div>

    <script>
        async function call(step, prompt) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="pulse">🔄 ${step}...</div>`;
            
            const res = await fetch('/api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt})
            });
            
            if (!res.ok) {
                const error = await res.text();
                throw new Error(`API Error: ${error}`);
            }
            
            const data = await res.json();
            console.log('Response:', data);
            
            if (!data.success) throw new Error(data.error);
            if (!data.content || data.content === 'Generated content') {
                throw new Error('API returned empty content');
            }
            
            return data.content;
        }

        async function run() {
            const brand = document.getElementById('brand').value.trim();
            const desc = document.getElementById('desc').value.trim();
            if (!brand || !desc) return alert('Fill in both fields!');

            document.getElementById('btn').disabled = true;
            document.getElementById('input').classList.add('hidden');
            document.getElementById('progress').classList.remove('hidden');

            try {
                const r = {};
                
                r.trends = await call('Analyzing Trends', 
                    `You are a marketing analyst. List exactly 3 specific viral marketing trends for the ${brand} brand (${desc}) in 2025 for TikTok and Instagram Reels. Be specific and actionable.`);
                
                r.ideas = await call('Creating Ideas', 
                    `You are a content strategist. Based on these trends for ${brand}:\n${r.trends}\n\nGenerate exactly 3 viral short-form video ideas. Number them 1, 2, 3.`);
                
                r.script = await call('Writing Script', 
                    `You are a scriptwriter. Write a complete 30-second video script for ${brand} (${desc}). Use this format:\n\nHOOK (0-5s): [attention grabber]\nBODY (5-20s): [main content]\nCTA (20-30s): [call to action]\n\nBased on: ${r.ideas.substring(0,300)}`);
                
                r.thumbnail = await call('Designing Thumbnail', 
                    `You are a thumbnail designer. Describe a viral thumbnail design for this ${brand} video:\n${r.script.substring(0,300)}\n\nInclude: visual elements, text, colors.`);
                
                r.video = await call('Planning Video', 
                    `You are a video editor. Create a detailed editing plan for this ${brand} 30-second video:\n${r.script.substring(0,400)}\n\nInclude scene breakdown, transitions, and effects.`);
                
                r.abtest = await call('A/B Testing', 
                    `You are a growth analyst. Design an A/B testing plan for ${brand} content on TikTok and Reels. Include 2 variants, metrics, and success criteria.`);

                document.getElementById('progress').classList.add('hidden');
                const div = document.getElementById('results');
                div.classList.remove('hidden');
                div.innerHTML = Object.entries({
                    '📊 Trends': r.trends,
                    '💡 Ideas': r.ideas,
                    '✍️ Script': r.script,
                    '🎨 Thumbnail': r.thumbnail,
                    '🎬 Video': r.video,
                    '📈 A/B Test': r.abtest
                }).map(([k,v]) => `
                    <div class="card rounded-2xl p-6 border border-white/20">
                        <h3 class="text-2xl font-bold text-white mb-3">${k}</h3>
                        <div class="text-gray-100 text-lg whitespace-pre-wrap leading-relaxed">${v}</div>
                    </div>
                `).join('') + `
                    <button onclick="location.reload()" 
                        class="w-full bg-green-600 text-white py-4 rounded-xl font-bold text-xl hover:bg-green-700">
                        Create Another ↻
                    </button>
                `;
            } catch(e) {
                alert('Error: ' + e.message + '\\n\\nCheck the terminal for details.');
                location.reload();
            }
        }
    </script>
</body>
</html>'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path == '/api':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            prompt = data.get('prompt', '')
            
            try:
                print(f"\n{'='*60}")
                print(f"Prompt: {prompt[:150]}...")
                print(f"{'='*60}")
                
                # Try with streaming
                response = requests.post(
                    YOU_API_URL,
                    headers={
                        'Authorization': f'Bearer {YOU_API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'agent': 'advanced',
                        'input': prompt,
                        'stream': True  # Enable streaming
                    },
                    stream=True,
                    timeout=90
                )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Collect streaming response
                    full_content = []
                    for line in response.iter_lines():
                        if line:
                            line_text = line.decode('utf-8')
                            if line_text.startswith('data: '):
                                try:
                                    event_data = json.loads(line_text[6:])
                                    if event_data.get('type') == 'response.output_text.delta':
                                        delta = event_data.get('response', {}).get('delta', '')
                                        if delta:
                                            full_content.append(delta)
                                            print(delta, end='', flush=True)
                                except:
                                    pass
                    
                    content = ''.join(full_content)
                    print(f"\n\nTotal content length: {len(content)} characters")
                    
                    if not content:
                        print("WARNING: Empty content received!")
                        content = "Error: API returned empty response. Check API key and quota."
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'content': content}).encode())
                else:
                    error_text = response.text
                    print(f"API Error Response: {error_text}")
                    raise Exception(f"API returned {response.status_code}: {error_text}")
                    
            except Exception as e:
                print(f"Exception: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    PORT = 8080
    print(f"🚀 AutoBrand Studio (Streaming) running at http://localhost:{PORT}")
    print(f"🔑 Using API Key: {YOU_API_KEY[:30]}...")
    print(f"📱 Open http://localhost:{PORT} in your browser\n")
    
    server = HTTPServer(('localhost', PORT), Handler)
    server.serve_forever()