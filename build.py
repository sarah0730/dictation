# -*- coding: utf-8 -*-
import json, os

with open('words.json','r',encoding='utf-8') as f:
    DATA = json.load(f)
WORDS_JSON = json.dumps(DATA, ensure_ascii=False)

with open('cn_words.json','r',encoding='utf-8') as f:
    CN_DATA = json.load(f)
CN_JSON = json.dumps(CN_DATA, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>听写练习</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --pri:#FF8C42; --pri-d:#E06B20; --accent:#4FC3F7;
  --bg1:#FFF8F0; --bg2:#E3F2FD; --card:#fff;
  --text:#3D2C1D; --muted:#9B8B7D; --ok:#66BB6A; --err:#EF5350;
  --radius:18px; --shadow:0 4px 20px rgba(0,0,0,.08);
  --side-bg:rgba(255,255,255,.82); --side-border:rgba(0,0,0,.06);
}
body.subject-cn{
  --pri:#26A69A; --pri-d:#00897B; --accent:#80CBC4;
  --bg1:#F0FFF8; --bg2:#E0F7FA; --text:#1A3C34;
  --muted:#7A9B95;
}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  background:linear-gradient(135deg,var(--bg1),var(--bg2));
  color:var(--text);min-height:100vh;font-size:17px;line-height:1.5;
  transition:background .4s;
}
/* ===== 侧边栏 ===== */
.app{display:flex;min-height:100vh}
.sidebar{
  width:220px;position:fixed;left:0;top:0;height:100vh;
  background:var(--side-bg);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-right:1px solid var(--side-border);z-index:100;
  display:flex;flex-direction:column;padding:16px 12px;
  transition:transform .3s ease,background .4s;
}
.sidebar-logo{font-size:18px;font-weight:800;text-align:center;margin-bottom:16px;letter-spacing:1px}
.sidebar-logo span{color:var(--pri)}
.subj-tabs{display:flex;gap:6px;margin-bottom:16px}
.subj-tab{
  flex:1;padding:12px 8px;border-radius:14px;border:2px solid transparent;
  background:rgba(0,0,0,.04);text-align:center;cursor:pointer;transition:.2s;
}
.subj-tab .icon{font-size:24px;display:block;margin-bottom:4px}
.subj-tab .name{font-size:13px;font-weight:600;color:var(--muted)}
.subj-tab.active{background:var(--pri);border-color:var(--pri-d)}
.subj-tab.active .name{color:#fff}
.side-nav{flex:1;display:flex;flex-direction:column;gap:4px}
.side-nav-item{
  display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:12px;
  cursor:pointer;font-size:15px;font-weight:500;color:var(--text);
  transition:background .15s;
}
.side-nav-item:hover{background:rgba(0,0,0,.04)}
.side-nav-item.active{background:var(--pri);color:#fff;font-weight:600}
.side-nav-item .ic{font-size:18px;width:22px;text-align:center}
.side-foot{margin-top:auto;padding-top:12px;border-top:1px solid var(--side-border)}
.side-foot .side-nav-item{font-size:14px;color:var(--muted)}
.sb-toggle{display:none}
.sidebar-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.4);z-index:99}
/* ===== 主区域 ===== */
.main{flex:1;margin-left:220px;transition:margin .3s}
.wrap{max-width:680px;margin:0 auto;padding:12px 16px 24px}
.topbar{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.topbar h1{font-size:20px;font-weight:800;flex:1}
.topbar h1 span{color:var(--pri)}
/* ===== 卡片 ===== */
.card{background:var(--card);border-radius:16px;padding:14px 16px;box-shadow:var(--shadow);margin-bottom:12px;transition:box-shadow .2s}
.card:hover{box-shadow:0 6px 28px rgba(0,0,0,.1)}
.card h2{font-size:15px;margin-bottom:10px;color:var(--pri-d);font-weight:700}
label{display:block;font-size:14px;color:var(--muted);margin:10px 0 4px;font-weight:600}
/* ===== 按钮 ===== */
.btn{
  display:inline-block;border:none;border-radius:14px;padding:14px 28px;font-size:17px;font-weight:600;
  cursor:pointer;background:var(--pri);color:#fff;transition:transform .1s,filter .2s;text-align:center;
}
.btn:active{transform:scale(.96)}
.btn:hover{filter:brightness(1.06)}
.btn-block{display:block;width:100%}
.btn-lg{padding:16px 28px;font-size:18px}
.btn-ghost{background:#F5F0EB;color:var(--text)}
.btn-ghost.active{background:var(--pri);color:#fff}
.btn-sm{padding:6px 12px;font-size:13px;border-radius:10px}
.btn-dis{opacity:.4;pointer-events:none}
select,input[type=number],input[type=range]{
  width:100%;padding:10px 12px;border:2px solid #E8DFD3;border-radius:12px;font-size:16px;background:#fff;color:var(--text);
}
.row{display:flex;gap:10px;flex-wrap:wrap}
.row>*{flex:1;min-width:120px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{
  padding:7px 14px;border-radius:20px;background:#F5F0EB;font-size:13px;cursor:pointer;border:2px solid transparent;
  user-select:none;transition:.15s;font-weight:500;
}
.chip:hover{filter:brightness(.96)}
.chip.active{background:var(--pri);color:#fff;border-color:var(--pri-d)}
.chip.chip4.active{background:#FF7043}
.chip.chip2.active{background:#42A5F5}
.unit-list{display:flex;flex-direction:column;gap:5px;max-height:220px;overflow-y:auto;padding:2px}
.unit-item{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:#FAF6F1;border-radius:10px;cursor:pointer;font-size:13px;transition:.15s}
.unit-item:hover{background:#FFF3E0}
.unit-item.active{background:var(--pri);color:#fff}
.unit-item.active .cnt{color:rgba(255,255,255,.8)}
.unit-item .cnt{font-size:12px;color:var(--muted)}
/* ===== 词表浏览 ===== */
.word-grid{display:flex;flex-wrap:wrap;gap:8px}
.word-item{
  flex:1 1 30%;min-width:150px;background:#FAF6F1;border-radius:10px;padding:8px 12px;
  cursor:pointer;transition:background .15s;
}
.word-item:hover{background:#FFF3E0}
.word-item:active{transform:scale(.97)}
.word-item .w{font-weight:700;font-size:15px}
.word-item .ph{font-size:12px;color:var(--pri-d);font-family:Georgia,'Times New Roman',serif;margin-top:1px}
.word-item .m{font-size:12px;color:var(--muted);margin-top:1px}
.topic-h{font-size:13px;color:var(--pri-d);font-weight:700;margin:12px 0 4px}
/* ===== 听写页 ===== */
.dictate-area{text-align:center}
.big-word{font-size:32px;font-weight:700;margin:20px 0;min-height:48px;letter-spacing:1px}
.meaning-hint{font-size:20px;color:var(--muted);margin-bottom:16px;min-height:30px}
.play-btn{
  width:110px;height:110px;border-radius:50%;border:none;background:var(--pri);color:#fff;font-size:40px;
  cursor:pointer;box-shadow:0 6px 24px rgba(255,140,66,.4);margin:10px auto 20px;display:flex;align-items:center;justify-content:center;transition:transform .15s;
}
.play-btn:active{transform:scale(.92)}
.play-btn.playing{animation:pulse 1s infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
.progress-bar{height:8px;background:#F0E8DC;border-radius:4px;overflow:hidden;margin:14px 0}
.progress-bar .fill{height:100%;background:var(--pri);transition:width .3s;border-radius:4px}
.dictate-controls{display:flex;gap:10px;justify-content:center;margin-top:10px}
.word-num{font-size:13px;color:var(--muted);margin-bottom:6px}
.result-list{display:flex;flex-direction:column;gap:6px}
.result-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-radius:10px;background:#FAF6F1}
.result-item .w{font-weight:600}
.result-item .m{font-size:13px;color:var(--muted)}
.result-item .judge{display:flex;gap:6px}
.result-item .judge button{padding:6px 14px;border-radius:8px;border:none;font-size:13px;cursor:pointer;font-weight:600}
.judge .ok{background:#E8F5E9;color:#2E7D32}
.judge .ok.active{background:var(--ok);color:#fff}
.judge .no{background:#FFEBEE;color:#C62828}
.judge .no.active{background:var(--err);color:#fff}
.stat-box{display:flex;gap:10px;margin-bottom:14px}
.stat-box .stat{flex:1;background:#FAF6F1;border-radius:12px;padding:14px;text-align:center}
.stat .num{font-size:28px;font-weight:700;color:var(--pri-d)}
.stat .lbl{font-size:12px;color:var(--muted)}
.empty{text-align:center;padding:30px;color:var(--muted)}
.history-item{padding:12px;background:#FAF6F1;border-radius:10px;margin-bottom:8px;font-size:14px}
.history-item .hi-top{display:flex;justify-content:space-between;margin-bottom:4px}
.history-item .hi-range{font-weight:600}
.history-item .hi-stat{font-size:13px;color:var(--muted)}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge.b4{background:#FFE0B2;color:#E65100}
.badge.b2{background:#BBDEFB;color:#0D47A1}
.badge.bF{background:#E1BEE7;color:#4A148C}
.toggle-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0}
.toggle-row .t-label{font-size:15px;font-weight:600;color:var(--text)}
.toggle{width:48px;height:28px;background:#DDD;border-radius:14px;position:relative;cursor:pointer;transition:.2s}
.toggle.on{background:var(--ok)}
.toggle::after{content:'';position:absolute;width:22px;height:22px;background:#fff;border-radius:50%;top:3px;left:3px;transition:.2s}
.toggle.on::after{left:23px}
.range-val{font-size:13px;color:var(--pri-d);font-weight:600}
.tip{font-size:12px;color:var(--muted);background:#FFF8E1;border-radius:8px;padding:8px 10px;margin-top:8px;line-height:1.5}
.hide{display:none!important}
.mode-desc{font-size:13px;color:var(--muted);margin-top:6px;padding:8px 12px;background:#F5F0EB;border-radius:10px}
.wrong-item{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#FAF6F1;border-radius:10px;margin-bottom:6px}
.wrong-item .wi-w{font-weight:600}
.wrong-item .wi-m{font-size:13px;color:var(--muted)}
.wrong-item .del{background:none;border:none;color:var(--err);font-size:20px;cursor:pointer;padding:4px 8px}
/* 微信引导遮罩 */
.wx-mask{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.88);z-index:99999;text-align:center;color:#fff;-webkit-touch-callout:none}
.wx-mask .arrow{position:absolute;top:8px;right:16px;font-size:42px;animation:wx-bounce 1s ease-in-out infinite}
.wx-mask .tip-box{position:absolute;top:70px;right:16px;text-align:right;max-width:220px}
.wx-mask .tip-box p{font-size:16px;line-height:1.6;margin:0}
.wx-mask .center{padding-top:160px}
.wx-mask .icon{font-size:56px}
.wx-mask .title{font-size:19px;font-weight:700;margin-top:12px}
.wx-mask .desc{font-size:14px;margin-top:8px;padding:0 32px;line-height:1.6;color:rgba(255,255,255,.75)}
.wx-mask .step{font-size:14px;margin-top:14px;padding:0 32px;line-height:1.8;color:rgba(255,255,255,.6)}
.wx-mask .step b{color:#FFD54F}
@keyframes wx-bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
/* ===== 响应式：手机侧边栏抽屉 ===== */
@media(max-width:768px){
  .sidebar{transform:translateX(-100%);box-shadow:4px 0 30px rgba(0,0,0,.15)}
  .sidebar.open{transform:translateX(0)}
  .sidebar-overlay.show{display:block}
  .main{margin-left:0}
  .sb-toggle{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:var(--card);box-shadow:var(--shadow);font-size:20px;cursor:pointer;border:none}
  .wrap{padding:10px 12px 20px}
}
</style>
</head>
<body class="subject-en">

<div class="wx-mask" id="wxMask">
  <div class="arrow">↗️</div>
  <div class="tip-box"><p>请点击右上角<br>「···」按钮</p></div>
  <div class="center">
    <div class="icon">📱</div>
    <div class="title">请在 Safari 浏览器中打开</div>
    <div class="desc">微信内置浏览器无法播放语音，听写功能将无法正常使用。</div>
    <div class="step">请点击右上角 <b>「···」</b><br>→ 选择 <b>「在浏览器中打开」</b><br>→ 用 Safari 打开即可正常使用</div>
  </div>
</div>

<div class="app">
  <div class="sidebar-overlay" id="sbOverlay" onclick="closeSidebar()"></div>
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-logo">📝 <span>听写</span>练习</div>
    <div class="subj-tabs">
      <div class="subj-tab active" id="tab-en" onclick="switchSubject('en')"><span class="icon">🔤</span><span class="name">英语</span></div>
      <div class="subj-tab" id="tab-cn" onclick="switchSubject('cn')"><span class="icon">📖</span><span class="name">语文</span></div>
    </div>
    <nav class="side-nav">
      <div class="side-nav-item active" id="nav-home" onclick="go('home')"><span class="ic">✏️</span> 听写</div>
      <div class="side-nav-item" id="nav-wrong" onclick="go('wrong')"><span class="ic">📋</span> 错词本</div>
      <div class="side-nav-item" id="nav-history" onclick="go('history')"><span class="ic">📊</span> 记录</div>
      <div class="side-nav-item" id="nav-browse" onclick="go('browse')"><span class="ic">📚</span> 词表浏览</div>
    </nav>
    <div class="side-foot">
      <div class="side-nav-item" onclick="toggleSettings()"><span class="ic">⚙️</span> 设置</div>
    </div>
  </aside>

  <div class="main">
    <div class="wrap">
      <div class="topbar">
        <button class="sb-toggle" onclick="openSidebar()">☰</button>
        <h1 id="page-title">英语听写</h1>
      </div>

      <!-- 首页 -->
      <div id="view-home">
        <div class="card">
          <h2 id="book-title">选册别</h2>
          <div class="chips" id="book-chips"></div>
        </div>
        <div class="card" id="unit-card">
          <div class="row" style="align-items:center;margin-bottom:6px">
            <h2 style="margin:0" id="unit-title">选单元</h2>
            <div style="display:flex;gap:6px;margin-left:auto">
              <button class="btn btn-ghost btn-sm" onclick="unitAll(true)">全选</button>
              <button class="btn btn-ghost btn-sm" onclick="unitAll(false)">清除</button>
            </div>
          </div>
          <div class="unit-list" id="unit-list"></div>
        </div>
        <div class="card" id="settings-card" style="display:none">
          <h2>设置</h2>
          <div class="toggle-row" id="row-cn">
            <span class="t-label" id="lbl-cn">朗读时附带中文释义</span>
            <div class="toggle" id="set-cn" onclick="toggleSet('cn',this)"></div>
          </div>
          <div class="toggle-row">
            <span class="t-label" id="lbl-show-cn">听写时显示中文提示</span>
            <div class="toggle" id="set-show-cn" onclick="toggleSet('showCn',this)"></div>
          </div>
          <label>朗读语速 <span class="range-val" id="rate-val">0.8x</span></label>
          <input type="range" id="set-rate" min="0.5" max="1.2" step="0.1" value="0.8" oninput="setRange('rate',this.value,'rate-val','x')">
          <label>每词朗读次数 <span class="range-val" id="repeat-val">3 遍</span></label>
          <input type="range" id="set-repeat" min="1" max="3" step="1" value="3" oninput="setRange('repeat',this.value,'repeat-val',' 遍')">
          <label>朗读间隔 <span class="range-val" id="interval-val">4 秒</span></label>
          <input type="range" id="set-interval" min="2" max="20" step="1" value="4" oninput="setRange('interval',this.value,'interval-val',' 秒')">
          <div id="lang-row">
            <label>发音</label>
            <div class="chips" id="lang-chips">
              <div class="chip" data-lang="en-GB">🇬🇧 英音</div>
              <div class="chip active" data-lang="en-US">🇺🇸 美音</div>
            </div>
          </div>
          <label>语音嗓音（点试听后选择）</label>
          <div id="voice-list" style="max-height:180px;overflow-y:auto;border:1px solid #E8DFD3;border-radius:10px;padding:4px"></div>
          <button class="btn btn-ghost btn-sm" style="margin-top:6px" onclick="loadVoiceList()">🔄 刷新声音列表</button>
          <div class="toggle-row">
            <span class="t-label">自动连播下一题</span>
            <div class="toggle on" id="set-auto" onclick="toggleSet('auto',this)"></div>
          </div>
          <div style="border-top:1px solid #EEE;margin-top:10px;padding-top:10px">
            <label>进度备份（建议每周点一次）</label>
            <div class="row" style="margin-top:6px">
              <button class="btn btn-ghost btn-sm" onclick="exportData()">⬇ 导出备份</button>
              <button class="btn btn-ghost btn-sm" onclick="document.getElementById('import-file').click()">⬆ 导入恢复</button>
            </div>
            <input type="file" id="import-file" accept=".json" style="display:none" onchange="importData(event)">
          </div>
        </div>
        <div class="row" style="gap:8px;margin-bottom:8px">
          <div class="chips" id="count-chips" style="flex:1">
            <div class="chip" data-count="10">10个</div>
            <div class="chip active" data-count="15">15个</div>
            <div class="chip" data-count="20">20个</div>
            <div class="chip" data-count="0">全部</div>
          </div>
        </div>
        <button class="btn btn-lg btn-block" onclick="startDictation()">开始听写 ▶</button>
        <div class="tip" id="range-tip"></div>
      </div>

      <!-- 听写页 -->
      <div id="view-dictate" class="hide">
        <div class="card dictate-area">
          <div class="word-num" id="word-num">第 1 / 15 题</div>
          <div class="progress-bar"><div class="fill" id="prog-fill" style="width:0"></div></div>
          <div class="big-word" id="big-word">准备好了吗？</div>
          <div class="meaning-hint" id="meaning-hint"></div>
          <button class="play-btn" id="play-btn" onclick="playCurrent()">🔊</button>
          <div class="dictate-controls">
            <button class="btn btn-ghost btn-sm" onclick="prevWord()">⏮ 上一题</button>
            <button class="btn btn-ghost btn-sm" id="pause-btn" onclick="togglePause()">⏸ 暂停</button>
            <button class="btn btn-ghost btn-sm" onclick="nextWord()">下一题 ⏭</button>
          </div>
        </div>
        <button class="btn btn-ghost btn-block" onclick="endDictation(true)">结束并结算</button>
      </div>

      <!-- 结算页 -->
      <div id="view-result" class="hide">
        <div class="card">
          <h2>听写完成 🎉</h2>
          <div class="stat-box">
            <div class="stat"><div class="num" id="r-total">0</div><div class="lbl">总词数</div></div>
            <div class="stat"><div class="num" id="r-right" style="color:var(--ok)">0</div><div class="lbl">正确</div></div>
            <div class="stat"><div class="num" id="r-wrong" style="color:var(--err)">0</div><div class="lbl">错误</div></div>
          </div>
          <div style="font-size:14px;color:var(--muted);margin-bottom:10px">点击每个词标记对/错，错的会自动加入错词本：</div>
          <div class="result-list" id="result-list"></div>
        </div>
        <div class="row">
          <button class="btn btn-ghost" onclick="go('home')">返回</button>
          <button class="btn" onclick="replayWrong()">错词重听</button>
        </div>
      </div>

      <!-- 错词本 -->
      <div id="view-wrong" class="hide">
        <div class="card">
          <h2>错词本</h2>
          <div id="wrong-list"></div>
        </div>
        <button class="btn btn-block" onclick="startWrongDictation()">错词听写 ▶</button>
        <button class="btn btn-ghost btn-block" style="margin-top:8px" onclick="clearWrong()">清空错词本</button>
      </div>

      <!-- 记录 -->
      <div id="view-history" class="hide">
        <div class="card">
          <h2>听写记录</h2>
          <div id="history-list"></div>
        </div>
      </div>

      <!-- 词表浏览 -->
      <div id="view-browse" class="hide">
        <div class="card">
          <h2 id="browse-book-title">选册别</h2>
          <div class="chips" id="browse-book-chips"></div>
          <div style="font-size:13px;color:var(--muted);margin-top:8px">点击单词可试听发音</div>
        </div>
        <div id="browse-list"></div>
      </div>

    </div>
  </div>
</div>

<script>
// 微信环境检测
(function(){
  var ua = navigator.userAgent.toLowerCase();
  if(/micromessenger/i.test(ua)){
    var m = document.getElementById('wxMask');
    if(m) m.style.display = 'block';
  }
})();

const EN_WORDS = __WORDS_JSON__;
const CN_WORDS = __CN_JSON__;
const SUBJECTS = {
  en:{ name:'英语',icon:'🔤', books:['1A','1B','2A','2B','3A','3B','4A','4B','5A','5B','6A','6B'],
       words:EN_WORDS, title:'英语听写', bookLabel:'选册别', unitLabel:'选单元',
       hintLabel:'听写时显示中文提示', contextLabel:'朗读时附带中文释义', hasLevels:true },
  cn:{ name:'语文',icon:'📖', books:['三年级上册','三年级下册'],
       words:CN_WORDS, title:'语文听写', bookLabel:'选册别', unitLabel:'选课文',
       hintLabel:'听写时显示拼音提示', contextLabel:'', hasLevels:false }
};
const STORAGE_KEY = 'nm_dictation_v2';

// ---------- 状态 ----------
let S = loadState();
let curSubject = S.subject || 'en';
S.books = S.books || {}; S.units = S.units || {};
let curBook = S.books[curSubject] || SUBJECTS[curSubject].books[0];
let curUnits = S.units[curSubject] || [];
let curMode = 'four-priority';
let curCount = 15;
let curLang = S.lang || 'en-US';
let settings = S.settings || {cn:false, showCn:false, rate:0.8, repeat:3, interval:4, auto:true};
let dictList = [];
let dictIdx = 0;
let synth = window.speechSynthesis;
let voices = [];
let speakingTimer = null;

function loadState(){
  try{ return JSON.parse(localStorage.getItem(STORAGE_KEY))||{}; }catch(e){ return {}; }
}
function saveState(){
  S.subject = curSubject;
  S.books[curSubject] = curBook; S.units[curSubject] = curUnits;
  S.lang = curLang; S.settings = settings;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(S));
}
function curWords(){ return SUBJECTS[curSubject].words; }
function curBooks(){ return SUBJECTS[curSubject].books; }
function wordHint(w){ var s=w.subject||curSubject; return s==='cn'?(w.pinyin||w.meaning||''):(w.meaning||''); }
function getMastered(){ return S.mastered || (S.mastered={}); }
function getWrong(){ return S.wrong || (S.wrong=[]); }
function getHistory(){ return S.history || (S.history=[]); }
function wKey(w){ return (w.subject||curSubject)+'|'+w.book+'|'+w.unit+'|'+w.word; }
function isMastered(w){ return !!getMastered()[wKey(w)]; }
function setMastered(w,v){ getMastered()[wKey(w)] = v; saveState(); }
function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; }

// ---------- 侧边栏 ----------
function openSidebar(){ document.getElementById('sidebar').classList.add('open'); document.getElementById('sbOverlay').classList.add('show'); }
function closeSidebar(){ document.getElementById('sidebar').classList.remove('open'); document.getElementById('sbOverlay').classList.remove('show'); }
function applySubjectTheme(){
  document.body.className = 'subject-'+curSubject;
  document.getElementById('tab-en').classList.toggle('active',curSubject==='en');
  document.getElementById('tab-cn').classList.toggle('active',curSubject==='cn');
}
function switchSubject(subj){
  if(curSubject===subj){ closeSidebar(); return; }
  saveState();
  curSubject = subj;
  curBook = S.books[subj] || SUBJECTS[subj].books[0];
  curUnits = S.units[subj] || [];
  applySubjectTheme();
  go('home');
  closeSidebar();
}

// ---------- 语音 ----------
// ===== 声音管理（兼容 iOS Safari 异步加载）=====
function loadVoices(){
  var v = synth.getVoices();
  if(v && v.length>0) voices = v;
  return voices;
}
loadVoices();
// iOS 上 voiceschanged 可能触发多次，每次都更新缓存
if(synth.onvoiceschanged!==undefined) synth.onvoiceschanged = function(){ loadVoices(); autoPickSamantha(); };
// iOS 上有时 voiceschanged 不触发，用轮询兜底
var voicePollT = 0, voicePollCount = 0;
function pollVoices(){
  if(voicePollCount>20) return;
  voicePollCount++;
  var v = synth.getVoices();
  if(v && v.length>0){ voices = v; autoPickSamantha(); loadVoiceList(); }
  else { voicePollT = setTimeout(pollVoices, 300); }
}
pollVoices();

var FEMALE_NAMES = ['Samantha','Kate','Serena','Karen','Moira','Tessa','Fiona','Veena','Zoe','Ellie','Victoria','Susan','Allison','Ava','Nora'];
var MALE_NAMES = ['Daniel','Aaron','Alex','Fred','Oliver','Rishi','Tom','Arthur','Gordon','Nicky'];
function getVoicesSafe(){
  var v = synth.getVoices();
  if(v && v.length>0) voices = v;
  return voices;
}
function pickVoice(lang){
  var all = getVoicesSafe();
  if(all.length===0) return null;
  var base = lang.split('-')[0];
  var pool = all.filter(v=>v.lang===lang);
  if(pool.length===0) pool = all.filter(v=>v.lang.indexOf(base)===0);
  if(pool.length===0) pool = all.filter(v=>/^en/i.test(v.lang));
  if(pool.length===0) return null;
  for(var i=0;i<FEMALE_NAMES.length;i++){ var fv=pool.find(v=>v.name.indexOf(FEMALE_NAMES[i])>=0); if(fv) return fv; }
  var nonMale = pool.find(v=>{ for(var j=0;j<MALE_NAMES.length;j++){ if(v.name.indexOf(MALE_NAMES[j])>=0) return false; } return true; });
  return nonMale || pool[0];
}
function autoPickSamantha(){
  if(S.voiceURI) return;   // 用户已手动选过就不覆盖
  var all = getVoicesSafe();
  if(all.length===0) return;
  var sam = all.find(v=>/samantha/i.test(v.name));
  if(sam){ S.voiceURI = sam.voiceURI; saveState(); }
}
// 用户首次交互时强制初始化声音（iOS 必须有交互才能加载声音）
var voiceInited = false;
function initVoiceOnInteract(){
  if(voiceInited) return;
  voiceInited = true;
  loadVoices();
  autoPickSamantha();
  loadVoiceList();
  // 再轮询几次确保拿到
  voicePollCount = 0; pollVoices();
}
document.addEventListener('click', initVoiceOnInteract, {once:false});
document.addEventListener('touchstart', initVoiceOnInteract, {once:false});

function loadVoiceList(){
  var list = document.getElementById('voice-list');
  if(!list) return;
  var vs = getVoicesSafe();
  if(vs.length===0){ list.innerHTML='<div style="padding:8px;color:var(--muted)">声音列表尚未加载，请点"刷新"重试</div>'; return; }
  var en = vs.filter(v=>/^en/i.test(v.lang));
  if(en.length===0) en = vs;
  var saved = S.voiceURI || '';
  list.innerHTML = en.map(v=>{
    var sel = v.voiceURI===saved ? ' background:var(--pri);color:#fff' : '';
    return '<div style="padding:8px 10px;border-bottom:1px solid #F0EBE5;cursor:pointer;display:flex;justify-content:space-between;align-items:center'+sel+'" onclick="pickVoiceURI(\''+v.voiceURI.replace(/'/g,"\\'")+'\')"><span style="font-size:14px">'+v.name+'</span><span style="font-size:12px;opacity:.6">'+v.lang+'</span></div>';
  }).join('');
}
function pickVoiceURI(uri){
  S.voiceURI = uri; saveState();
  synth.cancel();
  var vs = getVoicesSafe();
  var v = vs.find(x=>x.voiceURI===uri);
  var u = new SpeechSynthesisUtterance('Hello, this is a test.');
  if(v) u.voice = v; u.lang = v ? v.lang : 'en-US'; u.rate = settings.rate || 0.8;
  synth.speak(u);
  loadVoiceList();
}
function speak(text, opts){
  opts = opts||{};
  synth.cancel();
  let u = new SpeechSynthesisUtterance(text);
  let lang = opts.lang || curLang;
  let v = null;
  var allV = getVoicesSafe();
  if(S.voiceURI) v = allV.find(x=>x.voiceURI===S.voiceURI);
  if(!v && S.voiceURI) v = voices.find(x=>x.voiceURI===S.voiceURI);
  if(!v) v = allV.find(x=>/samantha/i.test(x.name));
  if(!v) v = voices.find(x=>/samantha/i.test(x.name));
  if(!v) v = pickVoice(lang);
  if(v){ u.voice=v; u.lang=v.lang; } else { u.lang = lang; }
  u.rate = opts.rate || settings.rate;
  u.pitch = 1;
  synth.speak(u);
  return u;
}
var TONE_CHARS = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜńňǹ';
function isLightTone(syllable){
  // 没有声调符号的音节 = 轻声
  for(var i=0;i<syllable.length;i++){
    if(TONE_CHARS.indexOf(syllable[i])>=0) return false;
  }
  return syllable.length>0;
}
function speakCN(text, pinyin){
  synth.cancel();
  var allV = getVoicesSafe();
  let zhVoices = allV.filter(v=>/^zh/i.test(v.lang));
  if(zhVoices.length===0) zhVoices = voices.filter(v=>/^zh/i.test(v.lang));
  let v = zhVoices.find(v=>/Ting|Mei|Sin|Tian|Li/i.test(v.name)) || zhVoices[0];

  // 检查是否含轻声音节
  if(pinyin){
    var syllables = pinyin.trim().split(/\s+/);
    var chars = text.split('');
    var hasLight = false;
    if(syllables.length===chars.length){
      for(var k=0;k<syllables.length;k++){
        if(isLightTone(syllables[k])){ hasLight=true; break; }
      }
    }
    // 含轻声的词：逐字朗读，轻声字用低音调+短时长模拟
    if(hasLight){
      var ci = 0;
      function readNextChar(){
        if(ci>=chars.length) return;
        var u = new SpeechSynthesisUtterance(chars[ci]);
        if(v) u.voice=v;
        u.lang='zh-CN';
        var syl = syllables[ci] || '';
        if(isLightTone(syl)){
          u.pitch = 0.45;       // 低音调模拟轻声
          u.rate = (settings.rate||0.9) * 1.6;  // 短时长
        } else {
          u.pitch = 1.0;
          u.rate = settings.rate || 0.9;
        }
        ci++;
        if(ci<chars.length) u.onend = readNextChar;
        synth.speak(u);
      }
      readNextChar();
      return;
    }
  }
  // 无轻声的词：整词朗读
  let u = new SpeechSynthesisUtterance(text);
  if(v) u.voice=v; u.lang='zh-CN'; u.rate=settings.rate||0.9;
  synth.speak(u);
}
function speakWord(w){
  synth.cancel();
  clearTimeout(speakingTimer);
  seqToken++;
  let seq = [];
  var subj = w.subject || curSubject;
  for(let i=0;i<settings.repeat;i++){
    var isLast = (i===settings.repeat-1);
    if(subj==='cn'){
      seq.push({t:'cn',text:w.word, pinyin:w.pinyin, main:true, round:i, isLastRound:isLast});
      if(settings.cn && w.ci) seq.push({t:'cn',text:w.ci, main:false, round:i, isLastRound:isLast});
    } else {
      seq.push({t:'en',text:w.word, main:true, round:i, isLastRound:isLast});
      if(settings.cn) seq.push({t:'cn',text:w.meaning, main:false, round:i, isLastRound:isLast});
    }
  }
  playSeq(seq, 0, seqToken);
}
let isPaused = false;
let pausedSeq = null;
let pausedIdx = 0;
function togglePause(){
  var btn = document.getElementById('pause-btn');
  if(!isPaused){
    isPaused = true;
    clearTimeout(speakingTimer);
    synth.cancel();
    seqToken++;
    if(btn){ btn.textContent='▶ 继续'; btn.classList.add('active'); }
  } else {
    isPaused = false;
    if(btn){ btn.textContent='⏸ 暂停'; btn.classList.remove('active'); }
    if(pausedSeq && pausedSeq.length>0){
      seqToken++;
      playSeq(pausedSeq, pausedIdx, seqToken);
    }
  }
}
let seqToken = 0;
function playSeq(seq, i, token){
  if(token!==seqToken) return;
  if(isPaused){ pausedSeq=seq; pausedIdx=i; return; }
  if(i>=seq.length){
    if(settings.auto) speakingTimer = setTimeout(()=>nextWord(), 800);
    return;
  }
  let it=seq[i];
  if(it.t==='en') speak(it.text);
  else speakCN(it.text, it.pinyin);
  // 语文：非最后一遍间隔4秒，最后一遍间隔10秒
  // 英语：用滑块设置的间隔
  var wait;
  if(it.main){
    if(curSubject==='cn'){
      wait = it.isLastRound ? 10000 : 4000;
    } else {
      wait = settings.interval * 1000;
    }
  } else {
    wait = 1500;
  }
  pausedSeq=seq; pausedIdx=i+1;
  speakingTimer = setTimeout(()=>playSeq(seq,i+1,token), wait);
}

// ---------- 首页渲染 ----------
function renderHome(){
  let bc = document.getElementById('book-chips');
  bc.innerHTML='';
  curBooks().forEach(b=>{
    let c=document.createElement('div');
    c.className='chip'+(b===curBook?' active':'');
    c.textContent=b;
    if(b==='2A'||b==='2B'||b==='3A'||b==='3B') c.style.fontWeight='700';
    c.onclick=()=>{ curBook=b; curUnits=[]; renderHome(); saveState(); };
    bc.appendChild(c);
  });
  renderUnits();
  document.getElementById('lbl-cn').textContent = SUBJECTS[curSubject].contextLabel;
  document.getElementById('lbl-show-cn').textContent = SUBJECTS[curSubject].hintLabel;
  document.getElementById('book-title').textContent = SUBJECTS[curSubject].bookLabel;
  document.getElementById('unit-title').textContent = SUBJECTS[curSubject].unitLabel;
  document.getElementById('page-title').textContent = SUBJECTS[curSubject].title;
  document.getElementById('lang-row').style.display = curSubject==='cn'?'none':'';
  document.getElementById('row-cn').style.display = curSubject==='cn'?'none':'';
  document.getElementById('set-cn').className='toggle'+(settings.cn?' on':'');
  document.getElementById('set-show-cn').className='toggle'+(settings.showCn?' on':'');
  document.getElementById('set-auto').className='toggle'+(settings.auto?' on':'');
  document.getElementById('set-rate').value=settings.rate;
  document.getElementById('rate-val').textContent=settings.rate+'x';
  document.getElementById('set-repeat').value=settings.repeat;
  document.getElementById('repeat-val').textContent=settings.repeat+' 遍';
  document.getElementById('set-interval').value=settings.interval;
  document.getElementById('interval-val').textContent=settings.interval+' 秒';
  renderRangeTip();
}
function renderUnits(){
  let ul=document.getElementById('unit-list');
  ul.innerHTML='';
  let words = curWords()[curBook]||[];
  let units=[]; let seen={};
  words.forEach(w=>{ if(!seen[w.unit]){seen[w.unit]=1; units.push(w.unit);} else seen[w.unit]++; });
  units.forEach(u=>{
    let total=words.filter(w=>w.unit===u).length;
    let mastered=words.filter(w=>w.unit===u&&isMastered(w)).length;
    let d=document.createElement('div');
    d.className='unit-item'+(curUnits.includes(u)?' active':'');
    let hasLvl = words.some(w=>w.unit===u&&(w.level==='四会'||w.level==='二会'));
    if(SUBJECTS[curSubject].hasLevels && hasLvl){
      let cnt4=words.filter(w=>w.unit===u&&w.level==='四会').length;
      let cnt2=words.filter(w=>w.unit===u&&w.level==='二会').length;
      d.innerHTML='<span>'+u+'</span><span class="cnt">四会'+cnt4+' · 二会'+cnt2+' · 已掌握'+mastered+'/'+total+'</span>';
    } else {
      d.innerHTML='<span>'+u+'</span><span class="cnt">'+total+'词 · 已掌握'+mastered+'/'+total+'</span>';
    }
    d.onclick=()=>{ curUnits = (curUnits.length===1&&curUnits[0]===u)?[]:[u]; renderUnits(); renderRangeTip(); saveState(); };
    ul.appendChild(d);
  });
}
function unitAll(all){
  let words=curWords()[curBook]||[];
  let seen={}; let units=[];
  words.forEach(w=>{ if(!seen[w.unit]){seen[w.unit]=1; units.push(w.unit);} });
  curUnits = all?units.slice():[];
  renderUnits(); renderRangeTip(); saveState();
}
function renderRangeTip(){
  let tip=document.getElementById('range-tip');
  if(curUnits.length===0){ tip.textContent = curSubject==='cn'?'请在上方选择至少一篇课文':'请在上方选择至少一个单元'; return; }
  let words=(curWords()[curBook]||[]).filter(w=>curUnits.includes(w.unit));
  let mastered=words.filter(w=>isMastered(w)).length;
  let avail=words.length-mastered; if(avail<=0) avail=words.length;
  let fillNote=(curCount>0&&avail<curCount)?'<br>所选词量不足，将自动补入错词本及其他单元的词（结算页标注「补充」）':'';
  if(curSubject==='cn'){
    tip.innerHTML='当前：<b>'+curBook+'</b> · '+curUnits.length+'课文 · 共'+words.length+'词 ｜ 已掌握'+mastered+'/'+words.length+fillNote;
  } else {
    let f4=words.filter(w=>w.level==='四会'); let f2=words.filter(w=>w.level==='二会');
    if(f4.length+f2.length===0){
      tip.innerHTML='当前：<b>'+curBook+'</b> · '+curUnits.length+'单元 · 共'+words.length+'词 ｜ 已掌握'+mastered+'/'+words.length+fillNote;
    } else {
      let m4=f4.filter(w=>isMastered(w)).length; let m2=f2.filter(w=>isMastered(w)).length;
      tip.innerHTML='当前：<b>'+curBook+'</b> · '+curUnits.length+'单元 · 共'+words.length+'词 ｜ 四会 '+m4+'/'+f4.length+'掌握 · 二会 '+m2+'/'+f2.length+'掌握<br>模式：四会优先（四会清完自动加入二会）'+fillNote;
    }
  }
}
function toggleSet(key,el){ settings[key]=!settings[key]; el.className='toggle'+(settings[key]?' on':''); saveState(); }
function setRange(key,val,id,suffix){ settings[key]=key==='rate'?parseFloat(val):parseInt(val); document.getElementById(id).textContent=val+suffix; saveState(); }
function toggleSettings(){ let c=document.getElementById('settings-card'); c.style.display = c.style.display==='none'?'block':'none'; }
function exportData(){
  let blob = new Blob([JSON.stringify(S,null,1)], {type:'application/json'});
  let url = URL.createObjectURL(blob);
  let a = document.createElement('a'); let d = new Date();
  let ts = d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  a.href = url; a.download = 'dictation-backup-'+ts+'.json';
  document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
}
function importData(ev){
  let file = ev.target.files[0]; if(!file) return;
  let reader = new FileReader();
  reader.onload = function(e){
    try{
      let data = JSON.parse(e.target.result);
      if(!data || typeof data!=='object') throw 'bad';
      S = data; saveState();
      curSubject = S.subject || 'en';
      curBook = (S.books&&S.books[curSubject]) || SUBJECTS[curSubject].books[0];
      curUnits = (S.units&&S.units[curSubject]) || [];
      curLang = S.lang || curLang;
      settings = S.settings || settings;
      alert('导入成功！进度已恢复。');
      applySubjectTheme(); renderHome();
    }catch(err){ alert('导入失败：文件格式不正确'); }
  };
  reader.readAsText(file); ev.target.value='';
}

// ---------- 选词 ----------
function normWord(s){ return String(s||'').toLowerCase().replace(/\s+/g,' ').trim(); }
function pickCand(pool){
  if(pool.length===0) return [];
  if(SUBJECTS[curSubject].hasLevels){
    let f4=pool.filter(w=>w.level==='四会'); let f2=pool.filter(w=>w.level==='二会');
    let c=f4.filter(w=>!isMastered(w)); if(c.length===0) c=f4;
    if(c.length===0) c=f2.filter(w=>!isMastered(w)); if(c.length===0) c=f2;
    if(c.length===0) c=pool;
    return c;
  }
  let c=pool.filter(w=>!isMastered(w)); if(c.length===0) c=pool;
  return c;
}
function pickWords(){
  let all = curWords()[curBook]||[];
  let pool = all.filter(w=>curUnits.includes(w.unit));
  if(pool.length===0) return [];
  // 优先：所选单元的词
  let sel = pickCand(pool);
  let n = curCount===0?sel.length:curCount;
  let list = shuffle(sel).slice(0,n);
  // 所选词量不足时补充：本单元剩余未掌握词 → 错词本（当前册）→ 其他单元未掌握词
  if(curCount>0 && list.length<n){
    let seen={}; list.forEach(w=>seen[normWord(w.word)]=1);
    let fresh = a=>a.filter(w=>!isMastered(w) && !seen[normWord(w.word)]);
    let lvlSort = a=>{
      let s=shuffle(a);
      if(SUBJECTS[curSubject].hasLevels && s.some(w=>w.level==='四会'||w.level==='二会'))
        s=s.filter(w=>w.level==='四会').concat(s.filter(w=>w.level==='二会'));
      return s;
    };
    let wrongSet={};
    getWrong().forEach(x=>{ if(x.book===curBook && (x.subject||'en')===curSubject) wrongSet[normWord(x.word)]=1; });
    let rest = all.filter(w=>!curUnits.includes(w.unit));
    let own = fresh(pool);
    let wb  = fresh(rest).filter(w=>wrongSet[normWord(w.word)]);
    let ot  = fresh(rest).filter(w=>!wrongSet[normWord(w.word)]);
    let fills = lvlSort(own).concat(lvlSort(wb)).concat(lvlSort(ot)).slice(0, n-list.length)
      .map(w=>Object.assign({},w,{_fill:true}));
    list = list.concat(fills);
  }
  return list;
}

// ---------- 听写流程 ----------
function startDictation(){
  if(curUnits.length===0){ alert(curSubject==='cn'?'请先选择课文':'请先选择单元'); return; }
  dictList=pickWords();
  if(dictList.length===0){ alert('该范围没有可听写的词，可能已全部掌握。'); return; }
  dictIdx=0; go('dictate'); showWord();
  setTimeout(()=>playCurrent(),300);
}
function showWord(){
  let w=dictList[dictIdx];
  document.getElementById('word-num').textContent='第 '+(dictIdx+1)+' / '+dictList.length+' 题';
  document.getElementById('prog-fill').style.width=((dictIdx)/(dictList.length)*100)+'%';
  document.getElementById('big-word').textContent='🎧 听写中…';
  document.getElementById('big-word').style.fontSize='32px';
  document.getElementById('meaning-hint').textContent = settings.showCn ? wordHint(w) : '';
}
function playCurrent(){
  let w=dictList[dictIdx];
  let btn=document.getElementById('play-btn');
  btn.classList.add('playing');
  speakWord(w);
  // 语文：4秒*(遍数-1) + 10秒；英语：间隔*遍数
  var aniInt = curSubject==='cn' ? (4000*(settings.repeat-1)+10000) : settings.interval * 1000 * settings.repeat;
  setTimeout(()=>btn.classList.remove('playing'), aniInt);
}
function nextWord(){
  if(dictIdx<dictList.length-1){
    dictIdx++; showWord(); clearTimeout(speakingTimer);
    if(settings.auto) setTimeout(()=>playCurrent(),200);
  } else { endDictation(false); }
}
function prevWord(){
  if(dictIdx>0){ dictIdx--; showWord(); clearTimeout(speakingTimer); if(settings.auto) setTimeout(()=>playCurrent(),200); }
}
function endDictation(early){
  clearTimeout(speakingTimer); seqToken++; synth.cancel();
  renderResult(); go('result');
}

// ---------- 结算 ----------
function renderResult(){
  let rl=document.getElementById('result-list'); rl.innerHTML='';
  dictList.forEach((w,i)=>{
    let d=document.createElement('div'); d.className='result-item';
    let hint=wordHint(w); let badge='';
    if(SUBJECTS[curSubject].hasLevels && w.level) badge='<span class="badge '+(w.level==='四会'?'b4':'b2')+'">'+w.level+'</span>';
    if(w._fill) badge+=' <span class="badge bF">补充</span>';
    d.innerHTML='<div><span class="w">'+w.word+'</span> '+badge+'<div class="m">'+hint+'</div></div><div class="judge"><button class="ok" onclick="judge('+i+',true,this)">✓对</button><button class="no" onclick="judge('+i+',false,this)">✗错</button></div>';
    rl.appendChild(d);
  });
  document.getElementById('r-total').textContent=dictList.length;
  document.getElementById('r-right').textContent=0; document.getElementById('r-wrong').textContent=0;
  window._judge={}; _resultSaved=false;
}
function judge(i,right,el){
  let w=dictList[i]; window._judge[i]=right;
  let row=el.parentElement.parentElement;
  row.querySelectorAll('.judge button').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  if(right){ setMastered(w,true); }
  else{
    setMastered(w,false);
    let wrong=getWrong(); let k=wKey(w);
    if(!wrong.find(x=>wKey(x)===k)){ wrong.push({word:w.word,meaning:wordHint(w),ci:w.ci,book:w.book,unit:w.unit,level:w.level||'',subject:w.subject||curSubject,time:Date.now()}); }
    saveState();
  }
  document.getElementById('r-right').textContent=Object.values(window._judge).filter(v=>v).length;
  document.getElementById('r-wrong').textContent=Object.values(window._judge).filter(v=>!v).length;
}
function replayWrong(){
  let wrong=getWrong();
  if(wrong.length===0){ alert('错词本为空'); return; }
  dictList=shuffle(wrong).slice(0,20).map(x=>({word:x.word,meaning:x.meaning,pinyin:x.pinyin||x.meaning,ci:x.ci,book:x.book,unit:x.unit,level:x.level||'',subject:x.subject||'en'}));
  dictIdx=0; go('dictate'); showWord(); setTimeout(()=>playCurrent(),300);
}

// ---------- 错词本 ----------
function renderWrong(){
  let wrong=getWrong(); let wl=document.getElementById('wrong-list');
  if(wrong.length===0){ wl.innerHTML='<div class="empty">还没有错词，继续加油！💪</div>'; return; }
  wl.innerHTML='';
  wrong.forEach((x,i)=>{
    let d=document.createElement('div'); d.className='wrong-item';
    let subj=x.subject||'en'; let badge='';
    if(subj==='en' && x.level) badge='<span class="badge '+(x.level==='四会'?'b4':'b2')+'">'+x.level+'</span>';
    var playFn = subj==='cn' ? 'speakCN(\''+(x.word||'').replace(/'/g,"\\'")+'\')' : 'speak(\''+(x.word||'').replace(/'/g,"\\'")+'\')';
    d.innerHTML='<div><div class="wi-w">'+x.word+' '+badge+'</div><div class="wi-m">'+(x.meaning||'')+' · '+(x.book||'')+' '+(x.unit||'')+'</div></div><div><button class="btn btn-ghost btn-sm" onclick="'+playFn+'">🔊</button> <button class="del" onclick="delWrong('+i+')">×</button></div>';
    wl.appendChild(d);
  });
}
function delWrong(i){ getWrong().splice(i,1); saveState(); renderWrong(); }
function clearWrong(){ if(confirm('确定清空错词本？')){ S.wrong=[]; saveState(); renderWrong(); } }
function startWrongDictation(){ let wrong=getWrong(); if(wrong.length===0){ alert('错词本为空'); return; } replayWrong(); }

// ---------- 记录 ----------
function renderHistory(){
  let h=getHistory(); let hl=document.getElementById('history-list');
  if(h.length===0){ hl.innerHTML='<div class="empty">还没有听写记录</div>'; return; }
  hl.innerHTML='';
  h.slice().reverse().forEach(r=>{
    let d=document.createElement('div'); d.className='history-item';
    let dt=new Date(r.time);
    let ts=dt.getMonth()+1+'/'+dt.getDate()+' '+String(dt.getHours()).padStart(2,'0')+':'+String(dt.getMinutes()).padStart(2,'0');
    d.innerHTML='<div class="hi-top"><span class="hi-range">'+r.range+'</span><span class="hi-stat">'+ts+'</span></div><div class="hi-stat">共'+r.total+'词 · 正确'+r.right+' · 错误'+r.wrong+(r.wrongWords?' · 错词: '+r.wrongWords:'')+'</div>';
    hl.appendChild(d);
  });
}
function saveHistory(rightCnt,wrongCnt,wrongWordsStr){
  let h=getHistory();
  h.push({time:Date.now(),range:curBook+' · '+curUnits.length+(curSubject==='cn'?'课文':'单元'),total:dictList.length,right:rightCnt,wrong:wrongCnt,wrongWords:wrongWordsStr});
  if(h.length>100) h=h.slice(-100);
  S.history=h; saveState();
}

// ---------- 词表浏览 ----------
let browseBook = null;
function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function renderBrowse(){
  let subj = SUBJECTS[curSubject];
  if(!browseBook || subj.books.indexOf(browseBook)<0) browseBook = curBook;
  if(subj.books.indexOf(browseBook)<0) browseBook = subj.books[0];
  let bc = document.getElementById('browse-book-chips');
  bc.innerHTML='';
  subj.books.forEach(b=>{
    let c=document.createElement('div');
    c.className='chip'+(b===browseBook?' active':'');
    c.textContent=b;
    if(b==='2A'||b==='2B'||b==='3A'||b==='3B') c.style.fontWeight='700';
    c.onclick=()=>{ browseBook=b; renderBrowse(); };
    bc.appendChild(c);
  });
  document.getElementById('browse-book-title').textContent = subj.bookLabel;
  document.getElementById('page-title').textContent = subj.name+' · 词表浏览';
  let list=document.getElementById('browse-list');
  list.innerHTML='';
  let words = subj.words[browseBook]||[];
  let units=[]; let seen={};
  words.forEach(w=>{ if(!seen[w.unit]){seen[w.unit]=1; units.push(w.unit);} });
  units.forEach(u=>{
    let ws=words.filter(w=>w.unit===u);
    let card=document.createElement('div');
    card.className='card';
    let h=document.createElement('h2');
    h.textContent=u+'（'+ws.length+'词）';
    card.appendChild(h);
    // 有话题分组（如扩展单词）的按话题分小节展示
    let topics=[]; let tseen={};
    ws.forEach(w=>{ if(w.topic && !tseen[w.topic]){tseen[w.topic]=1; topics.push(w.topic);} });
    let groups;
    if(topics.length>0){
      groups = topics.map(t=>({label:t, ws:ws.filter(w=>w.topic===t)}));
      let noTopic = ws.filter(w=>!w.topic);
      if(noTopic.length>0) groups.push({label:'', ws:noTopic});
    } else {
      groups = [{label:'', ws:ws}];
    }
    groups.forEach(g=>{
      if(g.label){
        let sh=document.createElement('div');
        sh.className='topic-h';
        sh.textContent=g.label;
        card.appendChild(sh);
      }
      let grid=document.createElement('div');
      grid.className='word-grid';
      g.ws.forEach(w=>{
        let it=document.createElement('div');
        it.className='word-item';
        let sub = curSubject==='cn' ? (w.pinyin||'') : (w.phonetic||'');
        let html='<div class="w">'+esc(w.word)+'</div>';
        if(sub) html+='<div class="ph">'+esc(sub)+'</div>';
        if(w.meaning) html+='<div class="m">'+esc(w.meaning)+'</div>';
        it.innerHTML=html;
        it.onclick=()=>{
          if(curSubject==='cn'){ speakCN(w.word, w.pinyin); }
          else { speak(w.word, {lang:curLang}); }
        };
        grid.appendChild(it);
      });
      card.appendChild(grid);
    });
    list.appendChild(card);
  });
}

// ---------- 页面切换 ----------
function go(view){
  ['home','dictate','result','wrong','history','browse'].forEach(v=>{
    document.getElementById('view-'+v).classList.toggle('hide',v!==view);
  });
  document.getElementById('nav-home').classList.toggle('active',view==='home'||view==='dictate'||view==='result');
  document.getElementById('nav-wrong').classList.toggle('active',view==='wrong');
  document.getElementById('nav-history').classList.toggle('active',view==='history');
  document.getElementById('nav-browse').classList.toggle('active',view==='browse');
  if(view==='home') renderHome();
  if(view==='wrong') renderWrong();
  if(view==='history') renderHistory();
  if(view==='browse') renderBrowse();
  window.scrollTo(0,0);
}
let _resultSaved=false;
let _origGo=go;
go=function(view){
  if(!_resultSaved && document.getElementById('view-result') && !document.getElementById('view-result').classList.contains('hide')){
    let j=window._judge||{};
    if(Object.keys(j).length>0){
      let rc=Object.values(j).filter(v=>v).length;
      let wc=Object.values(j).filter(v=>!v).length;
      let ww=dictList.filter((w,i)=>j[i]===false).map(w=>w.word).join(', ');
      saveHistory(rc,wc,ww);
    }
    _resultSaved=true;
  }
  _origGo(view);
};

// ---------- 事件监听 ----------
document.getElementById('count-chips').addEventListener('click',e=>{
  if(e.target.dataset.count){ curCount=parseInt(e.target.dataset.count);
    document.querySelectorAll('#count-chips .chip').forEach(c=>c.classList.toggle('active',parseInt(c.dataset.count)===curCount));
  }
});
document.getElementById('lang-chips').addEventListener('click',e=>{
  if(e.target.dataset.lang){ curLang=e.target.dataset.lang;
    document.querySelectorAll('#lang-chips .chip').forEach(c=>c.classList.toggle('active',c.dataset.lang===curLang));
    saveState();
  }
});

// ---------- 初始化 ----------
// 单元改为单选语义：载入时清掉历史多选，避免旧勾选混入其他单元的词
['en','cn'].forEach(s=>{ if((S.units[s]||[]).length>1) S.units[s]=[]; });
curUnits = S.units[curSubject] || [];
saveState();
applySubjectTheme();
renderHome();
setTimeout(loadVoiceList, 500);
setTimeout(loadVoiceList, 1500);
setTimeout(loadVoiceList, 3000);
</script>
</body>
</html>
'''

with open('dictation.html','w',encoding='utf-8') as f:
    f.write(HTML.replace('__WORDS_JSON__', WORDS_JSON).replace('__CN_JSON__', CN_JSON))
print('generated dictation.html', os.path.getsize('dictation.html'), 'bytes')
