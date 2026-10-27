(() => {
  'use strict';
  const pending = new Map();
  function load(url) {
    if (!pending.has(url)) pending.set(url, new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = url;
      script.onload = resolve;
      script.onerror = () => { pending.delete(url); script.remove(); reject(new Error('No se pudo cargar la biblioteca de exportación.')); };
      document.head.append(script);
    }));
    return pending.get(url);
  }
  window.FCDExportPresentation = async ({format, stage, pages, render}) => {
    const libraries = document.querySelector('.presentation-export-actions').dataset;
    const message = document.getElementById('presentation-message');
    message.textContent = 'Preparando exportación…';
    await Promise.all([load(libraries.captureLibrary), load(format === 'pdf' ? libraries.pdfLibrary : libraries.pptxLibrary)]);
    await document.fonts.ready;
    const pdf = format === 'pdf' ? new window.jspdf.jsPDF({orientation:'landscape', unit:'pt', format:[960,540], compress:true}) : null;
    const pptx = format === 'pptx' ? new window.PptxGenJS() : null;
    if (pptx) { pptx.layout = 'LAYOUT_WIDE'; pptx.author = 'FCD'; pptx.subject = 'Auditorías filtradas'; pptx.title = 'Presentación de auditorías'; }
    stage.classList.add('export-capture');
    for (let index = 0; index < pages; index++) {
      message.textContent = `Exportando diapositiva ${index + 1} de ${pages}…`;
      await render(index);
      const canvas = await window.html2canvas(stage, {scale:1.5, width:1600, height:900, windowWidth:1600, windowHeight:1000, scrollX:0, scrollY:0, backgroundColor:'#101114', logging:false});
      const image = canvas.toDataURL('image/png');
      if (pdf) {
        if (index) pdf.addPage([960,540], 'landscape');
        pdf.addImage(image, 'PNG', 0, 0, 960, 540, undefined, 'FAST');
      } else {
        const slide = pptx.addSlide();
        slide.addImage({data:image, x:0, y:0, w:13.333333, h:7.5, altText:stage.querySelector('#slide-title').textContent});
        slide.addNotes([stage.innerText, `Filtros: ${location.search || 'Sin filtros adicionales'}`]);
      }
      canvas.width = canvas.height = 0;
    }
    const filename = `FCD-presentacion-${new Date().toISOString().slice(0,10)}`;
    if (pdf) await pdf.save(filename + '.pdf', {returnPromise:true});
    else await pptx.writeFile({fileName:filename + '.pptx'});
    message.textContent = `Presentación exportada: ${pages} ${pages === 1 ? 'diapositiva' : 'diapositivas'}.`;
  };
})();
