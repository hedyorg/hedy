import puppeteer from 'puppeteer';

async function main() {
  const languages = process.argv.slice(2);
  if (languages.length === 0) {
    console.log('Usage: tsx print-workbook.ts [LANGUAGE] [...]');
    console.log('');
    console.log('  Example: tsx print-workbook.ts en nl');
    return;
  }

  // Or import puppeteer from 'puppeteer-core';
  // Launch the browser and open a new blank page
  const browser = await puppeteer.launch();

  try {
    const page = await browser.newPage();

    for (const lang of languages) {
      // Navigate the page to a URL.
      await page.goto(`http://localhost:8080/for-teachers/workbooks/all?language=${lang}`, {
        waitUntil: 'networkidle2',
      });

      const H_MARGIN = 70;
      const V_MARGIN = 50;

      // Saves the PDF to hn.pdf.
      const path = `workbook-${lang}.pdf`;
      await page.pdf({
        path,
        format: 'A4',
        margin: {
          top: V_MARGIN,
          bottom: V_MARGIN,
          left: H_MARGIN,
          right: H_MARGIN,
        },
      });
      console.log(path);
    }

  } finally {
    await browser.close();
  }
}

main().catch(e => {
  console.error(e);
  process.exitCode = 1;
});
