(function(){
// countdowns
var now=Date.now();document.querySelectorAll('.cd').forEach(function(el){var end=now+(+el.dataset.days)*864e5-3600e3*5;function t(){var s=Math.max(0,(end-Date.now())/1e3),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),x=Math.floor(s%60);el.textContent=(el.classList.contains('big')?'':'Ends in ')+d+'d '+h+'h '+m+'m '+(el.classList.contains('big')?x+'s':'')}t();setInterval(t,1000)});
// filters (query params; canonical stays on hub)
var g=document.getElementById('grid'),cat=document.getElementById('cat');
if(g&&cat){var q=new URLSearchParams(location.search),nocc=document.getElementById('nocc'),sort=document.getElementById('sort'),cards=[].slice.call(g.querySelectorAll('.card')),ad=g.querySelector('.native');
nocc.checked=q.get('nocc')==='1';if(q.get('sort'))sort.value=q.get('sort');var c=q.get('cat')||'';
function apply(push){cat.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.v===c)});
var v=cards.filter(function(e){return(!c||e.dataset.cat===c)&&(!nocc.checked||e.dataset.nocc==='1')});var k=sort.value;
v.sort(function(a,b){return k==='name'?a.dataset.name.localeCompare(b.dataset.name):k==='days'?b.dataset.days-a.dataset.days:a.dataset.ends-b.dataset.ends});
cards.forEach(function(e){e.hidden=true});v.forEach(function(e,i){e.hidden=false;g.appendChild(e);if(i===2&&ad)g.appendChild(ad)});if(ad&&v.length<3)g.appendChild(ad);
document.getElementById('count').textContent=v.length+' of '+cards.length+' services · Sample data';
if(push){var p=new URLSearchParams();if(c)p.set('cat',c);if(k!=='ends')p.set('sort',k);if(nocc.checked)p.set('nocc','1');history.replaceState(null,'',location.pathname+(p+''?'?'+p:''))}}
cat.addEventListener('click',function(e){if(e.target.dataset.v!==undefined){c=e.target.dataset.v;apply(1)}});nocc.onchange=sort.onchange=function(){apply(1)};apply(0)}
// newsletter
document.querySelectorAll('.nl').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var i=f.querySelector('input'),ok=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value);f.querySelector('.err').hidden=ok;if(ok){f.querySelector('.ok').hidden=false;i.hidden=true;f.querySelector('button').hidden=true}})});
})();
