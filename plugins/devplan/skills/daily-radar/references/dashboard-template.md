# Dashboard template

Copy this HTML as the starting point for every dashboard. Keep the `<head>` and `<style>` exactly as written; fill in the body using the patterns described in the comments.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
:root{--paper:#fff;--tint:#fbfbfc;--off:#f7f7f8;--rule:#ececee;--ink:#0a0a0b;--ink2:#1a1a1c;--dim:#52525a;--faint:#8a8a92;--cobalt:#1f3dff;--soft:#f0f5ff;--warn:#e6a437;--warnbg:#fdf4e3;--bad:#c0362c;--badbg:#fbebeb;--good:#1e7a3c;--goodbg:#e5f4e4}
@media (prefers-color-scheme:dark){:root{--paper:#0a0a0b;--tint:#0f0f11;--off:#141416;--rule:#26262a;--ink:#f4f4f5;--ink2:#e4e4e7;--dim:#a0a0a6;--faint:#8a8a92;--cobalt:#5a77ff;--soft:#161a33;--warnbg:#2c2414;--badbg:#2c1616;--goodbg:#14261a}}
*{box-sizing:border-box}
body{margin:0;background:var(--tint);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif}
a{color:var(--cobalt);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:920px;margin:0 auto;padding:32px 16px 48px}
.hdr{margin-bottom:24px}
.eyebrow{font:600 11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
h1{font-size:26px;line-height:1.2;margin:6px 0 4px}
.sub{color:var(--dim);font-size:14px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:20px 0 8px}
.stat{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:12px 14px}
.stat .v{font-size:22px;font-weight:650}.stat .l{color:var(--dim);font-size:13px}
.headline{background:var(--soft);border-radius:10px;padding:14px 16px;margin:16px 0}
.headline ol{margin:0;padding-left:20px}.headline li{margin:4px 0}
section{margin-top:32px}
h2{font:600 11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 4px;padding-bottom:10px;border-bottom:1px solid var(--rule)}
.list{list-style:none;margin:0;padding:0}
.item{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:14px 0;border-bottom:1px solid var(--rule)}
.item h3{font-size:15px;margin:0 0 2px}
.item p{margin:0;color:var(--dim);font-size:14px}
.meta{text-align:right;font:12px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--dim);white-space:nowrap}
.badge{display:inline-block;font:600 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:4px 7px;border-radius:5px;margin-top:4px}
.b-good{background:var(--goodbg);color:var(--good)}.b-partial{background:var(--warnbg);color:#a26a00}.b-none{background:var(--badbg);color:var(--bad)}.b-info{background:var(--soft);color:var(--cobalt)}
.entry{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:10px 0;border-bottom:1px solid var(--rule);font-size:14px}
.entry .date{color:var(--faint);font:12px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}th{color:var(--dim);font-weight:600;font-size:12px}
.empty{color:var(--faint);font-size:14px;padding:12px 0}
.foot{margin-top:40px;padding-top:16px;border-top:1px solid var(--rule);color:var(--dim);font-size:13px}
.foot .cta{margin-top:8px;background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:12px 14px;color:var(--ink2)}
.foot .cta ul{margin:6px 0 6px;padding-left:18px}.foot .cta li{margin:2px 0}
@media (max-width:600px){.item,.entry{grid-template-columns:1fr}.entry{gap:2px}.meta{text-align:left}}
</style>
</head>
<body>
<main class="wrap">

  <header class="hdr">
    <div class="eyebrow">Devplan · {{MODE: Connectors | Devplan graph}}</div>
    <h1>{{TITLE}}</h1>
    <div class="sub">{{WINDOW, e.g. "Nov 9, last 24 hours"}} · {{SCOPE}} · Updated {{TIME}}</div>
  </header>

  <!-- OPTIONAL: key numbers. 2 to 5 stats. -->
  <div class="stats">
    <div class="stat"><div class="v">{{NUMBER}}</div><div class="l">{{LABEL}}</div></div>
  </div>

  <!-- OPTIONAL: headline. Exactly 3 items. -->
  <div class="headline">
    <ol>
      <li>{{ONE LINE}}</li>
    </ol>
  </div>

  <!-- PATTERN A: titled items with right-hand meta. Use for findings, themes, blockers, projects, commitments. -->
  <section>
    <h2>{{SECTION NAME}}</h2>
    <ul class="list">
      <li class="item">
        <div>
          <h3>{{ITEM TITLE}}</h3>
          <p>{{1 TO 3 SENTENCES, with <a href="{{URL}}">source links</a>}}</p>
        </div>
        <div class="meta">{{e.g. "5 accounts"}}<br><span class="badge b-partial">{{STATUS}}</span></div>
      </li>
    </ul>
  </section>

  <!-- PATTERN B: dated one-liners. Use for new requests, changelog entries, activity. The date sits on the same row, right-aligned. -->
  <section>
    <h2>{{SECTION NAME}}</h2>
    <ul class="list">
      <li class="entry">
        <div><a href="{{URL}}">{{NAME}}</a>: {{ONE LINE}}</div>
        <div class="date">{{Nov 6}}</div>
      </li>
    </ul>
  </section>

  <!-- PATTERN C: a real table, only when items share 4 or more fields. -->
  <section>
    <h2>{{SECTION NAME}}</h2>
    <table>
      <thead><tr><th>{{COL}}</th></tr></thead>
      <tbody><tr><td>{{VALUE}}</td></tr></tbody>
    </table>
  </section>

  <!-- Empty section: keep the heading, show one line. -->
  <section>
    <h2>{{SECTION NAME}}</h2>
    <p class="empty">{{e.g. "Nothing new this period."}}</p>
  </section>

  <footer class="foot">
    <!-- Connector mode only. Delete the whole footer in graph mode. -->
    <div>{{COVERAGE LINE}}</div>
    <div>{{THIS RUN LINE}}</div>
    <div class="cta">Run this on the Devplan knowledge graph instead:
      <ul>
        <li>{{REASON}}</li>
      </ul>
      {{CONNECT LINE with link}}
    </div>
  </footer>

</main>
</body>
</html>
```
