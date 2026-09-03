const roles=['Data Scientist','Data Analyst','Machine Learning Engineer','AI / ML Enthusiast'];
let roleIndex=0;
const roleText=document.getElementById('roleText');
setInterval(()=>{roleIndex=(roleIndex+1)%roles.length;roleText.style.opacity='0';setTimeout(()=>{roleText.textContent=roles[roleIndex];roleText.style.opacity='1'},180)},2600);
roleText.style.transition='opacity .18s';
const menu=document.getElementById('menu'),nav=document.getElementById('navLinks');
menu?.addEventListener('click',()=>nav.classList.toggle('open'));
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
const messages=document.getElementById('messages'),form=document.getElementById('chatForm'),input=document.getElementById('chatInput');
function addBubble(text,type){const el=document.createElement('div');el.className=`bubble ${type}`;el.textContent=text;messages.appendChild(el);messages.scrollTop=messages.scrollHeight;return el}
async function ask(text){if(!text.trim())return;addBubble(text,'user');input.value='';const wait=addBubble('Thinking…','bot');try{const res=await fetch('/api/gemini',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});const data=await res.json();wait.remove();addBubble(data.reply||'I could not answer that right now.','bot')}catch(e){wait.remove();addBubble('The assistant is temporarily unavailable. Please try again.','bot')}}
form?.addEventListener('submit',e=>{e.preventDefault();ask(input.value)});
document.querySelectorAll('.prompt-chips button').forEach(btn=>btn.addEventListener('click',()=>ask(btn.textContent)));
