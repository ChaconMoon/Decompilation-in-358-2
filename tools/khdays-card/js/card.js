/**
 * card.js — Lógica del generador de tarjetas KHDays
 *
 * Carga los SVG desde svg/rule.svg y svg/heart.svg mediante fetch,
 * por lo que necesitas servir la carpeta con un servidor local
 * (ej: "npx serve ." o Live Server de VS Code).
 *
 * Si prefieres incrustar los SVG directamente sin servidor, cambia
 * las funciones loadSVG() por funciones que devuelvan el SVG literal
 * (ver comentario al final de este archivo).
 */

(function () {

  /* ── Configuración ── */
  var TOTAL = 358.5;
  var SIZES = { li: [1200, 627], sq: [1080, 1080] };

  /* ── Estado ── */
  var fmt       = 'li';
  var manualDay = false;
  var svgCache  = {};   // { rule: '<svg>…</svg>', heart: '<svg>…</svg>' }

  /* ── Utilidades de fecha ── */
  function iso(d) {
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (day < 10 ? '0' : '') + day;
  }
  function parse(s) {
    var p = s.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function fmtDate(d) {
    return d.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' }).replace('.', '');
  }

  /* ── Escape HTML ── */
  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* ── Acceso al DOM ── */
  function $(id) { return document.getElementById(id); }

  /* ───────────────────────────────────────────────────────────
     Carga de SVG externos
     Los SVG viven en svg/rule.svg y svg/heart.svg.
     Edítalos con Inkscape / Illustrator / VS Code y se
     reflejarán aquí automáticamente al recargar la página.
  ─────────────────────────────────────────────────────────── */
  function loadSVG(name) {
    if (svgCache[name]) return Promise.resolve(svgCache[name]);
    return fetch('svg/' + name + '.svg')
      .then(function (r) { return r.text(); })
      .then(function (text) {
        // Elimina la declaración XML y el DOCTYPE si los hubiera
        svgCache[name] = text.replace(/<\?xml[^?]*\?>/gi, '').replace(/<!DOCTYPE[^>]*>/gi, '').trim();
        return svgCache[name];
      });
  }

  /* ───────────────────────────────────────────────────────────
     Cálculo del día actual
  ─────────────────────────────────────────────────────────── */
  function autoDay() {
    var s = parse($('start').value);
    var t = parse($('today').value);
    var d = Math.round((t - s) / 86400000) + 1;
    return Math.max(1, Math.min(359, d));
  }

  /* ───────────────────────────────────────────────────────────
     Construcción de la tarjeta
  ─────────────────────────────────────────────────────────── */
  function build() {
    Promise.all([loadSVG('rule'), loadSVG('heart')]).then(function (svgs) {
      var ruleSVG  = svgs[0];
      var heartSVG = svgs[1];
      render(ruleSVG, heartSVG);
    });
  }

  function render(ruleSVG, heartSVG) {
    var W  = SIZES[fmt][0], H = SIZES[fmt][1];
    var sq = (fmt === 'sq');

    var day = manualDay ? (+$('dayov').value || 1) : autoDay();
    if (!manualDay) $('dayov').value = day;

    var start  = parse($('start').value);
    var end    = new Date(start.getTime() + (TOTAL - 1) * 86400000);
    var pct    = Math.min(100, (day / TOTAL) * 100);
    var left   = Math.max(0, Math.ceil(TOTAL - day));
    var pts    = $('pts').value.split('\n').map(function (x) { return x.trim(); }).filter(Boolean);
    var phase  = $('phase').value;
    var ttl    = $('ttl').value.trim();

    /* Dimensiones de fuente */
    var base     = sq ? 15 : 16;          // px → 1em
    var headSize = sq ? 7.5 : 8;       // em
    var numSize  = headSize * 1.55;
    if (String(day).length >= 3) numSize *= 0.9;

    var c = $('card');
    c.style.width    = W + 'px';
    c.style.height   = H + 'px';
    c.style.fontSize = base + 'px';

    /* HTML de la tarjeta */
    c.innerHTML =
      '<div class="head" style="font-size:' + headSize + 'em">' +
        '<div class="d">DÍA</div>' +
        '<div class="gap" style="width:' + (sq ? 1.0 : 0.9) + 'em"></div>' +
        '<div class="n" style="font-size:' + (numSize / headSize) + 'em">' + day + '</div>' +
      '</div>' +
      '<div style="height:' + (sq ? 1.2 : 0.9) + 'em"></div>' +

      /* ── SVG regla (archivo svg/rule.svg) ── */
      ruleSVG +

      '<div style="height:' + (sq ? 1.6 : 1.2) + 'em"></div>' +
      (ttl ? '<div class="st" style="font-size:' + (sq ? 3.2 : 3.0) + 'em">' + esc(ttl) + '</div>' : '') +
      '<div style="height:' + (sq ? 2.0 : 1.6) + 'em"></div>' +

      /* ── SVG corazón (archivo svg/heart.svg) ── */
      '<div style="width:' + (sq ? 5.2 : 4.6) + 'em">' + heartSVG + '</div>' +

      ($('showph').checked
        ? '<div style="height:1.4em"></div>' +
          '<div class="cap" style="font-size:' + (sq ? 1.5 : 1.35) + 'em">' + esc(phase) + '</div>'
        : '');

    scale();
    post(day, pct, left, end, pts, ttl, phase);
  }

  /* ───────────────────────────────────────────────────────────
     Escalado del escenario
  ─────────────────────────────────────────────────────────── */
  function scale() {
    var W  = SIZES[fmt][0], H = SIZES[fmt][1];
    var st = $('stage');
    var k  = st.clientWidth / W;
    $('card').style.transform = 'scale(' + k + ')';
    st.style.height = (H * k) + 'px';
  }

  /* ───────────────────────────────────────────────────────────
     Texto de publicación
  ─────────────────────────────────────────────────────────── */
  function post(day, pct, left, end, pts, ttl, phase) {
    var t =
      'Día ' + day + (ttl ? ' — "' + ttl + '"' : '') + '\n' +
      'Reto KHDays: día ' + day + ' de 358½ · ' + phase + '\n\n' +
      pts.map(function (p) { return '• ' + p; }).join('\n') +
      (pts.length ? '\n\n' : '') +
      'Progreso: ' + Math.round(pct) + '% · quedan ' + left + ' días (meta: ' + fmtDate(end) + ').\n' +
      'Aprendiendo C y decompilación matching con Kingdom Hearts 358/2 Days como caso de estudio.\n\n' +
      '#KHDays #Decompilación #Cprogramming #ReverseEngineering #Aprendizaje';
    $('post').textContent = t;
  }

  /* ───────────────────────────────────────────────────────────
     Eventos
  ─────────────────────────────────────────────────────────── */
  $('today').value = iso(new Date());

  ['start', 'today', 'ttl', 'pts', 'phase', 'showph'].forEach(function (id) {
    var ev = (id === 'showph') ? 'change' : 'input';
    $(id).addEventListener(ev, function () {
      if (id === 'start' || id === 'today') manualDay = false;
      build();
    });
  });

  $('dayov').addEventListener('input', function () {
    manualDay = true;
    build();
  });

  $('fmt').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    fmt = b.getAttribute('data-f');
    Array.prototype.forEach.call($('fmt').children, function (x) {
      x.classList.toggle('on', x === b);
    });
    build();
  });

  $('copy').addEventListener('click', function () {
    try {
      navigator.clipboard.writeText($('post').textContent);
      $('copy').textContent = 'Copiado';
      setTimeout(function () { $('copy').textContent = 'Copiar'; }, 1500);
    } catch (e) {}
  });

  $('export').addEventListener('click', function () {
    var button = $('export');
    var status = $('export-status');
    var card = $('card');
    var W = SIZES[fmt][0];
    var H = SIZES[fmt][1];
    var day = $('dayov').value || '1';
    var exportCard = card.cloneNode(true);

    if (typeof html2canvas !== 'function') {
      status.textContent = 'No se pudo cargar el exportador.';
      return;
    }

    button.disabled = true;
    status.textContent = 'Generando imagen…';
    exportCard.style.position = 'fixed';
    exportCard.style.left = '-10000px';
    exportCard.style.top = '0';
    exportCard.style.transform = 'none';
    exportCard.style.width = W + 'px';
    exportCard.style.height = H + 'px';
    document.body.appendChild(exportCard);

    html2canvas(exportCard, {
      backgroundColor: '#000',
      height: H,
      logging: false,
      scale: 1,
      useCORS: true,
      width: W,
      windowWidth: W,
      windowHeight: H
    }).then(function (canvas) {
      return new Promise(function (resolve, reject) {
        canvas.toBlob(function (blob) {
          if (blob) resolve(blob);
          else reject(new Error('No se pudo crear el archivo PNG.'));
        }, 'image/png');
      });
    }).then(function (blob) {
      var link = document.createElement('a');
      link.download = 'khdays-dia-' + day + '-' + fmt + '.png';
      link.href = URL.createObjectURL(blob);
      link.click();
      URL.revokeObjectURL(link.href);
      status.textContent = 'Imagen exportada.';
    }).catch(function () {
      status.textContent = 'No se pudo exportar la imagen.';
    }).then(function () {
      exportCard.remove();
      button.disabled = false;
    });
  });

  window.addEventListener('resize', scale);

  /* Espera a las fuentes antes de la primera renderización */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(build);
  } else {
    build();
  }

  /*
   * ── MODO SIN SERVIDOR (inline SVG) ──────────────────────────
   * Si no puedes usar fetch (p.ej. abres el HTML directamente
   * como file://), sustituye la función build() por esta versión:
   *
   *   function build() {
   *     var ruleSVG  = document.getElementById('tpl-rule').innerHTML;
   *     var heartSVG = document.getElementById('tpl-heart').innerHTML;
   *     render(ruleSVG, heartSVG);
   *   }
   *
   * Y añade en el HTML (fuera de .card):
   *   <template id="tpl-rule">  … contenido de rule.svg  … </template>
   *   <template id="tpl-heart"> … contenido de heart.svg … </template>
   */

})();
