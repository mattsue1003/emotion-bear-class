#!/usr/bin/env python3
"""熊熊心情教室 學習單：從 index.html 取出熊熊臉的畫法，做 4 頁 A4，再用 Chrome 印成 PDF。"""
import pathlib, re, subprocess

HERE = pathlib.Path(__file__).resolve().parent
src = (HERE.parent / "index.html").read_text(encoding="utf-8")
em = src[src.index("const EM={"):src.index("const NEG=")]
fn = src[src.index("function face(id,cls=''){"):src.index("/* ---------- 聲音")]

HTML = r"""<!doctype html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8">
<title>熊熊心情學習單</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Huninn&family=Noto+Sans+TC:wght@400;700&display=swap">
<style>
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Sans TC","PingFang TC",sans-serif;color:#24384A;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:12mm 13mm 10mm;display:flex;flex-direction:column;gap:5mm;page-break-after:always;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto}
.head{display:flex;align-items:center;gap:4mm}
.head svg{width:22mm;height:22mm;flex:none}
.head h1{font-family:"Huninn","PingFang TC",sans-serif;font-size:30pt;margin:0;line-height:1.1}
.head .no{margin-left:auto;font-family:"Huninn",sans-serif;font-size:13pt;background:#FFF4D6;border:2px solid #FFC23C;border-radius:99px;padding:1mm 4mm;white-space:nowrap}
.meta{display:flex;gap:10mm;font-size:12pt}
.meta span{flex:1;border-bottom:1.5px solid #9DB3C0;padding-bottom:1mm}
.adult{font-size:10.5pt;line-height:1.6;background:#EEF6F8;border-radius:4mm;padding:2.5mm 4mm}
.adult b{color:#2B7AA3}
.foot{margin-top:auto;font-size:8.5pt;color:#7D909E;display:flex;justify-content:space-between}
.kid{font-family:"Huninn","PingFang TC",sans-serif}

/* 1 連連看 */
.match{flex:1;display:grid;grid-template-columns:62mm 1fr 52mm;row-gap:5mm;align-items:center}
.scene{height:48mm;border:2.5px solid #CFE1E7;border-radius:6mm;background:linear-gradient(#E3F1FF,#F8FCFF 68%,#E9F4E1 68%);display:flex;align-items:center;justify-content:center;gap:2mm;flex-direction:column}
.scene .em{font-size:44pt;line-height:1}
.scene small{font-size:10pt;color:#62788A}
.dot{width:6mm;height:6mm;border-radius:50%;background:#24384A}
.lcol{display:flex;align-items:center;gap:4mm}
.rcol{display:flex;align-items:center;gap:4mm;justify-self:end}
.rcol svg{width:44mm;height:44mm}

/* 2 圈一樣 */
.rows{flex:1;display:flex;flex-direction:column;justify-content:space-between}
.frow{display:flex;align-items:center;gap:3mm}
.target{width:38mm;height:38mm;border:3px dashed #2B7AA3;border-radius:6mm;padding:1mm;background:#F4FAFC;flex:none}
.arrow{font-size:26pt;color:#9DB3C0;flex:none}
.opts{display:flex;justify-content:space-between;flex:1}
.opts svg{width:33mm;height:33mm}

/* 3 畫表情 */
.draw{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:4mm}
.cell{border:2.5px solid #CFE1E7;border-radius:6mm;position:relative;display:flex;align-items:center;justify-content:center}
.cell .blank{width:56mm;height:56mm;margin-left:18mm}
.cell .model{position:absolute;left:3mm;top:3mm;width:22mm;text-align:center;font-size:12pt}
.cell .model svg{width:22mm;height:22mm;display:block}

/* 4 一週＋氣球 */
table{width:100%;border-collapse:collapse}
td,th{border:1.5px solid #CFE1E7;text-align:center;padding:1mm}
th{font-family:"Huninn",sans-serif;font-size:14pt;background:#F4FAFC;width:16mm}
td svg{width:15.5mm;height:15.5mm;display:block;margin:auto}
thead td{font-size:10pt;color:#62788A;padding:1mm}
.balloons{display:flex;justify-content:space-around;align-items:flex-end}
.balloons svg{width:22mm;height:31mm}
.sec{font-family:"Huninn",sans-serif;font-size:17pt;margin:0;display:flex;align-items:center;gap:3mm}
.talk{display:flex;gap:4mm;align-items:center;border:2.5px dashed #3DBE84;border-radius:6mm;padding:2mm 4mm}
.talk svg{width:24mm;height:24mm;flex:none}
.talk .kid{font-size:20pt}
.talk .boxes{margin-left:auto;display:flex;gap:2mm}
.talk .boxes i{width:9mm;height:9mm;border:2px solid #3DBE84;border-radius:2mm;display:block}
</style></head><body>
<div id="out"></div>
<script>
__EM__
__FN__
function blank(){return `<svg viewBox="0 0 200 200" class="blank" aria-label="空白熊熊臉">
 <g fill="#fff" stroke="#3A2618" stroke-width="3">
  <circle cx="44" cy="50" r="27"/><circle cx="44" cy="50" r="14" stroke-dasharray="4 4"/>
  <circle cx="156" cy="50" r="27"/><circle cx="156" cy="50" r="14" stroke-dasharray="4 4"/>
  <circle cx="100" cy="112" r="76"/>
  <ellipse cx="100" cy="144" rx="40" ry="30" stroke-dasharray="5 4"/>
 </g><ellipse cx="100" cy="128" rx="11" ry="8" fill="#3A2618"/></svg>`}
function balloon(){return `<svg viewBox="0 0 120 170"><ellipse cx="60" cy="62" rx="50" ry="58" fill="#fff" stroke="#EF5350" stroke-width="4"/>
 <path d="M54 118 L66 118 L60 128Z" fill="#fff" stroke="#EF5350" stroke-width="3"/><path d="M60 128 Q50 145 62 158 Q70 166 60 170" stroke="#8A6A55" stroke-width="3" fill="none"/></svg>`}
const head=(icon,title,no)=>`<div class="head">${face(icon)}<h1>${title}</h1><span class="no">學習單 ${no}／4</span></div>
 <div class="meta"><span>名字：</span><span>日期：</span></div>`;
const foot=`<div class="foot"><span>熊熊心情教室・情緒辨識練習</span><span>mattsue1003.github.io/emotion-bear-class</span></div>`;
let h='';

// 1 連連看
const sc=[['🎁✨','收到禮物','happy'],['🍦💧','冰淇淋掉了','sad'],['🧱💥','積木倒了','angry'],['⛈️⚡','打雷了','scared']];
const right=['angry','happy','scared','sad'];
h+=`<section class="page">${head('happy','熊熊怎麼了？連連看',1)}
<div class="adult"><b>大人唸：</b>指著左邊的圖說「熊熊收到禮物，熊熊覺得怎麼樣？」請孩子用手指找右邊的臉，再用蠟筆把點和點連起來。說得出感覺名稱就給一個大讚。</div>
<div class="match">${sc.map((s,i)=>`<div class="lcol"><div class="scene" style="flex:1"><span class="em">${s[0]}</span><small>${s[1]}</small></div><i class="dot"></i></div><div></div><div class="rcol"><i class="dot"></i>${face(right[i])}</div>`).join('')}</div>${foot}</section>`;

// 2 圈一樣
const rows=[['angry',['happy','angry','calm','sad']],['happy',['sad','scared','happy','angry']],['sad',['sad','surprised','happy','calm']],['scared',['calm','angry','surprised','scared']],['surprised',['scared','surprised','sad','happy']]];
h+=`<section class="page">${head('surprised','找一樣的臉，圈起來',2)}
<div class="adult"><b>大人唸：</b>「看左邊框框裡的熊熊，牠是什麼心情？」請孩子在右邊找出一樣的臉圈起來。找到後一起做一次那個表情。要看<b>眉毛</b>和<b>嘴巴</b>。</div>
<div class="rows">${rows.map(r=>`<div class="frow"><div class="target">${face(r[0])}</div><span class="arrow">➜</span><div class="opts">${r[1].map(x=>face(x)).join('')}</div></div>`).join('')}</div>${foot}</section>`;

// 3 畫表情
h+=`<section class="page">${head('calm','幫熊熊畫表情',3)}
<div class="adult"><b>大人唸：</b>看左上角的小熊熊，說「熊熊開心了，嘴巴怎麼樣？眼睛怎麼樣？」請孩子在大熊熊臉上畫眼睛和嘴巴，畫完照顏色塗臉。不用畫得像，<b>說得出來比畫得好更重要</b>。</div>
<div class="draw">${['happy','sad','angry','scared','surprised','calm'].map(id=>`<div class="cell"><div class="model">${face(id)}<span class="kid">${EM[id].name}</span></div>${blank()}</div>`).join('')}</div>${foot}</section>`;

// 4 一週心情＋冷靜魔法
const days=['一','二','三','四','五','六','日'],six=['happy','sad','angry','scared','surprised','calm'];
h+=`<section class="page">${head('sad','我的心情一週＋冷靜魔法',4)}
<div class="adult"><b>每天睡前：</b>請孩子圈出今天的心情，問「今天什麼時候有這個心情？」幫他把事情寫在旁邊。<b>難過、生氣時：</b>一起吹氣球（鼻子吸、嘴巴慢慢吹），吹一次塗一顆。說出「我好生氣，幫幫我」就在方格打勾。</div>
<table><thead><tr><td></td>${six.map(id=>`<td>${EM[id].name}</td>`).join('')}</tr></thead><tbody>
${days.map(d=>`<tr><th>${d}</th>${six.map(id=>`<td>${face(id)}</td>`).join('')}</tr>`).join('')}</tbody></table>
<p class="sec">🎈 吹氣球：吹一次，塗一顆</p>
<div class="balloons">${Array.from({length:5},balloon).join('')}</div>
<div class="talk">${face('angry')}<span class="kid">我好生氣，幫幫我！</span><span class="boxes">${'<i></i>'.repeat(7)}</span></div>
${foot}</section>`;
document.getElementById('out').innerHTML=h;
</script></body></html>"""

out = HERE / "worksheets.html"
out.write_text(HTML.replace("__EM__", em).replace("__FN__", fn), encoding="utf-8")
pdf = HERE / "熊熊心情學習單.pdf"
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", out.as_uri()],
               check=True, capture_output=True)
print(pdf, pdf.stat().st_size)
