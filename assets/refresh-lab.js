/* Interactive teaching aids; the students' three project files remain separate. */
(function () {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const steps = [
    { phase: 0, title: 'عنوان الصفحة', note: 'HTML يضيف المحتوى. هذا السطر يبني عنوان رصد.', code: '<h1>🛡 رصد</h1>', focus: 'title' },
    { phase: 0, title: 'بطاقة واحدة', note: 'الحاوية تجمع اسم الحساس وقيمته. انظر إلى البطاقة التي ظهرت.', code: '<div class="card" id="temp-card">\n  <h2>🌡️ الحرارة</h2>\n  <p id="temp">-- °C</p>\n</div>', focus: 'temp' },
    { phase: 0, title: 'الحساسات الأربعة', note: 'نكرر شكل البطاقة، ولكل قيمة id مختلف. القيم الآن مؤقتة.', code: '<div class="card"><h2>🌡️ الحرارة</h2><p id="temp">-- °C</p></div>\n<div class="card"><h2>💧 الرطوبة</h2><p id="humidity">-- %</p></div>\n<div class="card"><h2>🌊 مستوى الماء</h2><p id="water">-- %</p></div>\n<div class="card"><h2>📏 المسافة</h2><p id="distance">-- cm</p></div>', focus: 'cards' },
    { phase: 1, title: 'الألوان', note: 'المحتوى نفسه؛ CSS يعطي الصفحة والبطاقات ألوانها.', code: 'body { background-color: #0d1117; color: #e6edf3; }\n.card { background-color: #161b22; }', focus: 'cards' },
    { phase: 1, title: 'المسافات والزوايا', note: 'padding يضيف مساحة داخل البطاقة، وmargin حولها. border-radius يدوّر الزوايا.', code: '.card {\n  padding: 20px;\n  margin: 8px;\n  border-radius: 12px;\n}', focus: 'temp' },
    { phase: 1, title: 'البطاقات في صف', note: 'الحاوية توزّع البطاقات بجوار بعضها باستخدام Flex.', code: '.cards {\n  display: flex;\n  justify-content: space-evenly;\n}', focus: 'cards' },
    { phase: 2, title: 'نختار قيمة الحرارة', note: 'المعرّف temp يوصل JavaScript إلى قيمة الحرارة تحديدًا. انظر إلى الإطار حولها.', code: 'const temp = document.getElementById("temp");', focus: 'value' },
    { phase: 2, title: 'نغيّر النص', note: 'textContent يغيّر نص العنصر المختار. نكرر الفكرة نفسها مع قيم الحساسات الأربعة.', code: 'temp.textContent = "28 °C";\nhumidity.textContent = "61 %";\nwater.textContent = "20 %";\ndistance.textContent = "80 cm";', focus: 'value' },
    { phase: 2, title: 'التحديث كل ٣ ثوانٍ', note: 'المؤقت يكرر دالة التحديث. انتظر ثلاث ثوانٍ وشاهد الرقم؛ هذه قراءات توضيحية محاكية.', code: 'setInterval(updateReadings, 3000);', focus: 'value' },
    { phase: 2, title: 'شرط الحرارة', note: 'جرّب ٢٥ ثم ٣٢. المقارنة مع ٣٠ تحدد اللون والحالة. الفرع else يعيد اللون الآمن.', code: 'if (temperature > 30) {\n  tempCard.style.backgroundColor = "#f85149";\n  status.textContent = "⚠️ تنبيه";\n} else {\n  tempCard.style.backgroundColor = "#161b22";\n  status.textContent = "✅ الغرفة آمنة";\n}', focus: 'temp' },
    { phase: 2, title: 'الحرارة والماء معًا', note: 'جرّب حرارة آمنة وماء مرتفعًا. يكفي خطر واحد لظهور التنبيه. أعد القيم الآمنة لترى رجوع اللون.', code: 'let alert = false;\nif (temperature > 30) { alert = true; }\nif (waterLevel > 70) { alert = true; }\nif (alert) {\n  status.textContent = "⚠️ تنبيه";\n} else {\n  status.textContent = "✅ الغرفة آمنة";\n}', focus: 'water' }
  ];
  function button(text, action) { const b = document.createElement('button'); b.type = 'button'; b.textContent = text; b.dataset.action = action; return b; }
  function initLab(host) {
    const initial = Number(host.dataset.start || 0);
    let index = initial, playing = null, ticker = null, temperature = 25, water = 20, tick = 0;
    host.innerHTML = '<div class="lab-heading"><div><span class="lab-eyebrow">شاهد · جرّب · افهم</span><h2>شاهد رصد وهو يُبنى</h2><p>كل خطوة تُظهر كودًا وأثره. جرّب هنا، ثم نفّذ الخطوات في ملفات مشروعك.</p></div><span class="lab-count"></span></div><div class="lab-phases" role="group" aria-label="اختر مرحلة البناء"></div><div class="lab-stage-title" aria-live="polite"></div><div class="lab-workbench"><div class="lab-source"><div class="lab-panel-title">الكود الذي يصنع الفرق</div><pre><code></code></pre></div><div class="lab-result"><div class="lab-panel-title">النتيجة أمامك</div><div class="lab-preview"><h3 class="lab-brand">🛡 رصد</h3><div class="lab-sensors"></div><p class="lab-room-status"></p></div></div></div><p class="lab-explanation" aria-live="polite"></p><div class="lab-readings" hidden></div><div class="lab-controls" role="group" aria-label="التحكم في تجربة البناء"></div>';
    const phases = host.querySelector('.lab-phases');
    [['🏗️ HTML · الهيكل',0],['🎨 CSS · الشكل',3],['⚡ JavaScript · الحياة',6]].forEach(([label,start])=>{const b=button(label,'phase');b.dataset.step=start;phases.append(b);});
    const controls = host.querySelector('.lab-controls');
    [['→ السابق','prev'],['تشغيل تلقائي ▶','play'],['التالي ←','next'],['إعادة من البداية ↺','reset']].forEach(([label,action])=>controls.append(button(label,action)));
    const readingControls=host.querySelector('.lab-readings');
    [['حرارة آمنة · ٢٥ °C','temp-safe'],['حرارة مرتفعة · ٣٢ °C','temp-high'],['ماء آمن · ٢٠٪','water-safe'],['ماء مرتفع · ٨٠٪','water-high']].forEach(([label,action])=>readingControls.append(button(label,action)));
    const preview=host.querySelector('.lab-preview');
    const sensors=host.querySelector('.lab-sensors');
    [['🌡️ الحرارة','temp','-- °C'],['💧 الرطوبة','humidity','-- %'],['🌊 مستوى الماء','water','-- %'],['📏 المسافة','distance','-- cm']].forEach(([name,id,value])=>{const c=document.createElement('div');c.className='lab-sensor';c.dataset.sensor=id;const h=document.createElement('h4');h.textContent=name;const p=document.createElement('p');p.className='lab-value';p.textContent=value;c.append(h,p);sensors.append(c);});
    const tempCard=host.querySelector('[data-sensor="temp"]'), waterCard=host.querySelector('[data-sensor="water"]');
    const tempValue=tempCard.querySelector('.lab-value'), waterValue=waterCard.querySelector('.lab-value');
    const status=host.querySelector('.lab-room-status');
    function stopTick(){if(ticker!==null){clearInterval(ticker);ticker=null;}}
    function stop(){if(playing!==null){clearInterval(playing);playing=null;}host.querySelector('[data-action="play"]').textContent='تشغيل تلقائي ▶';}
    function readings(){
      tempValue.textContent=temperature+' °C';waterValue.textContent=water+' %';
      const tempDanger=index>=9 && temperature>30,waterDanger=index>=10 && water>70;
      tempCard.classList.toggle('lab-danger',tempDanger);waterCard.classList.toggle('lab-danger',waterDanger);
      status.textContent=index>=9?(tempDanger||waterDanger?'⚠️ تنبيه':'✅ الغرفة آمنة'):'';
      status.classList.toggle('lab-status-danger',tempDanger||waterDanger);
      readingControls.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.action==='temp-safe'&&temperature===25)||(b.dataset.action==='temp-high'&&temperature===32)||(b.dataset.action==='water-safe'&&water===20)||(b.dataset.action==='water-high'&&water===80))));
    }
    function render(){
      stopTick();const step=steps[index];
      host.querySelector('.lab-count').textContent=(index+1)+' / '+steps.length;
      host.querySelector('.lab-stage-title').textContent=step.title;
      host.querySelector('.lab-explanation').textContent=step.note;
      const code=host.querySelector('.lab-source code');code.className='language-'+(step.phase===0?'html':step.phase===1?'css':'javascript');code.textContent=step.code;
      if(window.Prism)window.Prism.highlightElement(code);
      phases.querySelectorAll('button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===step.phase)));
      preview.className='lab-preview'+(index>=3?' lab-painted':'')+(index>=4?' lab-spaced':'')+(index>=5?' lab-flexed':'');
      sensors.querySelectorAll('.lab-sensor').forEach((c,i)=>{c.hidden=index===0||(index===1&&i>0);c.classList.remove('lab-target','lab-danger');});
      host.querySelectorAll('.lab-target').forEach(e=>e.classList.remove('lab-target'));
      const target=step.focus==='title'?host.querySelector('.lab-brand'):step.focus==='cards'?sensors:step.focus==='value'?tempValue:step.focus==='water'?waterCard:tempCard;
      target.classList.add('lab-target');
      tempValue.textContent=index>=7?'28 °C':'-- °C';waterValue.textContent=index>=7?'20 %':'-- %';host.querySelector('[data-sensor="humidity"] .lab-value').textContent=index>=7?'61 %':'-- %';host.querySelector('[data-sensor="distance"] .lab-value').textContent=index>=7?'80 cm':'-- cm';status.textContent='';status.classList.remove('lab-status-danger');
      readingControls.hidden=index<9;
      readingControls.querySelectorAll('[data-action^="water"]').forEach(b=>b.hidden=index<10);
      host.querySelector('[data-action="prev"]').disabled=index===0;
      host.querySelector('[data-action="next"]').disabled=index===steps.length-1;
      if(index>=9)readings();
      if(index===8){tick=0;ticker=setInterval(()=>{tick++;tempValue.textContent=[28,29,27][tick%3]+' °C';tempValue.classList.remove('lab-tick');void tempValue.offsetWidth;tempValue.classList.add('lab-tick');},3000);}
      preview.scrollTop=0;
    }
    host.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||!host.contains(b))return;const action=b.dataset.action;
      if(action==='play'){
        if(playing!==null){stop();stopTick();return;}
        if(index===steps.length-1){index=0;render();}else if(index===8&&ticker===null){render();}
        b.textContent='إيقاف مؤقت ⏸';playing=setInterval(()=>{if(index<steps.length-1){index++;render();}if(index===steps.length-1)stop();},5000);return;
      }
      stop();
      if(action==='prev'){index=Math.max(0,index-1);render();}else if(action==='next'){index=Math.min(steps.length-1,index+1);render();}else if(action==='phase'){index=Number(b.dataset.step);render();}else if(action==='reset'){index=initial;temperature=25;water=20;render();}else {temperature=action==='temp-safe'?25:action==='temp-high'?32:temperature;water=action==='water-safe'?20:action==='water-high'?80:water;readings();}
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();stopTick();}});
    render();
  }
  function initJourney(map){
    const pipeline=map.querySelector('.pipeline');if(!pipeline)return;
    const snapshot=pipeline.innerHTML;let index=-1,playing=null;
    const panel=document.createElement('div');panel.className='journey-panel';
    panel.innerHTML='<span class="lab-eyebrow">لاحقًا في المشروع · محاكاة توضيحية</span><p class="journey-status" aria-live="polite">اضغط «ابدأ الرحلة» وتابع الرقم ٢٩ من الحساس حتى الشاشة.</p><div class="journey-controls" role="group" aria-label="التحكم في رحلة القراءة"></div>';
    const controls=panel.querySelector('.journey-controls');[['ابدأ الرحلة ▶','play'],['المرحلة التالية ←','next'],['إعادة الرحلة ↺','reset']].forEach(([label,action])=>controls.append(button(label,action)));
    map.querySelector('.map-scroll').before(panel);
    const messages=['🌡️ الحساس يقيس الحرارة: ٢٩ °C. هذه هي القراءة التي سنتابعها.','📶 Pico W يقرأ ٢٩ °C ويرسلها عبر WiFi.','📥 Flask يستقبل ٢٩ °C ويجهّزها للحفظ والعرض.','🗂️ أضفنا ٢٩ °C إلى السجل عند ١٤:٠٩. القراءات القديمة بقيت محفوظة.','🖥️ وصلت ٢٩ °C إلى لوحة رصد. نفس الرقم مرّ بكل المراحل؛ الغرفة آمنة.'];
    function stop(){map.classList.add('journey-paused');if(playing!==null){clearInterval(playing);playing=null;}controls.querySelector('[data-action="play"]').textContent=index===4?'تشغيل الرحلة مجددًا ▶':index<0?'ابدأ الرحلة ▶':'تابع الرحلة ▶';}
    function reset(){stop();index=-1;pipeline.innerHTML=snapshot;pipeline.classList.remove('journey-running');map.classList.remove('journey-paused');panel.querySelector('.journey-status').textContent='اضغط «ابدأ الرحلة» وتابع الرقم ٢٩ من الحساس حتى الشاشة.';controls.querySelector('[data-action="next"]').disabled=false;controls.querySelector('[data-action="play"]').textContent='ابدأ الرحلة ▶';}
    function step(){index++;const pipes=pipeline.querySelectorAll('.pipe');pipeline.classList.add('journey-running');pipes.forEach((p,i)=>{p.classList.toggle('journey-active',i===index);p.classList.toggle('journey-done',i<index);});
      const arrows=pipeline.querySelectorAll('.map-arrow');arrows.forEach((a,i)=>a.classList.toggle('journey-arrow',i===index-1));
      if(index===0)pipes[0].querySelector('.reading').textContent='29 °C';
      if(index===1){const p=document.createElement('p');p.className='journey-payload';p.textContent='📶 29 °C';p.dir='ltr';pipes[1].querySelector('.map-picture').append(p);}
      if(index===2)pipes[2].querySelector('.server-packet .reading').textContent='29 °C';
      if(index===3){const row=document.createElement('tr');row.className='journey-new-row';const time=document.createElement('td');time.textContent='14:09';time.dir='ltr';const val=document.createElement('td');val.textContent='29';row.append(time,val);pipes[3].querySelector('tbody').append(row);}
      if(index===4)pipes[4].querySelector('.dashboard-mini b').textContent='29 °C';
      panel.querySelector('.journey-status').textContent=messages[index];
      if(!reducedMotion)pipes[index].scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
      if(index===4){stop();controls.querySelector('[data-action="next"]').disabled=true;}
    }
    panel.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const action=b.dataset.action;
      if(action==='reset'){reset();return;}
      if(action==='next'){stop();if(index<4)step();return;}
      if(playing!==null){stop();return;}
      if(index===4)reset();
      if(index<4)step();
      if(index<4){map.classList.remove('journey-paused');b.textContent='إيقاف مؤقت ⏸';playing=setInterval(step,3000);}
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  }
  document.querySelectorAll('.rasd-lab').forEach(initLab);
  document.querySelectorAll('.project-map').forEach(initJourney);
})();
