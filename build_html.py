import json, os

with open(r'C:\Users\Win 10\.gemini\antigravity\scratch\liga1-bet-tracker\liga1_master_data.json', encoding='utf-8') as f:
    master_data = json.load(f)

teams_json = json.dumps(master_data['teams'], ensure_ascii=False)
fixtures_json = json.dumps(master_data['fixtures'], ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LIGA 1 INDONESIA — Smart Betting Terminal & Bankroll Tracker</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --background: #f8fafc;
      --foreground: #0f172a;
      --card: #ffffff;
      --border: #e2e8f0;
      --muted: #f1f5f9;
      --muted-foreground: #64748b;
      --primary: #1d4ed8;
      --accent: #f8fafc;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --background: #090d16;
        --foreground: #f1f5f9;
        --card: #0f172a;
        --border: #1e293b;
        --muted: #1e293b;
        --muted-foreground: #94a3b8;
        --primary: #3b82f6;
        --accent: #0f172a;
      }
    }
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--background); color: var(--foreground); }
    html, body {
      max-width: 100vw;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }
    *, *::before, *::after {
      box-sizing: border-box;
    }
    .tab-bar-container {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding-bottom: 2px;
    }
    .tab-bar-container::-webkit-scrollbar { display: none; }
    .tab-bar { 
      display: flex; 
      background: var(--muted); 
      padding: 3px; 
      border-radius: 12px; 
      gap: 3px; 
      border: 1px solid var(--border);
      width: max-content;
      min-width: 100%;
    }
    .tab-btn { 
      padding: 7px 13px; 
      border-radius: 9px; 
      font-size: 12px; 
      font-weight: 700; 
      color: var(--muted-foreground); 
      transition: all 0.15s; 
      cursor: pointer; 
      white-space: nowrap; 
      flex-shrink: 0;
      user-select: none;
    }
    .tab-btn:hover { color: var(--foreground); }
    .tab-btn.active { background: var(--card); color: var(--foreground); box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .scrollbar-none {
      scrollbar-width: none;
      -ms-overflow-style: none;
    }
    .scrollbar-none::-webkit-scrollbar { display: none; }
    @media (max-width: 640px) {
      body { padding: 8px !important; }
      .tab-btn { padding: 6px 11px !important; font-size: 11px !important; }
      /* Mencegah auto-zoom di browser iOS iPhone saat tap input */
      input, select, textarea { font-size: 16px !important; }
      .btn-sm { padding: 5px 8px !important; font-size: 11px !important; }
    }
    .chip { cursor: pointer; padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 600; border: 1px solid var(--border); background: var(--card); color: var(--muted-foreground); transition: all 0.15s; white-space: nowrap; }
    .chip:hover:not(.active) { background: var(--muted); color: var(--foreground); }
    .chip.active { background: #1d4ed8 !important; color: #ffffff !important; border-color: #1d4ed8 !important; font-weight: 700; box-shadow: 0 2px 8px rgba(29,78,216,0.3); }
    .btn-primary { background: #1d4ed8; color: white; font-weight: 700; border-radius: 8px; transition: all 0.15s; cursor: pointer; }
    .btn-primary:hover { background: #1e40af; }
    .btn-sm { background: var(--card); border: 1px solid var(--border); border-radius: 8px; font-weight: 600; padding: 5px 10px; font-size: 11.5px; transition: all 0.15s; cursor: pointer; }
    .btn-sm:hover { background: var(--muted); }
    .market-pill { cursor: pointer; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid var(--border); background: var(--muted); transition: all 0.12s; }
    .market-pill:hover { border-color: var(--primary); background: rgba(29, 78, 216, 0.08); color: var(--primary); }
    .pulse-dot { animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} }
    .custom-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scroll::-webkit-scrollbar-track { background: transparent; }
    .custom-scroll::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.4); border-radius: 999px; }
  </style>
</head>
<body class="p-2 sm:p-5 min-h-screen overflow-x-hidden">
<div class="max-w-5xl mx-auto space-y-3 sm:space-y-4 w-full overflow-hidden">

  <!-- HEADER -->
  <header class="flex flex-col sm:flex-row items-stretch sm:items-start justify-between gap-3 pb-2 border-b border-[var(--border)]">
    <div class="min-w-0">
      <div class="flex items-center gap-2.5">
        <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center p-1.5 border border-[var(--border)] shrink-0 shadow-2xs">
          <img src="https://r2.thesportsdb.com/images/media/league/badge/qoz13e1630265283.png" class="w-full h-full object-contain" alt="Liga 1 Indonesia" onerror="this.src='https://media.api-sports.io/football/teams/10134.png'" />
        </div>
        <div class="min-w-0">
          <h1 class="text-base sm:text-lg font-black tracking-tight flex items-center gap-2 flex-wrap">
            <span>LIGA 1 INDONESIA</span>
            <span class="text-[9.5px] bg-emerald-600 text-white px-2 py-0.5 rounded-md font-extrabold tracking-wide uppercase shrink-0">Smart Bet Terminal</span>
          </h1>
          <p class="text-[11px] text-[var(--muted-foreground)] truncate">BRI Super League 2026/27 · 18 Klub Profesional · Analisis Empiris &amp; Bankroll Tracker</p>
        </div>
      </div>
      <div class="flex items-center gap-1.5 sm:gap-2 mt-2 flex-wrap text-xs">
        <div class="flex items-center gap-1.5 text-[11px] text-[var(--muted-foreground)]">
          <span class="w-2 h-2 rounded-full bg-emerald-500 pulse-dot inline-block shrink-0"></span>
          <span id="status-text">Live API TheSportsDB</span>
        </div>
        <span class="text-[10px] text-slate-300 dark:text-slate-600 hidden xs:inline">•</span>
        <span id="header-1xbet-badge" onclick="openOddsModal()" style="cursor:pointer" class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10.5px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 hover:bg-emerald-200 transition-all shadow-2xs cursor-pointer" title="Klik untuk rincian feed 1xBet &amp; sinkronisasi odds">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shrink-0"></span>
          <span id="header-1xbet-text">1xBet Feed: Sinyal Khusus Odds Rilis Resmi</span>
        </span>
        <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10.5px] font-bold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300 dark:border-blue-800 shadow-2xs" title="Auto-Refresh real-time setiap 60 detik">
          <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse shrink-0"></span>
          <span>Auto-Sync (60s)</span>
        </span>
      </div>
    </div>

    <!-- MAIN BETTING TABS (Touch swipeable on mobile) -->
    <nav class="tab-bar-container">
      <div class="tab-bar">
        <button class="tab-btn active" onclick="setMainTab('standings')" id="main-tab-standings">🏆 Klasemen &amp; Peluang Juara</button>
        <button class="tab-btn" onclick="setMainTab('fixtures')" id="main-tab-fixtures">⚔️ Jadwal &amp; Hasil (Live)</button>
        <button class="tab-btn" onclick="setMainTab('bet')" id="main-tab-bet">💡 Sinyal &amp; Bankroll</button>
        <button class="tab-btn" onclick="setMainTab('history')" id="main-tab-history">📜 Histori Sinyal (4 Hari)</button>
        <button class="tab-btn" onclick="setMainTab('compound')" id="main-tab-compound">📈 Rolling Compound (DNB)</button>
        <button class="tab-btn" onclick="setMainTab('parlay')" id="main-tab-parlay">🎯 Smart Parlay</button>
      </div>
    </nav>
  </header>

  <!-- QUICK MATCH & ROUND SELECTOR CHIPS -->
  <div class="p-2 sm:p-2.5 rounded-xl border border-[var(--border)] bg-[var(--card)] shadow-2xs">
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2">
      <div class="flex items-center gap-1.5 overflow-x-auto scrollbar-none pb-0.5">
        <span class="chip active text-xs shrink-0" id="chip-filter-all">⭐ Semua Odds 1xBet Rilis (Pekan Ini)</span>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn-sm text-xs flex-1 sm:flex-none text-center" onclick="openOddsModal()">🎰 Pasaran &amp; API Odds</button>
        <button class="btn-sm text-xs flex-1 sm:flex-none text-center" id="btn-sync-data" onclick="syncLiga1Odds(true)">🔄 Segarkan Data</button>
      </div>
    </div>
  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB 1: TRACKER BET & SINYAL NILAI              -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-bet" class="hidden space-y-3.5">

    <!-- STRATEGY SELECTOR PRESETS -->
    <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-2">
      <div class="flex items-center justify-between text-xs">
        <div class="font-bold flex items-center gap-1.5">
          <span>🎯</span>
          <span>Pilih Profil Strategi Taruhan Liga 1:</span>
        </div>
        <span class="text-[10.5px] text-[var(--muted-foreground)]" id="strategy-active-label">Profil Aktif: Benteng Kandang</span>
      </div>
      <div class="flex sm:grid sm:grid-cols-5 gap-2 overflow-x-auto pb-1 scrollbar-none" id="strategy-presets-grid">
        <!-- Rendered by JS without odds and without % -->
      </div>
    </div>

    <!-- SINYAL REKOMENDASI TERVERIFIKASI & RADAR JEBAKAN -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <!-- Sinyal Rekomendasi (2 Kolom) -->
      <div class="md:col-span-2 p-3.5 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-2.5">
        <div class="flex items-center justify-between pb-2 border-b border-[var(--border)]">
          <div>
            <h3 class="text-xs sm:text-sm font-bold flex items-center gap-1.5" id="value-picks-header-title">
              <span>🏰</span>
              <span>Sinyal Rekomendasi Paling Worth It</span>
            </h3>
            <p class="text-[11px] text-[var(--muted-foreground)]" id="value-picks-header-subtitle">Laga Mendatang dengan Pasaran Resmi 1xBet. Klik pasaran mana saja untuk pasang ke slip.</p>
          </div>
          <span class="text-[9.5px] px-2 py-0.5 rounded font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300" id="value-picks-header-badge">1xBet Terverifikasi</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5" id="value-picks-container">
          <!-- Rendered by JS -->
        </div>
      </div>

      <!-- Radar Perangkap Bandar (1 Kolom) -->
      <div class="p-3.5 rounded-xl border border-amber-300 dark:border-amber-900 bg-amber-50/40 dark:bg-amber-950/20 space-y-2.5">
        <div class="flex items-center justify-between pb-2 border-b border-amber-200 dark:border-amber-900">
          <div>
            <h3 class="text-xs sm:text-sm font-bold text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
              <span>🚨</span>
              <span>Radar Jebakan Bandar (Trap)</span>
            </h3>
            <p class="text-[10.5px] text-[var(--muted-foreground)]">Tim overhyped publik tapi rawan terpeleset di laga tandang.</p>
          </div>
          <span class="text-[9px] bg-red-600 text-white px-2 py-0.5 rounded font-black">Waspada!</span>
        </div>
        <div class="space-y-2" id="trap-alerts-container">
          <!-- Rendered by JS -->
        </div>
      </div>
    </div>

    <!-- PENCATATAN TARUHAN BARU & KALKULATOR BANKROLL -->
    <div class="p-3.5 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-3" id="bet-form-card">
      <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
        <div class="font-bold text-xs sm:text-sm flex items-center gap-1.5">
          <span>📝</span>
          <span>Catat Tiket Bankroll Liga 1</span>
        </div>
        <span class="text-[10px] text-emerald-600 font-bold">⚡ Kuotasi Resmi: 1xBet Indonesia</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5 text-xs">
        <!-- Match Selector -->
        <div class="sm:col-span-2 space-y-1">
          <label class="text-[11px] font-semibold text-[var(--muted-foreground)]">Pilih Pertandingan (Laga Mendatang):</label>
          <select id="bet-match-select" onchange="onBetMatchChange()" class="w-full p-2 rounded-lg border border-[var(--border)] bg-[var(--background)] font-medium">
            <!-- Populated by JS -->
          </select>
        </div>

        <!-- Bet Type -->
        <div class="space-y-1">
          <label class="text-[11px] font-semibold text-[var(--muted-foreground)]">Jenis Taruhan:</label>
          <select id="bet-selection-type" onchange="updateBetCalculator()" class="w-full p-2 rounded-lg border border-[var(--border)] bg-[var(--background)] font-medium">
            <option value="home">1 (Home Win)</option>
            <option value="draw">X (Seri / Draw)</option>
            <option value="away">2 (Away Win)</option>
            <option value="1x">1X (Home / Seri)</option>
            <option value="x2">X2 (Away / Seri)</option>
            <option value="home_dnb">Home DNB (Seri Refund)</option>
            <option value="away_dnb">Away DNB (Seri Refund)</option>
            <option value="over_15">Over 1.5 Gol Total</option>
            <option value="over_25">Over 2.5 Gol Total</option>
          </select>
        </div>

        <!-- Odds -->
        <div class="space-y-1">
          <label class="text-[11px] font-semibold text-[var(--muted-foreground)]">Odds 1xBet Resmi:</label>
          <input type="number" step="0.01" id="bet-odds-input" oninput="updateBetCalculator()" placeholder="1.85" class="w-full p-2 rounded-lg border border-[var(--border)] bg-[var(--background)] font-bold font-mono">
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 items-end text-xs">
        <!-- Stake -->
        <div class="space-y-1">
          <div class="flex items-center justify-between">
            <label class="text-[11px] font-semibold text-[var(--muted-foreground)]">Nominal Taruhan (Rp):</label>
            <div class="flex items-center gap-1">
              <span onclick="setStake(50000)" class="cursor-pointer text-[10px] bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono hover:bg-slate-200">50k</span>
              <span onclick="setStake(100000)" class="cursor-pointer text-[10px] bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono hover:bg-slate-200">100k</span>
              <span onclick="setStake(250000)" class="cursor-pointer text-[10px] bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono hover:bg-slate-200">250k</span>
            </div>
          </div>
          <input type="number" id="bet-stake-input" oninput="updateBetCalculator()" value="100000" class="w-full p-2 rounded-lg border border-[var(--border)] bg-[var(--background)] font-bold">
        </div>

        <!-- Potential Payout -->
        <div class="p-2.5 rounded-lg border border-emerald-300 dark:border-emerald-900 bg-emerald-50 dark:bg-emerald-950/30 flex items-center justify-between">
          <span class="text-[11px] text-[var(--muted-foreground)]">Potensi Payout:</span>
          <strong class="text-emerald-600 font-mono text-sm" id="calc-potential-payout">Rp 185.000</strong>
        </div>

        <!-- Submit Button -->
        <button type="button" onclick="saveBetRecord()" class="btn-primary py-2.5 px-4 flex items-center justify-center gap-1.5 shadow-sm text-xs">
          <span>💾</span>
          <span>Simpan ke Bankroll</span>
        </button>
      </div>
    </div>

    <!-- KPI SUMMARY BAR -->
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Total Taruhan</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-primary" id="kpi-total-bets">0 Tiket</div>
      </div>
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Total Modal</span>
        <div class="text-base sm:text-lg font-black mt-0.5" id="kpi-total-staked">Rp 0</div>
      </div>
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Laba Bersih</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-emerald-600" id="kpi-net-profit">+Rp 0</div>
      </div>
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Win Rate</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-emerald-600" id="kpi-win-rate">0.0%</div>
      </div>
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] col-span-2 sm:col-span-1">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Yield / ROI</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-emerald-600" id="kpi-roi">+0.0%</div>
      </div>
    </div>

    <!-- HISTORI TIKET TARUHAN BANKROLL -->
    <div class="p-3.5 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-2.5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-2 border-b border-[var(--border)] gap-2">
        <div class="font-bold text-xs sm:text-sm flex items-center gap-1.5">
          <span>📋</span>
          <span>Histori Bankroll</span>
          <span class="text-[10.5px] text-[var(--muted-foreground)] font-normal" id="bet-history-count">(0 tiket)</span>
        </div>
        <div class="flex items-center gap-1 overflow-x-auto scrollbar-none pb-0.5">
          <button id="btn-filter-all" class="btn-sm text-[10.5px] font-bold bg-slate-800 text-white border border-slate-700 shadow-sm" onclick="filterBetStatus('all')">Semua</button>
          <button id="btn-filter-won" class="btn-sm text-[10.5px] text-emerald-500 font-semibold hover:text-emerald-400" onclick="filterBetStatus('won')">Menang</button>
          <button id="btn-filter-lost" class="btn-sm text-[10.5px] text-rose-500 font-semibold hover:text-rose-400" onclick="filterBetStatus('lost')">Kalah</button>
          <button id="btn-filter-pending" class="btn-sm text-[10.5px] text-amber-500 font-semibold hover:text-amber-400" onclick="filterBetStatus('pending')">Menunggu</button>
        </div>
      </div>
      <div id="bet-history-list" class="space-y-2">
        <!-- Populated by JS -->
      </div>
    </div>
  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB: JADWAL & HASIL LIGA 1 (LIVE & 34 PEKAN)   -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-fixtures" class="hidden space-y-3.5">

    <!-- Live Match Alert Banner (Auto-updates when match is in-play) -->
    <div id="sched-live-banner" class="hidden"></div>

    <!-- Header & Info -->
    <div class="p-3.5 rounded-xl border border-sky-200 dark:border-sky-900 bg-sky-50/70 dark:bg-sky-950/20 flex flex-wrap items-center justify-between gap-3 shadow-2xs">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-xl shrink-0">
          ⚔️
        </div>
        <div>
          <div class="text-xs sm:text-sm font-black flex items-center gap-2 text-sky-950 dark:text-sky-200">
            <span>Jadwal Resmi Liga 1 2026/27 &amp; Live Monitoring</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> 100% Dinamis API
            </span>
          </div>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5 max-w-2xl leading-relaxed">
            Jadwal seluruh 34 pekan (306 laga) tersinkronisasi otomatis dari API resmi Liga 1. Perubahan tanggal, jam <em>kick-off</em>, stadion, maupun penundaan laga diperbarui secara <em>real-time</em>. Memantau menit laga berjalan dan skor langsung saat bertanding.
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button class="btn-sm text-xs font-bold" onclick="syncLiga1Odds(true)">🔄 Segarkan Jadwal</button>
      </div>
    </div>

    <!-- Filter & Week Selector Toolbar -->
    <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-2.5 shadow-2xs">
      <div class="flex items-center justify-between gap-2 flex-wrap">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="text-xs font-bold text-[var(--muted-foreground)]">Pilih Pekan:</span>
          <select id="sched-week-dropdown" onchange="filterScheduleWeek(this.value)" class="text-xs font-semibold py-1.5 px-3 border border-[var(--border)] rounded-lg bg-[var(--background)] text-[var(--foreground)]">
            <option value="all">Semua Pekan (Total 306 Laga)</option>
          </select>
          <button class="btn-sm text-xs py-1.5 px-3 font-bold" onclick="filterScheduleActiveWeek()" id="sched-active-week-btn">
            ⭐ Pekan Berjalan
          </button>
          <button class="btn-sm text-xs py-1.5 px-3 font-black text-white bg-red-600 hover:bg-red-700 animate-pulse border-red-500 cursor-pointer" onclick="filterScheduleWeek('live')" id="sched-live-quick-btn" style="display:none">
            🔴 Laga LIVE (<span id="sched-live-count-num">0</span>)
          </button>
        </div>
        <div class="flex items-center gap-2">
          <button class="btn-sm text-xs py-1.5 px-3" onclick="toggleScheduleSort()" id="sched-sort-btn">
            ⏱️ Urutan: Terlama ➔ Terbaru
          </button>
        </div>
      </div>

      <!-- Scrollable Week Chips (Pekan 1 s/d 34) -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 custom-scroll" id="sched-week-chips">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- Match Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3" id="sched-match-grid">
      <!-- Populated dynamically by JS -->
    </div>
  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB: KLASEMEN & PELUANG JUARA (SOS SISA LAWAN) -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-standings" class="space-y-3.5">

    <!-- Methodology & Info Banner -->
    <div class="p-3.5 rounded-xl border border-indigo-200 dark:border-indigo-900 bg-indigo-50/70 dark:bg-indigo-950/20 flex flex-wrap items-center justify-between gap-3 shadow-2xs">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-xl shrink-0">
          🏆
        </div>
        <div>
          <div class="text-xs sm:text-sm font-black flex items-center gap-2 text-indigo-950 dark:text-indigo-200">
            <span>Klasemen Resmi Liga 1 2026/27 &amp; Analisis Peluang Juara</span>
            <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-indigo-600 text-white shadow-2xs">Analisis Sisa Lawan (SOS)</span>
          </div>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5 max-w-2xl leading-relaxed">
            Peluang Juara dihitung <strong>bukan hanya dari poin klasemen saat ini</strong>, melainkan melalui simulasi laga-per-laga dari seluruh sisa jadwal musim (*Strength of Schedule / SOS*). Sistem memperhitungkan bobot lawan (PPG &amp; posisi), rekor *Head-to-Head* (H2H 5 laga), dan keunggulan laga kandang (+0.35 Liga 1).
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[11px] font-bold bg-emerald-100/80 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 shadow-2xs">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="standings-sync-status-text">🟢 Live API: Klasemen Otomatis Terhubung</span>
        </span>
        <button id="btn-sync-standings" onclick="syncLiga1Odds(true)" class="btn-sm text-xs font-bold py-1.5 px-3 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-[var(--border)] shadow-2xs cursor-pointer flex items-center gap-1.5" title="Klik untuk menyinkronkan skor &amp; klasemen terbaru dari server API">
          <span>🔄</span>
          <span>Segarkan Klasemen</span>
        </button>
      </div>
    </div>

    <!-- Quick Metric Cards (Top Favorite, Jadwal Terberat, Jadwal Teringan, Sisa Laga) -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5" id="standings-summary-cards">
      <!-- Rendered dynamically by JS -->
    </div>

    <!-- Filter & Sort Toolbar -->
    <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--card)] flex flex-wrap items-center justify-between gap-2.5 shadow-2xs">
      <div class="flex items-center gap-1.5 flex-wrap" id="standings-filter-chips">
        <button class="chip active" onclick="setStandingsFilter('all')" id="st-filter-all">⭐ Semua Klub (18)</button>
        <button class="chip" onclick="setStandingsFilter('relegation')" id="st-filter-relegation">🔴 Zona Degradasi (#16 - #18)</button>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <label class="text-[11px] text-[var(--muted-foreground)] font-semibold">Urutkan:</label>
        <select id="standings-sort-select" onchange="setStandingsSort(this.value)" class="text-xs bg-[var(--background)] border border-[var(--border)] rounded-lg px-2.5 py-1.5 font-bold text-[var(--foreground)] outline-none cursor-pointer">
          <option value="pos">Klasemen Resmi (Pos 1 ➔ 18)</option>
          <option value="prob">Peluang Juara (Tertinggi ➔ Terendah)</option>
          <option value="sos">Jadwal Sisa Terberat (SOS 🔴)</option>
          <option value="proj">Proyeksi Poin Akhir</option>
        </select>
      </div>
    </div>

    <!-- Mobile Swipe Hint -->
    <div class="sm:hidden px-3 py-1.5 rounded-lg bg-sky-500/10 border border-sky-500/20 text-[10.5px] text-sky-700 dark:text-sky-300 flex items-center justify-between gap-1 font-medium">
      <span>👉 Geser tabel ke kanan untuk melihat SOS &amp; Peluang Juara</span>
      <span class="text-[9px] font-bold bg-sky-500 text-white px-1.5 py-0.5 rounded">18 Klub</span>
    </div>

    <!-- Standings Table Container -->
    <div class="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden shadow-2xs w-full max-w-full">
      <div class="overflow-x-auto custom-scroll w-full" style="overscroll-behavior-x: contain;">
        <table class="w-full text-left border-collapse text-xs whitespace-nowrap">
          <thead>
            <tr class="border-b border-[var(--border)] bg-slate-50 dark:bg-slate-900/50 text-[11px] font-bold text-[var(--muted-foreground)]">
              <th class="py-2.5 px-3 text-center w-12">Pos</th>
              <th class="py-2.5 px-3">Klub</th>
              <th class="py-2.5 px-2 text-center" title="Pertandingan Dimainkan">Main</th>
              <th class="py-2.5 px-2 text-center text-emerald-600 dark:text-emerald-400" title="Menang">M</th>
              <th class="py-2.5 px-2 text-center" title="Seri">S</th>
              <th class="py-2.5 px-2 text-center text-rose-500" title="Kalah">K</th>
              <th class="py-2.5 px-2 text-center" title="Selisih Gol (Goal Difference)">SG</th>
              <th class="py-2.5 px-3 text-center font-black text-[var(--foreground)]" title="Total Poin Saat Ini">Poin</th>
              <th class="py-2.5 px-2 text-center text-[var(--muted-foreground)]" title="Jumlah Pertandingan Tersisa">Sisa</th>
              <th class="py-2.5 px-3 text-center min-w-[155px]" title="Tingkat Kesulitan Sisa Lawan berdasarkan Kekuatan Lawan, Venue, &amp; H2H">Kesulitan Sisa Lawan (SOS)</th>
              <th class="py-2.5 px-3 text-center min-w-[130px]" title="Estimasi Poin Akhir Musim setelah 34 Pekan">Proyeksi Poin Akhir</th>
              <th class="py-2.5 px-4 min-w-[160px]" title="Peluang Juara dihitung dari simulasi Softmax sisa jadwal">Peluang Juara (%)</th>
            </tr>
          </thead>
          <tbody id="standings-table-body" class="divide-y divide-[var(--border)]">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>

      <!-- Legend & Notes -->
      <div class="p-3 bg-slate-50 dark:bg-slate-900/30 border-t border-[var(--border)] flex flex-wrap items-center justify-between gap-2.5 text-[11px] text-[var(--muted-foreground)]">
        <div class="flex items-center gap-3 flex-wrap">
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-rose-500 inline-block"></span> <span>#16-18: Zona Degradasi ke Liga 2</span></span>
        </div>
        <div class="flex items-center gap-3 flex-wrap">
          <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-500 inline-block"></span> <span>🔴 Berat (Sisa lawan berat / mayoritas rival papan atas)</span></span>
          <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500 inline-block"></span> <span>🟡 Sedang (Sisa lawan berimbang)</span></span>
          <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> <span>🟢 Ringan (Sisa lawan relatif ringan / banyak laga kandang)</span></span>
        </div>
      </div>
    </div>

  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB 2: HISTORI SINYAL (RETENSI OTOMATIS 4 HARI) -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-history" class="hidden space-y-3.5">

    <!-- Notice & Info Banner -->
    <div class="p-3.5 rounded-xl border border-sky-300 dark:border-sky-900 bg-sky-50 dark:bg-sky-950/20 flex flex-wrap items-center justify-between gap-2.5">
      <div class="flex items-center gap-2.5">
        <div class="w-9 h-9 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-lg shrink-0">
          📜
        </div>
        <div>
          <div class="text-xs sm:text-sm font-bold flex items-center gap-2">
            <span>Histori Sinyal Rekomendasi Liga 1</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-500 text-white shadow-2xs">Retensi 4 Hari</span>
          </div>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5">
            Semua sinyal dari laga Liga 1 selesai (Full Time) tersimpan selama <strong>4 hari (96 jam)</strong> untuk evaluasi akurasi empiris. Laga yang telah lewat otomatis berpindah ke tab ini.
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-[11px] font-bold px-2.5 py-1 rounded-lg bg-[var(--card)] border border-[var(--border)] text-[var(--foreground)]" id="hist-total-badge">
          ⏳ Memuat Sinyal...
        </span>
        <button class="btn-sm text-xs font-semibold" onclick="renderSignalHistoryView()">
          🔄 Refresh
        </button>
        <button class="btn-sm text-xs text-rose-500 hover:text-rose-600 font-semibold" onclick="clearSignalHistory()" title="Reset histori sinyal">
          🗑️ Reset Histori
        </button>
      </div>
    </div>

    <!-- KPI Summary Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Total Sinyal Selesai</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-primary" id="kpi-hist-total">0 Laga</div>
      </div>
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)]">
        <span class="text-[10.5px] text-[var(--muted-foreground)]">Akurasi / Win Rate</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-emerald-600" id="kpi-hist-winrate">0%</div>
      </div>
      <div class="p-3 rounded-xl border border-emerald-300/50 dark:border-emerald-900/50 bg-emerald-500/5">
        <span class="text-[10.5px] text-emerald-600 font-semibold">✅ Sinyal Tembus</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-emerald-600" id="kpi-hist-won">0</div>
      </div>
      <div class="p-3 rounded-xl border border-rose-300/50 dark:border-rose-900/50 bg-rose-500/5">
        <span class="text-[10.5px] text-rose-600 font-semibold">❌ Meleset</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-rose-600" id="kpi-hist-lost">0</div>
      </div>
      <div class="p-3 rounded-xl border border-amber-300/50 dark:border-amber-900/50 bg-amber-500/5">
        <span class="text-[10.5px] text-amber-600 font-semibold">🔄 Seri / Refund</span>
        <div class="text-base sm:text-lg font-black mt-0.5 text-amber-600" id="kpi-hist-refund">0</div>
      </div>
    </div>

    <!-- Filter & Search Controls -->
    <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-2.5">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <!-- Status Tabs -->
        <div class="flex items-center gap-1.5 flex-wrap" id="hist-status-filters">
          <button class="chip active text-xs py-1 px-3" onclick="setHistFilterStatus('all')" id="hist-btn-all">Semua Sinyal (<span id="hist-cnt-all">0</span>)</button>
          <button class="chip text-xs py-1 px-3" onclick="setHistFilterStatus('won')" id="hist-btn-won">✅ Tembus (<span id="hist-cnt-won">0</span>)</button>
          <button class="chip text-xs py-1 px-3" onclick="setHistFilterStatus('lost')" id="hist-btn-lost">❌ Meleset (<span id="hist-cnt-lost">0</span>)</button>
          <button class="chip text-xs py-1 px-3" onclick="setHistFilterStatus('refund')" id="hist-btn-refund">🔄 Refund (<span id="hist-cnt-refund">0</span>)</button>
        </div>

        <!-- Search input -->
        <div class="flex items-center gap-2 flex-1 sm:max-w-xs">
          <input type="text" id="hist-search-input" oninput="renderSignalHistoryView()" placeholder="🔍 Cari klub (cth: Persija, Persib, Dewa)..." class="w-full text-xs p-2 rounded-lg border border-[var(--border)] bg-[var(--background)]">
        </div>
      </div>
    </div>

    <!-- Signals Cards Container -->
    <div id="hist-signals-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      <!-- Injected by JS -->
    </div>

    <!-- Empty State -->
    <div id="hist-empty-state" class="hidden p-8 text-center rounded-xl border border-dashed border-[var(--border)] bg-[var(--card)] space-y-2">
      <div class="text-3xl">📭</div>
      <div class="font-bold text-sm">Belum Ada Sinyal yang Selesai (FT)</div>
      <p class="text-xs text-[var(--muted-foreground)] max-w-md mx-auto">
        Histori ini murni mencatat sinyal rekomendasi Anda yang telah <strong>selesai dimainkan (Full Time)</strong>.
      </p>
    </div>
  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB 3: ROLLING COMPOUND (3-MODE DNB)           -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-compound" class="hidden space-y-3.5">
    <!-- Compound Mode Selector (3 Solusi) -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
      <div onclick="setCompoundSolution(1)" id="comp-btn-sol1" class="p-3 rounded-xl border-2 border-primary bg-primary/5 cursor-pointer transition-all shadow-2xs">
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="font-black text-primary">Solusi 1</span>
          <span class="text-[9px] bg-primary text-white px-2 py-0.5 rounded font-bold">Aktif</span>
        </div>
        <div class="font-bold text-xs">DNB Single Jalur (7 Step)</div>
        <p class="text-[10.5px] text-[var(--muted-foreground)] mt-0.5">100k ➔ 150k ➔ 225k ➔ Target 1.5 Juta. Seri refund aman.</p>
      </div>

      <div onclick="setCompoundSolution(2)" id="comp-btn-sol2" class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] cursor-pointer hover:border-primary/50 transition-all">
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="font-bold text-[var(--foreground)]">Solusi 2</span>
          <span class="text-[9px] text-[var(--muted-foreground)]">Diversifikasi</span>
        </div>
        <div class="font-bold text-xs">DNB Jalur Paralel A &amp; B</div>
        <p class="text-[10.5px] text-[var(--muted-foreground)] mt-0.5">2 tiket terpisah di pekan yang sama. Tahan banting resiko.</p>
      </div>

      <div onclick="setCompoundSolution(3)" id="comp-btn-sol3" class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] cursor-pointer hover:border-primary/50 transition-all">
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="font-bold text-[var(--foreground)]">Solusi 3</span>
          <span class="text-[9px] text-[var(--muted-foreground)]">Escalation</span>
        </div>
        <div class="font-bold text-xs">DNB Naik Kelas Bertahap</div>
        <p class="text-[10.5px] text-[var(--muted-foreground)] mt-0.5">Amankan profit pokok saat tembus target ganda.</p>
      </div>
    </div>

    <!-- Active Compound Card -->
    <div class="p-4 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-3" id="compound-cycle-card">
      <!-- Rendered by JS -->
    </div>
  </div>

  <!-- ══════════════════════════════════════════════ -->
  <!-- TAB 4: SMART PARLAY KHUSUS LIGA 1              -->
  <!-- ══════════════════════════════════════════════ -->
  <div id="view-parlay" class="hidden space-y-3.5">
    <div class="p-4 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-3">
      <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5 flex-wrap gap-2">
        <div>
          <h3 class="text-xs sm:text-sm font-bold flex items-center gap-1.5">
            <span>🎯</span>
            <span>Kombinasi Smart Parlay Liga 1 Indonesia</span>
          </h3>
          <p class="text-[11px] text-[var(--muted-foreground)]">Hanya menggabungkan sinyal dari laga yang memiliki kuotasi resmi 1xBet.</p>
        </div>
        <button class="btn-sm" onclick="renderSmartParlay()">🔄 Regenerasi Parlay</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3" id="smart-parlay-packages">
        <!-- Rendered by JS -->
      </div>
    </div>
  </div>

</div>

<!-- GLOBAL CUSTOM DIALOG MODAL -->
<div id="custom-dialog-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.75);backdrop-filter:blur(5px);z-index:99999;align-items:center;justify-content:center;padding:16px">
  <div class="p-6 rounded-2xl border border-[var(--border)] bg-[var(--card)] max-w-sm w-full space-y-4 shadow-2xl text-center">
    <div id="custom-dialog-icon" class="text-4xl mx-auto">🎉</div>
    <div class="space-y-1.5">
      <h3 id="custom-dialog-title" class="font-black text-sm text-[var(--foreground)]">Konfirmasi</h3>
      <p id="custom-dialog-message" class="text-xs text-[var(--muted-foreground)] leading-relaxed"></p>
    </div>
    <div id="custom-dialog-buttons" class="flex items-center justify-center gap-2.5 pt-2">
      <!-- Buttons rendered dynamically -->
    </div>
  </div>
</div>

<!-- ODDS & API MODAL -->
<div id="odds-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(3px);z-index:999;align-items:center;justify-content:center;padding:16px">
  <div class="p-5 rounded-xl border border-[var(--border)] bg-[var(--card)] max-w-lg w-full space-y-3 shadow-2xl">
    <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
      <h3 class="font-bold text-sm flex items-center gap-1.5">
        <span>🎰</span>
        <span>Integrasi Feed 1xBet &amp; API-Sports Liga 1</span>
      </h3>
      <button onclick="closeOddsModal()" class="text-slate-400 hover:text-slate-600 text-lg">✕</button>
    </div>
    <div class="space-y-3 text-xs">
      <p class="text-[var(--muted-foreground)]">Terminal ini menerapkan aturan ketat: <strong>Sinyal hanya aktif jika pasaran odds resmi telah dirilis oleh 1xBet</strong>.</p>
      
      <div class="p-3 rounded-lg border border-[var(--border)] bg-[var(--muted)] space-y-1.5">
        <div class="font-bold flex items-center justify-between">
          <span>Feed Pasaran 1xBet:</span>
          <span class="text-emerald-600 font-bold">🟢 Terverifikasi Aktif</span>
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Laga Pekan 6 yang belum kick-off (Bali vs Garudayaksa, Persija vs Arema, PSM vs Persebaya, Persik vs PSS, Madura vs Persib) memiliki odds resmi 1xBet terverifikasi.</p>
        <p class="text-[10px] text-slate-500">Laga masa lalu (Pekan 5 &amp; awal Pekan 6) otomatis diarsipkan ke tab Histori Sinyal.</p>
      </div>

      <div class="p-3 rounded-lg border border-[var(--border)] bg-[var(--muted)] space-y-1.5">
        <div class="font-bold flex items-center justify-between">
          <span>Database Cloud Supabase:</span>
          <span class="text-emerald-600 font-bold">🟢 Terhubung</span>
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Tabel: <code>bankroll_bets</code> | League Code: <code>LIGA1</code></p>
      </div>

      <div class="flex justify-end pt-2">
        <button class="btn-primary py-2 px-4 text-xs" onclick="closeOddsModal()">Tutup</button>
      </div>
    </div>
  </div>
</div>

<!-- SCHEDULE BREAKDOWN & SOS MODAL -->
<div id="schedule-breakdown-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(4px);z-index:9999;align-items:center;justify-content:center;padding:16px;">
  <div class="max-w-3xl w-full max-h-[92vh] bg-[var(--card)] rounded-2xl border border-[var(--border)] shadow-2xl flex flex-col overflow-hidden animate-in fade-in duration-150">
    <!-- Header -->
    <div class="p-4 border-b border-[var(--border)] flex items-center justify-between gap-3 bg-slate-50 dark:bg-slate-900/50">
      <div class="flex items-center gap-3 min-w-0">
        <div id="sched-modal-logo" class="w-10 h-10 rounded-xl bg-white dark:bg-slate-800 p-1.5 border border-[var(--border)] flex items-center justify-center shrink-0 shadow-2xs">
          <!-- Logo -->
        </div>
        <div class="min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <h3 id="sched-modal-team" class="font-black text-sm sm:text-base text-[var(--foreground)] truncate">Nama Klub</h3>
            <span id="sched-modal-rank-badge" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">Pos #1</span>
          </div>
          <p id="sched-modal-subtitle" class="text-[11px] text-[var(--muted-foreground)]">Analisis Rincian Sisa Lawan &amp; Estimasi Poin Laga per Laga</p>
        </div>
      </div>
      <button onclick="closeScheduleBreakdown()" class="w-8 h-8 rounded-lg bg-[var(--muted)] hover:bg-slate-200 dark:hover:bg-slate-800 flex items-center justify-center text-sm font-bold text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors cursor-pointer shrink-0">✕</button>
    </div>

    <!-- Scrollable Body -->
    <div class="p-4 overflow-y-auto custom-scroll space-y-3.5">
      <!-- 4 Quick Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5" id="sched-modal-kpis">
        <!-- Rendered by JS -->
      </div>

      <!-- Schedule SOS Overview Banner -->
      <div id="sched-modal-sos-banner" class="p-3 rounded-xl border flex items-center justify-between gap-3 text-xs">
        <!-- Rendered by JS -->
      </div>

      <!-- Match by Match List -->
      <div class="space-y-2">
        <div class="flex items-center justify-between text-xs font-bold text-[var(--foreground)] px-1">
          <span class="flex items-center gap-1.5">
            <span>📅</span>
            <span>Daftar Seluruh Laga Sisa &amp; Tingkat Kesulitan:</span>
          </span>
          <span id="sched-modal-matches-count" class="text-[11px] font-normal text-[var(--muted-foreground)]">28 Pertandingan Sisa</span>
        </div>
        <div id="sched-modal-matches-list" class="space-y-2">
          <!-- Rendered by JS -->
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-3 border-t border-[var(--border)] bg-slate-50 dark:bg-slate-900/50 flex items-center justify-between text-xs">
      <span class="text-[11px] text-[var(--muted-foreground)]">💡 Diperbarui otomatis setiap kali skor dan status pertandingan tersinkronisasi.</span>
      <button onclick="closeScheduleBreakdown()" class="btn-sm text-xs font-bold py-1.5 px-4 bg-primary text-white border-0 hover:bg-blue-700">Tutup</button>
    </div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════
// DATA LIGA 1 INDONESIA (TEAMS & FIXTURES)
// ══════════════════════════════════════════════
const LIGA1_TEAMS = __TEAMS_JSON__;
let allFixtures = __FIXTURES_JSON__;

// Bersihkan seluruh cache usang versi lama agar browser pengguna tidak menggunakan hasil lampau
const CACHE_VERSION = 'v6';
[
  'liga1_live_fixtures_cache',
  'liga1_live_fixtures_cache_v2',
  'liga1_live_fixtures_cache_v3',
  'liga1_live_fixtures_cache_v4',
  'liga1_live_fixtures_cache_v5',
  'liga1_dynamic_standings',
  'liga1_dynamic_standings_v2',
  'liga1_dynamic_standings_v3',
  'liga1_dynamic_standings_v4',
  'liga1_dynamic_standings_v5',
  'bri_super_league_2026_fixtures_live',
  'bri_super_league_2026_standings_live',
  'bri_super_league_2026_standings_live_v3'
].forEach(k => {
  try { localStorage.removeItem(k); } catch(e) {}
});

// Pulihkan cache real-time API terbaru jika tersedia
try {
  const cachedFixtures = localStorage.getItem(`liga1_live_fixtures_cache_${CACHE_VERSION}`);
  if (cachedFixtures) {
    const parsed = JSON.parse(cachedFixtures);
    if (Array.isArray(parsed) && parsed.length) {
      allFixtures = parsed;
    }
  }
} catch (e) {}

// SINKRONISASI KLASEMEN 100% DINAMIS BERDASARKAN HASIL SELURUH LAGA TERKINI
let currentStandingsTeams = computeDynamicStandings(allFixtures, LIGA1_TEAMS);

// ══════════════════════════════════════════════
// FUNGSI CEK STATUS PERTANDINGAN REALTIME
// ══════════════════════════════════════════════
function isMatchUpcoming(f) {
  if (!f) return false;
  // 1. Status pertandingan sudah selesai secara resmi
  if (f.isFinished || f.status === 'FT' || f.status === 'AET' || f.status === 'PEN') return false;
  
  // 2. Jika ada skor tercatat berarti sudah dimainkan
  if (f.homeScore !== null && f.homeScore !== undefined && f.awayScore !== null && f.awayScore !== undefined) {
    return false;
  }

  // 3. Kick-off sudah lewat waktu sekarang
  const matchTime = new Date(f.date).getTime();
  if (!isNaN(matchTime)) {
    const now = Date.now();
    const diffMin = (now - matchTime) / (1000 * 60);
    // Jika lewat 130 menit dari waktu jadwal -> laga sudah selesai
    if (diffMin > 130) {
      return false;
    }
  }

  return true;
}

// ══════════════════════════════════════════════
// SUPABASE REALTIME CLOUD SYNC (KHUSUS LIGA 1)
// ══════════════════════════════════════════════
const SUPABASE_URL = 'https://hzydzrpxvxieqpnwtdem.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6eWR6cnB4dnhpZXFwbnd0ZGVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI1MTAyMTMsImV4cCI6MjEwODA4NjIxM30.6ZWzJnFBSaT26lup9H_zMlBzHxbah9k9eIMnn2X0vfk';

let supabaseClient = null;
try {
  if (window.supabase && typeof window.supabase.createClient === 'function') {
    supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    console.log('⚡ Supabase Client (Liga 1) initialized successfully.');
  }
} catch (e) {
  console.warn('Supabase client init error:', e);
}

let userBets = [];

function betToRow(b) {
  return {
    id: b.id,
    user_id: 'owner',
    match: b.match || '',
    home: b.home || '',
    away: b.away || '',
    date_str: b.dateStr || b.date_str || '',
    league_code: 'LIGA1',
    type: b.type || '',
    type_label: b.typeLabel || b.type_label || '',
    odds: Number(b.odds) || 1,
    stake: Number(b.stake) || 0,
    status: b.status || 'pending',
    created_at: b.date || b.created_at || new Date().toISOString()
  };
}

function rowToBet(r) {
  return {
    id: r.id,
    match: r.match,
    home: r.home,
    away: r.away,
    dateStr: r.date_str,
    leagueCode: 'LIGA1',
    type: r.type,
    typeLabel: r.type_label,
    odds: Number(r.odds),
    stake: Number(r.stake),
    status: r.status,
    date: r.created_at
  };
}

async function syncBetToCloud(bet) {
  if (!supabaseClient) return;
  try {
    const row = betToRow(bet);
    await supabaseClient.from('bankroll_bets').upsert(row);
  } catch (err) {
    console.warn('Sync bet error:', err);
  }
}

async function deleteBetFromCloud(betId) {
  if (!supabaseClient) return;
  try {
    await supabaseClient.from('bankroll_bets').delete().eq('id', String(betId));
  } catch (err) {
    console.warn('Delete bet error:', err);
  }
}

async function initBankrollCloudSync() {
  const LOCAL_KEY = 'liga1_user_bets_v1';
  if (!supabaseClient) {
    userBets = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
    renderBetKPIs();
    renderBetHistory();
    renderValuePicks();
    return;
  }

  try {
    const { data, error } = await supabaseClient
      .from('bankroll_bets')
      .select('*')
      .eq('league_code', 'LIGA1')
      .order('created_at', { ascending: false });

    if (!error && Array.isArray(data)) {
      const cloudBets = data.map(rowToBet);
      const localBets = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');

      // Sinkronkan tiket lokal yang mungkin belum ada di cloud
      localBets.forEach(lb => {
        if (!cloudBets.some(cb => cb.id === lb.id)) {
          cloudBets.push(lb);
          syncBetToCloud(lb);
        }
      });

      userBets = cloudBets;
      localStorage.setItem(LOCAL_KEY, JSON.stringify(userBets));
      renderBetKPIs();
      renderBetHistory();
      renderValuePicks();
    }
  } catch (e) {
    console.warn('Bankroll cloud fetch failed:', e);
    userBets = JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
    renderBetKPIs();
    renderBetHistory();
    renderValuePicks();
  }

  // Realtime subscription (Listen changes from laptop or mobile)
  try {
    supabaseClient.channel('realtime_liga1_bankroll')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'bankroll_bets' }, (payload) => {
        if (payload.new && payload.new.league_code !== 'LIGA1') return;
        if (payload.eventType === 'INSERT') {
          const newBet = rowToBet(payload.new);
          if (!userBets.some(b => b.id === newBet.id)) {
            userBets.unshift(newBet);
          }
        } else if (payload.eventType === 'UPDATE') {
          const updated = rowToBet(payload.new);
          const idx = userBets.findIndex(b => b.id === updated.id);
          if (idx !== -1) {
            userBets[idx] = { ...userBets[idx], ...updated };
          } else {
            userBets.unshift(updated);
          }
        } else if (payload.eventType === 'DELETE') {
          const delId = payload.old.id;
          userBets = userBets.filter(b => b.id !== delId);
        }
        localStorage.setItem(LOCAL_KEY, JSON.stringify(userBets));
        renderBetKPIs();
        renderBetHistory();
        renderValuePicks();
      })
      .subscribe();
  } catch (err) {
    console.warn('Realtime subscription warning:', err);
  }
}

let activeFilterCategory = 'all';

// ══════════════════════════════════════════════
// MESIN KUANTITATIF & LOGIKA RESMI LIGA 1 INDONESIA
// (Porting Matematika Langsung dari liga1-tracker)
// ══════════════════════════════════════════════

function normalizeTeamKey(name) {
  const n = (name || '').toUpperCase().trim();
  if (n.includes('PERSIJAP')) return 'PERSIJAP';
  if (n.includes('PERSIJA')) return 'PERSIJA';
  if (n.includes('PERSIB')) return 'PERSIB';
  if (n.includes('PERSEBAYA')) return 'PERSEBAYA';
  if (n.includes('AREMA')) return 'AREMA';
  if (n.includes('BALI UNITED') || n.includes('BALI')) return 'BALI';
  if (n.includes('MADURA')) return 'MADURA';
  if (n.includes('BORNEO')) return 'BORNEO';
  if (n.includes('PSM')) return 'PSM';
  if (n.includes('PSS')) return 'PSS';
  if (n.includes('PSIM')) return 'PSIM';
  if (n.includes('PERSIK')) return 'PERSIK';
  if (n.includes('PERSITA')) return 'PERSITA';
  if (n.includes('DEWA')) return 'DEWA';
  if (n.includes('BHAYANGKARA')) return 'BHAYANGKARA';
  if (n.includes('GARUDA') || n.includes('GARUDAYAKSA')) return 'GARUDAYAKSA';
  if (n.includes('JAVA')) return 'JAVA';
  if (n.includes('ISENMULANG') || n.includes('KALTENG')) return 'ISENMULANG';
  return n.split(' ')[0];
}

const TIER_1_FORTRESS = ['PERSIB', 'PERSIJA', 'PERSEBAYA', 'PSS', 'AREMA', 'BALI UNITED', 'PSM'];
const TIER_2_FORTRESS = ['BORNEO', 'MADURA', 'PSIM', 'PERSIK', 'PERSITA'];

function matchTier(teamName, list) {
  const up = (teamName || '').toUpperCase();
  const words = up.split(/\\s+/);
  return list.some(k => k.includes(' ') ? up.includes(k) : words.includes(k));
}

function getStadiumAtmosphere(teamName) {
  if (matchTier(teamName, TIER_1_FORTRESS)) return { tier: 1, homeBoost: 0.38, awayFriction: 0.16, tag: '🔥 Kandang Angker' };
  if (matchTier(teamName, TIER_2_FORTRESS)) return { tier: 2, homeBoost: 0.30, awayFriction: 0.08, tag: '⚡ Atmosfer Kuat' };
  return { tier: 3, homeBoost: 0.24, awayFriction: 0.04, tag: null };
}

const H2H_DATA = {
  'PERSIJA_PERSEBAYA': { w: 2, d: 2, l: 1 },
  'PERSIJA_AREMA': { w: 2, d: 2, l: 1 },
  'PERSIJA_PSM': { w: 3, d: 1, l: 1 },
  'PERSIJA_BALI': { w: 1, d: 2, l: 2 },
  'PERSIJA_DEWA': { w: 2, d: 1, l: 2 },
  'PERSIJA_MADURA': { w: 1, d: 2, l: 2 },
  'PERSIJA_BORNEO': { w: 1, d: 1, l: 3 },
  'PERSIJA_PERSIK': { w: 3, d: 1, l: 1 },
  'PERSIJA_PSS': { w: 3, d: 2, l: 0 },
  'PERSIJA_BHAYANGKARA': { w: 2, d: 2, l: 1 },
  'PERSIJA_PERSITA': { w: 3, d: 1, l: 1 },
  'PERSIB_PERSEBAYA': { w: 2, d: 1, l: 2 },
  'PERSIB_AREMA': { w: 3, d: 2, l: 0 },
  'PERSIB_PSM': { w: 2, d: 1, l: 2 },
  'PERSIB_BALI': { w: 1, d: 3, l: 1 },
  'PERSIB_DEWA': { w: 2, d: 2, l: 1 },
  'PERSIB_MADURA': { w: 3, d: 1, l: 1 },
  'PERSIB_BORNEO': { w: 2, d: 1, l: 2 },
  'PERSIB_PERSIK': { w: 3, d: 1, l: 1 },
  'PERSIB_PSS': { w: 4, d: 1, l: 0 },
  'PERSIB_BHAYANGKARA': { w: 3, d: 1, l: 1 },
  'PERSIB_PERSITA': { w: 3, d: 2, l: 0 },
  'PERSEBAYA_AREMA': { w: 4, d: 1, l: 0 },
  'PERSEBAYA_PSM': { w: 2, d: 1, l: 2 },
  'PERSEBAYA_BALI': { w: 2, d: 0, l: 3 },
  'PERSEBAYA_DEWA': { w: 1, d: 2, l: 2 },
  'PERSEBAYA_MADURA': { w: 3, d: 2, l: 0 },
  'PERSEBAYA_BORNEO': { w: 2, d: 1, l: 2 },
  'PERSEBAYA_PERSIK': { w: 2, d: 2, l: 1 },
  'PERSEBAYA_PSS': { w: 3, d: 1, l: 1 },
  'PERSEBAYA_BHAYANGKARA': { w: 2, d: 1, l: 2 },
  'BALI_AREMA': { w: 3, d: 1, l: 1 },
  'BALI_PSM': { w: 2, d: 2, l: 1 },
  'BALI_DEWA': { w: 3, d: 1, l: 1 },
  'BALI_MADURA': { w: 2, d: 1, l: 2 },
  'BALI_BORNEO': { w: 2, d: 1, l: 2 },
  'BALI_PERSIK': { w: 2, d: 2, l: 1 },
  'DEWA_MADURA': { w: 2, d: 1, l: 2 },
  'DEWA_BORNEO': { w: 1, d: 2, l: 2 },
  'DEWA_PSM': { w: 2, d: 2, l: 1 },
  'DEWA_AREMA': { w: 2, d: 2, l: 1 },
  'AREMA_PSM': { w: 2, d: 1, l: 2 },
  'AREMA_MADURA': { w: 1, d: 2, l: 2 },
  'AREMA_BORNEO': { w: 1, d: 2, l: 2 }
};

function getH2H(teamA, teamB) {
  const cA = normalizeTeamKey(teamA);
  const cB = normalizeTeamKey(teamB);
  const keyDirect = `${cA}_${cB}`;
  const keyRev = `${cB}_${cA}`;
  if (H2H_DATA[keyDirect]) return H2H_DATA[keyDirect];
  if (H2H_DATA[keyRev]) {
    const rev = H2H_DATA[keyRev];
    return { w: rev.l, d: rev.d, l: rev.w };
  }
  return { w: 2, d: 2, l: 1 };
}

function computeGoalStats(fixtures) {
  const stats = {};
  fixtures.forEach(f => {
    if (!f.played && f.status !== 'FT') return;
    if (f.homeScore === null || f.awayScore === null) return;
    [f.home, f.away].forEach(n => { if (!stats[n]) stats[n] = { gf: 0, ga: 0 }; });
    stats[f.home].gf += f.homeScore;
    stats[f.home].ga += f.awayScore;
    stats[f.away].gf += f.awayScore;
    stats[f.away].ga += f.homeScore;
  });
  return stats;
}

function getTeamDynamicState(teamName) {
  const norm = normalizeTeamKey(teamName);
  let formPts = 0, formGf = 0, formGa = 0, playedCount = 0;
  if (typeof allFixtures !== 'undefined' && Array.isArray(allFixtures)) {
    const finishedMatches = allFixtures
      .filter(f => (f.played || f.status === 'FT') && f.homeScore !== null && f.awayScore !== null)
      .filter(f => normalizeTeamKey(f.home) === norm || normalizeTeamKey(f.away) === norm);
    const recent = finishedMatches.slice(-5);
    playedCount = recent.length;
    recent.forEach(m => {
      const isHome = normalizeTeamKey(m.home) === norm;
      const myScore = isHome ? m.homeScore : m.awayScore;
      const oppScore = isHome ? m.awayScore : m.homeScore;
      formGf += myScore;
      formGa += oppScore;
      if (myScore > oppScore) formPts += 3;
      else if (myScore === oppScore) formPts += 1;
    });
  }
  const ppg = playedCount > 0 ? (formPts / playedCount) : 1.35;
  return { formPts, ppg, formGf, formGa, played: playedCount };
}

function matchProb(homeName, awayName) {
  const goalStats = computeGoalStats(allFixtures);
  const home = LIGA1_TEAMS.find(t => normalizeTeamKey(t.name) === normalizeTeamKey(homeName) || normalizeTeamKey(t.short) === normalizeTeamKey(homeName));
  const away = LIGA1_TEAMS.find(t => normalizeTeamKey(t.name) === normalizeTeamKey(awayName) || normalizeTeamKey(t.short) === normalizeTeamKey(awayName));

  const leagueAvg = 1.38;
  const PRIOR = 4;
  function shrink(rawRate, n) { return (n * rawRate + PRIOR * leagueAvg) / (n + PRIOR); }

  const hDyn = getTeamDynamicState(homeName);
  const aDyn = getTeamDynamicState(awayName);

  const hG = goalStats[homeName] || { gf: (home ? home.gf : leagueAvg * 5), ga: (home ? home.ga : leagueAvg * 5) };
  const aG = goalStats[awayName] || { gf: (away ? away.gf : leagueAvg * 5), ga: (away ? away.ga : leagueAvg * 5) };

  const hGames = home?.played || 5;
  const aGames = away?.played || 5;

  const rawHAtk = (hDyn.played >= 3) ? (0.55 * (hDyn.formGf / hDyn.played) + 0.45 * (hG.gf / hGames)) : (hG.gf / hGames);
  const rawHDef = (hDyn.played >= 3) ? (0.55 * (hDyn.formGa / hDyn.played) + 0.45 * (hG.ga / hGames)) : (hG.ga / hGames);
  const rawAAtk = (aDyn.played >= 3) ? (0.55 * (aDyn.formGf / aDyn.played) + 0.45 * (aG.gf / aGames)) : (aG.gf / aGames);
  const rawADef = (aDyn.played >= 3) ? (0.55 * (aDyn.formGa / aDyn.played) + 0.45 * (aG.ga / aGames)) : (aG.ga / aGames);

  const hAtk = shrink(rawHAtk, hGames);
  const hDef = shrink(rawHDef, hGames);
  const aAtk = shrink(rawAAtk, aGames);
  const aDef = shrink(rawADef, aGames);

  const stadium = getStadiumAtmosphere(homeName);
  const netHomeBoost = Math.max(0.10, stadium.homeBoost);
  const netAwayFriction = Math.max(0.02, stadium.awayFriction);

  const hLambda = Math.max(0.40, hAtk + netHomeBoost + 0.22 * (aDef - leagueAvg));
  const aLambda = Math.max(0.35, aAtk - netAwayFriction + 0.22 * (hDef - leagueAvg));

  function poisson(k, lam) {
    let p = Math.exp(-lam);
    for (let i = 0; i < k; i++) p *= lam / (i + 1);
    return p;
  }

  let hw = 0, d = 0, aw = 0;
  for (let h = 0; h <= 7; h++) for (let a = 0; a <= 7; a++) {
    const p = poisson(h, hLambda) * poisson(a, aLambda);
    if (h > a) hw += p; else if (h === a) d += p; else aw += p;
  }
  const tot = hw + d + aw;
  return {
    home: +(hw / tot * 100).toFixed(1),
    draw: +(d / tot * 100).toFixed(1),
    away: +(aw / tot * 100).toFixed(1),
    hLambda: +hLambda.toFixed(2),
    aLambda: +aLambda.toFixed(2),
    hPPG: +hDyn.ppg.toFixed(2),
    aPPG: +aDyn.ppg.toFixed(2),
    hFormPts: hDyn.formPts,
    aFormPts: aDyn.formPts
  };
}

// ══════════════════════════════════════════════
// EVALUASI VALUE MARKET & PERANGKAP BANDAR (1XBET)
// ══════════════════════════════════════════════
function evaluateMarketOpportunity(prob, odds, f) {
  if (!prob || !odds || !odds.hasOdds || !odds.market) return null;

  const oH = odds.market.h;
  const oD = odds.market.d;
  const oA = odds.market.a;
  const sumInv = (1/oH) + (1/oD) + (1/oA);

  const vigFreeH = (1/oH) / sumInv;
  const vigFreeD = (1/oD) / sumInv;
  const vigFreeA = (1/oA) / sumInv;

  const modelH = prob.home / 100;
  const modelD = prob.draw / 100;
  const modelA = prob.away / 100;

  const evH = (modelH * oH) - 1;
  const evD = (modelD * oD) - 1;
  const evA = (modelA * oA) - 1;

  // Rumus Pasar Double Chance (1X dan X2) dengan estimasi margin bandar (~4%)
  const o1X = +((1 / ((1/oH) + (1/oD))) * 0.96).toFixed(2);
  const oX2 = +((1 / ((1/oA) + (1/oD))) * 0.96).toFixed(2);
  const prob1X = +(prob.home + prob.draw).toFixed(1);
  const probX2 = +(prob.away + prob.draw).toFixed(1);

  const ev1X = ((prob1X / 100) * o1X) - 1;
  const evX2 = ((probX2 / 100) * oX2) - 1;

  // 1. Trap Detection (Perangkap Bandar):
  let trap = null;
  if (vigFreeH - modelH >= 0.10 && oH <= 1.65) {
    trap = {
      side: 'home',
      team: f.home,
      opp: f.away,
      odds: oH,
      gap: +((vigFreeH - modelH) * 100).toFixed(1),
      marketProb: +(vigFreeH * 100).toFixed(1),
      modelProb: +(modelH * 100).toFixed(1),
      counterDcOdds: oX2,
      counterWinRate: probX2,
      advice: `🚨 PERANGKAP BANDAR: ${f.homeShort} terlalu murah (@${oH}), pasar overhype! Disarankan: Pasang ${f.awayShort} (X2 @${oX2}) atau Skip.`
    };
  } else if (vigFreeA - modelA >= 0.10 && oA <= 1.65) {
    trap = {
      side: 'away',
      team: f.away,
      opp: f.home,
      odds: oA,
      gap: +((vigFreeA - modelA) * 100).toFixed(1),
      marketProb: +(vigFreeA * 100).toFixed(1),
      modelProb: +(modelA * 100).toFixed(1),
      counterDcOdds: o1X,
      counterWinRate: prob1X,
      advice: `🚨 PERANGKAP BANDAR: ${f.awayShort} terlalu murah (@${oA}), pasar overhype! Disarankan: Pasang ${f.homeShort} (1X @${o1X}) atau Skip.`
    };
  } else if (oA < 1.90 && f.homeRank <= 11 && (f.awayRank - f.homeRank) > -5) {
    trap = {
      side: 'away',
      team: f.away,
      opp: f.home,
      odds: oA,
      counterDcOdds: o1X,
      counterWinRate: prob1X,
      advice: `🚨 PERANGKAP BANDAR: ${f.awayShort} diunggulkan (@${oA}) padahal ${f.homeShort} (#${f.homeRank}) sangat tangguh di kandang. Saran: 1X atau Skip.`
    };
  }

  // 2. Kategori A: 🌟 FAVORIT EMAS (Win Rate >= 50% & EV >= +3%)
  let favoriteValue = null;
  if (prob.home >= 50.0 && evH >= 0.03 && oH >= 1.50) {
    favoriteValue = {
      type: 'favorite',
      side: 'home',
      team: f.homeShort,
      odds: oH,
      winRate: prob.home,
      ev: +(evH * 100).toFixed(1),
      advice: `🌟 FAVORIT EMAS: ${f.homeShort} Win (@${oH}) · Win Rate ${prob.home}% (EV +${(evH*100).toFixed(1)}%)`
    };
  } else if (prob.away >= 48.0 && evA >= 0.03 && oA >= 1.50) {
    favoriteValue = {
      type: 'favorite',
      side: 'away',
      team: f.awayShort,
      odds: oA,
      winRate: prob.away,
      ev: +(evA * 100).toFixed(1),
      advice: `🌟 FAVORIT EMAS: ${f.awayShort} Win (@${oA}) · Win Rate ${prob.away}% (EV +${(evA*100).toFixed(1)}%)`
    };
  }

  // 3. Kategori B: 🛡️ DOUBLE CHANCE & HANDICAP EMAS
  let safetyNet = null;
  if (probX2 >= 50.0 && evX2 >= 0.05 && (oA >= 2.80 || (trap && trap.side === 'home'))) {
    safetyNet = {
      type: 'double_chance',
      side: 'away_dc',
      team: f.awayShort,
      opp: f.homeShort,
      label: `${f.awayShort} Seri atau Menang (X2)`,
      odds: oX2,
      winRate: probX2,
      ev: +(evX2 * 100).toFixed(1),
      advice: `🛡️ PENGAMAN UNDERDOG: ${f.awayShort} (X2) @${oX2} · Win Rate ${probX2}% (EV +${(evX2*100).toFixed(1)}%)`
    };
  } else if (prob1X >= 52.0 && ev1X >= 0.05 && (oH >= 2.80 || (trap && trap.side === 'away'))) {
    safetyNet = {
      type: 'double_chance',
      side: 'home_dc',
      team: f.homeShort,
      opp: f.awayShort,
      label: `${f.homeShort} Seri atau Menang (1X)`,
      odds: o1X,
      winRate: prob1X,
      ev: +(ev1X * 100).toFixed(1),
      advice: `🛡️ PENGAMAN UNDERDOG: ${f.homeShort} (1X) @${o1X} · Win Rate ${prob1X}% (EV +${(ev1X*100).toFixed(1)}%)`
    };
  }

  // 4. Kategori C: 🏰 BENTENG KANDANG DOMINAN (P_Home >= 52%, Odds @1.60-@2.35)
  let homeFortress = null;
  if (prob.home >= 52.0 && oH >= 1.60 && oH <= 2.35 && (!trap || trap.side !== 'home')) {
    homeFortress = {
      type: 'home_fortress',
      side: 'home',
      team: f.homeShort,
      opp: f.awayShort,
      odds: oH,
      winRate: prob.home,
      ev: +(evH * 100).toFixed(1),
      advice: `🏰 BENTENG KANDANG: ${f.homeShort} Win (@${oH}) · Win Rate ${prob.home}% (EV ${(evH >= 0 ? '+' : '')}${(evH*100).toFixed(1)}%)`
    };
  }

  // 5. Kategori D: 🎯 HIGH-YIELD VALUE SNIPER (Odds Tinggi 1.85 - 2.80)
  let highOddsSniper = null;
  if (prob.home >= 46.0 && oH >= 1.85 && oH <= 2.60 && evH >= 0.05 && (!trap || trap.side !== 'home')) {
    highOddsSniper = {
      type: 'high_odds',
      side: 'home',
      team: f.homeShort,
      opp: f.awayShort,
      odds: oH,
      winRate: prob.home,
      ev: +(evH * 100).toFixed(1),
      advice: `🎯 HIGH ODDS SNIPER: ${f.homeShort} Win (@${oH}) · Peluang ${prob.home}% (EV +${(evH*100).toFixed(1)}%)`
    };
  } else if (prob.away >= 40.0 && oA >= 2.00 && oA <= 2.80 && evA >= 0.05 && (!trap || trap.side !== 'away')) {
    highOddsSniper = {
      type: 'high_odds',
      side: 'away',
      team: f.awayShort,
      opp: f.homeShort,
      odds: oA,
      winRate: prob.away,
      ev: +(evA * 100).toFixed(1),
      advice: `🎯 HIGH ODDS SNIPER: ${f.awayShort} Win (@${oA}) · Peluang ${prob.away}% (EV +${(evA*100).toFixed(1)}%)`
    };
  }

  // 6. Kategori E: 🔄 DRAW NO BET (DNB Sintetis: Odds = oH * (1 - 1/oD))
  let dnbValue = null;
  const dnbOdds = +((oH * (1 - (1 / oD)))).toFixed(2);
  if (prob.home >= 50.0 && (!trap || trap.side !== 'home') && dnbOdds >= 1.45 && dnbOdds <= 2.25) {
    dnbValue = {
      type: 'dnb',
      side: 'home',
      isDnb: true,
      team: f.homeShort,
      opp: f.awayShort,
      odds: dnbOdds,
      winRate: prob.home,
      ev: +(evH * 100).toFixed(1),
      advice: `🔄 DRAW NO BET: ${f.homeShort} DNB (@${dnbOdds}) · Win Rate ${prob.home}% (Seri 100% Refund)`
    };
  }

  return {
    trap,
    favoriteValue,
    safetyNet,
    homeFortress,
    highOddsSniper,
    dnbValue,
    dcOdds: { o1X, oX2, prob1X, probX2 },
    ev: { h: +(evH * 100).toFixed(1), d: +(evD * 100).toFixed(1), a: +(evA * 100).toFixed(1) },
    vigFree: { h: +(vigFreeH * 100).toFixed(1), d: +(vigFreeD * 100).toFixed(1), a: +(vigFreeA * 100).toFixed(1) }
  };
}

// ══════════════════════════════════════════════
// ARBITRASE "WORTH IT" RESOLVER (4 KATEGORI INTI SALING MENGUNCI)
// ══════════════════════════════════════════════
function resolveBestWorthItPick(opp, f, prob, odds) {
  if (!opp) return null;
  const coreCandidates = [];

  if (opp.homeFortress) {
    coreCandidates.push({
      ...opp.homeFortress,
      strategyKey: 'home_fortress',
      icon: '🏰',
      badge: 'BENTENG KANDANG',
      badgeColor: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
    });
  }
  if (opp.favoriteValue) {
    coreCandidates.push({
      ...opp.favoriteValue,
      strategyKey: 'favorit_emas',
      icon: '🌟',
      badge: 'FAVORIT EMAS',
      badgeColor: 'bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300'
    });
  }
  if (opp.safetyNet) {
    coreCandidates.push({
      ...opp.safetyNet,
      strategyKey: 'double_chance',
      icon: '🛡️',
      badge: 'PENGAMAN DC',
      badgeColor: 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300'
    });
  }
  if (opp.dnbValue) {
    coreCandidates.push({
      ...opp.dnbValue,
      strategyKey: 'dnb_shield',
      icon: '⚖️',
      badge: 'DNB SHIELD',
      badgeColor: 'bg-teal-100 text-teal-700 dark:bg-teal-950 dark:text-teal-300'
    });
  }
  if (opp.highOddsSniper) {
    coreCandidates.push({
      ...opp.highOddsSniper,
      strategyKey: 'high_odds_sniper',
      icon: '🎯',
      badge: 'HIGH ODDS SNIPER',
      badgeColor: 'bg-purple-100 text-purple-700 dark:bg-purple-950 dark:text-purple-300'
    });
  }

  if (!coreCandidates.length) return null;
  if (coreCandidates.length === 1) {
    return {
      ...coreCandidates[0],
      decisionReason: `Satu-satunya opsi kuantitatif yang lolos filter ketat (@${coreCandidates[0].odds} · Win ${coreCandidates[0].winRate}%).`
    };
  }

  // ════════════════════════════════════════════════════════════
  // HIERARKI KEPUTUSAN MUTLAK:
  // 1. PERTIMBANGAN PERTAMA: MANA YANG PALING MENGUNTUNGKAN (ODDS TERTINGGI)
  // 2. PERTIMBANGAN KEDUA: APAKAH PALING WORTH IT / BESAR PELUANG UNTUK WIN TIKET
  // ════════════════════════════════════════════════════════════
  coreCandidates.sort((a, b) => b.odds - a.odds);
  const highestOddsPick = coreCandidates[0];

  const hDyn = getTeamDynamicState(f.home);
  const aDyn = getTeamDynamicState(f.away);
  const h2h = getH2H(f.home, f.away);

  const isHomePick = !highestOddsPick.side.includes('away');
  const pickDyn = isHomePick ? hDyn : aDyn;
  const h2hDominant = isHomePick ? (h2h.w >= h2h.l) : (h2h.l >= h2h.w);
  const isFormConsistent = (pickDyn.ppg >= 1.50 || pickDyn.formPts >= 7);
  const isWinRateStrong = (highestOddsPick.winRate >= 58.0);

  // Jika odds tertinggi didukung Win Rate kuat (>=58%) & form/H2H konsisten -> Ambil Odds Tertinggi
  if (isWinRateStrong && (h2hDominant || isFormConsistent)) {
    return {
      ...highestOddsPick,
      decisionReason: `Paling Menguntungkan (@${highestOddsPick.odds}) & Peluang Win Sangat Kuat (${highestOddsPick.winRate}%).`
    };
  }

  // Jika odds tertinggi terlalu berisiko, prioritaskan opsi paling Worth It untuk memenangkan tiket:
  // 1. Double Chance (Peluang lolos 2 hasil >= 65%)
  const dcPick = coreCandidates.find(c => c.strategyKey === 'double_chance');
  if (dcPick && dcPick.winRate >= 65.0 && dcPick.odds >= 1.40) {
    return {
      ...dcPick,
      decisionReason: `Paling Worth It untuk Win Tiket (Peluang Tembus 2 Hasil ${dcPick.winRate}% @${dcPick.odds}) dibanding opsi tebak tunggal yang berisiko.`
    };
  }

  // 2. DNB Shield (Seri refund 100%)
  const dnbPick = coreCandidates.find(c => c.strategyKey === 'dnb_shield');
  if (dnbPick && dnbPick.odds >= 1.45) {
    return {
      ...dnbPick,
      decisionReason: `Paling Worth It untuk Win Tiket (Proteksi DNB Seri Refund @${dnbPick.odds}).`
    };
  }

  // 3. Fallback: Kandidat dengan Win Rate tertinggi
  coreCandidates.sort((a, b) => b.winRate - a.winRate);
  const bestSafe = coreCandidates[0];
  return {
    ...bestSafe,
    decisionReason: `Paling Worth It untuk Win Tiket: Memprioritaskan Win Rate Tertinggi (${bestSafe.winRate}% @${bestSafe.odds}).`
  };
}

// ══════════════════════════════════════════════
// STRATEGY PRESETS (LIGA 1 INDONESIA)
// ══════════════════════════════════════════════
const STRATEGY_PRESETS = {
  'home_fortress': {
    id: 'home_fortress',
    name: 'Benteng Kandang Dominan',
    shortName: 'Benteng Kandang',
    icon: '🏰',
    desc: 'Memaksimalkan keunggulan kandang angker Liga 1 (P_Home >= 52%, Odds @1.60-@2.35)'
  },
  'favorit_emas': {
    id: 'favorit_emas',
    name: 'Favorit Emas',
    shortName: 'Favorit Emas',
    icon: '🌟',
    desc: 'Tim unggulan dengan kestabilan performa 5 laga terakhir & EV >= +3%'
  },
  'double_chance': {
    id: 'double_chance',
    name: 'Pengaman Underdog (Double Chance)',
    shortName: 'Double Chance',
    icon: '🛡️',
    desc: 'Pengaman 2 dari 3 hasil (1X / X2) dengan estimasi margin 4%'
  },
  'dnb_shield': {
    id: 'dnb_shield',
    name: 'Draw No Bet (DNB - Seri Refund)',
    shortName: 'DNB Shield',
    icon: '⚖️',
    desc: 'Rumus sintetis kompensasi draw 1xBet: Modal kembali 100% jika skor imbang'
  },
  'high_odds_sniper': {
    id: 'high_odds_sniper',
    name: 'High-Yield Value Sniper',
    shortName: 'High Odds Sniper',
    icon: '🎯',
    desc: 'Membidik salah harga bandar dengan odds tinggi @1.85-@2.80 & EV >= +5%'
  }
};

let currentStrategyPreset = 'home_fortress';

function setStrategyPreset(presetKey) {
  if (currentStrategyPreset === presetKey) {
    currentStrategyPreset = 'all';
  } else {
    currentStrategyPreset = presetKey;
  }
  renderStrategyPresetsGrid();
  renderValuePicks();
}

function renderStrategyPresetsGrid() {
  const g = document.getElementById('strategy-presets-grid');
  if (!g) return;
  const label = document.getElementById('strategy-active-label');
  if (label) {
    if (currentStrategyPreset === 'all') {
      label.textContent = 'Profil Aktif: ⭐ Semua Sinyal Paling Worth It';
    } else if (STRATEGY_PRESETS[currentStrategyPreset]) {
      label.textContent = `Profil Aktif: ${STRATEGY_PRESETS[currentStrategyPreset].name}`;
    }
  }
  g.innerHTML = Object.values(STRATEGY_PRESETS).map(p => {
    const isActive = p.id === currentStrategyPreset;
    return `
      <div onclick="setStrategyPreset('${p.id}')" class="min-w-[130px] sm:min-w-0 flex-shrink-0 sm:flex-shrink p-2.5 rounded-lg border transition-all cursor-pointer ${
        isActive 
          ? 'border-emerald-500 bg-emerald-50/70 dark:bg-emerald-950/40 text-emerald-950 dark:text-emerald-100 ring-2 ring-emerald-500/30 font-bold shadow-xs' 
          : 'border-[var(--border)] bg-[var(--background)] hover:border-emerald-500/50 hover:bg-slate-50 dark:hover:bg-slate-800/50 text-[var(--foreground)]'
      }">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-base">${p.icon}</span>
          ${isActive ? '<span class="text-[9px] bg-emerald-600 text-white px-1.5 py-0.5 rounded font-black tracking-wide">AKTIF</span>' : ''}
        </div>
        <div class="font-bold truncate text-[11.5px]">${p.shortName}</div>
      </div>
    `;
  }).join('');
}

// ══════════════════════════════════════════════
// VALUE PICKS & TRAP RADAR ALGORITHM
// ══════════════════════════════════════════════
function evaluateLiga1Match(f) {
  // ATURAN MUTLAK: Hanya laga yang memiliki odds resmi dari 1xBet yang dievaluasi!
  if (!f.odds || !f.odds.h || !f.has1xBetOdds) return null;

  const oH = Number(f.odds.h);
  const oD = Number(f.odds.d);
  const oA = Number(f.odds.a);
  const marketOdds = { hasOdds: true, market: { h: oH, d: oD, a: oA } };

  const prob = matchProb(f.home, f.away);
  if (!prob) return null;

  const opp = evaluateMarketOpportunity(prob, marketOdds, f);
  if (!opp) return null;

  const markets = {
    oH, oD, oA,
    homeDnbOdds: opp.dnbValue ? opp.dnbValue.odds : +((oH * (1 - (1 / oD)))).toFixed(2),
    awayDnbOdds: +((oA * (1 - (1 / oD)))).toFixed(2),
    dc1xOdds: opp.dcOdds.o1X,
    dcX2Odds: opp.dcOdds.oX2
  };

  const isTrap = Boolean(opp.trap);
  const trapReason = opp.trap ? opp.trap.advice : '';

  // Evaluasi 1 pilihan terbaik eksklusif berdasarkan hierarki keuntungan & peluang win
  const bestPick = resolveBestWorthItPick(opp, f, prob, marketOdds);

  return { isTrap, trapReason, markets, prob, opp, bestPick };
}

function formatIndoDateTime(dateVal, dateStr) {
  let d = null;
  if (dateVal) {
    d = new Date(dateVal);
  }
  if (!d || isNaN(d.getTime())) {
    if (dateStr) {
      const clean = dateStr.replace(' WIB', '').trim();
      const parts = clean.split(' ');
      if (parts.length >= 2) {
        const [y, m, day] = parts[0].split('-').map(Number);
        const [hh, mm] = parts[1].replace('.', ':').split(':').map(Number);
        if (y && m && day) {
          d = new Date(Date.UTC(y, m - 1, day, (hh || 0) - 7, mm || 0));
        }
      }
    }
  }
  if (!d || isNaN(d.getTime())) return dateStr || '';

  const DAYS = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];

  // Konversi tepat ke Waktu Indonesia Barat (WIB, UTC+7) tanpa terpengaruh zona waktu lokal klien
  const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
  const wib = new Date(utc + (7 * 3600000));

  const dayName = DAYS[wib.getDay()];
  const dayNum = wib.getDate();
  const monthName = MONTHS[wib.getMonth()];
  const hh = String(wib.getHours()).padStart(2, '0');
  const mm = String(wib.getMinutes()).padStart(2, '0');

  // Format baku sesuai permintaan: "Sab, 24 Okt, 01.45 WIB"
  return `${dayName}, ${dayNum} ${monthName}, ${hh}.${mm} WIB`;
}

function renderValuePicks() {
  const container = document.getElementById('value-picks-container');
  const trapContainer = document.getElementById('trap-alerts-container');
  if (!container || !trapContainer) return;

  const strat = STRATEGY_PRESETS[currentStrategyPreset] || STRATEGY_PRESETS['home_fortress'];
  const titleEl = document.getElementById('value-picks-header-title');
  const subEl = document.getElementById('value-picks-header-subtitle');
  if (titleEl) {
    titleEl.innerHTML = `<span>${strat.icon}</span> <span>Sinyal Rekomendasi: ${strat.name}</span>`;
  }
  if (subEl) {
    subEl.textContent = `${strat.desc}. Kuotasi resmi 1xBet.`;
  }

  // Saring HANYA laga yang:
  // 1. Benar-benar belum selesai / belum kick-off (isMatchUpcoming)
  // 2. SUDAH RESMI DIKELUARKAN ODDS-NYA DARI 1xBET (f.has1xBetOdds)
  const list = allFixtures.filter(f => isMatchUpcoming(f) && f.has1xBetOdds && f.odds && f.odds.h);

  const picksHtml = [];
  const trapsHtml = [];

  list.forEach(f => {
    const evalResult = evaluateLiga1Match(f);
    if (!evalResult) return;

    const { isTrap, trapReason, markets, bestPick } = evalResult;

    // Render Trap Alert if any
    if (isTrap) {
      trapsHtml.push(`
        <div class="p-2.5 rounded-lg border border-amber-300 dark:border-amber-800 bg-amber-100/40 dark:bg-amber-900/20 text-xs space-y-1">
          <div class="flex items-center justify-between">
            <strong class="text-amber-900 dark:text-amber-200">${f.homeShort} vs ${f.awayShort}</strong>
            <span class="text-[9px] bg-amber-500 text-white px-1.5 py-0.2 rounded font-bold">TRAP</span>
          </div>
          <p class="text-[11px] text-amber-800 dark:text-amber-300 leading-tight">${trapReason}</p>
          <div class="text-[10px] text-[var(--muted-foreground)] font-semibold mt-1">Saran: Pertimbangkan Double Chance (1X/X2) atau Skip.</div>
        </div>
      `);
    }

    // ════════════════════════════════════════════════════════════
    // ATURAN EKSKLUSIF (SALING MENGUNCI):
    // 1. Jika match ini tidak punya kandidat yang lolos syarat ketat -> Skip!
    if (!bestPick) return;

    // 2. Jika profil aktif bukan 'all' dan tidak cocok dengan strategi eksklusif match ini -> Skip!
    if (currentStrategyPreset !== 'all' && bestPick.strategyKey !== currentStrategyPreset) {
      return;
    }
    // ════════════════════════════════════════════════════════════

    const selType = bestPick.side === 'away_dc' ? 'x2' : (bestPick.side === 'home_dc' ? '1x' : (bestPick.isDnb ? (bestPick.side === 'home' ? 'home_dnb' : 'away_dnb') : (bestPick.side === 'away' ? 'away' : 'home')));
    const selectionTitle = bestPick.label || `${bestPick.team} Win`;

    picksHtml.push(`
      <div class="p-3.5 rounded-xl border border-[var(--border)] bg-[var(--card)] hover:border-primary/50 transition-all space-y-2.5 shadow-2xs">
        <!-- Baris 1: Informasi Jadwal & Badge Status (Trap & Paling Worth It) -->
        <div class="flex items-center justify-between text-[10px] sm:text-[11px] pb-1.5 border-b border-[var(--border)] text-[var(--muted-foreground)] flex-wrap gap-1">
          <div class="flex items-center gap-1.5 font-bold text-[var(--foreground)]">
            <span class="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-[10px] font-extrabold border border-[var(--border)]">🇮🇩 ${f.round}</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-mono font-bold text-[10.5px] sm:text-[11px]">🕒 ${formatIndoDateTime(f.date, f.dateStr)}</span>
          </div>
          <div class="flex items-center gap-1">
            ${isTrap ? `
              <span class="bg-red-600 text-white text-[8.5px] font-black px-1.5 py-0.5 rounded flex items-center gap-1 shadow-2xs animate-pulse" title="Pertandingan ini ada di Radar Jebakan Bandar! ${trapReason}">
                <span>🚨</span>
                <span>ADA DI RADAR TRAP</span>
              </span>` : ''}
            <span class="bg-amber-500 text-white text-[8.5px] px-1.5 py-0.5 rounded font-black shadow-2xs">⭐ Paling Worth It</span>
          </div>
        </div>

        <!-- Clubs display -->
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <img src="${f.homeLogo}" class="w-6 h-6 object-contain shrink-0" onerror="this.style.display='none'" alt="" />
            <div class="truncate">
              <div class="text-xs font-bold truncate text-[var(--foreground)]">${f.homeShort}</div>
              <div class="text-[10px] text-[var(--muted-foreground)]">Rank #${f.homeRank}</div>
            </div>
          </div>
          <span class="text-xs font-black text-slate-400">VS</span>
          <div class="flex items-center gap-2 flex-1 justify-end min-w-0 text-right">
            <div class="truncate">
              <div class="text-xs font-bold truncate text-[var(--foreground)]">${f.awayShort}</div>
              <div class="text-[10px] text-[var(--muted-foreground)]">Rank #${f.awayRank}</div>
            </div>
            <img src="${f.awayLogo}" class="w-6 h-6 object-contain shrink-0" onerror="this.style.display='none'" alt="" />
          </div>
        </div>

        <!-- Sinyal Rekomendasi Utama (Terpilih Paling Worth It - Layout Rapi & Lapang) -->
        <div class="p-3 rounded-xl bg-emerald-500/10 dark:bg-emerald-950/40 border border-emerald-500/25 space-y-2">
          <!-- Baris 1: Header Badge Profil & Odds Bandar -->
          <div class="flex items-center justify-between gap-2 border-b border-emerald-500/15 pb-1.5">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-[9.5px] font-extrabold uppercase px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 border border-emerald-500/30 flex items-center gap-1 shadow-2xs">
                <span>${bestPick.icon}</span>
                <span>${bestPick.badge}</span>
              </span>
            </div>
            <div class="flex items-center gap-1 shrink-0 font-mono">
              <span class="text-[10px] text-[var(--muted-foreground)]">Odds</span>
              <span class="text-sm sm:text-base font-black text-emerald-600 dark:text-emerald-400">@${bestPick.odds}</span>
            </div>
          </div>

          <!-- Baris 2: Target Pasaran Rekomendasi & Metrik Akurasi -->
          <div class="flex items-center justify-between gap-2 pt-0.5">
            <div class="font-extrabold text-xs sm:text-[13px] text-emerald-950 dark:text-emerald-100 flex items-center gap-1.5 truncate">
              <span class="text-emerald-600">🎯</span>
              <span class="truncate">${selectionTitle}</span>
            </div>
            <div class="flex items-center gap-1 font-mono text-[9.5px] shrink-0">
              <span class="px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 font-bold border border-emerald-500/20">
                Win: ${bestPick.winRate}%
              </span>
              <span class="px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 font-bold border border-emerald-500/20">
                +${bestPick.ev}% EV
              </span>
            </div>
          </div>

          <!-- Baris 3: Alasan Analisis Taktis yang Rapi -->
          <p class="text-[10.5px] text-[var(--muted-foreground)] leading-relaxed pt-0.5">
            💡 ${bestPick.decisionReason || bestPick.advice}
          </p>
        </div>

        <!-- Pilihan Pasaran Cepat 1xBet Langsung (Klik untuk pasang) -->
        <div class="space-y-1 pt-0.5">
          <div class="text-[10px] text-[var(--muted-foreground)] font-semibold flex items-center justify-between">
            <span>Pilihan Pasaran Resmi 1xBet:</span>
            <span class="text-[9.5px] text-slate-400 font-normal">Klik untuk pasang</span>
          </div>
          <div class="grid grid-cols-5 gap-1 text-center">
            <div onclick="quickSelectBet('${f.id}', 'home', ${markets.oH})" class="market-pill" title="Pasang ${f.homeShort} Menang">
              <span class="text-[9px] block text-[var(--muted-foreground)]">1</span>
              <span>${markets.oH}</span>
            </div>
            <div onclick="quickSelectBet('${f.id}', 'draw', ${markets.oD})" class="market-pill" title="Pasang Seri">
              <span class="text-[9px] block text-[var(--muted-foreground)]">X</span>
              <span>${markets.oD}</span>
            </div>
            <div onclick="quickSelectBet('${f.id}', 'away', ${markets.oA})" class="market-pill" title="Pasang ${f.awayShort} Menang">
              <span class="text-[9px] block text-[var(--muted-foreground)]">2</span>
              <span>${markets.oA}</span>
            </div>
            <div onclick="quickSelectBet('${f.id}', 'home_dnb', ${markets.homeDnbOdds})" class="market-pill" title="Pasang ${f.homeShort} DNB">
              <span class="text-[9px] block text-[var(--muted-foreground)]">DNB</span>
              <span>${markets.homeDnbOdds}</span>
            </div>
            <div onclick="quickSelectBet('${f.id}', '1x', ${markets.dc1xOdds})" class="market-pill" title="Pasang 1X Double Chance">
              <span class="text-[9px] block text-[var(--muted-foreground)]">1X</span>
              <span>${markets.dc1xOdds}</span>
            </div>
          </div>
        </div>

        <!-- Details & Quick Add Recommendation -->
        <div class="flex items-center justify-between pt-1">
          <div class="text-[10.5px] text-[var(--muted-foreground)] flex items-center gap-1.5">
            <span class="font-bold text-emerald-600">⚡ Sinyal Terverifikasi 1xBet</span>
          </div>
          <button onclick="quickSelectBet('${f.id}', '${selType}', ${bestPick.odds})" class="btn-sm text-[11px] py-1 px-3 bg-primary/10 text-primary hover:bg-primary hover:text-white border-primary/20 font-bold transition-all shadow-2xs">
            + Pasang Sinyal
          </button>
        </div>
      </div>
    `);
  });

  if (picksHtml.length === 0) {
    container.innerHTML = `
      <div class="p-6 text-center text-xs text-[var(--muted-foreground)] bg-[var(--card)] rounded-xl border border-dashed border-[var(--border)] col-span-2 space-y-2">
        <div class="text-2xl">${strat.icon || '🛡️'}</div>
        <div class="font-bold text-sm text-[var(--foreground)]">Tidak Ada Laga yang Dialokasikan ke Profil "${strat.name}" Pekan Ini</div>
        <p class="text-[11px] max-w-md mx-auto text-[var(--muted-foreground)]">
          Sistem secara otomatis mempertimbangkan <strong>opsi yang paling menguntungkan (odds tertinggi)</strong> dan <strong>paling tinggi peluang menangnya (*Worth It*)</strong>. Pertandingan aktif pekan ini dialokasikan ke profil strategi lain yang memiliki nilai lebih pasti, atau disaring (No Bet) demi melindungi modal Anda.
        </p>
      </div>
    `;
  } else {
    container.innerHTML = picksHtml.join('');
  }

  if (trapsHtml.length === 0) {
    trapContainer.innerHTML = `
      <div class="p-3 rounded-lg border border-dashed border-amber-200 dark:border-amber-900 text-center text-xs text-amber-800 dark:text-amber-400">
        ✅ Tidak ada jebakan bandar kritis pada laga mendatang yang rilis.
      </div>
    `;
  } else {
    trapContainer.innerHTML = trapsHtml.join('');
  }

  populateBetMatchSelect(list);
}

function filterMatchCategory(cat) {
  activeFilterCategory = cat;
  document.querySelectorAll('.chip[id^="chip-filter-"]').forEach(c => c.classList.remove('active'));
  const activeEl = document.getElementById('chip-filter-' + cat);
  if (activeEl) activeEl.classList.add('active');
  renderValuePicks();
}

// ══════════════════════════════════════════════
// BET SLIP & BANKROLL MANAGEMENT
// ══════════════════════════════════════════════
function populateBetMatchSelect(matchesList) {
  const sel = document.getElementById('bet-match-select');
  if (!sel) return;
  const currentVal = sel.value;
  sel.innerHTML = matchesList.map(m => `
    <option value="${m.id}">${m.round}: ${m.homeShort} vs ${m.awayShort} (${formatIndoDateTime(m.date, m.dateStr)})</option>
  `).join('');

  if (currentVal && matchesList.some(m => String(m.id) === String(currentVal))) {
    sel.value = currentVal;
  }
  onBetMatchChange();
}

function onBetMatchChange() {
  const sel = document.getElementById('bet-match-select');
  if (!sel) return;
  const matchId = Number(sel.value);
  const match = allFixtures.find(f => f.id === matchId);
  if (!match) return;

  const betType = document.getElementById('bet-selection-type').value;
  const oddsInput = document.getElementById('bet-odds-input');

  // Auto set odds based on bet type from 1xBet
  if (match.odds) {
    if (betType === 'home') oddsInput.value = match.odds.h;
    else if (betType === 'draw') oddsInput.value = match.odds.d;
    else if (betType === 'away') oddsInput.value = match.odds.a;
    else if (betType === '1x') oddsInput.value = (1 / ((1/match.odds.h) + (1/match.odds.d)) * 0.95).toFixed(2);
    else if (betType === 'x2') oddsInput.value = (1 / ((1/match.odds.a) + (1/match.odds.d)) * 0.95).toFixed(2);
    else if (betType === 'home_dnb') oddsInput.value = (match.odds.h * 0.72).toFixed(2);
    else if (betType === 'away_dnb') oddsInput.value = (match.odds.a * 0.72).toFixed(2);
    else if (betType === 'over_15') oddsInput.value = '1.35';
    else if (betType === 'over_25') oddsInput.value = '1.92';
  }
  updateBetCalculator();
}

function quickSelectBet(matchId, type, odds) {
  const matchSel = document.getElementById('bet-match-select');
  const typeSel = document.getElementById('bet-selection-type');
  const oddsInput = document.getElementById('bet-odds-input');

  if (matchSel) matchSel.value = matchId;
  if (typeSel) typeSel.value = type;
  if (oddsInput) oddsInput.value = odds;

  updateBetCalculator();

  // Scroll smoothly to form card
  const formCard = document.getElementById('bet-form-card');
  if (formCard) {
    formCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    formCard.classList.add('ring-2', 'ring-primary');
    setTimeout(() => formCard.classList.remove('ring-2', 'ring-primary'), 1200);
  }
}

function setStake(amount) {
  const stakeInput = document.getElementById('bet-stake-input');
  if (stakeInput) {
    stakeInput.value = amount;
    updateBetCalculator();
  }
}

function updateBetCalculator() {
  const stake = Number(document.getElementById('bet-stake-input').value) || 0;
  const odds = Number(document.getElementById('bet-odds-input').value) || 1;
  const payout = Math.round(stake * odds);
  const payoutEl = document.getElementById('calc-potential-payout');
  if (payoutEl) {
    payoutEl.textContent = 'Rp ' + payout.toLocaleString('id-ID');
  }
}

async function saveBetRecord() {
  const matchSel = document.getElementById('bet-match-select');
  const typeSel = document.getElementById('bet-selection-type');
  const oddsInput = document.getElementById('bet-odds-input');
  const stakeInput = document.getElementById('bet-stake-input');

  const matchId = Number(matchSel.value);
  const match = allFixtures.find(f => f.id === matchId);
  if (!match) return;

  const odds = Number(oddsInput.value) || 1;
  const stake = Number(stakeInput.value) || 0;
  if (stake <= 0) {
    showCustomDialog('Nominal Tidak Valid', 'Silakan masukkan nominal taruhan minimal Rp 10.000.', '⚠️', [{ label: 'OK', class: 'btn-primary' }]);
    return;
  }

  const newBet = {
    id: 'b_' + Date.now(),
    match: `${match.homeShort} vs ${match.awayShort}`,
    home: match.home,
    away: match.away,
    dateStr: match.dateStr,
    leagueCode: 'LIGA1',
    type: typeSel.value,
    typeLabel: typeSel.options[typeSel.selectedIndex].text,
    odds: odds,
    stake: stake,
    status: 'pending',
    date: new Date().toISOString()
  };

  userBets.unshift(newBet);
  localStorage.setItem('liga1_user_bets_v1', JSON.stringify(userBets));

  // Sync to Cloud Supabase
  await syncBetToCloud(newBet);

  renderBetKPIs();
  renderBetHistory();

  showCustomDialog('Tiket Disimpan!', `Taruhan <strong>${newBet.typeLabel}</strong> pada <strong>${newBet.match}</strong> berhasil dicatat ke bankroll.`, '✅', [{ label: 'Selesai', class: 'btn-primary' }]);
}

async function toggleBetStatus(betId, newStatus) {
  const bet = userBets.find(b => b.id === betId);
  if (!bet) return;
  bet.status = bet.status === newStatus ? 'pending' : newStatus;
  localStorage.setItem('liga1_user_bets_v1', JSON.stringify(userBets));
  await syncBetToCloud(bet);
  renderBetKPIs();
  renderBetHistory();
}

async function updateBetStatus(betId, newStatus) {
  const bet = userBets.find(b => b.id === betId);
  if (!bet) return;
  bet.status = newStatus;
  localStorage.setItem('liga1_user_bets_v1', JSON.stringify(userBets));
  await syncBetToCloud(bet);
  renderBetKPIs();
  renderBetHistory();
}

async function deleteBetRecord(betId) {
  showCustomDialog('Hapus Tiket', 'Apakah Anda yakin ingin menghapus tiket taruhan ini dari bankroll?', '🗑️', [
    {
      label: 'Hapus',
      class: 'bg-rose-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-rose-700 cursor-pointer',
      action: async () => {
        userBets = userBets.filter(b => b.id !== betId);
        localStorage.setItem('liga1_user_bets_v1', JSON.stringify(userBets));
        await deleteBetFromCloud(betId);
        renderBetKPIs();
        renderBetHistory();
      }
    },
    { label: 'Batal', class: 'btn-sm' }
  ]);
}

let activeBetStatusFilter = 'all';
function filterBetStatus(status) {
  activeBetStatusFilter = status;
  const filterKeys = ['all', 'won', 'lost', 'pending'];
  filterKeys.forEach(s => {
    const el = document.getElementById(`btn-filter-${s}`);
    if (el) {
      if (s === status) {
        el.className = 'btn-sm text-[10.5px] font-bold bg-slate-800 text-white border border-slate-700 shadow-sm';
      } else {
        const color = s === 'won' ? 'text-emerald-500' :
                      s === 'lost' ? 'text-rose-500' :
                      s === 'pending' ? 'text-amber-500' : 'text-[var(--muted-foreground)]';
        el.className = `btn-sm text-[10.5px] ${color} font-semibold hover:bg-[var(--muted)]`;
      }
    }
  });
  renderBetHistory();
}

function formatBetDateHeader(b) {
  const code = (b.leagueCode === 'LIGA1' || !b.leagueCode) ? 'L1' : b.leagueCode;
  let dStr = b.dateStr || '';
  if (b.date && (!dStr || dStr.includes('-') || dStr.includes('T'))) {
    const raw = formatIndoDateTime(b.date, dStr);
    const parts = raw.split(',');
    if (parts.length > 2) {
      dStr = parts.slice(1).join(',').replace('WIB', '').trim();
    } else {
      dStr = raw.replace('WIB', '').trim();
    }
  } else if (dStr) {
    const parts = dStr.split(',');
    if (parts.length > 2) {
      dStr = parts.slice(1).join(',').replace('WIB', '').trim();
    } else {
      dStr = dStr.replace('WIB', '').trim();
    }
  }
  return `${code} · ${dStr || '22 Okt, 15.30'}`;
}

function getBetSelectionLabel(b) {
  const matchParts = (b.match || '').split(' vs ');
  const homeTeam = b.home || (matchParts[0] ? matchParts[0].trim() : '');
  const awayTeam = b.away || (matchParts[1] ? matchParts[1].trim() : '');
  const t = (b.type || '').toUpperCase();
  const tl = (b.typeLabel || '').toUpperCase();

  if (t === '1X' || tl.includes('1X')) {
    return homeTeam ? `${homeTeam} Seri/Menang (1X)` : 'Seri / Menang (1X)';
  }
  if (t === 'X2' || tl.includes('X2')) {
    return awayTeam ? `${awayTeam} Seri/Menang (X2)` : 'Seri / Menang (X2)';
  }
  if (t === '1' || tl.includes('HOME WIN') || tl.includes('1 (HOME')) {
    return homeTeam ? `${homeTeam} Win` : 'Home Win (1)';
  }
  if (t === '2' || tl.includes('AWAY WIN') || tl.includes('2 (AWAY')) {
    return awayTeam ? `${awayTeam} Win` : 'Away Win (2)';
  }
  if (t === 'X' || tl.includes('DRAW') || tl.includes('SERI')) {
    return 'Seri (Draw X)';
  }
  if (t === '12' || tl.includes('12')) {
    return 'Home atau Away Win (12)';
  }
  return b.typeLabel || b.type || 'Pilihan';
}

function renderBetHistory() {
  const list = document.getElementById('bet-history-list');
  const countEl = document.getElementById('bet-history-count');
  if (!list) return;

  let filtered = userBets;
  if (activeBetStatusFilter !== 'all') {
    filtered = userBets.filter(b => b.status === activeBetStatusFilter);
  }

  if (countEl) countEl.textContent = `(${userBets.length} tiket)`;

  if (!filtered.length) {
    list.innerHTML = `
      <div class="p-6 text-center text-xs text-[var(--muted-foreground)] rounded-xl border border-dashed border-[var(--border)] bg-[var(--card)]/50">
        Belum ada tiket taruhan pada filter ini. Pasang sinyal dari tabel di atas untuk mulai mencatat.
      </div>
    `;
    return;
  }

  // Urutkan tiket kronologis terbaru di atas
  const sorted = [...filtered].sort((a, b) => new Date(b.date || 0).getTime() - new Date(a.date || 0).getTime());

  list.innerHTML = sorted.map(b => {
    const payout = Math.round((b.stake || 0) * (b.odds || 1));
    const profit = payout - (b.stake || 0);

    let statusText = 'PENDING';
    let statusBadgeClass = 'bg-amber-500/10 text-amber-500 border border-amber-500/30';
    if (b.status === 'won') {
      statusText = 'WON';
      statusBadgeClass = 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30';
    } else if (b.status === 'lost') {
      statusText = 'LOST';
      statusBadgeClass = 'bg-rose-500/10 text-rose-500 border border-rose-500/30';
    } else if (b.status === 'refund') {
      statusText = 'REFUND';
      statusBadgeClass = 'bg-blue-500/10 text-blue-500 border border-blue-500/30';
    }

    const dateHeader = formatBetDateHeader(b);

    let cleanMatch = b.match || '';
    if (cleanMatch.includes(']')) {
      const parts = cleanMatch.split(']');
      cleanMatch = parts[parts.length - 1].replace(/\\(@.*?\\)/, '').trim();
    }

    const selLabel = getBetSelectionLabel(b);
    let pilihanText = selLabel.toLowerCase().startsWith('pilihan:') ? selLabel : `Pilihan: ${selLabel}`;

    let payoutHtml = '';
    if (b.status === 'lost') {
      payoutHtml = `<span class="text-rose-400 font-bold">Payout: Rp 0 (-Rp ${(b.stake || 0).toLocaleString('id-ID')})</span>`;
    } else if (b.status === 'refund') {
      payoutHtml = `<span class="text-amber-400 font-bold">Payout: Rp ${(b.stake || 0).toLocaleString('id-ID')} (Refund)</span>`;
    } else {
      payoutHtml = `<span class="text-teal-400 dark:text-teal-400 font-bold">Payout: Rp ${payout.toLocaleString('id-ID')} (+Rp ${profit.toLocaleString('id-ID')})</span>`;
    }

    return `
      <div class="p-3.5 rounded-xl border border-[var(--border)] bg-[var(--background)] space-y-2.5 text-xs shadow-xs transition-all hover:border-slate-600">
        <!-- Top bar: Date & Status Action Buttons -->
        <div class="flex items-center justify-between text-[11px] text-[var(--muted-foreground)] border-b border-[var(--border)]/70 pb-2">
          <span class="font-medium text-slate-400">${dateHeader}</span>
          <div class="flex items-center gap-1.5">
            <span class="text-[9.5px] px-2 py-0.5 rounded font-black tracking-wider ${statusBadgeClass}">${statusText}</span>
            <button onclick="toggleBetStatus('${b.id}', 'won')" class="w-6 h-6 rounded-md bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-[11px] flex items-center justify-center transition-all shadow-xs cursor-pointer" title="Tandai Menang">W</button>
            <button onclick="toggleBetStatus('${b.id}', 'lost')" class="w-6 h-6 rounded-md bg-rose-500 hover:bg-rose-600 text-white font-bold text-[11px] flex items-center justify-center transition-all shadow-xs cursor-pointer" title="Tandai Kalah">L</button>
            <button onclick="deleteBetRecord('${b.id}')" class="w-6 h-6 rounded-md bg-slate-600 hover:bg-slate-500 text-white font-bold text-[11px] flex items-center justify-center transition-all shadow-xs cursor-pointer" title="Hapus Tiket">✕</button>
          </div>
        </div>

        <!-- Middle bar: Match title, selection, odds -->
        <div class="flex items-center justify-between flex-wrap gap-2 pt-0.5">
          <div>
            <div class="font-bold text-[13.5px] text-[var(--foreground)]">${cleanMatch}</div>
            <div class="text-[11px] text-teal-400 dark:text-teal-400 font-semibold mt-0.5">${pilihanText}</div>
          </div>
          <div class="text-right">
            <span class="font-mono font-bold text-sm sm:text-base text-[var(--foreground)]">@${b.odds}</span>
          </div>
        </div>

        <!-- Bottom bar: Modal & Payout -->
        <div class="p-2.5 rounded-lg bg-[var(--muted)]/40 border border-[var(--border)] flex items-center justify-between text-xs">
          <span class="text-[var(--muted-foreground)]">Modal: <strong class="text-[var(--foreground)] font-mono">Rp ${(b.stake || 0).toLocaleString('id-ID')}</strong></span>
          ${payoutHtml}
        </div>
      </div>
    `;
  }).join('');
}

function renderBetKPIs() {
  const totalBets = userBets.length;
  let totalStaked = 0;
  let netProfit = 0;
  let wonCount = 0;
  let resolvedCount = 0;

  userBets.forEach(b => {
    totalStaked += b.stake;
    if (b.status === 'won') {
      wonCount++;
      resolvedCount++;
      netProfit += Math.round(b.stake * b.odds) - b.stake;
    } else if (b.status === 'lost') {
      resolvedCount++;
      netProfit -= b.stake;
    } else if (b.status === 'refund') {
      resolvedCount++;
    }
  });

  const winRate = resolvedCount > 0 ? ((wonCount / resolvedCount) * 100).toFixed(1) : '0.0';
  const roi = totalStaked > 0 ? ((netProfit / totalStaked) * 100).toFixed(1) : '0.0';

  document.getElementById('kpi-total-bets').textContent = totalBets + ' Tiket';
  document.getElementById('kpi-total-staked').textContent = 'Rp ' + totalStaked.toLocaleString('id-ID');

  const profitEl = document.getElementById('kpi-net-profit');
  if (profitEl) {
    profitEl.textContent = (netProfit >= 0 ? '+Rp ' : '-Rp ') + Math.abs(netProfit).toLocaleString('id-ID');
    profitEl.className = 'text-base sm:text-lg font-black mt-0.5 ' + (netProfit >= 0 ? 'text-emerald-600' : 'text-rose-600');
  }

  document.getElementById('kpi-win-rate').textContent = winRate + '%';

  const roiEl = document.getElementById('kpi-roi');
  if (roiEl) {
    roiEl.textContent = (Number(roi) >= 0 ? '+' : '') + roi + '%';
    roiEl.className = 'text-base sm:text-lg font-black mt-0.5 ' + (Number(roi) >= 0 ? 'text-emerald-600' : 'text-rose-600');
  }
}

// ══════════════════════════════════════════════
// TAB 2: HISTORI SINYAL 4 HARI (RETENSI 96 JAM)
// ══════════════════════════════════════════════
let activeHistFilter = 'all';

function setHistFilterStatus(status) {
  activeHistFilter = status;
  document.querySelectorAll('#hist-status-filters button').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('hist-btn-' + status);
  if (btn) btn.classList.add('active');
  renderSignalHistoryView();
}

// ══════════════════════════════════════════════
// SIGNAL HISTORY & 4-DAY AUTO-PURGE ENGINE (LIGA 1)
// HISTORI MURNI: Hanya mencatat pertandingan yang MASUK KE SINYAL DULU & SUDAH SELESAI (FT)
// ══════════════════════════════════════════════
const SIGNAL_HISTORY_KEY = 'liga1_signal_history_v2';
const SIGNAL_RETENTION_MS = 4 * 24 * 60 * 60 * 1000; // 4 hari (96 jam)

function getSignalHistory() {
  let list = [];
  try {
    const raw = localStorage.getItem(SIGNAL_HISTORY_KEY);
    if (raw) list = JSON.parse(raw);
  } catch (e) {
    list = [];
  }
  return purgeExpiredSignals(list);
}

function saveSignalHistory(list) {
  try {
    localStorage.setItem(SIGNAL_HISTORY_KEY, JSON.stringify(list));
  } catch (e) {
    console.error('Gagal menyimpan signal history:', e);
  }
}

function clearSignalHistory() {
  showCustomDialog(
    'Reset Histori Sinyal',
    'Apakah Anda yakin ingin mengosongkan seluruh arsip histori sinyal saat ini? Riwayat akan dibersihkan.',
    '🗑️',
    [
      { label: 'Batal', class: 'btn-sm' },
      {
        label: 'Ya, Kosongkan',
        class: 'btn-primary bg-rose-600 hover:bg-rose-700 text-white',
        action: () => {
          saveSignalHistory([]);
          try {
            localStorage.setItem('liga1_signal_history_cleared_at', String(Date.now()));
            localStorage.removeItem(SIGNAL_HISTORY_KEY);
          } catch (e) {}
          renderSignalHistoryView();
          showCustomDialog('Histori Berhasil Dikosongkan', 'Seluruh arsip histori sinyal telah di-reset dan dibersihkan.', '✅', [{ label: 'Selesai', class: 'btn-primary' }]);
        }
      }
    ]
  );
}

function purgeExpiredSignals(list) {
  const now = Date.now();
  const valid = list.filter(item => {
    const matchTime = new Date(item.finishedAt || item.date || item.dateStr).getTime();
    return !isNaN(matchTime) && (now - matchTime) <= SIGNAL_RETENTION_MS;
  });
  if (valid.length !== list.length) {
    saveSignalHistory(valid);
  }
  return valid;
}

// Otomatis arsipkan sinyal yang SELESAI (FT) dari jadwal Liga 1
// ATURAN MUTLAK: Hanya laga yang PERNAH MASUK KE SINYAL & SUDAH SELESAI (FT) yang boleh masuk histori!
function autoArchiveFinishedSignals() {
  const history = getSignalHistory();
  const existingIds = new Set(history.map(h => String(h.fixtureId || h.id)));
  let clearedAt = 0;
  try { clearedAt = Number(localStorage.getItem('liga1_signal_history_cleared_at') || 0); } catch (e) {}
  let updated = false;

  allFixtures.forEach(f => {
    // 1. Abaikan laga kuno masa lalu (Pekan 1-5); hanya evaluasi laga sesi aktif (Pekan 6 ke atas)
    if (f.round && (f.round.includes('Pekan 1') || f.round.includes('Pekan 2') || f.round.includes('Pekan 3') || f.round.includes('Pekan 4') || f.round.includes('Pekan 5'))) {
      return;
    }

    const fTime = new Date(f.date || f.dateStr).getTime();
    if (clearedAt && fTime <= clearedAt) return;

    // 2. Hanya periksa laga yang SUDAH SELESAI (FT) dan memiliki skor akhir
    if (isMatchUpcoming(f)) return;
    if (f.homeScore === null || f.awayScore === null) return;

    const fid = String(f.id);
    if (existingIds.has(fid) || existingIds.has('hist_' + fid)) return;

    // 3. Evaluasi apakah laga ini MEMANG LOLOS DAN MENJADI SINYAL REKOMENDASI RESMI
    const evalResult = evaluateLiga1Match(f);
    if (!evalResult || !evalResult.bestPick) return;

    const best = evalResult.bestPick;
    const hScore = Number(f.homeScore);
    const aScore = Number(f.awayScore);

    let status = 'lost';
    const side = best.side;
    if (side === '1x' || side === 'home_dc') {
      if (hScore >= aScore) status = 'won';
    } else if (side === 'x2' || side === 'away_dc') {
      if (aScore >= hScore) status = 'won';
    } else if (side === 'home') {
      if (best.isDnb && hScore === aScore) status = 'refund';
      else if (hScore > aScore) status = 'won';
    } else if (side === 'away') {
      if (best.isDnb && hScore === aScore) status = 'refund';
      else if (aScore > hScore) status = 'won';
    }

    history.push({
      id: 'hist_' + fid,
      fixtureId: f.id,
      match: `${f.homeShort} vs ${f.awayShort}`,
      home: f.homeShort,
      away: f.awayShort,
      homeLogo: f.homeLogo,
      awayLogo: f.awayLogo,
      round: f.round || 'Pekan 6',
      venue: f.venue,
      date: f.date,
      dateStr: f.dateStr,
      hScore,
      aScore,
      strategyKey: best.strategyKey,
      strategyName: best.badge || best.strategyKey,
      sigLabel: best.label || `${best.team} Win`,
      sigOdds: best.odds,
      winRate: best.winRate,
      ev: best.ev,
      status: status,
      finishedAt: f.date || new Date().toISOString()
    });
    existingIds.add(fid);
    updated = true;
  });

  if (updated) {
    saveSignalHistory(history);
  }
}

function renderSignalHistoryView() {
  autoArchiveFinishedSignals();
  const container = document.getElementById('hist-signals-container');
  const emptyState = document.getElementById('hist-empty-state');
  if (!container) return;

  const signals = getSignalHistory();
  let cntWon = 0;
  let cntLost = 0;
  let cntRefund = 0;

  signals.forEach(s => {
    if (s.status === 'won') cntWon++;
    else if (s.status === 'lost') cntLost++;
    else if (s.status === 'refund') cntRefund++;
  });

  const total = signals.length;
  const settled = cntWon + cntLost;
  const winRate = settled > 0 ? ((cntWon / settled) * 100).toFixed(1) : '0.0';

  // Update counters
  const cntAllEl = document.getElementById('hist-cnt-all');
  const cntWonEl = document.getElementById('hist-cnt-won');
  const cntLostEl = document.getElementById('hist-cnt-lost');
  const cntRefEl = document.getElementById('hist-cnt-refund');
  if (cntAllEl) cntAllEl.textContent = total;
  if (cntWonEl) cntWonEl.textContent = cntWon;
  if (cntLostEl) cntLostEl.textContent = cntLost;
  if (cntRefEl) cntRefEl.textContent = cntRefund;

  const kTotal = document.getElementById('kpi-hist-total');
  const kWon = document.getElementById('kpi-hist-won');
  const kLost = document.getElementById('kpi-hist-lost');
  const kRef = document.getElementById('kpi-hist-refund');
  const kWinRate = document.getElementById('kpi-hist-winrate');
  const kBadge = document.getElementById('hist-total-badge');

  if (kTotal) kTotal.textContent = total + ' Laga';
  if (kWon) kWon.textContent = cntWon;
  if (kLost) kLost.textContent = cntLost;
  if (kRef) kRef.textContent = cntRefund;
  if (kWinRate) kWinRate.textContent = winRate + '%';
  if (kBadge) kBadge.textContent = total > 0 ? `✅ ${cntWon} Tembus dari ${total} Laga Selesai` : '📭 Belum Ada Sinyal Selesai';

  // Search filter
  const query = (document.getElementById('hist-search-input')?.value || '').toLowerCase().trim();

  let filtered = signals;
  if (activeHistFilter !== 'all') {
    filtered = filtered.filter(s => s.status === activeHistFilter);
  }
  if (query) {
    filtered = filtered.filter(s => s.home.toLowerCase().includes(query) || s.away.toLowerCase().includes(query) || (s.sigLabel && s.sigLabel.toLowerCase().includes(query)));
  }

  // Urutkan sinyal terbaru di atas
  filtered.sort((a, b) => new Date(b.finishedAt || b.date).getTime() - new Date(a.finishedAt || a.date).getTime());

  if (!filtered.length) {
    container.innerHTML = '';
    if (emptyState) emptyState.classList.remove('hidden');
    return;
  }

  if (emptyState) emptyState.classList.add('hidden');
  container.innerHTML = filtered.map(s => {
    let badge = '';
    let borderClass = 'border-[var(--border)]';
    if (s.status === 'won') {
      badge = '<span class="text-[10px] px-2 py-0.5 rounded font-black bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">✅ TEMBUS</span>';
      borderClass = 'border-emerald-300 dark:border-emerald-800';
    } else if (s.status === 'lost') {
      badge = '<span class="text-[10px] px-2 py-0.5 rounded font-black bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300">❌ MELESET</span>';
      borderClass = 'border-rose-300 dark:border-rose-800';
    } else {
      badge = '<span class="text-[10px] px-2 py-0.5 rounded font-black bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">🔄 REFUND</span>';
    }

    return `
      <div class="p-3 rounded-xl border ${borderClass} bg-[var(--card)] space-y-2 text-xs shadow-2xs">
        <div class="flex items-center justify-between text-[11px] text-[var(--muted-foreground)] pb-1 border-b border-[var(--border)]">
          <div class="flex items-center gap-1.5 font-bold text-[var(--foreground)]">
            <span class="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-[10px] font-extrabold border border-[var(--border)]">🇮🇩 ${s.round || 'LIGA 1'}</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-mono text-[10.5px] font-bold">${formatIndoDateTime(s.date, s.dateStr)}</span>
          </div>
          ${badge}
        </div>

        <div class="flex items-center justify-between py-1">
          <div class="flex items-center gap-1.5 flex-1 min-w-0">
            <img src="${s.homeLogo}" class="w-5 h-5 object-contain shrink-0" onerror="this.style.display='none'" />
            <span class="font-bold truncate text-[var(--foreground)]">${s.home}</span>
          </div>
          <div class="px-2.5 py-0.5 rounded-lg bg-[var(--muted)] font-mono font-black text-sm">
            ${s.hScore} - ${s.aScore}
          </div>
          <div class="flex items-center gap-1.5 flex-1 min-w-0 justify-end text-right">
            <span class="font-bold truncate text-[var(--foreground)]">${s.away}</span>
            <img src="${s.awayLogo}" class="w-5 h-5 object-contain shrink-0" onerror="this.style.display='none'" />
          </div>
        </div>

        <div class="p-2 rounded-lg bg-[var(--muted)] flex items-center justify-between text-[11px]">
          <div>
            <span class="text-[var(--muted-foreground)]">Sinyal:</span>
            <strong class="text-[var(--foreground)] ml-1">${s.sigLabel}</strong>
          </div>
          <div>
            <span class="text-[var(--muted-foreground)]">Odds:</span>
            <strong class="font-mono text-primary ml-1">@${s.sigOdds}</strong>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ══════════════════════════════════════════════
// TAB 3: ROLLING COMPOUND (3-MODE DNB LIGA 1)
// ══════════════════════════════════════════════
let compoundSolution = 1;
const COMPOUND_KEY = 'liga1_compound_state_v1';
let compoundState = JSON.parse(localStorage.getItem(COMPOUND_KEY) || JSON.stringify({
  step: 1,
  startCapital: 100000,
  currentBalance: 100000,
  history: []
}));

function setCompoundSolution(solNum) {
  compoundSolution = solNum;
  document.querySelectorAll('[id^="comp-btn-sol"]').forEach(el => {
    el.className = 'p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] cursor-pointer hover:border-primary/50 transition-all';
  });
  const activeBtn = document.getElementById('comp-btn-sol' + solNum);
  if (activeBtn) {
    activeBtn.className = 'p-3 rounded-xl border-2 border-primary bg-primary/5 cursor-pointer transition-all shadow-2xs';
  }
  renderCompoundCycle();
}

function renderCompoundCycle() {
  const card = document.getElementById('compound-cycle-card');
  if (!card) return;

  const currentStep = compoundState.step || 1;
  const currentBal = compoundState.currentBalance || 100000;

  // 7-Step Projection with 1.45 avg odds
  const stepsData = [
    { step: 1, odds: 1.45, stake: 100000, target: 145000 },
    { step: 2, odds: 1.42, stake: 145000, target: 205900 },
    { step: 3, odds: 1.48, stake: 205900, target: 304700 },
    { step: 4, odds: 1.44, stake: 304700, target: 438800 },
    { step: 5, odds: 1.46, stake: 438800, target: 640600 },
    { step: 6, odds: 1.45, stake: 640600, target: 928900 },
    { step: 7, odds: 1.50, stake: 928900, target: 1393400 }
  ];

  card.innerHTML = `
    <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5 flex-wrap gap-2">
      <div>
        <h3 class="text-xs sm:text-sm font-bold flex items-center gap-1.5">
          <span>📈</span>
          <span>Rolling Compound DNB Liga 1 (Siklus 7 Langkah)</span>
        </h3>
        <p class="text-[11px] text-[var(--muted-foreground)]">Memanfaatkan pasaran Draw No Bet (DNB) Liga 1 dengan proteksi seri refund.</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-950 px-2 py-1 rounded-md border border-emerald-200">
          Saldo Rolling: Rp ${currentBal.toLocaleString('id-ID')}
        </span>
        <button onclick="resetCompoundCycle()" class="btn-sm text-[10.5px] text-rose-500">Reset Cycle</button>
      </div>
    </div>

    <!-- Stepper Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 pt-2">
      ${stepsData.map(s => {
        const isDone = s.step < currentStep;
        const isCurrent = s.step === currentStep;
        let bg = 'bg-[var(--card)] border-[var(--border)]';
        let textStatus = `<span class="text-[9px] text-[var(--muted-foreground)]">Terkunci</span>`;
        if (isDone) {
          bg = 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800';
          textStatus = `<span class="text-[9px] font-bold text-emerald-600">✅ Selesai</span>`;
        } else if (isCurrent) {
          bg = 'bg-primary/10 border-primary ring-2 ring-primary/30';
          textStatus = `<span class="text-[9px] font-bold text-primary animate-pulse">Sedang Jalan</span>`;
        }

        return `
          <div class="p-2.5 rounded-xl border ${bg} space-y-1 text-center">
            <div class="flex items-center justify-between text-[10px]">
              <span class="font-bold">Step ${s.step}</span>
              ${textStatus}
            </div>
            <div class="text-[10px] text-[var(--muted-foreground)]">Odds ~${s.odds}</div>
            <div class="text-xs font-mono font-black text-emerald-600">Rp ${Math.round(s.target).toLocaleString('id-ID')}</div>
          </div>
        `;
      }).join('')}
    </div>

    <!-- Active Step Controls -->
    <div class="p-3 rounded-xl bg-[var(--muted)] border border-[var(--border)] flex flex-wrap items-center justify-between gap-3 text-xs mt-3">
      <div>
        <div class="font-bold text-[var(--foreground)]">Langkah Aktif: Step ${currentStep} dari 7</div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Pasang taruhan DNB pada pertandingan Liga 1 dengan modal <strong>Rp ${currentBal.toLocaleString('id-ID')}</strong>.</p>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="advanceCompound(true)" class="btn-primary py-1.5 px-3 text-xs flex items-center gap-1">
          <span>✅</span>
          <span>Menang (Naik Step)</span>
        </button>
        <button onclick="advanceCompound('refund')" class="btn-sm text-xs text-amber-600 flex items-center gap-1">
          <span>🔄</span>
          <span>Seri / Refund (Ulang Step)</span>
        </button>
        <button onclick="advanceCompound(false)" class="btn-sm text-xs text-rose-600 flex items-center gap-1">
          <span>❌</span>
          <span>Kalah (Gagal)</span>
        </button>
      </div>
    </div>
  `;
}

function advanceCompound(status) {
  if (status === true) {
    const currentStep = compoundState.step || 1;
    const estNext = Math.round((compoundState.currentBalance || 100000) * 1.45);
    compoundState.currentBalance = estNext;
    compoundState.step = Math.min(7, currentStep + 1);
    localStorage.setItem(COMPOUND_KEY, JSON.stringify(compoundState));
    renderCompoundCycle();
    showCustomDialog('Step Berhasil!', `Selamat! Anda berhasil tembus ke <strong>Step ${compoundState.step}</strong> dengan saldo <strong>Rp ${estNext.toLocaleString('id-ID')}</strong>.`, '🎉', [{ label: 'Lanjut', class: 'btn-primary' }]);
  } else if (status === 'refund') {
    showCustomDialog('Seri / Refund', 'Pertandingan imbang! Berkat Draw No Bet (DNB), modal Anda aman 100% dan step ini dapat diulang.', '🛡️', [{ label: 'OK', class: 'btn-primary' }]);
  } else {
    showCustomDialog('Siklus Terhenti', 'Tiket kalah. Siklus compound akan di-reset kembali ke Step 1 dengan modal awal Rp 100.000.', '⚠️', [
      { label: 'Mulai Baru', class: 'btn-primary', action: () => resetCompoundCycle() },
      { label: 'Batal', class: 'btn-sm' }
    ]);
  }
}

function resetCompoundCycle() {
  compoundState = {
    step: 1,
    startCapital: 100000,
    currentBalance: 100000,
    history: []
  };
  localStorage.setItem(COMPOUND_KEY, JSON.stringify(compoundState));
  renderCompoundCycle();
}

// ══════════════════════════════════════════════
// TAB 4: SMART PARLAY KHUSUS LIGA 1
// ══════════════════════════════════════════════
function renderSmartParlay() {
  const container = document.getElementById('smart-parlay-packages');
  if (!container) return;

  // Hanya gunakan laga mendatang yang memiliki odds 1xBet
  const upcoming = allFixtures.filter(f => isMatchUpcoming(f) && f.has1xBetOdds && f.odds);
  if (upcoming.length < 2) {
    container.innerHTML = '<div class="p-6 text-center text-xs text-[var(--muted-foreground)] col-span-3">Jadwal pertandingan aktif 1xBet belum mencukupi untuk paket parlay.</div>';
    return;
  }

  // Paket 1: 2-Fold Safe
  const p1_m1 = upcoming[0];
  const p1_m2 = upcoming[1] || upcoming[0];
  const p1_odds1 = Number((p1_m1.odds.h * 0.75).toFixed(2));
  const p1_odds2 = Number((p1_m2.odds.h * 0.75).toFixed(2));
  const p1_totalOdds = (p1_odds1 * p1_odds2).toFixed(2);

  // Paket 2: 3-Fold Value
  const p2_m1 = upcoming[0];
  const p2_m2 = upcoming[1] || upcoming[0];
  const p2_m3 = upcoming[2] || upcoming[0];
  const p2_odds1 = Number(p2_m1.odds.h);
  const p2_odds2 = Number((p2_m2.odds.h * 0.72).toFixed(2));
  const p2_odds3 = Number((p2_m3.odds.h * 0.75).toFixed(2));
  const p2_totalOdds = (p2_odds1 * p2_odds2 * p2_odds3).toFixed(2);

  // Paket 3: 4-Fold Longshot
  const p3_m1 = upcoming[0];
  const p3_m2 = upcoming[1] || upcoming[0];
  const p3_m3 = upcoming[2] || upcoming[0];
  const p3_m4 = upcoming[3] || upcoming[0];
  const p3_totalOdds = (Number(p3_m1.odds.h) * Number(p3_m2.odds.h) * 1.50 * 1.65).toFixed(2);

  container.innerHTML = `
    <!-- Paket 1 -->
    <div class="p-3.5 rounded-xl border border-emerald-300 dark:border-emerald-800 bg-emerald-50/30 dark:bg-emerald-950/20 space-y-3 flex flex-col justify-between">
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-black text-emerald-800 dark:text-emerald-200">🛡️ 2-Fold Safe Multiplier</span>
          <span class="text-[9.5px] px-2 py-0.5 rounded font-bold bg-emerald-200 text-emerald-900">Safety 90%</span>
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Kombinasi 2 sinyal DNB teraman di Pekan 6.</p>
        <div class="space-y-1.5 pt-1 text-xs">
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p1_m1.homeShort} DNB</span>
            <span class="font-mono font-bold text-primary">${p1_odds1}</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p1_m2.homeShort} DNB</span>
            <span class="font-mono font-bold text-primary">${p1_odds2}</span>
          </div>
        </div>
      </div>
      <div class="pt-2 border-t border-[var(--border)] flex items-center justify-between">
        <div>
          <span class="text-[10px] text-[var(--muted-foreground)] block">Total Odds 1xBet:</span>
          <strong class="text-base font-black text-emerald-600 font-mono">${p1_totalOdds}</strong>
        </div>
        <button onclick="placeParlayBet('2-Fold Safe Parlay', ${p1_totalOdds})" class="btn-primary py-1.5 px-3 text-xs font-bold">+ Simpan Parlay</button>
      </div>
    </div>

    <!-- Paket 2 -->
    <div class="p-3.5 rounded-xl border border-blue-300 dark:border-blue-800 bg-blue-50/30 dark:bg-blue-950/20 space-y-3 flex flex-col justify-between">
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-black text-blue-800 dark:text-blue-200">🚀 3-Fold Value Parlay</span>
          <span class="text-[9.5px] px-2 py-0.5 rounded font-bold bg-blue-200 text-blue-900">Worth-It</span>
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Kombinasi optimal reward &amp; resiko terkontrol.</p>
        <div class="space-y-1.5 pt-1 text-xs">
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p2_m1.homeShort} Win</span>
            <span class="font-mono font-bold text-primary">${p2_odds1}</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p2_m2.homeShort} DNB</span>
            <span class="font-mono font-bold text-primary">${p2_odds2}</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p2_m3.homeShort} DNB</span>
            <span class="font-mono font-bold text-primary">${p2_odds3}</span>
          </div>
        </div>
      </div>
      <div class="pt-2 border-t border-[var(--border)] flex items-center justify-between">
        <div>
          <span class="text-[10px] text-[var(--muted-foreground)] block">Total Odds 1xBet:</span>
          <strong class="text-base font-black text-blue-600 font-mono">${p2_totalOdds}</strong>
        </div>
        <button onclick="placeParlayBet('3-Fold Value Parlay', ${p2_totalOdds})" class="btn-primary py-1.5 px-3 text-xs font-bold">+ Simpan Parlay</button>
      </div>
    </div>

    <!-- Paket 3 -->
    <div class="p-3.5 rounded-xl border border-purple-300 dark:border-purple-800 bg-purple-50/30 dark:bg-purple-950/20 space-y-3 flex flex-col justify-between">
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-black text-purple-800 dark:text-purple-200">💣 4-Fold Longshot</span>
          <span class="text-[9.5px] px-2 py-0.5 rounded font-bold bg-purple-200 text-purple-900">Potensi Besar</span>
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)]">Payout maksimal dengan modal receh (Rp 25k-50k).</p>
        <div class="space-y-1.5 pt-1 text-xs">
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p3_m1.homeShort} Menang</span>
            <span class="font-mono font-bold text-primary">${p3_m1.odds.h}</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p3_m2.homeShort} Menang</span>
            <span class="font-mono font-bold text-primary">${p3_m2.odds.h}</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p3_m3.homeShort} 1X</span>
            <span class="font-mono font-bold text-primary">1.50</span>
          </div>
          <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex items-center justify-between">
            <span class="truncate max-w-[160px] font-semibold">${p3_m4.homeShort} DNB</span>
            <span class="font-mono font-bold text-primary">1.65</span>
          </div>
        </div>
      </div>
      <div class="pt-2 border-t border-[var(--border)] flex items-center justify-between">
        <div>
          <span class="text-[10px] text-[var(--muted-foreground)] block">Total Odds 1xBet:</span>
          <strong class="text-base font-black text-purple-600 font-mono">${p3_totalOdds}</strong>
        </div>
        <button onclick="placeParlayBet('4-Fold Longshot Parlay', ${p3_totalOdds})" class="btn-primary py-1.5 px-3 text-xs font-bold">+ Simpan Parlay</button>
      </div>
    </div>
  `;
}

async function placeParlayBet(name, odds) {
  const stake = 50000;
  const newBet = {
    id: 'b_' + Date.now(),
    match: name,
    home: 'Parlay',
    away: 'Liga 1',
    dateStr: 'Multi-Match',
    leagueCode: 'LIGA1',
    type: 'parlay',
    typeLabel: name,
    odds: Number(odds),
    stake: stake,
    status: 'pending',
    date: new Date().toISOString()
  };

  userBets.unshift(newBet);
  localStorage.setItem('liga1_user_bets_v1', JSON.stringify(userBets));
  await syncBetToCloud(newBet);
  renderBetKPIs();
  renderBetHistory();

  showCustomDialog('Parlay Ditambahkan!', `Paket <strong>${name}</strong> (Odds ${odds}) berhasil disimpan ke bankroll dengan modal Rp 50.000.`, '🎯', [{ label: 'Lihat di Bankroll', class: 'btn-primary' }]);
}

// ══════════════════════════════════════════════
// MESIN SIMULASI SISA LAWAN & KLASEMEN DINAMIS LIGA 1
// Menghitung Peluang Juara Berbasis Jadwal Sisa (SOS) & H2H
// ══════════════════════════════════════════════

let currentStandingsFilter = 'all';
let currentStandingsSort = 'pos';
let cachedStandingsProjections = [];

function teamMatch(fixtureName, standingsTeams) {
  if (!fixtureName) return null;
  const fn = fixtureName.toUpperCase().trim();
  const teamsList = standingsTeams || currentStandingsTeams || LIGA1_TEAMS;

  // 1. Exact match by full name or short name
  let t = teamsList.find(t => t.name.toUpperCase() === fn || (t.short && t.short.toUpperCase() === fn));
  if (t) return t;

  // 2. Normalized key match (e.g. PERSIJA, PERSIB, DEWA, etc.)
  const keyF = normalizeTeamKey(fixtureName);
  t = teamsList.find(t => normalizeTeamKey(t.name) === keyF || (t.short && normalizeTeamKey(t.short) === keyF));
  if (t) return t;

  // 3. Word overlap match (longest match wins)
  const words = fn.split(/\\s+/).filter(w => w.length > 3 && !['KOTA', 'BANTEN', 'RAYA', 'UNITED', 'FOOTBALL', 'CLUB'].includes(w));
  let best = null, bestScore = 0;
  teamsList.forEach(t => {
    const tn = t.name.toUpperCase();
    const score = words.filter(w => tn.includes(w)).length;
    if (score > bestScore) { bestScore = score; best = t; }
  });
  return bestScore > 0 ? best : null;
}


// ══════════════════════════════════════════════
// KALKULASI KLASEMEN RESMI 100% DINAMIS LIGA 1
// Menghitung poin, menang, seri, kalah, selisih gol, dan posisi klasemen
// secara otomatis dari setiap laga yang telah selesai (FT)
// ══════════════════════════════════════════════
function computeDynamicStandings(fixtures, baselineTeams) {
  if (!fixtures || !fixtures.length || !baselineTeams || !baselineTeams.length) {
    return baselineTeams || [];
  }

  const table = {};
  baselineTeams.forEach(t => {
    const k = normalizeTeamKey(t.name);
    table[k] = {
      ...t,
      played: 0,
      w: 0,
      d: 0,
      l: 0,
      gf: 0,
      ga: 0,
      gd: 0,
      pts: 0,
      formHistory: []
    };
  });

  const seenMatches = new Set();
  fixtures.forEach(f => {
    const isFT = f.status === 'FT' || f.isFinished || f.played;
    if (!isFT || f.homeScore === null || f.awayScore === null || f.homeScore === undefined || f.awayScore === undefined) return;
    const matchKey = f.id || `${f.week}_${f.home}_${f.away}`;
    if (seenMatches.has(matchKey)) return;
    seenMatches.add(matchKey);

    const hK = normalizeTeamKey(f.home);
    const aK = normalizeTeamKey(f.away);
    const hT = table[hK] || Object.values(table).find(t => normalizeTeamKey(t.name).includes(hK) || hK.includes(normalizeTeamKey(t.name)));
    const aT = table[aK] || Object.values(table).find(t => normalizeTeamKey(t.name).includes(aK) || aK.includes(normalizeTeamKey(t.name)));
    if (!hT || !aT) return;

    const hs = Number(f.homeScore);
    const as = Number(f.awayScore);

    hT.played++;
    aT.played++;
    hT.gf += hs; hT.ga += as; hT.gd = hT.gf - hT.ga;
    aT.gf += as; aT.ga += hs; aT.gd = aT.gf - aT.ga;

    if (hs > as) {
      hT.w++; hT.pts += 3;
      aT.l++;
      hT.formHistory.push('W'); aT.formHistory.push('L');
    } else if (hs < as) {
      aT.w++; aT.pts += 3;
      hT.l++;
      aT.formHistory.push('W'); hT.formHistory.push('L');
    } else {
      hT.d++; hT.pts += 1;
      aT.d++; aT.pts += 1;
      hT.formHistory.push('D'); aT.formHistory.push('D');
    }
  });

  const sorted = Object.values(table).sort((a, b) => {
    if (b.pts !== a.pts) return b.pts - a.pts;
    if (b.gd !== a.gd) return b.gd - a.gd;
    return b.gf - a.gf;
  });

  sorted.forEach((t, idx) => {
    t.rank = idx + 1;
    t.pos = idx + 1;
    t.remaining = Math.max(0, 34 - t.played);
    t.ppg = t.played > 0 ? Number((t.pts / t.played).toFixed(3)) : 0;
    if (t.formHistory && t.formHistory.length) {
      t.form = t.formHistory.slice(-5).join('');
    }
  });

  return sorted;
}

function calcScheduleBasedProjections(teamsList, fixtures) {
  if (!teamsList || !teamsList.length) return [];
  const tableMap = {};
  teamsList.forEach((t, idx) => {
    const played = Math.max(1, t.played || 0);
    const ppg = (t.pts || 0) / played;
    const gdPerGame = (t.gd || 0) / played;
    tableMap[t.name.toUpperCase()] = {
      ...t,
      pos: t.rank || (idx + 1),
      ppg,
      gdPerGame,
      rating: (ppg * 0.70) + (Math.max(-1.5, Math.min(1.5, gdPerGame)) * 0.20)
    };
  });

  // Filter unplayed fixtures
  const unplayed = (fixtures || []).filter(f => !f.played && f.status !== 'FT' && (f.homeScore === null || f.homeScore === undefined));

  const results = teamsList.map((t, idx) => {
    const nameU = t.name.toUpperCase();
    const myData = tableMap[nameU] || { rating: 1.35, ppg: 1.35, pos: idx + 1 };

    // Sisa pertandingan klub ini
    const myMatches = unplayed.filter(f => {
      const hT = teamMatch(f.home, teamsList);
      const aT = teamMatch(f.away, teamsList);
      return (hT && hT.name === t.name) || (aT && aT.name === t.name);
    });
    myMatches.sort((a, b) => (Number(a.week) || 0) - (Number(b.week) || 0));

    let totalExpectedPts = 0;
    const breakdown = [];
    const oppRatingsList = [];
    let homeMatchesCount = 0;
    let awayMatchesCount = 0;

    myMatches.forEach(f => {
      const hT = teamMatch(f.home, teamsList);
      const aT = teamMatch(f.away, teamsList);
      const isHome = (hT && hT.name === t.name);
      if (isHome) homeMatchesCount++; else awayMatchesCount++;

      const oppObj = isHome ? aT : hT;
      const oppName = oppObj ? oppObj.name : (isHome ? f.away : f.home);
      const oppData = tableMap[oppName.toUpperCase()] || { rating: 1.35, ppg: 1.35, pos: 10, pts: 0, logo: '' };
      oppRatingsList.push(oppData.rating);

      // 1. Kekuatan Lawan
      const oppRating = oppData.rating;

      // 2. Rekor H2H 5 Pertemuan Terakhir
      const h2h = getH2H(t.name, oppName);
      const h2hPpg = (3 * (h2h.w || 1) + 1 * (h2h.d || 1)) / 5;
      const h2hDelta = (h2hPpg - 1.35) * 0.25;

      // 3. Keunggulan Kandang / Tandang Liga 1 (+0.35 home boost)
      const venueDelta = isHome ? 0.35 : -0.25;

      // Perbedaan Rating Total Match
      const delta = (myData.rating - oppRating) + h2hDelta + venueDelta;

      // Probabilitas Match Liga 1
      let pH = Math.max(0.12, Math.min(0.78, 0.40 + delta * 0.18));
      let pD = Math.max(0.18, Math.min(0.35, 0.28 - Math.abs(delta) * 0.05));
      let pL = Math.max(0.08, 1.0 - pH - pD);
      const tot = pH + pD + pL;
      pH /= tot; pD /= tot; pL /= tot;

      // Expected Points untuk tim ini di match tersebut
      const xPts = +((3 * (isHome ? pH : pL) + 1 * pD)).toFixed(2);
      totalExpectedPts += xPts;

      // Tingkat kesulitan laga per individu lawan
      let diffLevel = 'Sedang';
      let diffBadge = '🟡 Sedang';
      let diffColor = 'text-amber-500';
      let diffBg = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
      if (oppRating >= 1.20 || (oppData.pos && oppData.pos <= 4)) {
        diffLevel = 'Berat';
        diffBadge = '🔴 Berat';
        diffColor = 'text-rose-500';
        diffBg = 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
      } else if (oppRating <= 0.88 || (oppData.pos && oppData.pos >= 15)) {
        diffLevel = 'Ringan';
        diffBadge = '🟢 Ringan';
        diffColor = 'text-emerald-500';
        diffBg = 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20';
      }

      breakdown.push({
        week: f.week || f.round || '?',
        dateStr: formatIndoDateTime(f.date, f.dateStr) || 'Jadwal Menyusul',
        oppName: oppObj ? (oppObj.short || oppObj.name) : oppName,
        oppFullName: oppName,
        oppLogo: oppObj ? (oppObj.logo || f.homeLogo || f.awayLogo) : '',
        oppPos: oppData.pos || 10,
        oppPpg: (oppData.ppg || 1.35).toFixed(2),
        isHome,
        venue: isHome ? '🏠 Kandang' : '✈️ Tandang',
        h2h: `${h2h.w}M ${h2h.d}S ${h2h.l}K`,
        xPts,
        diffLevel,
        diffBadge,
        diffColor,
        diffBg
      });
    });

    const avgOppRating = oppRatingsList.length ? (oppRatingsList.reduce((a, b) => a + b, 0) / oppRatingsList.length) : 1.35;
    let sosLabel = '🟡 Sedang';
    let sosColor = 'text-amber-500';
    let sosBg = 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border-amber-300 dark:border-amber-800';
    let sosDesc = 'Jadwal sisa berimbang menghadapi kombinasi rival atas dan bawah.';
    if (avgOppRating >= 0.96) {
      sosLabel = '🔴 Berat';
      sosColor = 'text-rose-500';
      sosBg = 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 border-rose-300 dark:border-rose-800';
      sosDesc = 'Jadwal sisa sangat menantang menghadapi mayoritas tim papan atas Liga 1.';
    } else if (avgOppRating <= 0.90) {
      sosLabel = '🟢 Ringan';
      sosColor = 'text-emerald-500';
      sosBg = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800';
      sosDesc = 'Jadwal sisa relatif menguntungkan menghadapi banyak tim di paruh bawah.';
    }

    const projPts = +((t.pts || 0) + totalExpectedPts).toFixed(1);
    const ptsMin = +((t.pts || 0) + (totalExpectedPts * 0.82)).toFixed(1);
    const ptsMax = +Math.min(34 * 3, (t.pts || 0) + (totalExpectedPts * 1.18)).toFixed(1);

    return {
      ...t,
      pos: idx + 1,
      remainingCount: myMatches.length,
      homeMatchesCount,
      awayMatchesCount,
      expectedAddPts: +totalExpectedPts.toFixed(1),
      avgOppRating: +avgOppRating.toFixed(2),
      projPts,
      ptsMin,
      ptsMax,
      sosLabel,
      sosColor,
      sosBg,
      sosDesc,
      breakdown
    };
  });

  // Softmax probabilitas juara proporsional berbasis proyeksi poin akhir
  const maxProj = Math.max(...results.map(r => r.projPts));
  const scores = results.map(r => Math.exp((r.projPts - maxProj) / 2.6));
  const totScore = scores.reduce((a, b) => a + b, 0);

  results.forEach((r, idx) => {
    r.probChamp = +((scores[idx] / totScore) * 100).toFixed(1);
  });

  return results;
}

function setStandingsFilter(f) {
  currentStandingsFilter = f;
  ['all', 'relegation'].forEach(k => {
    const btn = document.getElementById('st-filter-' + k);
    if (btn) btn.classList.toggle('active', k === f);
  });
  renderStandingsTable();
}

function setStandingsSort(s) {
  currentStandingsSort = s;
  const sel = document.getElementById('standings-sort-select');
  if (sel) sel.value = s;
  renderStandingsTable();
}

function renderStandingsTable() {
  const tbody = document.getElementById('standings-table-body');
  if (!tbody) return;

  // Hitung klasemen 100% dinamis dari data pertandingan terbaru
  currentStandingsTeams = computeDynamicStandings(allFixtures, currentStandingsTeams || LIGA1_TEAMS);
  const data = calcScheduleBasedProjections(currentStandingsTeams, allFixtures);
  cachedStandingsProjections = data;

  // 1. Render Summary KPI Cards
  const cardsContainer = document.getElementById('standings-summary-cards');
  if (cardsContainer && data.length) {
    const sortedByProb = [...data].sort((a, b) => b.probChamp - a.probChamp);
    const topFav = sortedByProb[0];
    const sortedBySosDesc = [...data].sort((a, b) => b.avgOppRating - a.avgOppRating);
    const hardestSos = sortedBySosDesc[0];
    const easiestSos = sortedBySosDesc[sortedBySosDesc.length - 1];

    cardsContainer.innerHTML = `
      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-1 shadow-2xs">
        <span class="text-[10.5px] text-[var(--muted-foreground)] font-semibold flex items-center gap-1">
          <span>🏁</span> Progres Musim
        </span>
        <div class="pt-0.5">
          <div class="font-extrabold text-xs text-[var(--foreground)]">Pekan 6 dari 34</div>
          <div class="text-[11px] text-[var(--muted-foreground)]">${34 - 6} Pekan Menuju Juara</div>
        </div>
      </div>

      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-1 shadow-2xs">
        <span class="text-[10.5px] text-[var(--muted-foreground)] font-semibold flex items-center gap-1">
          <span>🥇</span> Favorit Juara Utama
        </span>
        <div class="flex items-center gap-2 pt-0.5">
          <img src="${topFav.logo}" class="w-6 h-6 object-contain" onerror="this.style.display='none'" />
          <div class="truncate">
            <div class="font-extrabold text-xs text-[var(--foreground)] truncate">${topFav.short || topFav.name}</div>
            <div class="text-[11px] font-black text-emerald-600 dark:text-emerald-400">${topFav.probChamp}% Peluang</div>
          </div>
        </div>
      </div>

      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-1 shadow-2xs">
        <span class="text-[10.5px] text-[var(--muted-foreground)] font-semibold flex items-center gap-1">
          <span>⚔️</span> Sisa Lawan Paling Berat
        </span>
        <div class="flex items-center gap-2 pt-0.5">
          <img src="${hardestSos.logo}" class="w-6 h-6 object-contain" onerror="this.style.display='none'" />
          <div class="truncate">
            <div class="font-extrabold text-xs text-[var(--foreground)] truncate">${hardestSos.short || hardestSos.name}</div>
            <div class="text-[11px] font-bold text-rose-500">Jadwal Sisa 🔴 Berat</div>
          </div>
        </div>
      </div>

      <div class="p-3 rounded-xl border border-[var(--border)] bg-[var(--card)] space-y-1 shadow-2xs">
        <span class="text-[10.5px] text-[var(--muted-foreground)] font-semibold flex items-center gap-1">
          <span>🛣️</span> Sisa Lawan Paling Ringan
        </span>
        <div class="flex items-center gap-2 pt-0.5">
          <img src="${easiestSos.logo}" class="w-6 h-6 object-contain" onerror="this.style.display='none'" />
          <div class="truncate">
            <div class="font-extrabold text-xs text-[var(--foreground)] truncate">${easiestSos.short || easiestSos.name}</div>
            <div class="text-[11px] font-bold text-emerald-500">Jadwal Sisa 🟢 Ringan</div>
          </div>
        </div>
      </div>
    `;
  }

  // 2. Filter Table Rows
  let filtered = [...data];
  if (currentStandingsFilter === 'relegation') {
    filtered = filtered.filter(t => t.pos >= 16);
  }

  // 3. Sort Table Rows
  if (currentStandingsSort === 'prob') {
    filtered.sort((a, b) => b.probChamp - a.probChamp || b.projPts - a.projPts);
  } else if (currentStandingsSort === 'sos') {
    filtered.sort((a, b) => b.avgOppRating - a.avgOppRating || a.pos - b.pos);
  } else if (currentStandingsSort === 'proj') {
    filtered.sort((a, b) => b.projPts - a.projPts || b.probChamp - a.probChamp);
  } else {
    // default by official rank pos
    filtered.sort((a, b) => a.pos - b.pos);
  }

  // 4. Render Table Rows
  tbody.innerHTML = '';
  filtered.forEach(t => {
    const medal = t.pos === 1 ? '🥇 1' : t.pos === 2 ? '🥈 2' : t.pos === 3 ? '🥉 3' : `${t.pos}`;
    let zoneBorder = '';
    let zoneBadge = '';

    if (t.pos >= 16) {
      zoneBorder = 'border-l-4 border-l-rose-500';
      zoneBadge = `<span class="text-[9px] font-black px-1.5 py-0.5 rounded bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300">DEG</span>`;
    }

    // Form pills
    const formBadges = (t.form || '').split('').slice(-5).map(r => {
      const c = r === 'W' ? 'bg-emerald-500 text-white' : r === 'D' ? 'bg-amber-400 text-slate-900' : 'bg-rose-500 text-white';
      return `<span class="w-3.5 h-3.5 rounded-full ${c} inline-flex items-center justify-center text-[8.5px] font-black">${r}</span>`;
    }).join(' ');

    // Progress bar color
    const pColor = t.probChamp >= 15 ? '#10b981' : (t.probChamp >= 8 ? '#3b82f6' : (t.probChamp >= 3 ? '#f59e0b' : '#94a3b8'));
    const barWidth = Math.min(100, Math.max(3, t.probChamp * 4.5));

    const tr = document.createElement('tr');
    tr.className = `hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors cursor-pointer ${zoneBorder}`;
    tr.onclick = () => openScheduleBreakdown(t.name);

    tr.innerHTML = `
      <td class="py-2.5 px-3 text-center whitespace-nowrap">
        <div class="flex items-center justify-center gap-1">
          <span class="font-extrabold text-xs text-[var(--foreground)]">${medal}</span>
          ${zoneBadge}
        </div>
      </td>
      <td class="py-2.5 px-3 min-w-[180px]">
        <div class="flex items-center gap-2.5">
          <img src="${t.logo}" class="w-6 h-6 object-contain shrink-0" onerror="this.style.display='none'" />
          <div class="min-w-0">
            <div class="font-bold text-xs text-[var(--foreground)] truncate">${t.short || t.name}</div>
            <div class="flex items-center gap-1 mt-0.5">${formBadges}</div>
          </div>
        </div>
      </td>
      <td class="py-2.5 px-2 text-center text-slate-600 dark:text-slate-400 font-semibold">${t.played}</td>
      <td class="py-2.5 px-2 text-center text-emerald-600 dark:text-emerald-400 font-bold">${t.w}</td>
      <td class="py-2.5 px-2 text-center text-slate-500">${t.d}</td>
      <td class="py-2.5 px-2 text-center text-rose-500">${t.l}</td>
      <td class="py-2.5 px-2 text-center font-semibold ${t.gd > 0 ? 'text-emerald-600' : t.gd < 0 ? 'text-rose-500' : 'text-slate-400'}">${t.gd > 0 ? '+' : ''}${t.gd}</td>
      <td class="py-2.5 px-3 text-center text-sm font-black text-[var(--foreground)]">${t.pts}</td>
      <td class="py-2.5 px-2 text-center text-[11px] text-[var(--muted-foreground)] font-bold">${t.remainingCount}</td>
      <td class="py-2.5 px-3 text-center">
        <div class="inline-flex items-center gap-1.5">
          <span class="px-2 py-0.5 rounded-full text-[10.5px] font-black border ${t.sosBg}">${t.sosLabel}</span>
          <button onclick="event.stopPropagation(); openScheduleBreakdown('${t.name}')" class="btn-sm text-[10px] py-0.5 px-2 font-bold hover:border-primary shrink-0" title="Klik untuk rincian laga sisa">🔍 Sisa Lawan</button>
        </div>
      </td>
      <td class="py-2.5 px-3 text-center">
        <div class="font-black text-xs text-[var(--foreground)]">${t.projPts} <span class="text-[10px] text-[var(--muted-foreground)] font-normal">pts</span></div>
        <div class="text-[9.5px] text-[var(--muted-foreground)] font-medium">Rentang ${t.ptsMin} - ${t.ptsMax}</div>
      </td>
      <td class="py-2.5 px-4 min-w-[150px]">
        <div class="flex items-center gap-2">
          <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-slate-700/80 overflow-hidden">
            <div class="h-full rounded-full transition-all duration-300" style="width: ${barWidth}%; background: ${pColor};"></div>
          </div>
          <span class="text-xs font-black min-w-[40px] text-right" style="color: ${pColor}">${t.probChamp.toFixed(1)}%</span>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function openScheduleBreakdown(teamName) {
  const modal = document.getElementById('schedule-breakdown-modal');
  if (!modal) return;

  const data = cachedStandingsProjections.length ? cachedStandingsProjections : calcScheduleBasedProjections(currentStandingsTeams || LIGA1_TEAMS, allFixtures);
  const t = data.find(x => x.name.toUpperCase() === (teamName || '').toUpperCase() || (x.short && x.short.toUpperCase() === (teamName || '').toUpperCase())) || data[0];
  if (!t) return;

  // Header
  const logoEl = document.getElementById('sched-modal-logo');
  if (logoEl) logoEl.innerHTML = `<img src="${t.logo}" class="w-full h-full object-contain" />`;

  const teamEl = document.getElementById('sched-modal-team');
  if (teamEl) teamEl.textContent = t.name;

  const rankBadge = document.getElementById('sched-modal-rank-badge');
  if (rankBadge) rankBadge.textContent = `Peringkat #${t.pos} · ${t.pts} Poin`;

  // 4 KPIs
  const kpis = document.getElementById('sched-modal-kpis');
  if (kpis) {
    kpis.innerHTML = `
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)] space-y-0.5">
        <span class="text-[10px] text-[var(--muted-foreground)] block">Poin Sekarang:</span>
        <strong class="text-sm font-black text-[var(--foreground)]">${t.pts} Pts</strong>
        <span class="text-[10px] text-[var(--muted-foreground)] block">${t.played} laga dimainkan</span>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)] space-y-0.5">
        <span class="text-[10px] text-[var(--muted-foreground)] block">Estimasi Tambahan:</span>
        <strong class="text-sm font-black text-emerald-600 dark:text-emerald-400">+${t.expectedAddPts} Pts</strong>
        <span class="text-[10px] text-[var(--muted-foreground)] block">Dari ${t.remainingCount} sisa laga</span>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)] space-y-0.5">
        <span class="text-[10px] text-[var(--muted-foreground)] block">Proyeksi Poin Akhir:</span>
        <strong class="text-sm font-black text-primary">${t.projPts} Pts</strong>
        <span class="text-[10px] text-[var(--muted-foreground)] block">Rentang ${t.ptsMin} - ${t.ptsMax}</span>
      </div>
      <div class="p-2.5 rounded-xl border border-[var(--border)] bg-[var(--background)] space-y-0.5">
        <span class="text-[10px] text-[var(--muted-foreground)] block">Peluang Juara:</span>
        <strong class="text-sm font-black text-emerald-600 dark:text-emerald-400">${t.probChamp}%</strong>
        <span class="text-[10px] text-[var(--muted-foreground)] block">Metode SOS Empiris</span>
      </div>
    `;
  }

  // SOS Banner
  const sosBanner = document.getElementById('sched-modal-sos-banner');
  if (sosBanner) {
    sosBanner.className = `p-3 rounded-xl border flex flex-wrap items-center justify-between gap-3 text-xs ${t.sosBg}`;
    sosBanner.innerHTML = `
      <div>
        <div class="font-extrabold flex items-center gap-2">
          <span>Tingkat Kesulitan Jadwal Sisa (SOS):</span>
          <span class="px-2 py-0.5 rounded-full font-black text-xs border border-current">${t.sosLabel}</span>
        </div>
        <p class="text-[11px] mt-0.5 opacity-90">${t.sosDesc}</p>
      </div>
      <div class="text-[11px] font-bold opacity-90 flex items-center gap-2">
        <span>🏠 ${t.homeMatchesCount} Kandang</span>
        <span>•</span>
        <span>✈️ ${t.awayMatchesCount} Tandang</span>
      </div>
    `;
  }

  // Matches list
  const countEl = document.getElementById('sched-modal-matches-count');
  if (countEl) countEl.textContent = `${t.breakdown ? t.breakdown.length : 0} Pertandingan Sisa`;

  const listEl = document.getElementById('sched-modal-matches-list');
  if (listEl) {
    listEl.innerHTML = '';
    (t.breakdown || []).forEach(m => {
      const venueBadge = m.isHome
        ? `<span class="text-[9.5px] px-2 py-0.5 rounded font-extrabold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">🏠 Kandang (+0.35)</span>`
        : `<span class="text-[9.5px] px-2 py-0.5 rounded font-extrabold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300 dark:border-blue-800">✈️ Tandang (-0.25)</span>`;

      const xPtsColor = m.xPts >= 1.8 ? 'text-emerald-600 dark:text-emerald-400' : m.xPts >= 1.1 ? 'text-amber-500' : 'text-rose-500';

      listEl.insertAdjacentHTML('beforeend', `
        <div class="p-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] flex items-center justify-between gap-2.5 flex-wrap text-xs shadow-2xs">
          <div class="flex items-center gap-2.5 min-w-0">
            <span class="text-[10px] font-extrabold text-[var(--muted-foreground)] w-14 shrink-0">Pekan ${m.week}</span>
            ${venueBadge}
            <div class="flex items-center gap-2 min-w-0">
              <img src="${m.oppLogo}" class="w-5 h-5 object-contain shrink-0" onerror="this.style.display='none'" />
              <span class="font-bold text-[var(--foreground)] truncate">${m.oppName}</span>
            </div>
          </div>
          <div class="flex items-center gap-2.5 text-[11px] text-[var(--muted-foreground)] flex-wrap">
            <span>Kekuatan Lawan: <strong class="text-[var(--foreground)]">Pos #${m.oppPos} (${m.oppPpg} PPG)</strong></span>
            <span>·</span>
            <span>H2H: <strong class="text-[var(--foreground)]">${m.h2h}</strong></span>
            <span>·</span>
            <span class="px-2 py-0.5 rounded font-bold border text-[10px] ${m.diffBg}">${m.diffBadge}</span>
            <span>·</span>
            <span class="font-black text-xs ${xPtsColor}">+${m.xPts.toFixed(2)} pts</span>
          </div>
        </div>
      `);
    });
  }

  modal.style.display = 'flex';
}

function closeScheduleBreakdown() {
  const modal = document.getElementById('schedule-breakdown-modal');
  if (modal) modal.style.display = 'none';
}

// Close breakdown modal on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeScheduleBreakdown();
});

// ══════════════════════════════════════════════
// NAVIGATION TABS SWITCHER
// ══════════════════════════════════════════════

// ══════════════════════════════════════════════
// JADWAL & HASIL LIGA 1 (LIVE 100% DINAMIS ENGINE)
// ══════════════════════════════════════════════
let scheduleWeekFilter = 'all';
let scheduleSortAsc = true;

function getCurrentLeagueWeek() {
  if (!allFixtures || !allFixtures.length) return 6;
  const liveMatch = allFixtures.find(f => f.isLive);
  if (liveMatch) return liveMatch.week;
  const upcomingMatch = allFixtures.find(f => isMatchUpcoming(f));
  if (upcomingMatch) return upcomingMatch.week;
  const played = allFixtures.filter(f => f.played || f.status === 'FT');
  if (played.length) return played[played.length - 1].week;
  return 6;
}

function filterScheduleActiveWeek() {
  filterScheduleWeek(getCurrentLeagueWeek());
}

function filterScheduleWeek(w) {
  scheduleWeekFilter = (w === 'all' || w === 'live') ? w : parseInt(w);
  const dropdown = document.getElementById('sched-week-dropdown');
  if (dropdown) dropdown.value = scheduleWeekFilter;

  document.querySelectorAll('#sched-week-chips .chip').forEach(c => {
    const isLive = c.id === 'sched-chip-live';
    const isAll = c.id === 'sched-chip-all';
    if (isLive) {
      c.classList.toggle('active', scheduleWeekFilter === 'live');
    } else if (isAll) {
      c.classList.toggle('active', scheduleWeekFilter === 'all');
    } else {
      const wk = parseInt(c.id.replace('sched-chip-', ''));
      c.classList.toggle('active', wk === scheduleWeekFilter);
    }
  });

  renderScheduleMatches();
}

function toggleScheduleSort() {
  scheduleSortAsc = !scheduleSortAsc;
  const btn = document.getElementById('sched-sort-btn');
  if (btn) btn.textContent = scheduleSortAsc ? '⏱️ Urutan: Terlama ➔ Terbaru' : '⏱️ Urutan: Terbaru ➔ Terlama';
  renderScheduleMatches();
}

function buildScheduleWeekChips() {
  if (!allFixtures || !allFixtures.length) return;
  const weeks = [...new Set(allFixtures.map(f => f.week))].sort((a,b) => a - b);
  const container = document.getElementById('sched-week-chips');
  const dropdown = document.getElementById('sched-week-dropdown');
  const liveMatches = allFixtures.filter(f => f.isLive);
  const activeWk = getCurrentLeagueWeek();

  if (dropdown) {
    let dropHtml = `<option value="all">Semua Pekan (Total ${allFixtures.length} Laga)</option>`;
    if (liveMatches.length) {
      dropHtml += `<option value="live">🔴 Sedang LIVE (${liveMatches.length} Laga)</option>`;
    }
    weeks.forEach(w => {
      const isCur = w === activeWk ? ' ⭐ (Pekan Ini)' : '';
      const isEnd = w === weeks[weeks.length-1] ? ' 🏁 (Akhir Musim)' : '';
      dropHtml += `<option value="${w}">Pekan ${w}${isCur}${isEnd}</option>`;
    });
    dropdown.innerHTML = dropHtml;
    dropdown.value = scheduleWeekFilter;
  }

  if (container) {
    let chipsHtml = '';
    if (liveMatches.length) {
      chipsHtml += `<span class="chip ${scheduleWeekFilter === 'live' ? 'active' : ''}" onclick="filterScheduleWeek('live')" id="sched-chip-live" style="background:#ef4444;color:white;font-weight:900;animation:pulse 1.2s infinite">🔴 LIVE (${liveMatches.length})</span>`;
    }
    chipsHtml += `<span class="chip ${scheduleWeekFilter === 'all' ? 'active' : ''}" onclick="filterScheduleWeek('all')" id="sched-chip-all">Semua (${allFixtures.length})</span>`;

    weeks.forEach(w => {
      const isCur = w === activeWk ? ' ⭐' : '';
      const isEnd = w === weeks[weeks.length-1] ? ' 🏁' : '';
      chipsHtml += `<span class="chip ${scheduleWeekFilter === w ? 'active' : ''}" onclick="filterScheduleWeek(${w})" id="sched-chip-${w}">Pekan ${w}${isCur}${isEnd}</span>`;
    });
    container.innerHTML = chipsHtml;
  }
}

function renderScheduleBanner() {
  const liveMatches = (allFixtures || []).filter(f => f.isLive);
  const banner = document.getElementById('sched-live-banner');
  const quickBtn = document.getElementById('sched-live-quick-btn');
  const quickCount = document.getElementById('sched-live-count-num');

  if (liveMatches.length > 0) {
    if (banner) {
      banner.className = 'mb-3 space-y-2';
      banner.innerHTML = liveMatches.map(m => `
        <div class="flex items-center justify-between gap-3 flex-wrap p-3 rounded-xl bg-red-500/10 border-2 border-red-500 text-red-600 dark:text-red-400 font-medium shadow-md">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black bg-red-600 text-white animate-pulse">
              🔴 SEDANG LIVE
            </span>
            <span class="font-bold text-sm text-[var(--foreground)]">
              ${m.home} <span class="px-2.5 py-0.5 rounded bg-red-600 text-white font-extrabold text-base mx-1">${m.homeScore ?? 0} — ${m.awayScore ?? 0}</span> ${m.away}
            </span>
            <span class="text-xs font-bold text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-950/60 px-2 py-0.5 rounded border border-red-300 dark:border-red-800">
              ⏱️ Menit ${m.elapsed || '1'}' ⚽ (${m.status})
            </span>
            <span class="text-xs text-[var(--muted-foreground)]">· ${m.venue || 'Stadion'}</span>
          </div>
          <button onclick="setMainTab('fixtures'); filterScheduleWeek('live');" class="btn-sm text-xs py-1.5 px-3 bg-red-600 hover:bg-red-700 text-white font-bold border-none shadow-sm cursor-pointer rounded-lg">
            Fokus Laga Live ➔
          </button>
        </div>
      `).join('');
    }
    if (quickBtn) {
      quickBtn.style.display = 'inline-flex';
      if (quickCount) quickCount.textContent = liveMatches.length;
    }
  } else {
    if (banner) {
      banner.className = 'hidden';
      banner.innerHTML = '';
    }
    if (quickBtn) quickBtn.style.display = 'none';
  }
}

function renderScheduleMatches() {
  const grid = document.getElementById('sched-match-grid');
  if (!grid) return;
  grid.innerHTML = '';

  let filtered;
  if (scheduleWeekFilter === 'live') {
    filtered = allFixtures.filter(f => f.isLive);
  } else if (scheduleWeekFilter === 'all') {
    filtered = [...allFixtures];
  } else {
    filtered = allFixtures.filter(f => f.week === scheduleWeekFilter);
  }

  // Filter duplicate keys
  const seen = new Set();
  filtered = filtered.filter(f => {
    const k = `${f.week}_${f.home}_${f.away}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });

  if (!filtered.length) {
    grid.innerHTML = (scheduleWeekFilter === 'live')
      ? '<div class="p-8 text-center text-xs text-[var(--muted-foreground)] col-span-2 border border-dashed border-[var(--border)] rounded-xl">Saat ini tidak ada pertandingan Liga 1 yang sedang bertanding (LIVE). Silakan pilih pekan terkait untuk melihat jadwal berikutnya.</div>'
      : '<div class="p-8 text-center text-xs text-[var(--muted-foreground)] col-span-2 border border-dashed border-[var(--border)] rounded-xl">Tidak ada pertandingan pada filter pekan ini.</div>';
    return;
  }

  filtered.sort((a,b) => {
    const tA = a.timestamp || 0;
    const tB = b.timestamp || 0;
    return scheduleSortAsc ? tA - tB : tB - tA;
  });

  const cardsHtml = filtered.map(f => {
    const isLive = !!f.isLive;
    const isPlayed = !!(f.played || f.status === 'FT');
    const isPst = f.status === 'PST';

    let cardBorder = isLive
      ? 'border-2 border-red-500 shadow-md ring-2 ring-red-500/20 bg-red-500/5'
      : 'border border-[var(--border)] bg-[var(--card)]';

    let statusBadge = '';
    if (isLive) {
      statusBadge = `<span class="px-2.5 py-1 rounded-md text-[11px] font-black bg-red-600 text-white animate-pulse shadow-sm">🔴 LIVE ${f.elapsed ? f.elapsed + "'" : f.status}</span>`;
    } else if (isPst) {
      statusBadge = `<span class="px-2 py-0.5 rounded text-[10.5px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800">⏳ Diundur</span>`;
    } else if (isPlayed) {
      statusBadge = `<span class="px-2 py-0.5 rounded text-[10.5px] font-semibold bg-[var(--muted)] text-[var(--muted-foreground)]">Selesai (FT)</span>`;
    } else {
      statusBadge = `<span class="px-2 py-0.5 rounded text-[10.5px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">Mendatang</span>`;
    }

    let scoreOrTimeHtml = '';
    if (isLive || isPlayed) {
      const hs = f.homeScore ?? 0;
      const as = f.awayScore ?? 0;
      const winH = hs > as;
      const winA = as > hs;
      const liveSubtitle = isLive ? `<div class="text-[11.5px] font-extrabold text-red-600 dark:text-red-400 mt-1 flex items-center justify-center gap-1.5 animate-pulse">⏱️ Menit ${f.elapsed || '1'}' ⚽ (${f.status})</div>` : '';
      scoreOrTimeHtml = `
        <div class="flex flex-col items-center justify-center my-1">
          <div class="flex items-center gap-3">
            <span class="text-2xl font-black ${isLive ? 'text-red-600' : winH ? 'text-emerald-600' : 'text-[var(--foreground)]'}">${hs}</span>
            <span class="text-sm font-bold text-[var(--muted-foreground)]">—</span>
            <span class="text-2xl font-black ${isLive ? 'text-red-600' : winA ? 'text-emerald-600' : 'text-[var(--foreground)]'}">${as}</span>
          </div>
          ${liveSubtitle}
        </div>`;
    } else if (isPst) {
      scoreOrTimeHtml = `<div class="text-center text-xs font-bold text-amber-600 my-2">⏳ Jadwal Pertandingan Diundur</div>`;
    } else {
      scoreOrTimeHtml = `
        <div class="text-center my-1.5">
          <div class="text-xs font-extrabold text-[var(--foreground)]">${formatIndoDateTime(f.date, f.dateStr) || 'Segera Hadir'}</div>
          <div class="text-[10px] text-[var(--muted-foreground)] mt-0.5">Kick-off Resmi</div>
        </div>`;
    }

    let oddsFooter = '';
    if (isLive) {
      oddsFooter = `
        <div class="mt-2.5 pt-2 border-t border-red-200 dark:border-red-900/50 flex items-center justify-between text-[11px] font-bold text-red-600 dark:text-red-400">
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-red-600 animate-ping"></span>
            <span>Pertandingan Sedang Berlangsung di Lapangan</span>
          </span>
          <span class="px-2 py-0.5 rounded bg-white dark:bg-red-950 text-red-600 border border-red-300 dark:border-red-800">Menit ${f.elapsed ? f.elapsed + "'" : f.status}</span>
        </div>`;
    } else if (f.odds && f.odds.h) {
      oddsFooter = `
        <div class="mt-2.5 pt-2 border-t border-[var(--border)] flex items-center justify-between text-[10.5px] text-[var(--muted-foreground)]">
          <span class="font-bold text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
            <span>⚡ Pasaran 1xBet:</span>
          </span>
          <div class="flex items-center gap-2 font-mono font-bold text-[var(--foreground)]">
            <span class="px-1.5 py-0.5 rounded bg-[var(--muted)]">1: ${Number(f.odds.h).toFixed(2)}</span>
            <span class="px-1.5 py-0.5 rounded bg-[var(--muted)]">X: ${Number(f.odds.d).toFixed(2)}</span>
            <span class="px-1.5 py-0.5 rounded bg-[var(--muted)]">2: ${Number(f.odds.a).toFixed(2)}</span>
          </div>
        </div>`;
    } else if (!isPlayed) {
      oddsFooter = `
        <div class="mt-2.5 pt-2 border-t border-[var(--border)] flex items-center justify-between text-[10px] text-[var(--muted-foreground)]">
          <span class="flex items-center gap-1"><span>⏳</span><span>Pasaran 1xBet: Belum Dibuka Bandar</span></span>
          <span class="text-[9.5px] opacity-75">Update Berkala</span>
        </div>`;
    }

    return `
      <div class="p-3.5 rounded-xl ${cardBorder} flex flex-col justify-between transition-all">
        <div>
          <!-- Card Header -->
          <div class="flex items-center justify-between gap-2 border-b border-[var(--border)] pb-2 mb-2.5 text-[11px]">
            <div class="flex items-center gap-1.5">
              <span class="px-2 py-0.5 rounded font-black bg-primary/10 text-primary border border-primary/20">Pekan ${f.week}</span>
              <span class="text-[var(--muted-foreground)] text-[10.5px] truncate max-w-[170px]" title="${f.venue || ''}">📍 ${f.venue || 'Stadion'}</span>
            </div>
            ${statusBadge}
          </div>

          <!-- Card Matchup -->
          <div class="grid grid-cols-[1fr_auto_1fr] items-center gap-2">
            <!-- Home Team -->
            <div class="flex items-center gap-2.5 min-w-0">
              <img src="${f.homeLogo || ''}" class="w-8 h-8 object-contain shrink-0" onerror="this.style.display='none'" alt="" />
              <div class="min-w-0">
                <div class="font-extrabold text-xs text-[var(--foreground)] truncate" title="${f.home}">${f.home}</div>
                <div class="text-[10px] text-[var(--muted-foreground)] font-medium">Kandang (H)</div>
              </div>
            </div>

            <!-- Score / Time -->
            <div class="px-2 shrink-0">
              ${scoreOrTimeHtml}
            </div>

            <!-- Away Team -->
            <div class="flex items-center gap-2.5 flex-row-reverse text-right min-w-0">
              <img src="${f.awayLogo || ''}" class="w-8 h-8 object-contain shrink-0" onerror="this.style.display='none'" alt="" />
              <div class="min-w-0 text-right">
                <div class="font-extrabold text-xs text-[var(--foreground)] truncate" title="${f.away}">${f.away}</div>
                <div class="text-[10px] text-[var(--muted-foreground)] font-medium">Tandang (A)</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Odds -->
        ${oddsFooter}
      </div>
    `;
  }).join('');

  grid.innerHTML = cardsHtml;
}

function renderScheduleTab() {
  buildScheduleWeekChips();
  renderScheduleBanner();
  renderScheduleMatches();
}

function setMainTab(tab) {
  const tabs = ['standings', 'fixtures', 'bet', 'history', 'compound', 'parlay'];
  tabs.forEach(t => {
    const el = document.getElementById('view-' + t);
    const btn = document.getElementById('main-tab-' + t);
    if (el) el.classList.toggle('hidden', t !== tab);
    if (btn) btn.classList.toggle('active', t === tab);
  });

  const activeBtn = document.getElementById('main-tab-' + tab);
  if (activeBtn) {
    activeBtn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }

  if (tab === 'fixtures') {
    renderScheduleTab();
  } else if (tab === 'standings') {
    renderStandingsTable();
  } else if (tab === 'history') {
    renderSignalHistoryView();
  } else if (tab === 'compound') {
    renderCompoundCycle();
  } else if (tab === 'parlay') {
    renderSmartParlay();
  }
}

// ══════════════════════════════════════════════
// MODAL & UTILITY FUNCTIONS
// ══════════════════════════════════════════════
function openOddsModal() {
  const m = document.getElementById('odds-modal');
  if (m) m.style.display = 'flex';
}

function closeOddsModal() {
  const m = document.getElementById('odds-modal');
  if (m) m.style.display = 'none';
}

// ══════════════════════════════════════════════
// DYNAMIC REAL-TIME API ENGINE (LIGA 1 INDONESIA)
// Terhubung Langsung ke TheSportsDB API (CORS Free, Bebas Proxy)
// ══════════════════════════════════════════════
const TSDB_BASE_URL = 'https://www.thesportsdb.com/api/v1/json/123';
const TSDB_LEAGUE_ID = '4790';
const TSDB_SEASON = '2026-2027';
let isSyncing = false;

function normalizeApiTeamName(rawName) {
  const n = (rawName || '').toUpperCase().trim();
  if (n.includes('PERSIJAP')) return 'PERSIJAP JEPARA';
  if (n.includes('PERSIJA')) return 'PERSIJA JAKARTA';
  if (n.includes('PERSIB')) return 'PERSIB BANDUNG';
  if (n.includes('PERSEBAYA')) return 'PERSEBAYA SURABAYA';
  if (n.includes('PERSIK')) return 'PERSIK KEDIRI';
  if (n.includes('PERSITA')) return 'PERSITA';
  if (n.includes('PSIM')) return 'PSIM YOGYAKARTA';
  if (n.includes('PSS') || n.includes('SLEMAN')) return 'PSS SLEMAN';
  if (n.includes('PSM')) return 'PSM MAKASSAR';
  if (n.includes('BORNEO')) return 'BORNEO FC SAMARINDA';
  if (n.includes('AREMA')) return 'AREMA FC';
  if (n.includes('BALI')) return 'BALI UNITED FC';
  if (n.includes('MADURA')) return 'MADURA UNITED FC';
  if (n.includes('DEWA')) return 'DEWA UNITED BANTEN FC';
  if (n.includes('BHAYANGKARA')) return 'BHAYANGKARA PRESISI LAMPUNG FC';
  if (n.includes('GARUDAYAKSA') || n.includes('GARUDA')) return 'GARUDAYAKSA FC';
  if (n.includes('JAVA')) return 'JAVA UNITED FC';
  if (n.includes('ISENMULANG') || n.includes('KALTENG')) return 'ISENMULANG KALTENG FC';
  return n;
}
// 🔒 STRICT INTEGRITY ASSERTION LOCK: PERSIJA VS PERSIJAP (PERMANENT LOCK)
(function verifyPersijaPersijapLock() {
  const kPersijap = normalizeTeamKey('PERSIJAP JEPARA');
  const kPersija = normalizeTeamKey('PERSIJA JAKARTA');
  const apiPersijap = normalizeApiTeamName('Persijap Jepara');
  const apiPersija = normalizeApiTeamName('Persija Jakarta');
  if (kPersijap === kPersija || apiPersijap === apiPersija || apiPersijap !== 'PERSIJAP JEPARA' || apiPersija !== 'PERSIJA JAKARTA') {
    throw new Error('FATAL: INTEGRITY LOCK BREACHED - PERSIJA AND PERSIJAP COLLIDED!');
  }
})();


async function fetchLiveRoundEvents(roundNum) {
  try {
    const res = await fetch(`${TSDB_BASE_URL}/eventsround.php?id=${TSDB_LEAGUE_ID}&r=${roundNum}&s=${TSDB_SEASON}`, {
      cache: 'no-cache'
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.events || [];
  } catch (err) {
    console.warn(`[Live API] Gagal memuat Pekan ${roundNum}:`, err.message);
    return [];
  }
}

async function syncLiga1Odds(manual = false) {
  if (isSyncing) return;
  isSyncing = true;

  const statusText = document.getElementById('status-text');
  const btnSync = document.getElementById('btn-sync-data');
  const standingsSyncText = document.getElementById('standings-sync-status-text');
  const btnSyncStandings = document.getElementById('btn-sync-standings');

  if (statusText) statusText.textContent = '⏳ Mengambil Data Real-Time API...';
  if (btnSync) btnSync.innerHTML = '<span class="inline-block w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin"></span> Sinkronisasi...';
  if (standingsSyncText) standingsSyncText.textContent = '⏳ Mengambil Data Skor & Klasemen API...';
  if (btnSyncStandings) btnSyncStandings.innerHTML = '<span class="inline-block w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin"></span> Sinkronisasi...';

  try {
    // 1. Ambil data LIVE Real-Time dari API-Sports Pro (League ID: 274)
    const APISPORTS_PRO_KEY = 'a43387e489a6880487b830a06d51d8c8';
    try {
      const liveRes = await fetch('https://v3.football.api-sports.io/fixtures?league=274&live=all', {
        headers: { 'x-apisports-key': APISPORTS_PRO_KEY }
      });
      if (liveRes.ok) {
        const liveJson = await liveRes.json();
        if (liveJson && Array.isArray(liveJson.response) && liveJson.response.length) {
          liveJson.response.forEach(lf => {
            const hRaw = lf.teams?.home?.name || '';
            const aRaw = lf.teams?.away?.name || '';
            const hStd = normalizeApiTeamName(hRaw);
            const aStd = normalizeApiTeamName(aRaw);

            const fix = allFixtures.find(f => {
              const fH = normalizeApiTeamName(f.home);
              const fA = normalizeApiTeamName(f.away);
              return fH === hStd && fA === aStd;
            });

            if (fix) {
              const st = lf.fixture?.status?.short || 'LIVE';
              fix.isLive = true;
              fix.played = false;
              fix.status = st;
              fix.elapsed = lf.fixture?.status?.elapsed || fix.elapsed;
              fix.homeScore = lf.goals?.home ?? fix.homeScore;
              fix.awayScore = lf.goals?.away ?? fix.awayScore;
            }
          });
        }
      }
    } catch (e) {
      console.warn('API-Sports live polling warning:', e);
    }

    // 2. Ambil data pekan 5, 6, 7, 8 secara serentak dari TheSportsDB
    const [eventsR5, eventsR6, eventsR7, eventsR8] = await Promise.all([
      fetchLiveRoundEvents(5),
      fetchLiveRoundEvents(6),
      fetchLiveRoundEvents(7),
      fetchLiveRoundEvents(8)
    ]);

    const allEvents = [...eventsR5, ...eventsR6, ...eventsR7, ...eventsR8];
    let updatedCount = 0;

    allEvents.forEach(ev => {
      const hStd = normalizeApiTeamName(ev.strHomeTeam);
      const aStd = normalizeApiTeamName(ev.strAwayTeam);

      // Cari laga yang cocok di allFixtures (prioritaskan pekan laga yang sama agar tidak salah sasaran)
      const evRound = Number(ev.intRound);
      let fixture = null;
      if (evRound) {
        fixture = allFixtures.find(f => {
          if (Number(f.week) !== evRound) return false;
          const fH = normalizeApiTeamName(f.home);
          const fA = normalizeApiTeamName(f.away);
          return fH === hStd && fA === aStd;
        });
      }
      if (!fixture) {
        fixture = allFixtures.find(f => {
          const fH = normalizeApiTeamName(f.home);
          const fA = normalizeApiTeamName(f.away);
          return fH === hStd && fA === aStd;
        });
      }

      if (fixture) {
        // 1. Update skor real-time
        const hScore = ev.intHomeScore !== null && ev.intHomeScore !== undefined && ev.intHomeScore !== '' ? Number(ev.intHomeScore) : null;
        const aScore = ev.intAwayScore !== null && ev.intAwayScore !== undefined && ev.intAwayScore !== '' ? Number(ev.intAwayScore) : null;
        fixture.homeScore = hScore;
        fixture.awayScore = aScore;

        // 2. Update status laga (FT, 1H, HT, 2H, LIVE, NS, PST)
        const st = (ev.strStatus || 'NS').trim();
        fixture.status = st;
        const isFT = st === 'FT' || st === 'AET' || st === 'PEN';
        fixture.played = isFT;
        fixture.isLive = st === '1H' || st === 'HT' || st === '2H' || st === 'LIVE';

        // 3. Update jadwal dinamis jika ada perubahan waktu kick-off / reschedule
        if (ev.dateEvent && ev.strTime) {
          let [hh, mm] = (ev.strTime || '15:30:00').slice(0, 5).split(':').map(Number);
          if (hh < 13) hh = (hh + 7) % 24; // Convert UTC to WIB
          const hhStr = String(hh).padStart(2, '0');
          const mmStr = String(mm).padStart(2, '0');
          fixture.dateStr = `${ev.dateEvent} ${hhStr}:${mmStr} WIB`;
          fixture.date = `${ev.dateEvent}T${hhStr}:${mmStr}:00+07:00`;
          fixture.timestamp = new Date(fixture.date).getTime();
        }

        updatedCount++;
      }
    });

    // Hitung ulang klasemen 100% dinamis setelah mendapat skor terbaru
    currentStandingsTeams = computeDynamicStandings(allFixtures, currentStandingsTeams || LIGA1_TEAMS);

    // Simpan ke local cache v5
    try {
      localStorage.setItem(`liga1_live_fixtures_cache_${CACHE_VERSION}`, JSON.stringify(allFixtures));
      localStorage.setItem(`liga1_dynamic_standings_${CACHE_VERSION}`, JSON.stringify(currentStandingsTeams));
      localStorage.setItem('liga1_last_sync_time', String(Date.now()));
    } catch (e) {}

    const nowStr = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + ' WIB';
    if (statusText) statusText.innerHTML = `🟢 Live API Terhubung (${nowStr})`;
    if (standingsSyncText) standingsSyncText.innerHTML = `🟢 Live API: Klasemen Otomatis Terhubung (${nowStr})`;

    // Perbarui tampilan antarmuka dan arsipkan laga FT jika ada sinyal
    renderValuePicks();
    renderSignalHistoryView();
    if (typeof renderStandingsTable === 'function') renderStandingsTable();
    if (typeof renderScheduleTab === 'function') renderScheduleTab();

    if (manual) {
      showCustomDialog(
        'Data Real-Time Diperbarui!',
        `Berhasil menyinkronkan <strong>${updatedCount} pertandingan</strong> langsung dari server TheSportsDB API.<br><br>• Skor, status FT/Live, dan perubahan jadwal diperbarui secara otomatis.`,
        '✅',
        [{ label: 'Selesai', class: 'btn-primary' }]
      );
    }
  } catch (err) {
    console.error('Error saat sinkronisasi live API:', err);
    if (statusText) statusText.textContent = '⚠️ API Terkendala, Menggunakan Data Cache';
    if (manual) {
      showCustomDialog(
        'Gagal Sinkronisasi API',
        'Tidak dapat menghubungi server API real-time TheSportsDB. Pastikan perangkat Anda terhubung ke internet.',
        '❌',
        [{ label: 'Tutup', class: 'btn-sm' }]
      );
    }
  } finally {
    isSyncing = false;
    if (btnSync) btnSync.innerHTML = '🔄 Segarkan Data';
    if (btnSyncStandings) btnSyncStandings.innerHTML = '<span>🔄</span> <span>Segarkan Klasemen</span>';
  }
}

function showCustomDialog(title, message, icon, buttons) {
  const m = document.getElementById('custom-dialog-modal');
  const t = document.getElementById('custom-dialog-title');
  const msg = document.getElementById('custom-dialog-message');
  const ic = document.getElementById('custom-dialog-icon');
  const btnContainer = document.getElementById('custom-dialog-buttons');

  if (!m || !t || !msg) return;

  t.textContent = title;
  msg.innerHTML = message;
  ic.textContent = icon || 'ℹ️';

  btnContainer.innerHTML = '';
  (buttons || [{ label: 'Tutup', class: 'btn-primary' }]).forEach(b => {
    const btn = document.createElement('button');
    btn.className = (b.class || 'btn-primary') + ' py-2 px-4 text-xs font-bold rounded-lg cursor-pointer';
    btn.textContent = b.label;
    btn.onclick = () => {
      m.style.display = 'none';
      if (typeof b.action === 'function') b.action();
    };
    btnContainer.appendChild(btn);
  });

  m.style.display = 'flex';
}

// ══════════════════════════════════════════════
// INITIALIZATION
// ══════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  renderStrategyPresetsGrid();
  renderValuePicks();
  initBankrollCloudSync();
  renderStandingsTable();
  setMainTab('standings');

  // Sinkronisasi live API real-time saat halaman pertama kali dibuka
  syncLiga1Odds(false);

  // Auto-refresh berkala setiap 60 detik dari live server TheSportsDB
  setInterval(() => {
    syncLiga1Odds(false);
  }, 60000);
});
</script>
</body>
</html>
"""

final_html = html_template.replace('__TEAMS_JSON__', teams_json).replace('__FIXTURES_JSON__', fixtures_json)

out_html_path = r'C:\Users\Win 10\.gemini\antigravity\scratch\liga1-bet-tracker\index.html'
with open(out_html_path, 'w', encoding='utf-8') as out:
    out.write(final_html)

print(f"Generated clean index.html successfully at {out_html_path} ({len(final_html)} bytes)")
