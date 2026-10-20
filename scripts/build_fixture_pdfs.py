"""Optional fixture authoring tool. Requires reportlab; runtime tools do not."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

ROOT = Path(__file__).resolve().parents[1]


def build():
    for source in sorted((ROOT / 'examples/extraction/documents').glob('*.txt')):
        target = source.with_suffix('.pdf')
        pdf = canvas.Canvas(str(target), pagesize=letter, invariant=1)
        pdf.setTitle('Synthetic extraction fixture: ' + source.stem)
        pdf.setAuthor('WXO Bob Starter')
        y = 738
        for i, line in enumerate(source.read_text(encoding='utf-8').splitlines()):
            font, size = ('Helvetica-Bold', 14) if i == 0 else ('Helvetica', 12)
            pdf.setFont(font, size)
            for part in simpleSplit(line, font, size, 504):
                pdf.drawString(54, y, part)
                y -= 21
            y -= 7
        if y < 80:
            raise ValueError('Fixture exceeds one page; review layout')
        pdf.setFont('Helvetica', 10)
        pdf.drawString(54, 40, 'Fictional training data. No real account, client or payment information.')
        pdf.showPage();pdf.save()
        print(target.name)


if __name__ == '__main__':
    build()
