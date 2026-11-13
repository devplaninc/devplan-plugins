# Devplan dashboard template

Copy this page and fill it in. Keep the `<head>`, `<style>` and `<script>` exactly as they are. The comments name each pattern and when to use it; delete them, and every pattern you don't use, before publishing.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">
<style>
/* Devplan dashboard. Layout: ink masthead with the logomark's tile field, a ranked "Today" lede, a figures strip, then sections of evidence-linked rows. */
:root{
  --bg:#fbfbfc;--paper:#fff;--off:#f7f7f8;--rule:#ececee;--rule-2:#dcdce1;
  --ink:#0a0a0b;--ink-2:#1a1a1c;--dim:#52525a;--faint:#8a8a92;
  --accent:#1f3dff;--accent-2:#2d49ff;--accent-soft:#f0f5ff;--accent-line:#d5defe;
  --band:#0a0a0b;--band-ink:#fff;--band-dim:#a0a0a6;--band-accent:#5a77ff;
  --ok:#1b7a47;--ok-soft:#e8f5ee;--warn:#e6a437;--warn-ink:#7f5200;--warn-soft:#fdf3e1;--bad:#c4322b;--bad-soft:#fcecea;
  --sans:"Geist",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  --mono:"Geist Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0a0a0b;--paper:#0f0f11;--off:#151518;--rule:#232327;--rule-2:#303036;
  --ink:#f4f4f5;--ink-2:#e4e4e7;--dim:#a0a0a6;--faint:#6e6e76;
  --accent:#5a77ff;--accent-2:#7a91ff;--accent-soft:#141a38;--accent-line:#26306a;
  --band:#000;--band-ink:#fff;--band-dim:#a0a0a6;--band-accent:#5a77ff;
  --ok:#4cc488;--ok-soft:#10261a;--warn-ink:#f0bd62;--warn-soft:#2a2112;--bad:#f2786f;--bad-soft:#2c1514;color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0a0a0b;--paper:#0f0f11;--off:#151518;--rule:#232327;--rule-2:#303036;
  --ink:#f4f4f5;--ink-2:#e4e4e7;--dim:#a0a0a6;--faint:#6e6e76;
  --accent:#5a77ff;--accent-2:#7a91ff;--accent-soft:#141a38;--accent-line:#26306a;
  --band:#000;--band-ink:#fff;--band-dim:#a0a0a6;--band-accent:#5a77ff;
  --ok:#4cc488;--ok-soft:#10261a;--warn-ink:#f0bd62;--warn-soft:#2a2112;--bad:#f2786f;--bad-soft:#2c1514;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:2px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
.wrap{max-width:980px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}

/* Masthead */
.mast{position:relative;background:var(--band);color:var(--band-ink);overflow:hidden}
.mast canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.mast .wrap{position:relative;padding-block:28px 30px}
.brand{display:flex;align-items:center;gap:10px;font:500 13px/1 var(--sans);color:var(--band-dim)}
.brand b{color:var(--band-ink);font-weight:500;display:inline-flex;align-items:center;gap:8px}
.brand b::before{content:"";width:10px;height:10px;border-radius:3px;background:var(--band-accent)}
.mast h1{font:400 clamp(30px,5vw,44px)/1.08 var(--sans);letter-spacing:-.02em;margin:22px 0 10px;text-wrap:balance}
.mast .sub{display:flex;flex-wrap:wrap;gap:6px 18px;font:400 13px/1.4 var(--mono);color:var(--band-dim)}
.mast .sub span::before{content:"";display:inline-block;width:6px;height:6px;border-radius:2px;background:var(--band-accent);margin-right:8px;vertical-align:1px}

/* Today */
.today{padding-block:26px 6px}
.today h2{font:500 13px/1 var(--mono);color:var(--dim);margin:0 0 12px;letter-spacing:.02em}
.today ol{list-style:none;margin:0;padding:0;display:grid;gap:10px;counter-reset:t}
.today li{counter-increment:t;position:relative;padding-left:40px;font-size:clamp(17px,2.2vw,19px);line-height:1.45;color:var(--ink-2);max-width:72ch}
.today li::before{content:counter(t);position:absolute;left:0;top:2px;font:500 12px/24px var(--mono);text-align:center;width:24px;height:24px;border-radius:7px;background:var(--accent-soft);color:var(--accent)}

/* Figures */
.figs{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);border-block:1px solid var(--rule);margin-top:22px}
.fig{padding:16px 18px 16px 0;display:grid;gap:2px;align-content:start}
.fig+.fig{padding-left:18px;border-left:1px solid var(--rule)}
.fig b{font:400 30px/1.1 var(--sans);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.fig span{font-size:13px;color:var(--dim)}
.fig em{font:normal 500 12px/1.4 var(--mono);color:var(--dim)}
.fig em.up{color:var(--ok)}.fig em.down{color:var(--bad)}

/* Notice: graph still building, partial data */
.notice{display:flex;gap:12px;align-items:flex-start;margin-top:22px;padding:14px 16px;border:1px solid var(--accent-line);background:var(--accent-soft);border-radius:10px;font-size:14px;color:var(--ink-2)}
.notice::before{content:"";flex:0 0 10px;height:10px;margin-top:6px;border-radius:3px;background:var(--accent);box-shadow:14px 0 0 -1px color-mix(in srgb,var(--accent) 45%,transparent)}

/* Sections */
section{padding-top:38px}
.sh{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;padding-bottom:12px;border-bottom:1px solid var(--ink)}
.sh h2{font:600 17px/1.3 var(--sans);margin:0;letter-spacing:-.005em}
.sh .n{font:500 12px/1 var(--mono);color:var(--dim);padding:5px 7px;border:1px solid var(--rule-2);border-radius:6px}
.sh .tools{margin-left:auto;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.lead{color:var(--dim);font-size:14px;margin:12px 0 0;max-width:68ch}
.find{font:400 14px/1 var(--sans);color:var(--ink);background:var(--paper);border:1px solid var(--rule-2);border-radius:8px;padding:8px 10px 8px 30px;width:min(260px,100%);
  background-image:radial-gradient(circle at 13px 13px,transparent 4px,var(--faint) 4.5px,var(--faint) 5.5px,transparent 6px);background-repeat:no-repeat}
.find:focus{border-color:var(--accent);outline:none;box-shadow:0 0 0 3px var(--accent-soft)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.chip{font:500 12px/1 var(--sans);color:var(--dim);background:transparent;border:1px solid var(--rule-2);border-radius:999px;padding:6px 10px;cursor:pointer}
.chip[aria-pressed="true"]{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}

/* Rows */
.list{list-style:none;margin:0;padding:0}
.row{display:grid;grid-template-columns:12px minmax(0,1fr) auto;gap:4px 14px;padding:16px 0;border-bottom:1px solid var(--rule)}
.row>.tile{width:10px;height:10px;border-radius:3px;margin-top:7px;background:var(--faint)}
.row h3{font:500 15.5px/1.4 var(--sans);margin:0;color:var(--ink)}
.row h3 a{color:inherit}
.row p{margin:4px 0 0;color:var(--dim);font-size:14px;line-height:1.5;max-width:70ch}
.side{display:flex;flex-direction:column;align-items:flex-end;gap:6px;text-align:right}
.m{font:400 12px/1.4 var(--mono);color:var(--dim);white-space:nowrap;font-variant-numeric:tabular-nums}
.trail{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}
.src{display:inline-flex;align-items:center;gap:6px;font:400 12px/1 var(--mono);color:var(--ink-2);background:var(--off);border:1px solid var(--rule);border-radius:6px;padding:5px 7px;max-width:100%}
.src i{font-style:normal;color:var(--dim)}
a.src:hover{border-color:var(--accent-line);text-decoration:none;color:var(--accent)}

/* State: same four everywhere */
.pill{display:inline-flex;align-items:center;gap:6px;font:500 12px/1 var(--sans);padding:5px 8px;border-radius:6px;white-space:nowrap}
.pill::before{content:"";width:7px;height:7px;border-radius:2px;background:currentColor}
.s-ok .tile,.tile.s-ok{background:var(--ok)}.pill.s-ok{color:var(--ok);background:var(--ok-soft)}
.s-warn .tile,.tile.s-warn{background:var(--warn)}.pill.s-warn{color:var(--warn-ink);background:var(--warn-soft)}
.s-bad .tile,.tile.s-bad{background:var(--bad)}.pill.s-bad{color:var(--bad);background:var(--bad-soft)}
.s-info .tile,.tile.s-info{background:var(--accent)}.pill.s-info{color:var(--accent);background:var(--accent-soft)}

/* Groups: a parent row with child rows (themes > projects, projects > risks) */
.group{border-bottom:1px solid var(--rule)}
.group>.row{border-bottom:0}
.kids{list-style:none;margin:0 0 16px 26px;padding:0 0 0 16px;border-left:1px dashed var(--rule-2)}
.kids .row{padding:12px 0;border-bottom:1px solid var(--rule)}
.kids .row:last-child{border-bottom:0}
.kids .row h3{font-size:14.5px}
.kids-label{font:500 12px/1 var(--mono);color:var(--dim);margin:2px 0 4px 42px}

/* Actions */
.act{font:500 13px/1 var(--sans);color:var(--accent);background:var(--paper);border:1px solid var(--accent-line);border-radius:8px;padding:8px 11px;cursor:pointer;white-space:nowrap}
.act:hover{background:var(--accent-soft);border-color:var(--accent)}
.act.primary{color:#fff;background:var(--accent);border-color:var(--accent)}
.act.primary:hover{background:var(--accent-2)}

/* Dated entries */
.entry{display:grid;grid-template-columns:72px minmax(0,1fr) auto;gap:4px 14px;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--rule);font-size:14.5px}
.entry time{font:400 12px/1.6 var(--mono);color:var(--dim);font-variant-numeric:tabular-nums}
.entry .area{font:500 12px/1 var(--mono);color:var(--dim);margin-right:6px}

/* Table */
.tbl{overflow-x:auto;margin-top:4px}
table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th{font:500 12px/1.3 var(--mono);color:var(--dim)}
td.num,th.num{text-align:right}

/* Bars: weekly trend, heights set with --v (value / max) */
.trend{margin:18px 0 4px}
.trend figcaption{font:500 12px/1 var(--mono);color:var(--dim);margin-bottom:10px}
.bars{display:flex;align-items:flex-end;gap:6px;height:92px;border-bottom:1px solid var(--rule-2)}
.bars span{flex:1;min-width:6px;height:calc(var(--v) * 100%);background:var(--accent-line);border-radius:4px 4px 0 0;position:relative}
.bars span:last-child{background:var(--accent)}
.axis{display:flex;justify-content:space-between;font:400 11px/1 var(--mono);color:var(--dim);margin-top:6px}

.meter{margin:18px 0 6px}
.meter figcaption{display:flex;justify-content:space-between;gap:12px;font:500 12px/1 var(--mono);color:var(--dim);margin-bottom:10px}
.meter .track{display:flex;height:16px;border-radius:5px;overflow:hidden;background:var(--off);border:1px solid var(--rule)}
.meter .seg{width:calc(var(--w) * 100%);min-width:2px}
.seg.wip{background:var(--dim)}.seg.plan{background:var(--accent)}.seg.stretch{background:repeating-linear-gradient(135deg,var(--accent-line) 0 5px,var(--accent-soft) 5px 10px)}.seg.free{background:transparent}
.meter .legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:13px;color:var(--dim)}
.meter .legend span{display:inline-flex;align-items:center;gap:6px}
.meter .legend span::before{content:"";width:10px;height:10px;border-radius:3px;border:1px solid var(--rule-2)}
.meter .legend .wip::before{background:var(--dim)}.meter .legend .plan::before{background:var(--accent)}.meter .legend .stretch::before{background:var(--accent-line)}.meter .legend .free::before{background:var(--off)}
.empty{color:var(--dim);font-size:14px;padding:16px 0;margin:0}
.nomatch{color:var(--dim);font-size:14px;padding:16px 0;margin:0}

/* Footer */
.foot{margin-top:56px;padding-block:20px 40px;border-top:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between;font-size:13px;color:var(--dim)}
.foot .team{display:inline-flex;align-items:center;gap:8px}
.foot .team::before{content:"";width:8px;height:8px;border-radius:2px;background:var(--accent);box-shadow:-11px 0 0 0 color-mix(in srgb,var(--accent) 35%,transparent)}

/* Copy panel and toast */
.toast{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:var(--bg);font:500 13px/1.3 var(--sans);padding:10px 14px;border-radius:8px;max-width:calc(100% - 32px);z-index:20}
.panel{margin:10px 0 4px;padding:12px;border:1px solid var(--accent-line);border-radius:10px;background:var(--accent-soft);font-size:13px;color:var(--ink-2);grid-column:1/-1}
.panel textarea{width:100%;min-height:84px;margin-top:8px;font:400 13px/1.45 var(--mono);color:var(--ink);background:var(--paper);border:1px solid var(--rule-2);border-radius:8px;padding:8px;resize:vertical}

@media (max-width:640px){
  .row{grid-template-columns:12px minmax(0,1fr)}
  .side{grid-column:2;flex-direction:row;flex-wrap:wrap;align-items:center;justify-content:flex-start;text-align:left;gap:8px 10px;margin-top:6px}
  .entry{grid-template-columns:58px minmax(0,1fr)}
  .entry>.pill{grid-column:2;justify-self:start}
  .figs{grid-auto-flow:row;grid-template-columns:1fr 1fr}
  .fig,.fig+.fig{padding:14px 12px 14px 0;border-left:0}
  .fig:nth-child(even){padding-left:12px;border-left:1px solid var(--rule)}
  .fig:nth-child(n+3){border-top:1px solid var(--rule)}
  .kids{margin-left:6px;padding-left:12px}
  .kids-label{margin-left:22px}
  .sh .tools{margin-left:0;width:100%}.find{width:100%}
}
@media (prefers-reduced-motion:no-preference){.row,.entry{transition:background .15s}}
</style>
</head>
<body>

<header class="mast">
  <canvas aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="brand"><b>Devplan</b><span>{{WORKSPACE NAME}}</span></div>
    <h1>{{TITLE}}</h1>
    <div class="sub"><span>{{WINDOW, e.g. "Nov 12 · last 24 hours"}}</span><span>{{SCOPE, e.g. "5 repos · 3 teams"}}</span><span>Updated {{TIME}}</span></div>
  </div>
</header>

<main class="wrap">

  <!-- OPTIONAL. Graph still building or a source is missing. One sentence on what is missing and that the page fills in on its own. -->
  <div class="notice">{{e.g. "Devplan is still analyzing 2 of your 4 sources. This dashboard fills in automatically as they finish."}}</div>

  <!-- TODAY. Exactly 3 lines, ranked by what matters most. Plain sentences with links. -->
  <div class="today">
    <h2>Today</h2>
    <ol>
      <li>{{ONE SENTENCE, with a <a href="{{URL}}">link</a>}}</li>
    </ol>
  </div>

  <!-- FIGURES. 2 to 4 numbers that are the point of the page. em is optional: class "up" (good change) or "down" (bad change). -->
  <div class="figs">
    <div class="fig"><b>{{NUMBER}}</b><span>{{LABEL}}</span><em class="up">{{+3 vs last week}}</em></div>
  </div>

  <!-- PATTERN A: ROWS. Items with a state. Every row gets a state class on the li: s-ok, s-warn, s-bad, s-info. -->
  <section>
    <div class="sh"><h2>{{SECTION}}</h2><span class="n">{{COUNT}}</span></div>
    <ul class="list">
      <li class="row s-warn">
        <span class="tile"></span>
        <div>
          <h3><a href="{{URL}}">{{TITLE}}</a></h3>
          <p>{{1 TO 2 SENTENCES}}</p>
          <div class="trail"><a class="src" href="{{URL}}"><i>{{SOURCE, e.g. GitHub}}</i>{{e.g. PR #412}}</a></div>
        </div>
        <div class="side"><span class="pill s-warn">{{STATE}}</span><span class="m">{{e.g. "Ali · 4d idle"}}</span></div>
      </li>
    </ul>
  </section>

  <!-- PATTERN B: GROUPS. A parent row with child rows: demand theme > suggested projects, project > risks. -->
  <section>
    <div class="sh"><h2>{{SECTION}}</h2><span class="n">{{COUNT}}</span></div>
    <ul class="list">
      <li class="group">
        <div class="row s-info">
          <span class="tile"></span>
          <div>
            <h3>{{PARENT TITLE}}</h3>
            <p>{{1 TO 2 SENTENCES}}</p>
            <div class="trail"><a class="src" href="{{URL}}"><i>{{SOURCE}}</i>{{LABEL}}</a></div>
          </div>
          <div class="side"><span class="pill s-info">{{STATE}}</span><span class="m">{{e.g. "6 accounts"}}</span></div>
        </div>
        <div class="kids-label">{{CHILD LABEL, e.g. "Suggested projects"}}</div>
        <ul class="kids">
          <li class="row s-info">
            <span class="tile"></span>
            <div>
              <h3>{{CHILD TITLE}}</h3>
              <p>{{ONE SENTENCE}}</p>
            </div>
            <!-- OPTIONAL ACTION. data-prompt is the exact message the user will paste into Claude. -->
            <div class="side"><button class="act" type="button" data-prompt="{{PROMPT}}">{{ACTION, e.g. "Write spec"}}</button><span class="m">{{e.g. "Scope M"}}</span></div>
          </li>
        </ul>
      </li>
    </ul>
  </section>

  <!-- PATTERN C: DATED ENTRIES. Date, text, optional state pill, all on one row. -->
  <section>
    <div class="sh"><h2>{{SECTION}}</h2><span class="n">{{COUNT}}</span>
      <!-- OPTIONAL SEARCH. data-find points at the list it filters. -->
      <div class="tools"><input class="find" type="search" id="find-{{ID}}" data-find="#{{LIST ID}}" placeholder="{{e.g. Search changes}}" aria-label="{{Search changes}}"></div>
    </div>
    <!-- OPTIONAL CHIPS. Filter by data-area on each item. -->
    <div class="chips" data-for="#{{LIST ID}}"><button class="chip" type="button" data-area="{{AREA}}" aria-pressed="false">{{AREA}}</button></div>
    <ul class="list" id="{{LIST ID}}">
      <li class="entry" data-area="{{AREA}}"><time datetime="{{YYYY-MM-DD}}">{{Nov 12}}</time><div><span class="area">{{AREA}}</span>{{ONE SENTENCE with <a href="{{URL}}">link</a>}}</div><span class="pill s-ok">{{STATE}}</span></li>
    </ul>
  </section>

  <!-- PATTERN D: TABLE. Only when items share 4 or more fields. -->
  <section>
    <div class="sh"><h2>{{SECTION}}</h2></div>
    <div class="tbl"><table>
      <thead><tr><th>{{COL}}</th><th class="num">{{NUM COL}}</th></tr></thead>
      <tbody><tr><td>{{VALUE}}</td><td class="num">{{NUMBER}}</td></tr></tbody>
    </table></div>
  </section>

  <!-- PATTERN E: TREND. Weekly values; --v is value divided by the largest value (0 to 1). Last bar is the current period. -->
  <figure class="trend">
    <figcaption>{{e.g. "PRs merged per week"}}</figcaption>
    <div class="bars" role="img" aria-label="{{e.g. "PRs merged per week: 18, 22, 25, 31"}}"><span style="--v:.58" title="{{Oct 20: 18}}"></span></div>
    <div class="axis"><span>{{FIRST LABEL}}</span><span>{{LAST LABEL}}</span></div>
  </figure>

  <!-- PATTERN F: METER. How a fixed capacity is split. Each --w is that part divided by total capacity; the parts add up to 1 or less. Use only the segments you need. -->
  <figure class="meter">
    <figcaption><span>{{e.g. "Capacity: 48 engineer-weeks"}}</span><span>{{e.g. "85% planned"}}</span></figcaption>
    <div class="track" role="img" aria-label="{{e.g. "In progress 14, new 22, stretch 5, buffer 7 engineer-weeks"}}"><span class="seg wip" style="--w:.29"></span><span class="seg plan" style="--w:.46"></span><span class="seg stretch" style="--w:.10"></span><span class="seg free" style="--w:.15"></span></div>
    <div class="legend"><span class="wip">{{In progress · 14}}</span><span class="plan">{{New work · 22}}</span><span class="stretch">{{Stretch · 5}}</span><span class="free">{{Buffer · 7}}</span></div>
  </figure>

  <!-- EMPTY SECTION: keep the heading, one line. -->
  <section>
    <div class="sh"><h2>{{SECTION}}</h2></div>
    <p class="empty">{{e.g. "Nothing slipped this week."}}</p>
  </section>

  <footer class="foot">
    <span>From your Devplan workspace · Refreshes {{e.g. "weekdays at 7:47"}} · <a href="https://app.devplan.com">Open Devplan</a></span>
    <span class="team">{{TEAM LINE, e.g. "Your team can work from this same context."}} <a href="{{MEMBERS URL}}">Invite teammates</a></span>
  </footer>

</main>

<script>
(function(){
  // Masthead tile field, echoing the logomark. Static; redrawn on resize.
  var c=document.querySelector('.mast canvas');
  function draw(){
    if(!c)return;var r=c.getBoundingClientRect(),d=window.devicePixelRatio||1;
    c.width=r.width*d;c.height=r.height*d;var x=c.getContext('2d');x.scale(d,d);
    var s=9,g=7,step=s+g,cols=Math.ceil(r.width/step),rows=Math.ceil(r.height/step),seed=0,t=document.title;
    for(var i=0;i<t.length;i++)seed=(seed*31+t.charCodeAt(i))>>>0;
    function rnd(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296}
    var col=getComputedStyle(document.documentElement).getPropertyValue('--band-accent').trim()||'#5a77ff';
    for(var cy=0;cy<rows;cy++)for(var cx=0;cx<cols;cx++){
      var p=cx/cols,w=Math.max(0,(p-.45)/.55);if(w<=0)continue;
      var wave=.5+.5*Math.sin(cx*.35+cy*.6),k=rnd();
      if(k>w*.85*(.55+.45*wave))continue;
      x.globalAlpha=Math.min(.9,.12+w*.7*k+.1*wave);x.fillStyle=col;
      var px=cx*step+4,py=cy*step+4;x.beginPath();
      if(x.roundRect)x.roundRect(px,py,s,s,2.5);else x.rect(px,py,s,s);x.fill();
    }
  }
  draw();var to;window.addEventListener('resize',function(){clearTimeout(to);to=setTimeout(draw,120)});

  // Search and chip filters.
  function apply(list){
    var box=document.querySelector('[data-find="#'+list.id+'"]'),q=box?box.value.trim().toLowerCase().split(/\s+/).filter(Boolean):[];
    var on=[].slice.call(document.querySelectorAll('[data-for="#'+list.id+'"] .chip[aria-pressed="true"]')).map(function(b){return b.dataset.area});
    var shown=0;
    [].forEach.call(list.children,function(li){
      if(li.classList.contains('nomatch'))return;
      var txt=li.textContent.toLowerCase(),ok=q.every(function(w){return txt.indexOf(w)>-1})&&(!on.length||on.indexOf(li.dataset.area)>-1);
      li.hidden=!ok;if(ok)shown++;
    });
    var nm=list.querySelector('.nomatch');
    if(!shown&&!nm){nm=document.createElement('li');nm.className='nomatch';nm.textContent='No matches.';list.appendChild(nm)}
    if(nm)nm.hidden=!!shown;
  }
  document.querySelectorAll('[data-find]').forEach(function(box){var l=document.querySelector(box.dataset.find);if(l)box.addEventListener('input',function(){apply(l)})});
  document.querySelectorAll('[data-for] .chip').forEach(function(b){b.addEventListener('click',function(){
    b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');
    var l=document.querySelector(b.parentNode.dataset.for);if(l)apply(l);
  })});

  // Action buttons: copy the prompt so the user can paste it into Claude.
  function toast(msg){var t=document.createElement('div');t.className='toast';t.setAttribute('role','status');t.textContent=msg;document.body.appendChild(t);setTimeout(function(){t.remove()},2600)}
  function panel(btn,text){
    var host=btn.closest('.row,.sh')||btn.parentNode,old=host.querySelector('.panel');if(old){old.remove();return}
    var p=document.createElement('div');p.className='panel';p.textContent='Copy this and paste it into a Claude chat:';
    var ta=document.createElement('textarea');ta.readOnly=true;ta.value=text;p.appendChild(ta);host.appendChild(p);ta.focus();ta.select();
  }
  document.querySelectorAll('.act[data-prompt]').forEach(function(btn){btn.addEventListener('click',function(){
    var text=btn.dataset.prompt;
    try{navigator.clipboard.writeText(text).then(function(){toast('Copied. Paste it into Claude to start.')},function(){panel(btn,text)})}catch(e){panel(btn,text)}
  })});
})();
</script>
</body>
</html>
```
