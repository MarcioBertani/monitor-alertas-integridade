from playwright.sync_api import sync_playwright
import pathlib, shutil

HERE = pathlib.Path(__file__).parent
W, H = 1920, 1080

OVERLAY = r"""
(() => {
const css = `
#vx-card{position:fixed;inset:0;z-index:9000;background:#14202b;color:#eef2f5;display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Sans',sans-serif;opacity:1;transition:opacity .6s ease}
#vx-card.off{opacity:0;pointer-events:none}
#vx-card .in{width:1400px;max-width:90vw}
#vx-card .k{font-family:'IBM Plex Mono',monospace;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#e0a24a;margin-bottom:28px}
#vx-card h1{font-size:92px;line-height:1.04;font-weight:600;margin:0 0 28px;letter-spacing:-.01em;text-wrap:balance}
#vx-card p{font-size:38px;line-height:1.35;color:#b9c6d1;margin:0;max-width:1250px}
#vx-card .rule{width:120px;height:6px;background:#c0392b;margin:0 0 40px}
#vx-card .flow{display:flex;align-items:stretch;gap:0;margin-top:56px}
#vx-card .box{flex:1;border:2px solid #3a4f61;padding:28px 26px;background:#1b2b38;opacity:0;transform:translateY(16px);transition:all .5s ease}
#vx-card .box.on{opacity:1;transform:none}
#vx-card .box b{display:block;font-size:30px;font-weight:600;margin-bottom:10px}
#vx-card .box span{font-size:22px;color:#9fb0be;line-height:1.35;display:block}
#vx-card .box i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:18px;color:#e0a24a;letter-spacing:.1em;display:block;margin-bottom:14px}
#vx-card .arr{width:64px;display:flex;align-items:center;justify-content:center;color:#e0a24a;font-size:40px;opacity:0;transition:opacity .4s}
#vx-card .arr.on{opacity:1}
#vx-card ul{list-style:none;padding:0;margin:0 0 48px;display:grid;gap:22px}
#vx-card li{font-size:42px;padding-left:44px;position:relative}
#vx-card li:before{content:"";position:absolute;left:0;top:22px;width:22px;height:6px;background:#e0a24a}
#vx-card .foot{font-family:'IBM Plex Mono',monospace;font-size:22px;color:#9fb0be;letter-spacing:.06em;border-top:1px solid #3a4f61;padding-top:26px;display:flex;justify-content:space-between;gap:20px}
#vx-cap{position:fixed;left:50%;bottom:44px;transform:translateX(-50%) translateY(20px);z-index:8000;background:#14202bf2;color:#fff;
  font-family:'IBM Plex Sans',sans-serif;font-size:34px;font-weight:500;padding:20px 36px;border-left:8px solid #e0a24a;opacity:0;transition:all .4s ease;
  box-shadow:0 10px 40px #0005;white-space:nowrap}
#vx-cap.on{opacity:1;transform:translateX(-50%)}
#vx-cur{position:fixed;z-index:9500;width:28px;height:28px;pointer-events:none;left:-50px;top:-50px;transition:transform .12s}
#vx-cur.down{transform:scale(.82)}
#vx-ring{position:fixed;z-index:9400;width:60px;height:60px;border-radius:50%;border:3px solid #e0a24a;pointer-events:none;opacity:0;transform:translate(-50%,-50%) scale(.4)}
#vx-ring.go{animation:vxr .5s ease-out}
@keyframes vxr{from{opacity:.9;transform:translate(-50%,-50%) scale(.4)}to{opacity:0;transform:translate(-50%,-50%) scale(1.4)}}
`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
const card=document.createElement('div');card.id='vx-card';document.body.appendChild(card);
const cap=document.createElement('div');cap.id='vx-cap';document.body.appendChild(cap);
const cur=document.createElement('div');cur.id='vx-cur';
cur.innerHTML='<svg viewBox="0 0 28 28" width="28" height="28"><path d="M4 2 L4 22 L9.5 17 L13 25 L16.5 23.5 L13 15.5 L20.5 15.5 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
document.body.appendChild(cur);
const ring=document.createElement('div');ring.id='vx-ring';document.body.appendChild(ring);
addEventListener('mousemove',e=>{cur.style.left=(e.clientX-4)+'px';cur.style.top=(e.clientY-2)+'px';},true);
addEventListener('mousedown',e=>{cur.classList.add('down');ring.style.left=e.clientX+'px';ring.style.top=e.clientY+'px';ring.classList.remove('go');void ring.offsetWidth;ring.classList.add('go');},true);
addEventListener('mouseup',()=>cur.classList.remove('down'),true);
window.vx={
  card(html){card.innerHTML='<div class="in">'+html+'</div>';card.classList.remove('off');},
  hide(){card.classList.add('off');},
  cap(t){if(!t){cap.classList.remove('on');return;}cap.classList.remove('on');setTimeout(()=>{cap.textContent=t;cap.classList.add('on');},t&&cap.textContent?250:0);},
  step(sel){document.querySelectorAll(sel).forEach(e=>e.classList.add('on'));}
};
})();
"""

INTRO = """<div class="k">Projeto · Integridade em apostas esportivas</div><div class="rule"></div>
<h1>Monitor de Alertas<br>de Integridade</h1>
<p>Dos e-mails do Sportradar Integrity Exchange para uma fila de triagem e um painel de acompanhamento.</p>"""

PROBLEMA = """<div class="k">O problema</div><div class="rule"></div>
<h1>Alertas chegam por e-mail, um a um.</h1>
<p>Cada um precisava ser lido, classificado e registrado à mão, sem uma visão clara do que analisar primeiro.</p>"""

FLUXO = """<div class="k">Como funciona</div><div class="rule"></div>
<h1 style="font-size:72px">Do e-mail à decisão</h1>
<div class="flow">
<div class="box b1"><i>01</i><b>Gmail</b><span>Alertas e feedbacks da Sportradar chegam por e-mail</span></div><div class="arr a1">→</div>
<div class="box b2"><i>02</i><b>Apps Script</b><span>Lê, classifica e evita duplicados automaticamente</span></div><div class="arr a2">→</div>
<div class="box b3"><i>03</i><b>Google Sheets</b><span>Uma aba por mês, com histórico e indicadores</span></div><div class="arr a3">→</div>
<div class="box b4"><i>04</i><b>Monitor</b><span>Fila por prioridade e visão geral do volume</span></div>
</div>"""

FIM = """<div class="k">Resultado</div><div class="rule"></div>
<ul><li>Importação automática dos alertas</li><li>Prioridade clara do que analisar primeiro</li><li>Visão do volume por mês, esporte e mercado</li></ul>
<div class="foot"><span>Google Apps Script · Google Sheets · HTML/JS · Claude</span><span>Dados fictícios para demonstração</span></div>"""


def main():
    vdir = HERE / "rec"
    shutil.rmtree(vdir, ignore_errors=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": W, "height": H}, record_video_dir=str(vdir),
                            record_video_size={"width": W, "height": H}, color_scheme="light")
        pg = ctx.new_page()
        pg.goto((HERE.parent / "index.html").as_uri())
        pg.evaluate(OVERLAY)
        pg.evaluate("vx.card(%r)" % INTRO)
        pg.mouse.move(W - 40, H - 40)
        pg.wait_for_timeout(600)  # lead-in trimmed later
        pg.evaluate("document.title='MARK'")
        pg.wait_for_timeout(4200)
        pg.evaluate("vx.card(%r)" % PROBLEMA); pg.wait_for_timeout(4500)
        pg.evaluate("vx.card(%r)" % FLUXO); pg.wait_for_timeout(500)
        for i in range(1, 5):
            pg.evaluate(f"vx.step('.b{i}')"); pg.wait_for_timeout(450)
            if i < 4: pg.evaluate(f"vx.step('.a{i}')"); pg.wait_for_timeout(250)
        pg.wait_for_timeout(2600)

        def mv(sel, steps=28, pause=250):
            box = pg.locator(sel).first.bounding_box()
            pg.mouse.move(box["x"] + min(box["width"] / 2, 140), box["y"] + box["height"] / 2, steps=steps)
            pg.wait_for_timeout(pause)

        def click(sel, steps=28):
            mv(sel, steps)
            box = pg.locator(sel).first.bounding_box()
            pg.mouse.down(); pg.wait_for_timeout(90); pg.mouse.up()
            pg.locator(sel).first.click(position={"x": min(box["width"] / 2, 140), "y": box["height"] / 2}) if False else None

        # app
        pg.mouse.move(1100, 600)
        pg.evaluate("vx.hide()"); pg.wait_for_timeout(700)
        pg.evaluate("vx.cap('Fila de triagem: o que precisa de atenção aparece primeiro')")
        pg.wait_for_timeout(1500)
        items = pg.locator(".item")
        for k in range(3):
            box = items.nth(k).bounding_box()
            pg.mouse.move(box["x"] + 200, box["y"] + box["height"] / 2, steps=20); pg.wait_for_timeout(350)
        pg.wait_for_timeout(600)

        # open an alert with analysis
        pg.evaluate("vx.cap('Cada alerta abre com a análise completa da Sportradar')")
        idx = pg.evaluate("""(()=>{const els=[...document.querySelectorAll('.item')];for(let j=0;j<els.length;j++){
            const i=+els[j].dataset.i; if(ALERTAS[i]&&ALERTAS[i].analise) return j;} return 1;})()""")
        box = items.nth(idx).bounding_box()
        pg.mouse.move(box["x"] + 200, box["y"] + box["height"] / 2, steps=24); pg.wait_for_timeout(200)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up()
        pg.wait_for_timeout(700)
        mv(".analise", steps=30, pause=2600)

        # filters
        pg.evaluate("vx.cap('Busca e filtros por status, esporte, mês e suspeita')")
        tab = pg.locator("#tab-todos").bounding_box()
        pg.mouse.move(tab["x"] + tab["width"] / 2, tab["y"] + tab["height"] / 2, steps=30); pg.wait_for_timeout(200)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(900)
        mv("#f-esporte", steps=26, pause=200)
        pg.mouse.down(); pg.mouse.up()
        pg.select_option("#f-esporte", "Basketball"); pg.wait_for_timeout(1200)
        mv("#q", steps=26, pause=150)
        pg.mouse.down(); pg.mouse.up()
        pg.locator("#q").press_sequentially("Clausura", delay=110); pg.wait_for_timeout(1300)
        box = pg.locator(".item").first.bounding_box()
        pg.mouse.move(box["x"] + 200, box["y"] + box["height"] / 2, steps=24); pg.wait_for_timeout(150)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(900)

        # decision
        pg.evaluate("vx.cap('Decisão registrada: suspeita, status e notas')")
        pg.evaluate("document.querySelector('#suspeito-Sim').scrollIntoView({block:'center',behavior:'smooth'})")
        pg.wait_for_timeout(800)
        for sel in ["#suspeito-Sim", "#status-Arquivado"]:
            mv(sel, steps=24, pause=150)
            pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(700)
        mv("#notas", steps=24, pause=150)
        pg.mouse.down(); pg.mouse.up()
        pg.locator("#notas").press_sequentially("Volume concentrado em under. Reportado ao time de trading.", delay=40)
        pg.wait_for_timeout(900)

        pg.evaluate("vx.cap('Alterações prontas para atualizar a planilha')")
        mv("#chg-btn", steps=34, pause=200)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(2800)
        mv("#chg-close", steps=24, pause=150)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(500)

        # overview
        pg.evaluate("vx.cap('Visão geral: volume por mês, esporte, país e mercado')")
        mv("#nav-g", steps=30, pause=150)
        pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(2400)
        pg.mouse.move(1200, 700, steps=30); pg.wait_for_timeout(300)
        pg.mouse.wheel(0, 420); pg.wait_for_timeout(2200)
        pg.mouse.wheel(0, -420); pg.wait_for_timeout(600)
        mv("#g-mes", steps=24, pause=150)
        pg.mouse.down(); pg.mouse.up()
        pg.select_option("#g-mes", "Setembro"); pg.wait_for_timeout(2200)
        pg.evaluate("vx.cap('')"); pg.wait_for_timeout(400)

        pg.evaluate("vx.card(%r)" % FIM); pg.wait_for_timeout(5200)
        path = pg.video.path()
        ctx.close(); b.close()
    shutil.copy(path, HERE / "gravacao.webm")
    print("done", path)


if __name__ == "__main__":
    main()
